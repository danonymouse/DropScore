# 🔥 DropScore

**Reverse-engineer virality in seconds.**

Paste a YouTube link — DropScore scrapes the top comments, runs sentiment and keyword analysis, and reveals what made the video blow up. Great for creators, editors, marketers, or just curious minds.

---

## 🧠 Why I Built This

I kept asking a content strategist how he makes videos go viral.  
He always said: *"It’s just song choice."*

That didn’t sit right. So I spent a weekend building this to find out for myself.

Turns out the truth lies in the comments — raw emotional signals, hype moments, reactions, inside jokes. **DropScore decodes all that** using lightweight NLP, clean visualizations, and a bit of Gen-Z flair.

---

## 🧪 Features

- ✅ Scrape top YouTube comments via YouTube Data API
- ✅ Sentiment scoring using TextBlob
- ✅ Keyword clustering with spaCy
- ✅ AI-style local summary (free, no OpenAI key needed)
- ✅ Viral factor score based on comment volume, mood, and variance
- ✅ Meme Mode 🧠 (adds falling emoji and Comic Sans — because why not?)
- ✅ Built with Streamlit — runs locally, looks sleek

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/DropScore.git
cd DropScore
```

### 2. Set up a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. Add your YouTube API key

Create a `.env` file in the root folder with this:

```env
YOUTUBE_API_KEY=your_api_key_here
```

You can get a free API key from: https://console.cloud.google.com/apis/library/youtube.googleapis.com

### 5. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🖼 Demo (Coming Soon)

---

## 🧩 How It Works

- **🔍 Scraper**: Pulls 100 top-level YouTube comments using official API
- **📊 Analyzer**: Uses `TextBlob` for sentiment, `spaCy` for keyword lemmatization, and `Counter` for frequency
- **🧠 Summary Engine**: Synthesizes a quick AI-style writeup with Gen-Z flair
- **📈 Viral Factor**: A custom score based on mood, volume, and engagement variation
- **🎭 Meme Mode**: Optional toggle with emojis falling from the sky and Comic Sans aesthetics

---

## 🔮 Future Ideas

- [ ] Re-enable TikTok support with a more stable API
- [ ] Parse thumbnails and titles for visual cues
- [ ] Smart topic detection via LLM or BERTopic
- [ ] Downloadable PDF reports for creators
- [ ] Export-to-Notion / Copy-to-Clipboard for summaries

---

## 🤝 Acknowledgements

- [Streamlit](https://streamlit.io/)
- [TextBlob](https://textblob.readthedocs.io/en/dev/)
- [spaCy](https://spacy.io/)
- [Google YouTube Data API](https://developers.google.com/youtube/v3)
- Comic Sans and emoji rain for the vibes

---

## 📬 Contact

Built by **David Lai**  
🎻 Former concertmaster · 🧠 Start-Up strategist

> DropScore: Don’t predict the next trend. Decode the last one.
