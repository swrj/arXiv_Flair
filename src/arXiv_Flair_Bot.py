import praw
import Config_2
from bs4 import BeautifulSoup
import urllib2
import re


print("Logging in....")
reddit_instance=praw.Reddit(client_id=Config_2.client_id,
                            client_secret=Config_2.client_secret,
                            user_agent=Config_2.user_agent,
                            username=Config_2.username,
                            password=Config_2.password)
print("Logged in.")

TAG_RE = re.compile(r'<[^>]+>') #Specifies characters to ommit

def remove_tags(text):
    return TAG_RE.sub('', text) #Returns texts between <h1></h1> tags

while True:
    print "Searching"
    subreddit=reddit_instance.subreddit("") #Enter subreddit name between the quotes.
    flair=""
    for submission in subreddit.stream.submissions():
        if "arxiv.org" in submission.url:
            print ("Found submission: %s" % (submission.title))
            r=urllib2.urlopen(submission.url).read()
            soup=BeautifulSoup(r, 'xml') #using lxml's HTML parser for fast parsing
            html_line = soup.find_all('div', 'subheader')
            for i in html_line:
                text = str(i.find('h1'))
            cleantext=remove_tags(text)
            if ';' in cleantext:
                index=cleantext.index(';')+2 #returning index after special HTML entity (specifically '>')
                flair=str(cleantext[index:])
            else:
                flair=cleantext
            print ("Flaired post as %s"%(cleantext))
        submission.mod.flair(text=flair, css_class='') #bot needs to be a moderator of subreddit to flair posts
