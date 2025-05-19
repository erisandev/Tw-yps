import tweepy
import openai
import streamlit as st
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Ambil API keys dari environment variables
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Inisialisasi API
client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)
openai.api_key = OPENAI_API_KEY

# Ambil tweet
def get_tweets(username, count=5):
    try:
        user = client.get_user(username=username)
        user_id = user.data.id
        tweets = client.get_users_tweets(id=user_id, max_results=count)
        return [tweet.text for tweet in tweets.data]
    except Exception as e:
        import traceback
        return [f"Error: {traceback.format_exc()}"]

# Analisis tweet
def analyze_tweet(tweet_text):
    prompt = f"""
    Analyze the following crypto-related tweet for potential performance on Kaito AI's system (Yaps):
    ---
    "{tweet_text}"
    ---
    Evaluate: Relevance, Originality, Clarity, Use of Hashtags, Engagement Potential. 
    Give a score from 1-10 and brief feedback.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# UI Streamlit
st.title("Twitter Content Analyzer for Kaito Yaps")

username = st.text_input("Enter Twitter Username")
count = st.slider("Number of tweets to analyze", 1, 10, 5)

if st.button("Analyze"):
    tweets = get_tweets(username, count)
    for i, tweet in enumerate(tweets):
        st.subheader(f"Tweet {i+1}:")
        st.write(tweet)
        if not tweet.startswith("Error:"):
            analysis = analyze_tweet(tweet)
            st.markdown(f"Analysis:\n{analysis}")
        else:
            st.error(tweet)
