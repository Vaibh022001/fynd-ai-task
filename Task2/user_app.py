import streamlit as st
import google.generativeai as genai
from datetime import datetime
import os
import json
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Customer Feedback Portal", page_icon="⭐", layout="centered")

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY') or st.secrets.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("⚠️ GEMINI_API_KEY not found!")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

if 'rating' not in st.session_state:
    st.session_state.rating = 5
if 'review_text' not in st.session_state:
    st.session_state.review_text = ""

def get_gsheet_client():
    """Connect to Google Sheets"""
    try:
        credentials_dict = {
            "type": st.secrets["connections"]["gsheets"]["type"],
            "project_id": st.secrets["connections"]["gsheets"]["project_id"],
            "private_key_id": st.secrets["connections"]["gsheets"]["private_key_id"],
            "private_key": st.secrets["connections"]["gsheets"]["private_key"],
            "client_email": st.secrets["connections"]["gsheets"]["client_email"],
            "client_id": st.secrets["connections"]["gsheets"]["client_id"],
            "auth_uri": st.secrets["connections"]["gsheets"]["auth_uri"],
            "token_uri": st.secrets["connections"]["gsheets"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["connections"]["gsheets"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["connections"]["gsheets"]["client_x509_cert_url"]
        }
        
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        credentials = Credentials.from_service_account_info(credentials_dict, scopes=scopes)
        client = gspread.authorize(credentials)
        
        spreadsheet_url = st.secrets["connections"]["gsheets"]["spreadsheet"]
        sheet = client.open_by_url(spreadsheet_url).sheet1
        
        return sheet
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return None

def load_reviews():
    """Load reviews from Google Sheets"""
    try:
        sheet = get_gsheet_client()
        if sheet:
            data = sheet.get_all_records()
            return pd.DataFrame(data)
        return pd.DataFrame()
    except:
        return pd.DataFrame()

def save_review(review_data):
    """Append review to Google Sheets"""
    try:
        sheet = get_gsheet_client()
        if sheet:
            row = [
                review_data['id'],
                review_data['timestamp'],
                review_data['rating'],
                review_data['review'],
                review_data['user_response'],
                review_data['sentiment'],
                review_data['summary'],
                review_data['actions'],
                review_data['priority'],
                review_data['category']
            ]
            sheet.append_row(row)
            return True
        return False
    except Exception as e:
        st.error(f"Save error: {str(e)}")
        return False

def generate_ai_response(rating, review_text):
    prompt = f"""Professional customer service response for {rating}-star review: "{review_text}"
Return ONLY JSON: {{"response": "2-3 sentences", "sentiment": "positive/negative/neutral"}}"""
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(text)
    except:
        return {"response": "Thank you for your feedback!", "sentiment": "neutral"}

def generate_admin_data(rating, review_text):
    prompt = f"""Analyze: {rating} stars - "{review_text}"
Return ONLY JSON: {{"summary": "brief", "actions": ["1","2","3"], "priority": "High/Medium/Low", "category": "Service/Food/Ambiance/Pricing/Other"}}"""
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(text)
    except:
        return {"summary": "Review received", "actions": ["Review","Follow up","Thank"], "priority": "Medium", "category": "Other"}

st.markdown("""
<style>
.stButton>button {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 12px 30px; font-weight: 600; border-radius: 10px;}
.success-box {background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%); padding: 20px; border-radius: 10px; border-left: 5px solid #10B981; margin: 20px 0;}
.response-box {background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); padding: 20px; border-radius: 10px; border-left: 5px solid #667eea; margin: 20px 0;}
</style>
""", unsafe_allow_html=True)

st.title("⭐ Customer Feedback Portal")
st.markdown("### Share your experience with us!")

df = load_reviews()
if len(df) > 0:
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Reviews", len(df))
    with col2:
        avg = df['rating'].mean() if 'rating' in df.columns else 0
        st.metric("Average Rating", f"{avg:.1f} ⭐")

st.markdown("---")
st.markdown("### 📝 Your Review")
st.markdown("**How would you rate your experience?**")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("⭐", key="star1", use_container_width=True):
        st.session_state.rating = 1
        st.rerun()
with col2:
    if st.button("⭐⭐", key="star2", use_container_width=True):
        st.session_state.rating = 2
        st.rerun()
with col3:
    if st.button("⭐⭐⭐", key="star3", use_container_width=True):
        st.session_state.rating = 3
        st.rerun()
with col4:
    if st.button("⭐⭐⭐⭐", key="star4", use_container_width=True):
        st.session_state.rating = 4
        st.rerun()
with col5:
    if st.button("⭐⭐⭐⭐⭐", key="star5", use_container_width=True):
        st.session_state.rating = 5
        st.rerun()

rating = st.session_state.rating
stars = "⭐" * rating + "☆" * (5 - rating)
st.markdown(f"<h2 style='text-align: center; color: #FFD700;'>{stars} ({rating} star{'s' if rating != 1 else ''})</h2>", unsafe_allow_html=True)

st.markdown("---")

review_text = st.text_area("Tell us about your experience:", height=150, placeholder="What did you like? What could be improved?", value=st.session_state.review_text)
st.session_state.review_text = review_text

col1, col2 = st.columns([3, 1])

with col1:
    submit_clicked = st.button("📤 Submit Review", type="primary", use_container_width=True)
with col2:
    if st.button("🔄 Clear", use_container_width=True):
        st.session_state.rating = 5
        st.session_state.review_text = ""
        st.rerun()

if submit_clicked:
    if review_text.strip():
        with st.spinner("🤔 Processing your feedback..."):
            user_resp = generate_ai_response(rating, review_text)
            admin_data = generate_admin_data(rating, review_text)
            
            review_data = {
                "id": str(int(datetime.now().timestamp() * 1000)),
                "timestamp": datetime.now().isoformat(),
                "rating": rating,
                "review": review_text,
                "user_response": user_resp["response"],
                "sentiment": user_resp["sentiment"],
                "summary": admin_data["summary"],
                "actions": '|'.join(admin_data["actions"]),
                "priority": admin_data["priority"],
                "category": admin_data["category"]
            }
            
            if save_review(review_data):
                st.markdown(f"""
                <div class="success-box"><h3>✅ Thank you for your feedback!</h3></div>
                <div class="response-box"><h4>💬 Our Response</h4><p>{user_resp["response"]}</p></div>
                """, unsafe_allow_html=True)
                
                st.balloons()
                st.success("📊 Your review has been automatically saved and is now visible in the Admin Dashboard!")
            else:
                st.error("Could not save to Google Sheets. Please check connection.")
    else:
        st.error("⚠️ Please write a review before submitting.")

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>Fynd AI Assessment - Automatic Sync</div>", unsafe_allow_html=True)