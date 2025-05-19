import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from dropscore import (
    extract_video_id,
    get_comments,
    analyze_comments,
    compute_viral_score,
    generate_local_summary,
    get_mood_emoji,
    cluster_comment_contexts,
    fake_viral_take,
    draw_sentiment_bar,
)

# --------- Page Config ---------
st.set_page_config(page_title="DropScore", layout="centered")

# --------- Mode Toggle ---------
mode = st.radio("Choose Your Vibe:", ["Normal Mode", "Meme Mode"])

# --------- CSS Styling ---------
if mode == "Meme Mode":

    st.markdown("""
        <style>
        body {
            background-color: #fff0f5;
            color: #222;
            font-family: Comic Sans MS, cursive;
        }
        .block-container {
            padding-top: 3.5rem;
        }
        </style>
        <script>
        const emojis = ["🔥", "💀", "💬", "💡"];
        const interval = setInterval(() => {
            const emoji = document.createElement('div');
            emoji.textContent = emojis[Math.floor(Math.random() * emojis.length)];
            emoji.style.position = 'fixed';
            emoji.style.top = '-2em';
            emoji.style.left = Math.random() * 100 + 'vw';
            emoji.style.fontSize = '30px';
            emoji.style.zIndex = '9999';
            emoji.style.animation = 'drop 3s linear infinite';
            document.body.appendChild(emoji);
            setTimeout(() => emoji.remove(), 3000);
        }, 300);

        const style = document.createElement('style');
        style.innerHTML = `
            @keyframes drop {
                to { transform: translateY(100vh); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
        </script>
    """, unsafe_allow_html=True)




else:
    st.markdown("""
        <style>
        .block-container {
            padding-top: 3.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

# --------- App UI ---------
st.title("🔥 DropScore")
st.markdown("Paste a YouTube video link and we’ll help you reverse-engineer **why it popped**.")

url = st.text_input("🎥 YouTube Video URL")


if st.button("Analyze") and url:
    with st.spinner("Scraping and analyzing..."):
        video_id = extract_video_id(url)
        if not video_id:
            st.error("⚠️ That ain't a YouTube link, chief. Try again.")
            st.stop()

        comments = get_comments(video_id, max_comments=100)


        if not comments:
            st.warning("No comments found on this video.")
        else:
            try:
                results = analyze_comments(comments)
                df = pd.DataFrame(results["keywords"])
                st.markdown("### 🤖 What's the secret sauce?")
                summary = generate_local_summary(comments)
                st.success(summary)
                st.markdown("### 🧩 Context Clusters")
                clusters = cluster_comment_contexts(comments)
                if clusters:
                    for theme, count in clusters.items():
                        st.markdown(f"- **{theme}**: {count} mentions")
                else:
                    st.write("Couldn’t detect clear comment themes.")



                st.success("✅ Analysis complete!")
                if mode == "Meme Mode":
                    st.snow()

                st.toast("🤓 Data decrypted. The vibes are in.", icon="🧠")


                mood = get_mood_emoji(results["avg_sentiment"])
                st.markdown(f"### 🎭 Vibe Check: {mood}")
                draw_sentiment_bar(results["avg_sentiment"])

                st.markdown("### 🧠 Why This Might've Gone Viral")
                st.info(fake_viral_take(df))

                viral_score = compute_viral_score(results["avg_sentiment"], len(comments), results["lengths"], len(df))
                st.metric("🌐 Viral Factor Score", f"{viral_score}/100")

                st.markdown("### 🧠 Keyword Frequency + Sentiment")
                st.dataframe(df)

                st.markdown("### 📈 Top Keywords by Frequency")
                fig, ax = plt.subplots()
                chart_data = df.head(10)
                ax.bar(chart_data["keyword"], chart_data["count"])
                ax.set_ylabel("Count")
                ax.set_xlabel("Keyword")
                ax.set_title("Top Keywords")
                plt.xticks(rotation=45)
                st.pyplot(fig)

                st.markdown("### 💬 Top Positive Comments")
                for score, comment in results["top_positive_comments"]:
                    st.success(f"({round(score, 2)}) {comment}")

                st.markdown("### 😠 Top Negative Comments")
                for score, comment in results["top_negative_comments"]:
                    st.error(f"({round(score, 2)}) {comment}")

                st.markdown("### 📊 Average Sentiment Score")
                st.metric(label="📢 Video Mood", value=results["avg_sentiment"])

                st.markdown("### 📝 Comment Length Distribution")
                fig2, ax2 = plt.subplots()
                ax2.hist(results["lengths"], bins=10, color='hotpink' if mode == "Meme Mode" else 'skyblue')
                ax2.set_xlabel("Comment Length (chars)")
                ax2.set_ylabel("Frequency")
                ax2.set_title("Comment Length Distribution")
                st.pyplot(fig2)

            except Exception as e:
                st.error(f"Something went wrong: {e}")

    st.markdown("---")
    if st.button("🔁 Try Another Video"):
        st.experimental_rerun()
