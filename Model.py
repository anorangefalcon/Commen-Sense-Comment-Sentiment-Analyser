from ytAPI import youtubeAPI
import re
import string
import pandas as pd

class model: 
    def __init__(self):
        # test_df = pd.read_csv("/Users/rishabmehndiratta/Documents/Spic Project/Data/trainingTweets.csv", encoding='latin')
        self.training_df = pd.read_csv("/Users/anorangefalcon/Downloads/YT Project/trainingTweets.csv", encoding='latin')

        self.training_df.drop(columns = ['1467810369','Mon Apr 06 22:19:45 PDT 2009','NO_QUERY','_TheSpecialOne_'], inplace = True)
        print(type(self.training_df.Remark))
        # self.training_df.Remark = self.training_df.Remark.str.replace(0,'negative')
        # self.training_df.Remark = self.training_df.Remark.str.replace(4,'positive')
        self.training_df["Remark"] = self.training_df["Remark"].replace({0: "negative", 4: "positive"})
        self.training_df['comment'] = self.training_df['comment'].str.replace(r"@[A-Za-z0-9_]+", '')
        
        cleantext = lambda x: self.clean_text(x)
        self.training_df['comment'] = pd.DataFrame(self.training_df['comment'].apply(cleantext))
        print("hello I'm model's innit")

    def clean_text(self, text):

        text = text.lower()
        
        text = re.sub('\[.*?\]','', text)
        text = re.sub('[%s]'%re.escape(string.punctuation), '', text)
        
        text = re.sub('\w*\d\w*','', text)
        text = re.sub('\n','', text)
        
        return text

    def get_clean_training_data(self):
        return self.training_df

    # def clean_data(self):
    #     # if self.isAPI == False:
    #     #     test_df = pd.read_csv("/Users/rishabmehndiratta/Documents/Spic Project/Data/trainingTweets.csv", encoding='latin')
    #     #     # df.head()

    #     #     test_df.drop(columns = ['1467810369','Mon Apr 06 22:19:45 PDT 2009','NO_QUERY','_TheSpecialOne_'], inplace = True)
    #     #     test_df.Remark = test_df.Remark.str.replace(0,'negative')
    #     #     test_df.Remark = test_df.Remark.str.replace(4,'positive')
    #     #     test_df['comment'] = test_df['comment'].str.replace(r'@[A-Za-z0-9_]+', '')
    #     #     cleantext = lambda x: self.clean_text(x)

    #     #     test_df['Cleaned_Description'] = pd.DataFrame(test_df['comment'].apply(cleantext))
    #     else:
    #         cleantext = lambda x: self.clean_text(x)
    #         self.df['Cleaned_Description'] = pd.DataFrame(self.df['comment'].apply(cleantext))
    #         print(self.df['Cleaned_Description'].head())


# obj = model()
# obj.clean_data()

