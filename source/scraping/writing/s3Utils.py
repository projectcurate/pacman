#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 13:57:41 2019

@author: alutes
"""
import boto3
import pandas as pd

class s3Writer(bucketPath):

    # Assumes a security key stored locally in .aws/credentials    
    def __init__():
        s3_client = boto3.client('s3')
        
    """ Writes a pandas dataframe to the specified location in s3
    """
    def df_to_s3(df, path):
        binary_data = df.to_csv()
        return s3_client.put_object(Body=binary_data, Bucket=bucketPath, Key=path)
