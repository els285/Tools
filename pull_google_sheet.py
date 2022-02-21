def pull_from_google_sheets(SCOPES,SAMPLE_SPREADSHEET_ID,**kwargs):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """

    SAMPLE_RANGE_NAME = kwargs["SAMPLES_RANGE_NAME"] if "SAMPLES_RANGE_NAME" in kwargs else 'A1:AA1000'

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        # print(sheet.__dict__.keys())
        # input()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()

        values = result.get('values', [])

    except HttpError as err:
        print(err)

    return values