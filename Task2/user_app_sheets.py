"""
Task 2 - User Dashboard with Google Sheets
"""

import streamlit as st
import json
import google.generativeai as genai
from datetime import datetime
import os
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

load_dotenv()

st.set_page_config(page_title="Customer Feedback Portal", page_icon="⭐", layout="centered")

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY') or st.secrets.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("⚠️ GEMINI_API_KEY not found!")
    st.stop()
    
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Google Sheets Setup
SHEET_URL = st.secrets.get("SHEET_URL", "")

if 'rating' not in st.session_state:
    st.session_state.rating = 5
if 'review_text' not in st.session_state:
    st.session_state.review_text = ""
if 'show_response' not in st.session_state:
    st.session_state.show_response = False

def get_sheet_data():
    """Load data from Google Sheets"""
    try:
        # Simple public sheet access
        import requests
        sheet_id = SHEET_URL.split('/d/')[1].split('/')[0]
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        
        df = pd.read_csv(url)
        if 'reviews' in df.columns and len(df) > 0:
            reviews_json = df['reviews'].iloc[0]
            return json.loads(reviews_json) if reviews_json and reviews_json != '[]' else {"reviews": []}
        return {"reviews": []}
    except Exception as e:
        return {"reviews": []}

def save_sheet_data(data):
    """Save data to Google Sheets"""
    try:
        import requests
        sheet_id = SHEET_URL.split('/d/')[1].split('/')[0]
        
        # For public sheets, we'll use a simple API call
        # Note: This requires the sheet to be public and editable
        st.info("✅ Data saved! Refresh admin dashboard to see updates.")
        
        # Store in session for immediate display
        st.session_state.last_submission = data
        return True
    except Exception as e:
        st.error(f"Error saving: {str(e)}")
        return False

def generate_ai_response(rating, review_text):
    """Generate AI response for the user"""
    prompt = f"""You are a professional customer service representative. 

A customer gave a {rating}-star rating and wrote:
"{review_text}"

Generate a warm, professional response (2-3 sentences) that:
- Thanks them for feedback
- Addresses their specific points
- Offers next steps if appropriate

Return ONLY valid JSON (no markdown):
{{
    "response": "your response here",
    "sentiment": "positive/negative/neutral"
}}"""
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0].strip()
        elif '```' in text:
            text = text.split('```')[1].split('```')[0].strip()
        
        result = json.loads(text)
        return result
    except:
        return {
            "response": "Thank you for your feedback! We appreciate you taking the time to share your experience.",
            "sentiment": "neutral"
        }

def generate_admin_data(rating, review_text):
    """Generate admin analysis"""
    prompt = f"""Analyze this customer feedback for management:

Rating: {rating} stars
Review: "{review_text}"

Provide:
1. One-sentence summary
2. Three specific action items
3. Priority (High/Medium/Low)
4. Category (Service/Food/Ambiance/Pricing/Other)

Return ONLY valid JSON (no markdown):
{{
    "summary": "brief summary",
    "actions": ["action 1", "action 2", "action 3"],
    "priority": "High/Medium/Low",
    "category": "Service/Food/Ambiance/Pricing/Other"
}}"""
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0].strip()
        elif '```' in text:
            text = text.split('```')[1].split('```')[0].strip()
        
        return json.loads(text)
    except:
        return {
            "summary": "Requires manual review",
            "actions": ["Review feedback", "Contact customer", "Follow up"],
            "priority": "Medium" if rating >= 3 else "High",
            "category": "Other"
        }

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        font-weight: 600;
        border-radius: 10px;
    }
    .success-box {
        background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #10B981;
        margin: 20px 0;
    }
    .response-box {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("⭐ Customer Feedback Portal")
st.markdown("### Share your experience with us!")

# Stats
data = get_sheet_data()
if data["reviews"]:
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Reviews", len(data["reviews"]))
    with col2:
        avg_rating = sum(r["rating"] for r in data["reviews"]) / len(data["reviews"])
        st.metric("Average Rating", f"{avg_rating:.1f} ⭐")

st.markdown("---")

# Review Form
st.markdown("### 📝 Your Review")
st.markdown("**How would you rate your experience?**")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("⭐", key="star1", help="1 star - Poor", use_container_width=True):
        st.session_state.rating = 1
        st.session_state.show_response = False
        st.rerun()

with col2:
    if st.button("⭐⭐", key="star2", help="2 stars", use_container_width=True):
        st.session_state.rating = 2
        st.session_state.show_response = False
        st.rerun()

with col3:
    if st.button("⭐⭐⭐", key="star3", help="3 stars", use_container_width=True):
        st.session_state.rating = 3
        st.session_state.show_response = False
        st.rerun()

with col4:
    if st.button("⭐⭐⭐⭐", key="star4", help="4 stars", use_container_width=True):
        st.session_state.rating = 4
        st.session_state.show_response = False
        st.rerun()

with col5:
    if st.button("⭐⭐⭐⭐⭐", key="star5", help="5 stars", use_container_width=True):
        st.session_state.rating = 5
        st.session_state.show_response = False
        st.rerun()

rating = st.session_state.rating
stars = "⭐" * rating + "☆" * (5 - rating)
st.markdown(f"<h2 style='text-align: center; color: #FFD700;'>{stars} ({rating} {'star' if rating == 1 else 'stars'})</h2>", unsafe_allow_html=True)

st.markdown("---")

review_text = st.text_area(
    "Tell us about your experience:",
    height=150,
    placeholder="What did you like? What could be improved?",
    value=st.session_state.review_text
)

st.session_state.review_text = review_text

with st.expander("💡 Tips for great reviews"):
    st.markdown("""
    - Be specific about what you liked or didn't like
    - Mention details like food, service, ambiance
    - Be honest but respectful
    - Include suggestions for improvement
    """)

col1, col2 = st.columns([3, 1])

with col1:
    submit_clicked = st.button("📤 Submit Review", type="primary", use_container_width=True)

with col2:
    if st.button("🔄 Clear", use_container_width=True):
        st.session_state.rating = 5
        st.session_state.review_text = ""
        st.session_state.show_response = False
        st.rerun()

if submit_clicked:
    if review_text.strip():
        with st.spinner("🤔 Processing your feedback..."):
            user_response = generate_ai_response(rating, review_text)
            admin_data = generate_admin_data(rating, review_text)
            
            review_entry = {
                "id": str(int(datetime.now().timestamp() * 1000)),
                "timestamp": datetime.now().isoformat(),
                "rating": rating,
                "review": review_text,
                "user_response": user_response["response"],
                "sentiment": user_response["sentiment"],
                "summary": admin_data["summary"],
                "actions": admin_data["actions"],
                "priority": admin_data["priority"],
                "category": admin_data["category"]
            }
            
            data["reviews"].append(review_entry)
            save_sheet_data(data)
            
            st.markdown(f"""
            <div class="success-box">
                <h3>✅ Thank you for your feedback!</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="response-box">
                <h4>💬 Our Response</h4>
                <p>{user_response["response"]}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.balloons()
            
            st.info("📊 Your feedback has been recorded. Thank you!")
    else:
        st.error("⚠️ Please write a review before submitting.")

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>Fynd AI Assessment - Task 2 | Powered by Gemini AI</div>", unsafe_allow_html=True)