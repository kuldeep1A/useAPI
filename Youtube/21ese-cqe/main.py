import os
import dotenv
import googleapiclient.discovery

dotenv.load_dotenv()
API_KEY = os.getenv('API_KEY')
VIDEO_ID = 'KCrXgy8qtjM'


def get_comments(_key, _videoId):
    _youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=_key)
    
    # Get video details
    video_response = _youtube.videos().list(id=_videoId, part='snippet').execute()
    video_title = video_response['items'][0]['snippet']['title']

    # Get comments
    comments = []
    nextPageToken = None
    
    
    while True:
        
        comment_response = _youtube.commentThreads().list(part='snippet', videoId=_videoId, textFormat='plainText', pageToken=nextPageToken).execute()
        
        # view in json COMMENT_RESPONSE to understand whole details
        
        for item in comment_response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
                    
        nextPageToken = comment_response.get('nextPageToken')
        print(nextPageToken)
        
        if not nextPageToken:
            break
    
    return video_title, comments
    
if __name__ == '__main__':
    
    video_title, comments = get_comments(API_KEY, VIDEO_ID)
    
    print(f"Video Title: {video_title}")
    print("\nComments: ", len(comments))
    for i, comment in enumerate(comments, start=1):
        print(f"{i}. {comment}")
    