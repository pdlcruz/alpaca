import praw
from tqdm import tqdm
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Reddit client using environment variables
reddit = praw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    user_agent='ezLEGAL by /u/Gullible-Beautiful44',
    username=os.getenv('REDDIT_USER'),
    password=os.getenv('REDDIT_PASSWORD')
)

# List of subreddits to scrape
subreddits = ['es', 'argentina', 'mexico', 'spain', 'latinoamerica', 'Chile', 'vzla', 'PERU', 'Colombia', 'AskLatinAmerica']

# folder = 'reddit_data_unfiltered'
folder = 'test_data'
os.makedirs(folder, exist_ok=True) 
# Loop through each subreddit and scrape posts
for sub in subreddits:
    subreddit = reddit.subreddit(sub)
    text = ''
    file_name = f'{folder}/reddit_{sub}.txt'  # Unique file for each subreddit

    try:
        for i, submission in enumerate(tqdm(subreddit.top(limit=1000, time_filter='all'), desc=f"Scraping r/{sub}")):
            text += submission.title + ' ' + submission.selftext + '\n\n\n************'
            if i % 1000 == 0 and i != 0:  # Save every thousand submissions
                with open(file_name, 'a', encoding='utf-8') as f:
                    f.write(text)
                text = ''
    finally:
        if text:  # Save any remaining text if the loop ends before hitting another thousand
            with open(file_name, 'a', encoding='utf-8') as f:
                f.write(text)
