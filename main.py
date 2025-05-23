import requests
import json
import os
from data.client import RestClient
from google.oauth2 import service_account
import pandas as pd
from googleapiclient.discovery import build
from google.cloud import bigquery
from helper import get_data_from_gs, fetch_historical_search_volume


### for local debugging
#Authentication with service account for bigquery
credentials = service_account.Credentials.from_service_account_file(
     'bq_service_account.json', scopes=[
         "https://www.googleapis.com/auth/drive",
         "https://www.googleapis.com/auth/cloud-platform"],
 )

spreadsheet_id = os.environ['spreadsheet_id']
project_id = os.environ['project_id']
dataset_id = os.environ['dataset_id']
table_id = os.environ['table_id']

DFS_LOGIN = os.environ['DFS_LOGIN']
DFS_KEY = os.environ['DFS_KEY']

client = RestClient(DFS_LOGIN, DFS_KEY)

gs_data = get_data_from_gs (spreadsheet_id, build('sheets', 'v4', credentials=credentials))

print(gs_data)

make_api_call = fetch_historical_search_volume(gs_data, client)

print (make_api_call)