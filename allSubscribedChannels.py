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

def get_all_subscribed_channels(youtube):
    pageToken = None
    with open('channels.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Channel Title", "Channel ID"])

        while True:
            request = youtube.subscriptions().list(
                part="snippet,contentDetails",
                mine=True,
                maxResults=50,
                pageToken=pageToken
            )
            response = request.execute()

            for item in response['items']:
                channel_title = item['snippet']['title']
                channel_id = item['snippet']['resourceId']['channelId']
                writer.writerow([channel_title, channel_id])

            if 'nextPageToken' in response:
                pageToken = response['nextPageToken']
            else:
                break

    print("List of subscriptions exported to channels.csv.")

def main():
    youtube = get_authenticated_service()
    get_all_subscribed_channels(youtube)

if __name__ == "__main__":
    main()
