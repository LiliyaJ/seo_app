import pandas as pd



# # get data from googlesheet
def get_data_from_gs (spreadsheet_id, service):
    values = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='A1:Z10000').execute()['values']
    return pd.DataFrame(values[1:], columns = values[0])


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
