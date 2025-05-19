import streamlit as st
import snscrape.modules.twitter as sntwitter
import openai

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

def get_tweets_no_api(username, count=5):
    tweets = []
    try:
        for i, tweet in enumerate(sntwitter.TwitterUserScraper(username).get_items()):
            if i >= count:
                break
            tweets.append(tweet.content)
    except Exception as e:
        return [f"Error: {e}"]
    return tweets

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

st.title("Twitter Content Analyzer for Kaito Yaps (No API)")

username = st.text_input("Enter Twitter Username")
count = st.slider("Number of tweets to analyze", 1, 10, 5)

if st.button("Analyze"):
    tweets = get_tweets_no_api(username, count)
    for i, tweet in enumerate(tweets):
        st.subheader(f"Tweet {i+1}:")
        st.write(tweet)
        if not tweet.startswith("Error:"):
            analysis = analyze_tweet(tweet)
            st.markdown(f"Analysis:\n{analysis}")
        else:
            st.error(tweet)
