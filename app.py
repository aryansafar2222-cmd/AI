import streamlit as st
from groq import Groq

# ڕێکخستنی لاپەڕەکە
st.set_page_config(page_title="CodexAI Pro", page_icon="💻")
st.title("💻 CodexAI Pro")
st.subheader("یاریدەدەرێکی پسپۆڕ بۆ کۆد و لۆژیک")

# بانگکردنی API Key لە Secrets
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("تکایە کلیلی APIـەکەت لە بەشی Secrets دابنێ.")
    st.stop()

# سەرەتای چات
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "تۆ یاریدەدەرێکی شارەزایت لە کۆدینگی پایتۆن و چارەسەرکردنی هەڵەکان."}
    ]

# نیشاندانی چات
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# وەرگرتنی نووسین لە بەکارهێنەر
if prompt := st.chat_input("کۆدەکەت لێرە بنووسە یان پرسیار بکە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
