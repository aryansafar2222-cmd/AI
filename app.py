import streamlit as st
from openai import OpenAI

# پەیوەندی بە LM Studio (دڵنیابە سێرڤەرەکەت لەسەر پۆرت 1234 کار دەکات)
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

st.title("🤖 AI Assistant Pro")
st.write("پرسیارەکەت بنووسە و مۆدێلەکەت وەڵامت دەداتەوە!")

if prompt := st.chat_input("لێرە بینووسە..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="local-model",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content
        st.markdown(answer)