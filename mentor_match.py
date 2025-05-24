import streamlit as st
import openai
import fitz  # PyMuPDF for PDF text extraction
import io

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

# Optional: PAW Journey logo (if publicly accessible)
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
    },
    {
        "name": "Ahmed Musa",
        "bio": "International student from Nigeria and former track athlete. Studied computer science and now works in cybersecurity at a major healthcare provider.",
        "tags": ["international", "track", "cybersecurity", "healthcare"]
    },
    {
        "name": "Emily Rivera",
        "bio": "Former softball player and military veteran. Transitioned into public policy and advocacy for student-athletes with disabilities.",
        "tags": ["military", "softball", "public policy", "disability advocacy"]
    },
    {
        "name": "Tyler Nguyen",
        "bio": "Basketball player and artist who turned his passion for design into a career in advertising. Mentors students in creative fields.",
        "tags": ["basketball", "art", "advertising", "creative careers"]
    },
    {
        "name": "Priya Desai",
        "bio": "Former swimmer and pre-med student who shifted into healthcare consulting after working with underserved communities.",
        "tags": ["healthcare", "consulting", "swimming", "service"]
    }
]

# Additional option: Upload mentor resumes for future integration
st.markdown("""
    <hr>
    ### 📄 Upload Mentor Resumes (Experimental)
    You can upload PDF resumes here to simulate future mentor profiles.
    Note: These are not stored. They are used only during this session and are not saved after refresh.
""")

uploaded_files = st.file_uploader("Upload mentor resumes", type=["pdf"], accept_multiple_files=True)
if uploaded_files:
    st.markdown("### 📝 Extracted Text Preview")
    for file in uploaded_files:
        st.subheader(f"{file.name}")
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            text = "\n".join(page.get_text() for page in doc)
            st.text_area(label=f"Extracted text from {file.name}", value=text[:2000], height=200)
            try:
                summarization_prompt = f"Summarize this mentor resume in 2-3 sentences for student-athletes seeking guidance:\n{text[:3000]}"
                summary = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an assistant that generates brief mentor bios from resumes."},
                        {"role": "user", "content": summarization_prompt}
                    ]
                ).choices[0].message.content
                mentor_profiles.append({"name": file.name.replace(".pdf", ""), "bio": summary, "tags": []})
            except Exception as e:
                st.warning(f"Could not summarize {file.name}: {e}")

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
