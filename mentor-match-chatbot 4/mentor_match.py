import streamlit as st
import openai

# Use OpenAI's new client structure (openai>=1.0.0)
from openai import OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else "your-api-key")

# Apply Clemson color scheme and branding
st.set_page_config(page_title="Clemson PAW Journey Mentor Chatbot", page_icon="🌟")

# Clemson branding header
st.markdown("""
    <div style='background-color:#F56600; padding: 10px 20px; border-radius: 10px;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Clemson_Tigers_logo.svg/512px-Clemson_Tigers_logo.svg.png' width='60' style='float:left; margin-right:20px;'>
        <h1 style='color:white;'>Clemson University PAW Journey Mentor Chatbot</h1>
        <p style='color:white;'>Helping student-athletes discover mentors who share their path and passion.</p>
    </div>
""", unsafe_allow_html=True)

# Optional: PAW Journey logo
st.image("https://www.clemson.edu/studentaffairs/images/paw-journey-logo.png", width=200)

# Welcome message
st.markdown("""
    ### 👋 Welcome Student-Athletes!
    Use this tool to ask any question that might help you find a mentor. For example:
    - "I'm interested in someone who went from football to law."
    - "I'd like to connect with a first-generation college grad in STEM."
    - "Is there a mentor who's worked in product design after athletics?"
""")

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
                model="gpt-3.5-turbo",
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

# Footer with Clemson resources
st.markdown("""
    <hr>
    <small>
    <p style='text-align: center;'>
        This chatbot is a pilot tool of the <strong>PAW Journey Program</strong> at Clemson University.<br>
        For more information, visit <a href='https://www.clemson.edu/studentaffairs/paw-journey/' target='_blank'>PAW Journey</a> or contact your student-athlete development coordinator.
    </p>
    </small>
""", unsafe_allow_html=True)
