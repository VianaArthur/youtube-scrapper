from googleapiclient.discovery import build
import gspread
import constants as const


class GoogleCustom:
    """A class to represent a Google instance and services

    Attributes:
        api_name: A string the name of the API
        api_version: A string to represent the version of the API
        api_key: A string to represent the API key
        credentials_filename: A string to represent the path to credentials.json file
        authorized_user_filename: A string to represent the path to authorized_user.json file
    """

    def __init__(
        self,
        api_name: str = None,
        api_version: str = None,
        api_key: str = None,
        credentials_filename: str = None,
        authorized_user_filename: str = None,
    ):
        """Construct all the necessaries atributes for GoogleCustom

        Args:
            api_name (str, optional): The API name. Defaults to None.
            api_version (str, optional): The API version. Defaults to None.
            api_key (str, optional): The API key. Defaults to None.
            credentials_filename (str, optional): The path for credentials.json. Defaults to None.
            authorized_user_filename (str, optional): The path for authorized_user.json. Defaults to None.
        """

        self.api_name = api_name
        self.api_version = api_version
        self.api_key = api_key
        self.credentials_filename = credentials_filename
        self.authorized_user_filename = authorized_user_filename

    def construct_youtube_instance(self):
        """Initialize and authenticate the YouTube Service

        Returns:
            Resource: A Resource object with methods for interacting with the service.
        """
        try:
            service = build(self.api_name, self.api_version, developerKey=self.api_key)
            print("YouTube API Service Created.")
            return service
        except Exception as e:
            print(e)
            return None

    def construct_sheets_instance(self):
        """Initialize and authenticate the Google Sheets Service with OAuth

        Returns:
            Client: The authenticate Google Sheets Client
        """
        try:
            service = gspread.oauth(
                credentials_filename=self.credentials_filename,
                authorized_user_filename=self.authorized_user_filename,
            )
            print("Google Sheets API Service Created.")
            return service
        except Exception as e:
            print(e)
            return None


if __name__ == "__main__":
    # YouTube
    google_custom_yt = GoogleCustom(const.API_NAME, const.API_VERSION, const.API_KEY)
    yt_service = google_custom_yt.construct_youtube_instance()

    # Google Sheets
    google_custom_sheets = GoogleCustom(
        credentials_filename=const.CREDENTIALS_FILENAME,
        authorized_user_filename=const.AUTHORIZED_USER_FILENAME,
    )
    sheets_service = google_custom_sheets.construct_sheets_instance()
