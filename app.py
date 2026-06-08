import streamlit as st
from groq import Groq

# ڕێکخستنی پەڕەکە
st.set_page_config(page_title="CodexAI Pro", page_icon="🤖")
st.title("🤖 CodexAI Pro")

# بانگکردنی API Key
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("تکایە کلیلی API لە بەشی Secrets دابنێ!")
    st.stop()

# میمۆری بۆ وەڵامەکان
if "messages" not in st.session_state:
    st.session_state.messages = []

# نیشاندانی وەڵامە کۆنەکان
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# وەرگرتنی پرسیار
if prompt := st.chat_input("پرسیارەکەت بنووسە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ناردنی پرسیار بۆ مۆدێل
    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )
            # ئەمە وەڵامەکەت بە شێوەیەکی جوان و خوێندەوارانە نیشان دەدات
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"هەڵەیەک ڕوویدا: {e}")
