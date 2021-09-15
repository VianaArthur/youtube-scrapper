from google_custom import GoogleCustom
import constants as const


def save_to_sheets(data, spreadsheet_id):
    google = GoogleCustom(
        credentials_filename=const.CREDENTIALS_FILENAME,
        authorized_user_filename=const.AUTHORIZED_USER_FILENAME,
    )

    sheets = google.construct_sheets_instance()
    spreadsheet = sheets.open_by_key(const.SPREADSHEET_ID)

    # Video Columns
    video_columns = [
        [
            "Channel Title",
            "Video ID",
            "Video Title",
            "Duration",
            "Licensed",
            "Published",
            "Tags",
            "Thumbnail URL",
            "View Count",
            "Like Count",
            "Dislike Count",
            "Comment Count",
            "Video URL",
        ]
    ]

    update_worksheet(
        spreadsheet, 0, data.get("videos_info_sheets"), video_columns, "Videos_Info"
    )

    # Channel Columns
    channel_columns = [
        [
            "ID",
            "Title",
            "Description",
            "Custom URL",
            "Published",
            "Country",
            "Video Count",
            "View Count",
            "Hidden Subscriber Count",
            "Subscriber Count",
            "Channel URL",
        ]
    ]

    update_worksheet(
        spreadsheet,
        1,
        data.get("channel_info_sheets"),
        channel_columns,
        "Channels_Info",
    )


def update_worksheet(spreadsheet, index, rows, columns, title):
    worksheet = spreadsheet.get_worksheet(index)

    update_column_headers(worksheet, columns)

    update_worksheet_rows(worksheet, rows, title)


def update_column_headers(worksheet, columns):
    worksheet.update(
        "A1", columns, major_dimension="ROWS", value_input_option="USER_ENTERED"
    )

    worksheet.format(
        "1:1",
        {
            "textFormat": {"bold": True},
            "horizontalAlignment": "CENTER",
        },
    )


def update_worksheet_rows(worksheet, rows, title):
    worksheet.update(
        "A2", rows, major_dimension="ROWS", value_input_option="USER_ENTERED"
    )

    worksheet.update_title(title)
