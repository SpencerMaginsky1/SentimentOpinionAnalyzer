import praw
import sqlite3
import sentiment
import chart
import tkinter as tk
from tkinter import simpledialog


opinions = []




def redditInit(subreddit_name):
    reddit = praw.Reddit(
    client_id="JgZGz2-DqxGbXbKWMXUVpQ", 
    client_secret="V6FLK4hxhBIWBESrHcFuGGj6pJgzsw",  
    username="RestNo8881",  
    password="Intro2SE",   
    user_agent="MyRedditBot/1.0 by RestNo8881"  
    )
    # reddit = praw.Reddit(
    # client_id = '-sNjrH1D4GDBXhLT9w0QA',
    # client_secret = 'IJwmr-APta5T9SADu0QwXBZAwi_DA',
    # user_agent = 'my-app by: Valencia Student',
    # username = "Independent-Month552",
    # password = "Brooklyn1!"
    # )
     
    try:
        print("Authenticated as:", reddit.user.me()) # Prints reddit username
    except Exception as e:
        print("Login failed:", e)

    #Get subreddit posts
    subreddit = reddit.subreddit(subreddit_name)

    topPost = subreddit.hot(limit=2500)# make "limit=None"
    
    #create DB if one not created
    connect_db()
    clear_db()

    opinions.clear()


    for post in topPost:
        insert_db(post.id, post.title)
        print("\n")
        
    display()
    sentimentFunc()

def connect_db():
    connect = sqlite3.connect("database.db") 
    cursor = connect.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS president(
                        id INTEGER PRIMARY KEY autoincrement, 
                        postID TEXT, 
                        post TEXT)''')

    connect.commit()
    connect.close()

def clear_db():
    connect = sqlite3.connect("database.db")
    connect.execute("DELETE FROM president")  # Clear all rows
    connect.commit()
    connect.close()

#insert data in to DB
def insert_db(postID, post):
    connect = sqlite3.connect("database.db")
    connect.execute('''INSERT INTO president(postID,post) VALUES (?, ?)''', [postID, post])
    connect.commit()
    

#see if data was added to DB
def display():
    connect = sqlite3.connect('database.db')
    cur = connect.execute('SELECT post FROM president')
    res = cur.fetchall()

    print("Number of rows in DB:", len(res))

    #loop DB to get str
    for i in res:
        opinions.append(i[0])


def sentimentFunc():
    for opinion in opinions:
        sentiment.scoreText(opinion)
        print('PERSONAL OPINIONS: \n {}'.format(opinion))


# GUI Setup
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sentiment Opinion Analyzer")

        []
        self.state("zoomed")  
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight())) #adjusting for window/screen size

        self.subreddit_screen = SubredditScreen(self)
        self.chart_screen = ChartScreen(self)

        self.subreddit_screen.pack(fill="both", expand=True)

    def switch_to_chart(self):
        self.subreddit_screen.pack_forget()
        self.chart_screen.pack(fill="both", expand=True)

    def switch_to_subreddit(self):
        self.chart_screen.pack_forget()
        self.subreddit_screen.pack(fill="both", expand=True)

#Screen1: Enter subreddit name / Go to Chart screen
class SubredditScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        #Chart button at top right of the window 
        top_bar = tk.Frame(self, bg="#f0f0f0")
        top_bar.pack(side="top", fill="x")

        chart_button = tk.Button(top_bar, text="Chart", font=("Arial", 16), command=master.switch_to_chart)
        chart_button.pack(side="right", padx=10, pady=10)

        #Center content with Enter SubReddit
        center = tk.Frame(self)
        center.pack(expand=True)

        label = tk.Label(center, text="Enter the name of a subreddit (e.g. politics):", font=("Arial", 18))
        label.pack(pady=10)

        self.entry = tk.Entry(center, font=("Arial", 18), width=30)
        self.entry.pack(pady=10)

        submit_btn = tk.Button(center, text="Submit", font=("Arial", 18), command=self.submit_subreddit)
        submit_btn.pack(pady=20)


    def submit_subreddit(self):
        subreddit_name = self.entry.get().strip()
        if subreddit_name:
            sentiment.reset()
            redditInit(subreddit_name)
    
            # Get the sentiment results
            pos, neg, neu = sentiment.getPos(), sentiment.getNeg(), sentiment.getNeu()

            # Switch to chart screen
            self.master.switch_to_chart()

            # Plot chart inside the chart screen's chart_container
            chart.plot(pos, neg, neu, self.master.chart_screen.chart_container)
            


class ChartScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # Top bar with SubReddit button
        top_bar = tk.Frame(self, bg="#f0f0f0")
        top_bar.pack(side="top", fill="x")

        back_button = tk.Button(top_bar, text="SubReddit Entry", font=("Arial", 16), command=master.switch_to_subreddit)
        back_button.pack(side="right", padx=10, pady=10)

        self.chart_container = tk.Frame(self)
        self.chart_container.pack(expand=True, fill="both", pady=20)

# Run the app 
if __name__ == "__main__":
    app = App()
    app.mainloop()
    
    

