import matplotlib.pyplot as plt
import streamlit as st
from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
from textblob import TextBlob
from collections import defaultdict
from collections import Counter
import spacy
import re
import random
from sklearn.feature_extraction.text import CountVectorizer
from statistics import stdev


load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
nlp = spacy.load("en_core_web_sm")

def extract_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([\w-]+)", url)
    return match.group(1) if match else None


def get_comments(video_id, max_comments=100):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    comments = []
    next_page_token = None

    while len(comments) < max_comments:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=min(100, max_comments - len(comments)),
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return comments

def analyze_comments(comments):
    keyword_stats = defaultdict(lambda: {'count': 0, 'sentiment_sum': 0.0})
    sentiments = []
    lengths = []
    top_positive = []
    top_negative = []

    for comment in comments:
        sentiment = TextBlob(comment).sentiment.polarity
        sentiments.append(sentiment)
        lengths.append(len(comment))

        if sentiment > 0.4:
            top_positive.append((sentiment, comment))
        elif sentiment < -0.3:
            top_negative.append((sentiment, comment))

        doc = nlp(comment.lower())
        keywords = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]

        for kw in keywords:
            keyword_stats[kw]['count'] += 1
            keyword_stats[kw]['sentiment_sum'] += sentiment

    keyword_summary = []
    for kw, data in keyword_stats.items():
        avg_sent = data['sentiment_sum'] / data['count']
        keyword_summary.append({
            'keyword': kw,
            'count': data['count'],
            'avg_sentiment': round(avg_sent, 3)
        })

    keyword_summary.sort(key=lambda x: (x['count'], x['avg_sentiment']), reverse=True)
    top_positive.sort(reverse=True)
    top_negative.sort()

    return {
        "keywords": keyword_summary,
        "avg_sentiment": round(sum(sentiments) / len(sentiments), 3),
        "lengths": lengths,
        "top_positive_comments": top_positive[:3],
        "top_negative_comments": top_negative[:3]
    }


def get_top_phrases(comments, n=2, top_k=5):
    try:
        vectorizer = CountVectorizer(ngram_range=(n, n), stop_words='english').fit(comments)
        bag = vectorizer.transform(comments)
        counts = bag.sum(axis=0).A1
        phrases = vectorizer.get_feature_names_out()
        sorted_phrases = sorted(zip(phrases, counts), key=lambda x: x[1], reverse=True)
        return sorted_phrases[:top_k]
    except:
        return []

def compute_viral_score(sentiment, comment_count, lengths, keyword_count):
    variance = stdev(lengths) if len(lengths) > 1 else 0
    base = sentiment * 0.4 + min(1, comment_count / 100) * 0.3 + min(1, keyword_count / 20) * 0.3
    boost = 0.1 if variance > 40 else 0
    return round((base + boost) * 100)


def generate_local_summary(comments):
    if not comments:
        return "No comments to summarize."

    # Clean words
    words = []
    for c in comments:
        c = re.sub(r"[^\w\s]", "", c.lower())
        words += c.split()

    counts = Counter(words)

    stopwords = {
        "the", "and", "you", "this", "that", "for", "are", "was", "with", "have", "just",
        "like", "your", "what", "how", "can", "its", "not", "but", "too", "very", "out",
        "who", "why", "had", "they", "she", "he", "his", "her", "them", "then", "than",
    }
    keywords = [w for w in words if w not in stopwords and len(w) > 2]
    top = Counter(keywords).most_common(10)

    main_topics = [kw for kw, count in top if count >= 2]

    sentiment_words = {"love", "amazing", "awesome", "funny", "sad", "boring", "emotional", "vibe"}
    found_sentiment = [w for w in sentiment_words if w in counts]

    summary = ""

    if found_sentiment:
        templates = [
            f"The comments are emotionally charged {random.choice(['🔥', '😭', '😄'])} — words like **{'**, **'.join(found_sentiment)}** stood out.",
            f"Emotional vibes detected {random.choice(['💥', '❤️', '😤'])}. Common reactions included **{'**, **'.join(found_sentiment)}**.",
        ]
        summary += random.choice(templates) + "\n\n"

    if main_topics:
        summary += f"Most discussed topics: **{'**, **'.join(main_topics)}**."

    if summary == "":
        return "Comments were too generic or scattered to summarize meaningfully."

    return summary.strip()

def cluster_comment_contexts(comments):
    themes = {
        "Camera/Tech": {"camera", "lens", "gear", "equipment", "quality"},
        "Music/Sound": {"music", "song", "audio", "soundtrack", "beat"},
        "Emotion": {"cry", "goosebumps", "tears", "emotional", "chills"},
        "Editing/Style": {"edit", "cut", "transition", "color", "effect", "smooth"},
        "Hype/Reaction": {"fire", "🔥", "lit", "insane", "crazy"},
    }

    theme_counts = {k: 0 for k in themes}
    for c in comments:
        text = c.lower()
        for theme, keywords in themes.items():
            if any(k in text for k in keywords):
                theme_counts[theme] += 1

    return {k: v for k, v in theme_counts.items() if v > 0}

def get_mood_emoji(score):
    if score > 0.5:
        return "🔥 Hype"
    elif score > 0.1:
        return "😄 Positive"
    elif score > -0.1:
        return "😐 Neutral"
    elif score > -0.5:
        return "😤 Mixed"
    else:
        return "💀 Brutal"
    
def fake_viral_take(df):
    keywords = set(df["keyword"])
    if "dog" in keywords:
        return "People go crazy for dogs doing literally anything 🐶"
    if "edit" in keywords:
        return "Clean edits + fast pacing = dopamine machine 🧠"
    if "cry" in keywords:
        return "Emotional rollercoaster = instant shareability 😭"
    if df["avg_sentiment"].mean() > 0.5:
        return "Everyone’s loving this. Pure serotonin drip 🔥"
    return "Probably hits the sweet spot between funny, fast, and feels."


def draw_sentiment_bar(score):
    fig, ax = plt.subplots(figsize=(5, 0.5))
    ax.barh(0, score, color="green" if score >= 0 else "red")
    ax.set_xlim(-1, 1)
    ax.set_title("Mood Bar")
    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)
    st.pyplot(fig)
