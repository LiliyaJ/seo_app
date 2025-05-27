
# # get data from googlesheet
def get_data_from_gs (spreadsheet_id, service):
    values = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='input!A1:Z10000').execute()['values']
    return [
        (row[0].strip(), row[1].strip(), row[2].strip())
        for row in values[1:]  # Skip header
        if len(row) >= 3 and all(cell.strip() for cell in row[:3])  # Ensure first 3 values are non-empty
    ]



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
def extract_search_volume_rows(api_responses):
    """
    Flatten DataForSEO responses into a list of rows for Google Sheets.

    Parameters:
        api_responses (list): Responses returned by fetch_historical_search_volume.

    Returns:
        list of lists: Each sublist contains [keyword, location, language, year, month, search_volume]
    """
    rows = [["Keyword", "Location", "Language", "Year", "Month", "Search Volume"]]
    
    for response in api_responses:
        if "tasks" not in response:
            continue
        for task in response["tasks"]:
            keyword = task["data"]["keywords"][0]
            location = task["data"]["location_name"]
            language = task["data"]["language_name"]
            
            try:
                items = task["result"][0]["items"]
                if not items:
                    continue

                monthly_searches = items[0]["keyword_info"]["monthly_searches"]
                for record in monthly_searches:
                    rows.append([
                        keyword,
                        location,
                        language,
                        record["year"],
                        record["month"],
                        record["search_volume"]
                    ])
            except (KeyError, IndexError, TypeError):
                continue
    
    return rows

# send data back to googlesheet 
def upload_rows_to_sheet(service, spreadsheet_id, range_name, rows):
    """
    Uploads data to a Google Sheet using the Sheets API.

    Parameters:
        service: Authenticated Sheets API service instance.
        spreadsheet_id (str): The ID of the Google Sheet.
        range_name (str): The A1 notation of the range to update (e.g., "Sheet1!A1").
        rows (list of lists): The data to upload (including headers).
    """
    body = {
        "values": rows
    }

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption="RAW",
        body=body
    ).execute()


# insert data to bigquery
def upload_search_volume_bigquery(rows, bq_client, dataset_id, table_id):
    """
    Appends search volume rows to an existing BigQuery table.
    Assumes schema: keyword, location, language, year, month, search_volume
    """
    table_ref = bq_client.dataset(dataset_id).table(table_id)

    # Corrected field names to match BQ schema
    correct_headers = ["keyword", "location", "language", "year", "month", "search_volume"]
    data_rows = rows[1:]  # skip header row

    # Map each row to the correct field names
    json_rows = [dict(zip(correct_headers, row)) for row in data_rows]

    # Upload
    errors = bq_client.insert_rows_json(table_ref, json_rows)

    if errors:
        print("Insert errors:", errors)
    else:
        print(f"Successfully inserted {len(json_rows)} rows into {dataset_id}.{table_id}")
