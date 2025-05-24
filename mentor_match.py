import streamlit as st
import openai

from openai import OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else "your-api-key")

st.set_page_config(page_title="Mentor Match AI Chatbot", page_icon="🔎")
st.title("🌟 Mentor Match AI Chatbot")
st.markdown("Helping student-athletes discover mentors with shared journeys.")

mentor_profiles = [
    {
        "name": "Chris Thompson",
        "bio": "Former college soccer player. Transitioned into finance after earning an MBA. Works at Morgan Stanley as an investment analyst.",
        "tags": ["finance", "MBA", "soccer", "career switch"]
    },
    {
        "name": "Jasmine Lee",
        "bio": "Track and field athlete turned biomedical engineer. First-generation college graduate passionate about mentoring others in STEM.",
        "tags": ["STEM", "engineering", "first-gen", "track"]
    },
    {
        "name": "Marcus Reid",
        "bio": "Played football at a D1 school and later pursued law. Now works in sports law helping athletes with contracts and NIL rights.",
        "tags": ["law", "NIL", "football", "sports management"]
    },
    {
        "name": "Sophie Zhang",
        "bio": "Volleyball player who moved into UX design and tech product development. Based in San Francisco, working at a startup.",
        "tags": ["UX", "tech", "startup", "volleyball"]
    }
]

user_query = st.text_input("What kind of mentor are you looking for?", placeholder="e.g., Someone who played football and works in law")

if user_query:
    prompt = f"You are a mentor-matching assistant. Based on this student request: '{user_query}', suggest the most relevant mentors from the following profiles: {mentor_profiles}. For each suggestion, explain briefly why they might be a good match."

    with st.spinner("Finding your mentor match..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful AI mentor-matching assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            reply = response.choices[0].message.content
            st.markdown("---")
            st.markdown("### 🔍 Mentor Suggestions")
            st.write(reply)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
