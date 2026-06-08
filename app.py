import streamlit as st
from groq import Groq

# ١. ڕێکخستنی لاپەڕەکە: ناوی ئەپ و ئایکۆن دیاری دەکەین
st.set_page_config(page_title="CodexAI Pro", page_icon="🤖")
st.title("🤖 CodexAI Pro")
st.markdown("یاریدەدەرێکی زیرەک بە بەکارهێنانی مۆدێلی **Llama 3.1**")

# ٢. بانگکردنی کلیلی API: کلیلەکە لە Streamlit Secrets دەخوێنینەوە
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception as e:
    st.error("تکایە کلیلی API لە بەشی Secrets دابنێ!")
    st.stop()

# ٣. ڕێکخستنی مێمۆری چات (Session State)
# بۆ ئەوەی وەڵامەکان لە نێوان پرسیارەکاندا ون نەبن
if "messages" not in st.session_state:
    st.session_state.messages = []

# ٤. نیشاندانی مێژووی چات: هەرچی پرسیار و وەڵام هەیە دووبارە نیشانی دەدەین
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ٥. وەرگرتنی پرسیاری نوێ لە بەکارهێنەر
if prompt := st.chat_input("پرسیارەکەت بنووسە..."):
    # زیادکردنی پرسیارەکەی بەکارهێنەر بۆ لیستەکە
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ٦. ناردنی پرسیار بۆ Groq و نیشاندانی وەڵام
    with st.chat_message("assistant"):
        try:
            # پەیوەندی بە Groq
            stream = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )
            # ئەم فەرمانە وەڵامەکەت بە جوانی نیشان دەدات و کێشەی JSON چارەسەر دەکات
            response = st.write_stream(stream)
            
            # پاشەکەوتکردنی وەڵامی AI لە مێمۆریدا
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"هەڵەیەک ڕوویدا: {e}")
