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

def fetch_historical_search_volume(keyword_location_language_list, client):
    """
    Fetch historical search volume using DataForSEO API for specific keyword-location-language combinations.

    Parameters:
        keyword_location_language_list (list of tuples): Each tuple contains (keyword, location_name, language_name).

    Returns:
        list: Combined responses from DataForSEO API.
    """
    combined_responses = []

    for keyword, location, language in keyword_location_language_list:
        post_data = dict()

        post_data[0] = dict(
            keywords=[keyword],  # Single keyword in a list
            location_name=location,
            language_name=language
        )

        response = client.post("/v3/dataforseo_labs/google/historical_search_volume/live", post_data)

        if response["status_code"] == 20000:
            print(f"Success for: {keyword} | {location} | {language}")
            combined_responses.append(response)
        else:
            error_message = f"Error for {keyword} | {location}. Code: {response['status_code']} Message: {response['status_message']}"
            print(error_message)
            combined_responses.append({"error": error_message})

    return combined_responses

# transform data

# send data back to googlesheet
