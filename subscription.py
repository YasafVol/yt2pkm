import csv 
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of Cloud Console <https://cloud.google.com/console>
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyBeAWR5HRQgKlZ5Gsau4xbGvF0v57vv-Zk"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This OAuth 2.0 access scope allows for read-only access to the authenticated
# user's account, but not other types of account access.
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']


def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file("C:\Prog\youtube\client_secret.json", SCOPES)
    credentials = flow.run_local_server(port=0)
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)


def get_my_subscriptions(youtube):
    request = youtube.subscriptions().list(
        part="snippet,contentDetails",
        mine=True,
        maxResults=5000
    )
    response = request.execute()
    
    # Create a CSV file and write the header
    with open('subscriptions.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Channel Title", "Channel ID"])  # write the header

        for item in response['items']:
            channel_title = item['snippet']['title']
            channel_id = item['snippet']['resourceId']['channelId']
            print(f"Channel title: {channel_title}, Channel id: {channel_id}")
            writer.writerow([channel_title, channel_id])  # write a row for each subscription

print("List of subscriptions exported to subscriptions.csv.")


if __name__ == "__main__":
    youtube = get_authenticated_service()
    get_my_subscriptions(youtube)
