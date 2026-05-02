import streamlit as st
import edge_tts
import asyncio
import tempfile
import os

st.set_page_config(page_title="English TTS App", page_icon="🔊")

st.title("🔊 English Sentence Speaker")
st.write("輸入英文句子後，按下播放，即可產生美式英文男聲語音。")

# 較接近美國年輕男聲
VOICE = "en-US-AndrewNeural"

text = st.text_area(
    "請輸入英文句子：",
    value="Good morning! I am happy to learn English today.",
    height=120
)

rate = st.slider("語速調整", -30, 30, 0, step=5)
pitch = st.slider("音高調整", -20, 20, 5, step=5)

async def text_to_speech(text, output_file):
    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate=f"{rate:+d}%",
        pitch=f"{pitch:+d}Hz"
    )
    await communicate.save(output_file)

if st.button("▶️ 產生並播放語音"):
    if not text.strip():
        st.warning("請先輸入英文句子。")
    else:
        with st.spinner("正在產生語音..."):
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_path = temp_file.name
            temp_file.close()

            asyncio.run(text_to_speech(text, temp_path))

            with open(temp_path, "rb") as audio_file:
                audio_bytes = audio_file.read()

            st.audio(audio_bytes, format="audio/mp3")
            st.download_button(
                label="下載 MP3",
                data=audio_bytes,
                file_name="english_speech.mp3",
                mime="audio/mp3"
            )

            os.remove(temp_path)

st.caption("Voice: en-US-AndrewNeural")