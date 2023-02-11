from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import string
import re
import pandas as pd
# from Home import form


class youtubeAPI:
    def __init__(self):
        self.all_comments = []
        self.video_id = ''
        self.api_key = 'AIzaSyCeWL7FWHsYoFgrCEIjOug1qnhTEZzprIE'

    # recursive function to get all replies in a comment thread
    def get_replies(self, comment_id, token):
        replies_response = self.yt_object.comments().list(part = 'snippet', maxResults = 100, parentId = comment_id, pageToken = token).execute()

        for reply in replies_response['items']:
            self.self.all_comments.append(reply['snippet']['textDisplay'])

        if replies_response.get("nextPageToken"):
            return self.get_replies(comment_id, replies_response['nextPageToken'])
        else:
            return []

    # recursive function to get all comments
    def get_comments(self, youtube, video_id, next_view_token):
        # global self.all_comments
        # video_id = self.video_id

        # check for token
        if len(next_view_token.strip()) == 0:
            self.all_comments = []

        if next_view_token == '':
            # get the initial response
            comment_list = youtube.commentThreads().list(part = 'snippet', maxResults = 100, videoId = video_id, order = 'relevance').execute()
        else:
            # get the next page response
            comment_list = youtube.commentThreads().list(part = 'snippet', maxResults = 100, videoId = video_id, order='relevance', pageToken=next_view_token).execute()
        # loop through all top level comments
        for comment in comment_list['items']:
            # add comment to list
            self.all_comments.append([comment['snippet']['topLevelComment']['snippet']['textDisplay']])
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
            self.all_comments[-1].append(all_replies)

        if "nextPageToken" in comment_list:
            return self.get_comments(youtube, video_id, comment_list['nextPageToken'])
        else:
            return []

        # self.all_comments = []

    def clean_text(self, text):
        text = text.lower()
        
        text = re.sub('\[.*?\]','', text)
        text = re.sub('[%s]'%re.escape(string.punctuation), '', text)
        
        text = re.sub('\w*\d\w*','', text)
        text = re.sub('\n','', text)
        
        return text

    def get_yt_comments(self, vID):

        self.video_id = vID

        # build a youtube object using our api key
        yt_object = build('youtube', 'v3', developerKey = self.api_key)
        print(type(yt_object))
        # get all comments and replies
        self.get_comments(yt_object, self.video_id, '')

        # Create an empty list to store the comments and replies
        data = []

        for comment, replies in self.all_comments:
            data.append({'comment': comment, 'replies': replies})
        
        # Create a DataFrame from the list of comments
        
        self.df = pd.DataFrame(data)
        self.df.drop(columns=['replies'], inplace=True)
       

        cleantext = lambda x: self.clean_text(x)
        self.df['comment'] = pd.DataFrame(self.df['comment'].apply(cleantext))
        
        # print(self.df.head(10))
        return self.df

# obj = youtubeAPI()
# # obj.set_video_id('bB7xkRsEq-g')
# dff = obj.get_yt_comments('bB7xkRsEq-g')
# print(dff)
# # obj.main()