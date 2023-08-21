import csv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    credentials = flow.run_local_server(port=0)
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)

def get_video_details(youtube, video_id):
    request = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=video_id
    )
    response = request.execute()
    return response['items'][0] if response['items'] else None

def get_channel_videos(youtube, channel_id):
    page_token = None
    videos = []
    while True:
        request = youtube.search().list(
            part="id",
            channelId=channel_id,
            maxResults=50,
            pageToken=page_token
        )
        response = request.execute()
        videos.extend(response['items'])
        page_token = response.get('nextPageToken')
        if not page_token:
            break
    return videos

def write_videos_to_csv(youtube):
    with open('channels.csv', 'r', encoding='utf-8') as channels_file:
        reader = csv.reader(channels_file)
        next(reader) # Skip header row
        with open('videos.csv', 'w', newline='', encoding='utf-8') as videos_file:
            writer = csv.writer(videos_file)
            writer.writerow(["Channel ID", "Video ID", "Title", "Description", "Published At", "Thumbnail URL", "Tags", "Duration", "View Count", "Like Count", "Dislike Count", "Comment Count", "Category ID", "Privacy Status", "Live Broadcast Status", "Localized Title", "Localized Description"]) # Headers

            for row in reader:
                channel_id = row[1]
                video_list = get_channel_videos(youtube, channel_id)
                for video in video_list:
                    video_id = video['id']['videoId']
                    details = get_video_details(youtube, video_id)
                    title = details['snippet']['title']
                    description = details['snippet']['description']
                    published_at = details['snippet']['publishedAt']
                    thumbnail_url = details['snippet']['thumbnails']['default']['url']
                    tags = ",".join(details['snippet']['tags']) if 'tags' in details['snippet'] else "N/A"
                    duration = details['contentDetails']['duration']
                    view_count = details['statistics']['viewCount']
                    like_count = details['statistics']['likeCount']
                    dislike_count = details['statistics']['dislikeCount']
                    comment_count = details['statistics']['commentCount']
                    category_id = details['snippet']['categoryId']
                    privacy_status = details['status']['privacyStatus']
                    live_broadcast_status = details['snippet']['liveBroadcastContent']
                    localized_title = details['snippet']['localized']['title']
                    localized_description = details['snippet']['localized']['description']
                    writer.writerow([channel_id, video_id, title, description, published_at, thumbnail_url, tags, duration, view_count, like_count, dislike_count, comment_count, category_id, privacy_status, live_broadcast_status, localized_title, localized_description])

    print("List of videos exported to videos.csv.")

def main():
    youtube = get_authenticated_service()
    write_videos_to_csv(youtube)

if __name__ == "__main__":
    main()
