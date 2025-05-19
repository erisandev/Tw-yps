import tweepy
import openai
import streamlit as st

# Masukkan API keys kamu di sini
TWITTER_BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAO1O1wEAAAAAZlapElU%2FfvOtHTrL2JyKE%2Fp2%2Blc%3DnSHS5qCx7SY9sUZBr48TwzIVHazUl2ohx59XyhqeD0TAwoiq5v"
OPENAI_API_KEY = "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"

client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)
openai.api_key = OPENAI_API_KEY

def get_tweets(username, count=5):
    try:
        user = client.get_user(username=username)
        user_id = user.data.id
        tweets = client.get_users_tweets(id=user_id, max_results=count)
        return [tweet.text for tweet in tweets.data]
    except Exception as e:
        return [f"Error: {e}"]

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
            st.markdown(f"**Analysis:**\n{analysis}")
        else:
            st.error(tweet)
