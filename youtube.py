from google_custom import GoogleCustom
from googleapiclient import errors
import constants as const
import re


def scrap_youtube_data(channel_ids: list[str]):
    """Scrape YouTube data

    Args:
        channel_ids (list[str]): A list with channel ids for scrapping data

    Returns:
        dict: Formatted data with videos and channels information
    """
    google = GoogleCustom(const.API_NAME, const.API_VERSION, const.API_KEY)
    service = google.construct_youtube_instance()

    videos_info = []
    channels_info = []

    for channel_id in channel_ids:
        full_info = get_full_info(service, channel_id)
        videos_info.extend(full_info.get("videos_info"))
        channels_info.append(full_info.get("channel_info"))

    videos_info_sheets = format_videos_info(videos_info)
    channel_info_sheets = format_channels_info(channels_info)

    data = {
        "videos_info_sheets": videos_info_sheets,
        "channel_info_sheets": channel_info_sheets,
    }

    return data


def get_full_info(service, channel_id):
    """Get full information of the YouTube channel and videos.

    data = {
        "videos_info": videos_info,
        "channel_info": channel_info,
    }

    Args:
        service (Resource): The authenticated service
        channel_id (string): YouTube Channel ID

    Returns:
        dict: Full info of channel and videos.
    """
    response_channel = (
        service.channels()
        .list(part="snippet,contentDetails,statistics", id=channel_id)
        .execute()
    )

    uploads_playlist_id = get_uploads_playlist_id(response_channel)

    try:
        playlist_items = get_playlist_items(
            service,
            uploads_playlist_id,
            response_channel,
        )

        videos_info = get_videos_info(service, playlist_items)
        channel_info = response_channel["items"][0]

        data = {
            "videos_info": videos_info,
            "channel_info": channel_info,
        }

        return data

    except errors.HttpError:
        print("Channel has 0 videos")
        return ""
    except Exception as e:
        print(e)

    return ""


def get_uploads_playlist_id(channel):
    """Get uploads playlist ID

    Args:
        channel ([type]): [description]

    Returns:
        string: Uploads playlist ID
    """
    if channel["pageInfo"]["totalResults"] == 0:
        print("Channel not found.")
        return None
    else:
        items = channel.get("items")[0]
        uploads_playlist_id = items["contentDetails"]["relatedPlaylists"]["uploads"]
        return uploads_playlist_id


def get_playlist_items(service, uploads_playlist_id, response_channel):
    """Get playlist items from channel uploads playlist

    Args:
        service (Resource): The authenticated service
        uploads_playlist_id (string): Uploads playlist ID
        response_channel ([type]): [description]

    Returns:
        tuple: The playlist items
    """
    response_playlist_items = (
        service.playlistItems()
        .list(
            part="contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,
        )
        .execute()
    )

    playlistItems = response_playlist_items["items"]
    nextPageToken = response_playlist_items.get("nextPageToken")

    channel_title = response_channel["items"][0]["snippet"]["title"]
    print(f"Channel: {channel_title}")

    while nextPageToken:
        response_playlist_items = (
            service.playlistItems()
            .list(
                part="contentDetails",
                playlistId=uploads_playlist_id,
                maxResults=50,
                pageToken=nextPageToken,
            )
            .execute()
        )

        playlistItems.extend(response_playlist_items["items"])
        nextPageToken = response_playlist_items.get("nextPageToken")

        print(" Token {0}".format(nextPageToken))

    videos = tuple(v["contentDetails"] for v in playlistItems)

    return videos


def get_videos_info(service, playlist_items):
    """Get videos information

    Args:
        service (Resource): The authenticated service
        playlist_items (list): A list with playlist items from channel

    Returns:
        list: A list with all information from videos
    """
    videos_info = []

    for batch_num in range(0, len(playlist_items), 50):
        video_batch = playlist_items[batch_num : batch_num + 50]

        response_videos = (
            service.videos()
            .list(
                id=",".join(list(map(lambda v: v["videoId"], video_batch))),
                part="snippet,contentDetails,statistics",
                maxResults=50,
            )
            .execute()
        )

        videos_info.extend(response_videos["items"])

    return videos_info


def format_videos_info(videos_info):
    """Format videos data for google sheets spreadsheet

    Args:
        videos_info (list): All videos information for each channel

    Returns:
        list: A list with formatted videos data
    """
    rows = []

    for video in videos_info:
        snippet = video["snippet"]
        stats = video["statistics"]

        rows.append(
            [
                snippet["channelTitle"],
                video["id"],
                snippet["title"],
                convert_duration(video["contentDetails"]["duration"]),
                video["contentDetails"]["licensedContent"],
                snippet["publishedAt"][:-1],
                ", ".join(snippet["tags"]) if snippet.get("tags") else "",
                snippet["thumbnails"]["default"]["url"],
                int(stats["viewCount"]) if stats.get("viewCount") else 0,
                int(stats["likeCount"]) if stats.get("likeCount") else 0,
                int(stats["dislikeCount"]) if stats.get("dislikeCount") else 0,
                int(stats["commentCount"]) if stats.get("commentCount") else 0,
                "https://www.youtube.com/watch?v={0}".format(video["id"]),
            ]
        )

    return rows


def format_channels_info(channels_info):
    """Format channel data for google sheets spreadsheet

    Args:
        channels_info (list): All channels information

    Returns:
        list: A list with formatted channel data
    """
    rows = []

    for channel in channels_info:
        snippet = channel["snippet"]
        stats = channel["statistics"]

        rows.append(
            [
                channel["id"],
                snippet["title"],
                snippet["description"],
                snippet["customUrl"],
                snippet["publishedAt"][:-1],
                snippet["country"],
                int(stats["videoCount"]) if stats.get("videoCount") else 0,
                int(stats["viewCount"]) if stats.get("viewCount") else 0,
                stats["hiddenSubscriberCount"],
                int(stats["subscriberCount"]) if stats.get("subscriberCount") else 0,
                "https://www.youtube.com/channel/{0}".format(channel["id"]),
            ]
        )

    return rows


def convert_duration(duration: str):
    """Convert the duration to HH:MM:SS format

    Args:
        duration (str): The video duration.

    Returns:
        string: The duration is HH:MM:SS format
    """
    try:
        h = (
            re.search(r"\d+H", duration)[0][:-1]
            if re.search(r"\d+H", duration)
            else "00"
        )
        m = (
            re.search(r"\d+M", duration)[0][:-1]
            if re.search(r"\d+M", duration)
            else "00"
        )  # minute
        s = (
            re.search(r"\d+S", duration)[0][:-1]
            if re.search(r"\d+S", duration)
            else "00"
        )  # second

        formatted_time = ":".join([h, m, s])

        return formatted_time
    except Exception as e:
        print(e)
        return ""
