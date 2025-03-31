import requests
import json
import os
from data.client import RestClient
from google.oauth2 import service_account
import pandas as pd
from googleapiclient.discovery import build
from google.cloud import bigquery


### for local debugging
#Authentication with service account for bigquery
credentials = service_account.Credentials.from_service_account_file(
     'bq_service_account.json', scopes=[
         "https://www.googleapis.com/auth/drive",
         "https://www.googleapis.com/auth/cloud-platform"],
 )

spreadsheetId = os.environ['spreadsheetId']
project_id = os.environ['project_id']
dataset_id = os.environ['dataset_id']
table_id = os.environ['table_id']

# get data from googlesheet

# prepare parameters for API call function

# make an API call

# transform data

# send data back to googlesheet
