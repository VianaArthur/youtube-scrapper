from youtube import scrap_youtube_data
from sheets import save_to_sheets
import constants as const

# Channels

# Alura Cursos Online - https://www.youtube.com/channel/UCo7EHzKF2zDFWszw7Dg4mPw
# freeCodeCamp.org - https://www.youtube.com/channel/UC8butISFwT-Wl7EV0hUK0BQ
# Lucas Nhimi - https://www.youtube.com/channel/UCVE9-HO_GzLtDK4IGKVSYXA
# Rocketseat - https://www.youtube.com/channel/UCSfwM5u0Kce6Cce8_S72olg
# Traversy Media - https://www.youtube.com/channel/UC29ju8bIPH5as8OGnQzwJyA


if __name__ == "__main__":
    # Channel IDs to scrape data
    channel_ids = [
        "UCo7EHzKF2zDFWszw7Dg4mPw",
        "UC8butISFwT-Wl7EV0hUK0BQ",
        "UCVE9-HO_GzLtDK4IGKVSYXA",
        "UCSfwM5u0Kce6Cce8_S72olg",
        "UC29ju8bIPH5as8OGnQzwJyA",
    ]

    # Retrieve formatted data (channel and videos) from YouTube
    data = scrap_youtube_data(channel_ids)

    # Save data go spreadsheet in Google Sheets
    save_to_sheets(data, const.SPREADSHEET_ID)
