import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Treeview
from Model import model 
from ytAPI import youtubeAPI

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold

import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
matplotlib.use('TkAgg')

class form:
    def __init__ (self):
        self.frame = tk.Tk()
        self.frame.geometry("1200x1200")
        # self.frame.config(bg = "orange")
        self.frame.title("Youtube Video Comments Sentiment Analysis")

        yt_link_text = tk.StringVar()

        self.lbl = tk.Label(self.frame, text = 'Enter link to a youtube video')
        self.lbl.place(x=300, y=50)
        self.yt_link_textfield = tk.Entry(self.frame, textvariable = yt_link_text)
        self.yt_link_textfield.place(x=600, y =50)

        self.submit_button = tk.Button(self.frame, text="Submit", command = self.submit_click)
        self.submit_button.place(x = 480, y = 90)

        self.comment_tree = Treeview(self.frame)
        self.comment_tree['columns'] = ('c1')
        self.comment_tree.column("#0", width=700)
        self.comment_tree.column('c1', anchor = 'center')

        self.comment_tree.heading('#0', text = 'Comment')
        self.comment_tree.heading('c1', text = 'Sentiment')
        self.comment_tree.place(x= 100, y=170)

        self.frame.mainloop()

    def submit_click(self):    
        self.yt_link_text = self.yt_link_textfield.get()

        start = self.yt_link_text.find("v=")
        start += 2
        end = self.yt_link_text.find("&", start)
        self.video_id = self.yt_link_text[start:end]

        self.objAPI = youtubeAPI()
        yt_comments = self.objAPI.get_yt_comments(self.video_id)
        yt_comments['sentiment'] = None 
        # print(yt_comments)

        # getting training data for training:
        self.objModel = model()
        training_data = self.objModel.get_clean_training_data()

        Independent_var = training_data.comment
        Dependent_var = training_data.Remark

        vect = TfidfVectorizer()
        clf = LogisticRegression()
        model_logistic = Pipeline([('vectorizer', vect), ('classifier', clf)])

        model_logistic.fit(Independent_var, Dependent_var)

        for index, row in yt_comments.iterrows():
            prediction = model_logistic.predict([row['comment']])
            yt_comments.at[index,'sentiment'] = " ".join(prediction)

        print("hello before yt comments")
        print(yt_comments)


        x = ['+VE', '-VE']
        self.sentiment_count = yt_comments['sentiment'].value_counts()
        fig1 = Figure(figsize = (3,3), dpi =100)
        # fig1.set_facecolor('orange')
        plot1 = fig1.add_subplot(111)
        explode = (0, 0.1)
        colors = ['#99ff99', '#ff9999']
        plot1.pie(self.sentiment_count,explode = explode, labels = x, autopct = '%0.2f%%', colors = colors)
        canvas1 = FigureCanvasTkAgg(fig1, master = self.frame)
        canvas1.draw()
        canvas1.get_tk_widget().place(x = 100, y=450)

        fig2 = Figure(figsize=(3,3), dpi =100)
        # fig2.set_facecolor('orange')
        
        plot2 = fig2.add_subplot(111)
        plot2.bar(x, self.sentiment_count, color = colors)
        for index, value in enumerate(self.sentiment_count):
            plot2.text(value, index, str(value))
        canvas2 = FigureCanvasTkAgg(fig2, master = self.frame)
        canvas2.draw()
        canvas2.get_tk_widget().place(x = 500, y=450)


        for index, row in yt_comments.iterrows():
            # print(row[0])
            self.comment_tree.insert("", 0, text = row['comment'], values = (row['sentiment']))
        print(self.sentiment_count)
  

        


obj = form()
