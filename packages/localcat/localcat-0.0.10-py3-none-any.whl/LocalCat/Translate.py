#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
author:     Ewen Wang
email:      wolfgangwong2012@gmail.com
license:    Apache License 2.0
"""

from tqdm import tqdm
import numpy as np
import pandas as pd
import torch
from datasets import Dataset, DatasetDict
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import Seq2SeqTrainingArguments
from transformers import DataCollatorForSeq2Seq
from transformers import Seq2SeqTrainer
import evaluate


class Translate:
    """
    Translate class for language translation.
    """
    def __init__(self, 
                 model_name_or_path='facebook/mbart-large-50-many-to-one-mmt', 
                 src_lang='zh_CN', 
                 tgt_lang='en_XX'):
        """
        Initializes the Translate class.

        Args: 
            model_name_or_path (str): Name or path to the pretrained model and tokenizer. Default is 'facebook/mbart-large-50-many-to-one-mmt'. 
            src_lang (str): Source language for translation. Default is 'zh_CN'. 
            tgt_lang (str): Target language for translation. Default is 'en_XX'.
        """

        self.model_name_or_path = model_name_or_path
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name_or_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name_or_path).to(self.device)
        
        self.tokenizer.src_lang = src_lang
        self.tokenizer.tgt_lang = tgt_lang
        
        self.src_lang = src_lang.split('_')[0]
        self.tgt_lang = tgt_lang.split('_')[0]
        

    def translator(self, text, max_new_tokens=500):
        """
        Translates text from source language to target language.

        Args:
            text (str): Text to be translated.
            max_new_tokens (int): The maximum numbers of tokens to generate, ignoring the number of tokens in the prompt. Default is 500.

        Returns:
            str: Translated text.
        """

        encoded_text = self.tokenizer(text, return_tensors="pt").to(self.device)
        translated_output = self.model.generate(**encoded_text, max_new_tokens=max_new_tokens)
        translated_text = self.tokenizer.decode(translated_output[0], skip_special_tokens=True)

        return translated_text

    def translator_batch(self, df, col_src='Chinese', col_tgt='English'):
        """
        Translate a batch of text from one language to another using a provided translation
        function.

        Args:
            df (pd.DataFrame): The Pandas DataFrame containing the text to translate.
            col_src (str, optional): The name of the column containing the source language text. Defaults to "Chinese".
            col_tgt (str, optional): The name of the column to store the translated text. Defaults to "English".

        Returns:
            pd.DataFrame: The original DataFrame with the translated text added to the specified target column.

        Raises:
            AttributeError: If the specified columns (`col_src` or `col_tgt`) are not found in the DataFrame.

        Prints:
            The total time taken for the translation and the average speed per item.
        """
        
        tqdm.pandas()

        df[col_tgt] = df[col_src].progress_apply(lambda x: self.translator(x))

        return df

    def generate_dataset(self, df, train_size=0.9, col_src='Chinese', col_tgt='English'):
        """
        Generates a DatasetDict for machine translation from a pandas DataFrame.

        Args:
            df: A pandas DataFrame containing the source and target language columns.
            train_size: The proportion of the data to use for training (default: 0.9).
            col_src: The name of the source language column (default: 'Chinese').
            col_tgt: The name of the target language column (default: 'English').
            
        Returns:
            A DatasetDict containing the training, validation, and test datasets.
        """
        df = df.assign(translation=df.apply(lambda row: {self.src_lang: row[col_src], 
                                                         self.tgt_lang: row[col_tgt]}, axis=1))
        df.reset_index(inplace=True)
        df.drop(['index', col_src, col_tgt], axis=1, inplace=True)

        test_size = 1 - train_size
        dataset = Dataset.from_pandas(df, split='train')
        dataset = dataset.train_test_split(test_size=test_size)
        testset = dataset['test'].train_test_split(test_size=0.5)
        dataset = DatasetDict({
            'train': dataset['train'],
            'test': testset['test'],
            'valid': testset['train']})
        return dataset

    def tokenize_dataset(self, max_length_input=512, max_length_target=512, prefix=''):
        """
        Preprocesses a dataset of text pairs for machine translation models.

        Args:
            max_length_input (int): Maximum length of the input sequence (default: 512).
            max_length_target (int): Maximum length of the target sequence (default: 512).
            prefix (str, optional): String to prepend to each source language sentence (default: ''). T5 model requires a special prefix to put before the inputs, you should adopt the following code for defining the prefix. For mBART and MarianMT prefixes will remain blank.

        Returns:
            datasets.Dataset: The original dataset transformed with tokenized input, target sequences, and labels.
        """
        self.max_length_input = max_length_input
        self.max_length_target = max_length_target

        def tokenizer(case):
            inputs = [prefix + i[self.src_lang] for i in case['translation']]
            labels = [i[self.tgt_lang] for i in case['translation']]
            model_inputs = self.tokenizer(inputs, max_length=self.max_length_input, truncation=True)
            encoded_labels = self.tokenizer(text_target=labels, max_length=self.max_length_target, truncation=True)

            model_inputs["labels"] = encoded_labels["input_ids"]
            return model_inputs

        tokenized_dataset = self.dataset.map(tokenizer, batched=True)
        return tokenized_dataset
    
    def postprocess_text(self, preds, labels):
        """
        Removes leading and trailing whitespaces from predicted and label text sequences.

        Args:
            preds (list): List of predicted text sequences.
            labels (list): List of label text sequences.

        Returns:
            tuple: A tuple containing the postprocessed predicted and label sequences.
        """
        preds = [pred.strip() for pred in preds]
        labels = [[label.strip()] for label in labels]
        return preds, labels

    def compute_metrics(self, eval_preds):
        """
        Computes evaluation metrics for machine translation model predictions.

        Args:
            eval_preds (tuple): Tuple containing predicted and label sequences.

        Returns:
            dict: Dictionary containing computed evaluation metrics.
        """
        metric = evaluate.load("sacrebleu")
        meteor = evaluate.load('meteor')
        
        preds, labels = eval_preds
        
        if isinstance(preds, tuple):
            preds = preds[0]

        decoded_preds = self.tokenizer.batch_decode(preds, skip_special_tokens=True)
        labels = np.where(labels != -100, labels, self.tokenizer.pad_token_id) # Replace -100 in the labels as we can't decode them.
        decoded_labels = self.tokenizer.batch_decode(labels, skip_special_tokens=True)
        decoded_preds, decoded_labels = self.postprocess_text(decoded_preds, decoded_labels)
        
        result = metric.compute(predictions=decoded_preds, references=decoded_labels)
        meteor_result = meteor.compute(predictions=decoded_preds, references=decoded_labels)
        prediction_lens = [np.count_nonzero(pred != self.tokenizer.pad_token_id) for pred in preds]
        result = {'bleu' : result['score']}
        result["gen_len"] = np.mean(prediction_lens)
        result["meteor"] = meteor_result["meteor"]
        result = {k: round(v, 4) for k, v in result.items()}
        
        return result
    
    def finetune(self, 
                 df, train_size=0.9, col_src='Chinese', col_tgt='English', 
                 max_length_input=512, max_length_target=512, prefix='',
                 finetuned_model_path="model", batch_size=4, save_total_limit=3,
                 evaluation_strategy="epoch", learning_rate=2e-5, weight_decay=0.01, num_train_epochs=1):
        """
        Fine-tunes a pre-trained Seq2Seq model on a custom dataset.

        Args:
            df (pandas.DataFrame): DataFrame containing source and target language columns.
            train_size (float, optional): Proportion of data to use for training (default: 0.9).
            col_src (str, optional): Column name for source language text (default: 'Chinese').
            col_tgt (str, optional): Column name for target language text (default: 'English').
            max_length_input (int, optional): Maximum length of input sequences (default: 512).
            max_length_target (int, optional): Maximum length of target sequences (default: 512).
            prefix (str, optional): String to prepend to each source language sentence (default: '').
            finetuned_model_path (str, optional): Path to save the fine-tuned model (default: "model").
            batch_size (int, optional): Batch size for training and evaluation (default: 4).

        Returns:
            None: Saves the fine-tuned model and prints evaluation results.

        This function fine-tunes a pre-trained Seq2Seq model on a given dataset for machine translation. It performs the following steps:

        1. Generates a training dataset from the provided DataFrame.
        2. Tokenizes the dataset using the specified parameters and prefix.
        3. Defines training arguments for the fine-tuning process.
        4. Creates a data collator for efficient batch processing.
        5. Initializes a Seq2SeqTrainer object with the model, arguments, and datasets.
        6. Trains the model on the training dataset.
        7. Saves the fine-tuned model to the specified path.
        8. Evaluates the model on the test dataset and prints the results.
        """
        self.dataset = self.generate_dataset(df, 
                                             train_size=train_size, 
                                             col_src=col_src, col_tgt=col_tgt)
        self.tokenized_dataset = self.tokenize_dataset(max_length_input=max_length_input, 
                                                        max_length_target=max_length_input, 
                                                        prefix=prefix)
        self.args = Seq2SeqTrainingArguments(
           output_dir=finetuned_model_path,
           evaluation_strategy="epoch",
           learning_rate=learning_rate,
           per_device_train_batch_size=batch_size,
           per_device_eval_batch_size=batch_size,
           weight_decay=weight_decay,
           save_total_limit=save_total_limit,
           num_train_epochs=num_train_epochs,
           predict_with_generate=True,
        )

        self.data_collator = DataCollatorForSeq2Seq(tokenizer=self.tokenizer, model=self.model)

        self.trainer = Seq2SeqTrainer(
            model=self.model,
            args=self.args,
            train_dataset=self.tokenized_dataset['train'],
            eval_dataset=self.tokenized_dataset['valid'],
            data_collator=self.data_collator,
            tokenizer=self.tokenizer,
            compute_metrics=self.compute_metrics,
        )

        self.trainer.train()
        self.trainer.save_model()

        self.eval_result = self.trainer.evaluate(self.tokenized_dataset['test'])
        print(self.eval_result)
        return None