from googleapiclient.discovery import build
import secret

DEVELOPER_KEY = secret.api_key
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(
    YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

request = youtube.search().list(
    q = "워크맨",
    order = "relevance",
    part = "snippet",
    maxResults = 10
)

response = request.execute()
items = response['items']

# 검색 결과 가져오기
for item in items:
    publish_time = item['snippet']['publishedAt']
    channel_id = item['snippet']['channelId']
    title = item['snippet']['title']
    print(publish_time, channel_id, title)