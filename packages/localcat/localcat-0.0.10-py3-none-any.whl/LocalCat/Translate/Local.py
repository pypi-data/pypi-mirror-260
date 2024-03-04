#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
author:     Ewen Wang
email:      wolfgangwong2012@gmail.com
license:    Apache License 2.0
"""

import os
import json
from time import gmtime, strftime
import subprocess
import pandas as pd
from tqdm import tqdm
import boto3
import sagemaker
from sagemaker.huggingface.model import HuggingFaceModel
from sagemaker.huggingface.model import HuggingFacePredictor

pd.set_option('display.max_colwidth', None)

class Local:
    """
    Local class for model deployment in AWS.
    """

    def __init__(self, model_name=None, model_path=None):
            """
            Initialize the Local object.

            Args:
                model_name (str): The name of the model.
                model_path (str): The path to the model.
            """
            self.model_name = model_name
            self.model_path = model_path
            self.s3_model = None

    def push_to_s3(self, bucket, prefix=None):
        """
        Pushes the model to an S3 bucket.

        Args:
            bucket (str): The name of the S3 bucket.
            prefix (str, optional): The prefix to be added to the S3 key.

        Returns:
            None
        """
        current_dir = os.getcwd()

        file_tar = f"{self.model_name}.tar.gz"
        key = f"{file_tar}" if prefix is None else f"{prefix}/{file_tar}"
        self.s3_model = f"s3://{bucket}/{key}"

        # Define the bash command
        bash_command = f"""
        cd {self.model_path}
        tar zcvf {file_tar} *
        aws s3 cp {file_tar} {self.s3_model}
        rm {file_tar}
        cd {current_dir}
        """

        # Run the bash command
        process = subprocess.Popen(bash_command, shell=True)
        process.wait()
        return None

    def deploy(self, instance_type='ml.g4dn.4xlarge',
               transformers_version='4.37.0', pytorch_version='2.1.0', py_version='py310'):
        """
        Deploys the HuggingFace model to an Amazon SageMaker endpoint.

        Args:
            instance_type (str): The type of Amazon SageMaker instance to use for deployment. Default is 'ml.g4dn.4xlarge'.
            transformers_version (str): The version of the Transformers library to use. Default is '4.37.0'.
            pytorch_version (str): The version of PyTorch to use. Default is '2.1.0'.
            py_version (str): The version of Python to use. Default is 'py310'.

        Returns:
            None
        """
        try:
            self.role = sagemaker.get_execution_role()
        except ValueError:
            iam = boto3.client('iam')
            self.role = iam.get_role(RoleName='sagemaker_execution_role')['Role']['Arn']
            
        huggingface_model = HuggingFaceModel(
            model_data=self.s3_model,
            role=self.role,
            transformers_version=transformers_version,
            pytorch_version=pytorch_version,
            py_version=py_version,
        )
        
        self.endpoint_name = self.model_name.upper() + strftime("-%Y%m%d-%H%M%S", gmtime())
        
        self.predictor = huggingface_model.deploy(
            initial_instance_count=1,
            instance_type=instance_type,
            endpoint_name=self.endpoint_name,
        )
        
        return None
        
    def translator(self, text):
        """
        Translates the given text using the HuggingFace model.

        Args:
            text (str): The text to be translated.

        Returns:
            str: The translated text.
        """
        predictor = HuggingFacePredictor(
            endpoint_name=self.endpoint_name
        )
        runtime_client = boto3.client('sagemaker-runtime')
        input_data = {"inputs": text}

        response = runtime_client.invoke_endpoint(
                    EndpointName=self.endpoint_name,
                    ContentType='application/json',
                    Body=json.dumps(input_data)
                )
        result = json.loads(response['Body'].read().decode('utf-8'))[0]['generated_text']
        return result

    def translator_batch(self, df, col_src='Chinese', col_tgt='English'):
        """
        Translates a batch of text in a DataFrame column using the translator method.

        Args:
            df (pandas.DataFrame): The DataFrame containing the text to be translated.
            col_src (str, optional): The name of the source column containing the text to be translated. Defaults to 'Chinese'.
            col_tgt (str, optional): The name of the target column to store the translated text. Defaults to 'English'.

        Returns:
            pandas.DataFrame: The DataFrame with the translated text in the target column.
        """
        tqdm.pandas()
        df[col_tgt] = df[col_src].progress_apply(lambda x: self.translator(x))
        return df