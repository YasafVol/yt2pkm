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

def get_channel_details(youtube, channel_id):
    request = youtube.channels().list(
        part="snippet,topicDetails",
        id=channel_id
    )
    response = request.execute()
    return response['items'][0] if response['items'] else None

def append_channel_details_to_csv(youtube):
    # Read the channel IDs from channels.csv
    with open('channels.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        channels = list(reader)

    # Add headers for the metadata columns
    channels[0].extend(["Description", "Custom URL", "Published At", "Topics"])

    # Fetch and append the metadata for each channel
    for i in range(1, len(channels)):
        channel_id = channels[i][1]
        details = get_channel_details(youtube, channel_id)
        if details:
            description = details['snippet']['description']
            custom_url = details['snippet'].get('customUrl', 'N/A') # Custom URL might not be available
            published_at = details['snippet']['publishedAt']
            topics = details['topicDetails']['topicCategories'] if 'topicDetails' in details and 'topicCategories' in details['topicDetails'] else "N/A"
            channels[i].extend([description, custom_url, published_at, topics])

    # Write the updated rows back to channels.csv
    with open('channels.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(channels)

    print("Channel metadata appended to channels.csv.")

def main():
    youtube = get_authenticated_service()
    append_channel_details_to_csv(youtube)

if __name__ == "__main__":
    main()
