import praw
from tqdm import tqdm
import os

from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    user_agent='ezLEGAL by /u/Gullible-Beautiful44',
    username=os.getenv('REDDIT_USER'),
    password=os.getenv('REDDIT_PASSWORD')
)

# List of subreddits to scrape
subreddits = ['es', 'argentina', 'mexico', 'spain', 'latinoamerica', 'Chile', 'vzla', 'PERU', 'Colombia', 'AskLatinAmerica']


folder = 'test_data'
os.makedirs(folder, exist_ok=True) 

for sub in subreddits:
    subreddit = reddit.subreddit(sub)
    text = ''
    file_name = f'{folder}/reddit_{sub}.txt' 

    try:
        for i, submission in enumerate(tqdm(subreddit.top(limit=1000, time_filter='all'), desc=f"Scraping r/{sub}")):
            text += submission.title + ' ' + submission.selftext + '\n\n\n************'
            if i % 1000 == 0 and i != 0: 
                with open(file_name, 'a', encoding='utf-8') as f:
                    f.write(text)
                text = ''
    finally:
        if text:  
            with open(file_name, 'a', encoding='utf-8') as f:
                f.write(text)
