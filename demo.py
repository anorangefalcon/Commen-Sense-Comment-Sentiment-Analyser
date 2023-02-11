# This is a arbitrary file to see how google yt API works !
# Project is not dependent on this file

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd

# video_id = "j8NSMNx2yUM"
video_id = input("Give the video id (for eg: https://www.youtube.com/watch?v=((UV1ZF6pyhtM&ab))_channel=1littlecoder) the thing in double brackets is the video id ")
api_key = 'AIzaSyCeWL7FWHsYoFgrCEIjOug1qnhTEZzprIE'

# recursive function to get all replies in a comment thread
def get_replies(comment_id, token):
    replies_response = yt_object.comments().list(part = 'snippet', maxResults = 100, parentId = comment_id, pageToken = token).execute()

    for reply in replies_response['items']:
        all_comments.append(reply['snippet']['textDisplay'])

    if replies_response.get("nextPageToken"):
        return get_replies(comment_id, replies_response['nextPageToken'])
    else:
        return []


# recursive function to get all comments
def get_comments(youtube, video_id, next_view_token):
    global all_comments

    # check for token
    if len(next_view_token.strip()) == 0:
        all_comments = []

    if next_view_token == '':
        # get the initial response
        comment_list = youtube.commentThreads().list(part = 'snippet', maxResults = 100, videoId = video_id, order = 'relevance').execute()
    else:
        # get the next page response
        comment_list = youtube.commentThreads().list(part = 'snippet', maxResults = 100, videoId = video_id, order='relevance', pageToken=next_view_token).execute()
    # loop through all top level comments
    for comment in comment_list['items']:
        # add comment to list
        all_comments.append([comment['snippet']['topLevelComment']['snippet']['textDisplay']])
        # get number of replies
        reply_count = comment['snippet']['totalReplyCount']
        all_replies = []
        # if replies greater than 0
        if reply_count > 0:
            # get first 100 replies
            replies_list = youtube.comments().list(part='snippet', maxResults=100, parentId=comment['id']).execute()
            for reply in replies_list['items']:
                # add reply to list
                all_replies.append(reply['snippet']['textDisplay'])

            # check for more replies
            while "nextPageToken" in replies_list:
                token_reply = replies_list['nextPageToken']
                # get next set of 100 replies
                replies_list = youtube.comments().list(part = 'snippet', maxResults = 100, parentId = comment['id'], pageToken = token_reply).execute()
                for reply in replies_list['items']:
                    # add reply to list
                    all_replies.append(reply['snippet']['textDisplay'])

        # add all replies to the comment
        all_comments[-1].append(all_replies)

    if "nextPageToken" in comment_list:
        return get_comments(youtube, video_id, comment_list['nextPageToken'])
    else:
        return []


all_comments = []

# build a youtube object using our api key
yt_object = build('youtube', 'v3', developerKey=api_key)

# get all comments and replies
comments = get_comments(yt_object, video_id, '')

# for comment, replies in all_comments:
#     print(comment)
#     if len(replies) > 0:
#         print("There are", len(replies), "replies")
#         print("\tReplies:")
#         for reply in replies:
#             print("\t" + reply)
#     print()


# Create an empty list to store the comments and replies
data = []

for comment, replies in all_comments:
    data.append({'comment': comment, 'replies': replies})

# Create a DataFrame from the list of comments
df = pd.DataFrame(data)

df.drop(columns=['replies'], inplace=True)

print(df.head(10))