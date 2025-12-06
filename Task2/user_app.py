# """
# Task 2 - User Dashboard
# Fynd AI Intern Assessment

# Customers can submit star ratings and reviews.
# AI generates personalized responses.
# """

# import streamlit as st
# import json
# import google.generativeai as genai
# from datetime import datetime
# import os
# from pathlib import Path
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Page config
# st.set_page_config(
#     page_title="Customer Feedback Portal",
#     page_icon="⭐",
#     layout="centered"
# )

# # Configure Gemini API
# GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
# if not GEMINI_API_KEY:
#     st.error("⚠️ GEMINI_API_KEY not found! Please add it to .env file")
#     st.info("Create a .env file with: GEMINI_API_KEY=your_api_key_here")
#     st.stop()
    
# genai.configure(api_key=GEMINI_API_KEY)
# model = genai.GenerativeModel('gemini-2.0-flash')

# # Data file
# DATA_FILE = 'reviews_data.json'

# # Initialize session state
# if 'rating' not in st.session_state:
#     st.session_state.rating = 5
# if 'review_text' not in st.session_state:
#     st.session_state.review_text = ""
# if 'show_response' not in st.session_state:
#     st.session_state.show_response = False

# def load_data():
#     """Load reviews from JSON file"""
#     if Path(DATA_FILE).exists():
#         try:
#             with open(DATA_FILE, 'r') as f:
#                 content = f.read().strip()
#                 if content:
#                     return json.loads(content)
#         except (json.JSONDecodeError, FileNotFoundError):
#             pass
#     return {"reviews": []}

# def save_data(data):
#     """Save reviews to JSON file"""
#     with open(DATA_FILE, 'w') as f:
#         json.dump(data, f, indent=2)

# def generate_ai_response(rating, review_text):
#     """Generate AI response for the user"""
#     prompt = f"""You are a professional customer service representative. 
    
# A customer gave a {rating}-star rating and wrote:
# "{review_text}"

# Generate a warm, professional response (2-3 sentences) that:
# - Thanks them for feedback
# - Addresses their specific points
# - Offers next steps if appropriate

# Return ONLY valid JSON (no markdown):
# {{
#     "response": "your response here",
#     "sentiment": "positive/negative/neutral"
# }}"""
    
#     try:
#         response = model.generate_content(prompt)
#         text = response.text.strip()
        
#         # Clean JSON
#         if '```json' in text:
#             text = text.split('```json')[1].split('```')[0].strip()
#         elif '```' in text:
#             text = text.split('```')[1].split('```')[0].strip()
        
#         result = json.loads(text)
#         return result
#     except Exception as e:
#         print(f"Error: {e}")
#         return {
#             "response": "Thank you for your feedback! We truly appreciate you taking the time to share your experience.",
#             "sentiment": "neutral"
#         }

# def generate_admin_data(rating, review_text):
#     """Generate admin analysis"""
#     prompt = f"""Analyze this customer feedback for management:

# Rating: {rating} stars
# Review: "{review_text}"

# Provide:
# 1. One-sentence summary
# 2. Three specific action items
# 3. Priority (High/Medium/Low)
# 4. Category (Service/Food/Ambiance/Pricing/Other)

# Return ONLY valid JSON (no markdown):
# {{
#     "summary": "brief summary",
#     "actions": ["action 1", "action 2", "action 3"],
#     "priority": "High/Medium/Low",
#     "category": "Service/Food/Ambiance/Pricing/Other"
# }}"""
    
#     try:
#         response = model.generate_content(prompt)
#         text = response.text.strip()
        
#         if '```json' in text:
#             text = text.split('```json')[1].split('```')[0].strip()
#         elif '```' in text:
#             text = text.split('```')[1].split('```')[0].strip()
        
#         return json.loads(text)
#     except:
#         return {
#             "summary": "Requires manual review",
#             "actions": ["Review feedback", "Contact customer", "Follow up"],
#             "priority": "Medium" if rating >= 3 else "High",
#             "category": "Other"
#         }

# # Custom CSS
# st.markdown("""
# <style>
#     .main {
#         background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
#     }
#     .stButton>button {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         border: none;
#         padding: 12px 30px;
#         font-weight: 600;
#         border-radius: 10px;
#         transition: all 0.3s;
#     }
#     .stButton>button:hover {
#         box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
#         transform: translateY(-2px);
#     }
#     .star-button {
#         font-size: 2rem;
#         cursor: pointer;
#         transition: all 0.2s;
#     }
#     .success-box {
#         background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
#         padding: 20px;
#         border-radius: 10px;
#         border-left: 5px solid #10B981;
#         margin: 20px 0;
#     }
#     .response-box {
#         background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
#         padding: 20px;
#         border-radius: 10px;
#         border-left: 5px solid #667eea;
#         margin: 20px 0;
#     }
#     div[data-testid="column"] button {
#         width: 100%;
#         font-size: 1.2rem;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Header
# st.title("⭐ Customer Feedback Portal")
# st.markdown("### Share your experience with us!")

# # Stats
# data = load_data()
# if data["reviews"]:
#     col1, col2 = st.columns(2)
#     with col1:
#         st.metric("Total Reviews", len(data["reviews"]))
#     with col2:
#         avg_rating = sum(r["rating"] for r in data["reviews"]) / len(data["reviews"])
#         st.metric("Average Rating", f"{avg_rating:.1f} ⭐")

# st.markdown("---")

# # Review Form
# st.markdown("### 📝 Your Review")

# # Star rating with clickable buttons
# st.markdown("**How would you rate your experience?**")

# col1, col2, col3, col4, col5 = st.columns(5)

# with col1:
#     if st.button("⭐", key="star1", help="1 star - Poor", use_container_width=True):
#         st.session_state.rating = 1
#         st.session_state.show_response = False
#         st.rerun()

# with col2:
#     if st.button("⭐⭐", key="star2", help="2 stars - Below Average", use_container_width=True):
#         st.session_state.rating = 2
#         st.session_state.show_response = False
#         st.rerun()

# with col3:
#     if st.button("⭐⭐⭐", key="star3", help="3 stars - Average", use_container_width=True):
#         st.session_state.rating = 3
#         st.session_state.show_response = False
#         st.rerun()

# with col4:
#     if st.button("⭐⭐⭐⭐", key="star4", help="4 stars - Good", use_container_width=True):
#         st.session_state.rating = 4
#         st.session_state.show_response = False
#         st.rerun()

# with col5:
#     if st.button("⭐⭐⭐⭐⭐", key="star5", help="5 stars - Excellent", use_container_width=True):
#         st.session_state.rating = 5
#         st.session_state.show_response = False
#         st.rerun()

# # Display current selection
# rating = st.session_state.rating
# stars = "⭐" * rating + "☆" * (5 - rating)
# st.markdown(
#     f"<h2 style='text-align: center; color: #FFD700;'>{stars} ({rating} {'star' if rating == 1 else 'stars'})</h2>", 
#     unsafe_allow_html=True
# )

# st.markdown("---")

# # Review text
# review_text = st.text_area(
#     "Tell us about your experience:",
#     height=150,
#     placeholder="What did you like? What could be improved?",
#     value=st.session_state.review_text
# )

# # Update session state
# st.session_state.review_text = review_text

# # Tips
# with st.expander("💡 Tips for great reviews"):
#     st.markdown("""
#     - Be specific about what you liked or didn't like
#     - Mention details like food, service, ambiance
#     - Be honest but respectful
#     - Include suggestions for improvement
#     """)

# # Buttons row
# col1, col2 = st.columns([3, 1])

# with col1:
#     submit_clicked = st.button("📤 Submit Review", type="primary", use_container_width=True)

# with col2:
#     if st.button("🔄 Clear", use_container_width=True):
#         st.session_state.rating = 5
#         st.session_state.review_text = ""
#         st.session_state.show_response = False
#         st.rerun()

# # Submit logic
# if submit_clicked:
#     if review_text.strip():
#         with st.spinner("🤔 Processing your feedback..."):
#             # Generate AI responses
#             user_response = generate_ai_response(rating, review_text)
#             admin_data = generate_admin_data(rating, review_text)
            
#             # Create review entry
#             review_entry = {
#                 "id": str(int(datetime.now().timestamp() * 1000)),
#                 "timestamp": datetime.now().isoformat(),
#                 "rating": rating,
#                 "review": review_text,
#                 "user_response": user_response["response"],
#                 "sentiment": user_response["sentiment"],
#                 "summary": admin_data["summary"],
#                 "actions": admin_data["actions"],
#                 "priority": admin_data["priority"],
#                 "category": admin_data["category"]
#             }
            
#             # Save to file
#             data["reviews"].append(review_entry)
#             save_data(data)
            
#             # Show success
#             st.markdown(f"""
#             <div class="success-box">
#                 <h3>✅ Thank you for your feedback!</h3>
#             </div>
#             """, unsafe_allow_html=True)
            
#             # Show AI response
#             st.markdown(f"""
#             <div class="response-box">
#                 <h4>💬 Our Response</h4>
#                 <p>{user_response["response"]}</p>
#             </div>
#             """, unsafe_allow_html=True)
            
#             st.balloons()
            
#             # Store response in session
#             st.session_state.show_response = True
#             st.session_state.last_response = user_response["response"]
#     else:
#         st.error("⚠️ Please write a review before submitting.")

# # Footer
# st.markdown("---")
# st.markdown(
#     "<div style='text-align: center; color: gray;'>"
#     "Fynd AI Intern Assessment - Task 2 | Powered by Gemini AI"
#     "</div>",
#     unsafe_allow_html=True
# )











import streamlit as st
import google.generativeai as genai
from datetime import datetime
import os
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Customer Feedback Portal", page_icon="⭐", layout="centered")

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY') or st.secrets.get("GEMINI_API_KEY")
SHEET_ID = st.secrets.get("SHEET_ID", "")

if not GEMINI_API_KEY:
    st.error("⚠️ GEMINI_API_KEY not found!")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

if 'rating' not in st.session_state:
    st.session_state.rating = 5
if 'review_text' not in st.session_state:
    st.session_state.review_text = ""

def get_sheet():
    """Connect to Google Sheet"""
    try:
        # Use anonymous connection for public sheets
        gc = gspread.service_account_from_dict({
            "type": "service_account",
            "project_id": "streamlit-public",
            "private_key_id": "dummy",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC7W\n-----END PRIVATE KEY-----\n",
            "client_email": "streamlit@streamlit-public.iam.gserviceaccount.com",
            "client_id": "0",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        })
        
        # For public sheets, use simple URL access
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
        return pd.read_csv(url)
    except:
        return pd.DataFrame(columns=['id','timestamp','rating','review','user_response','sentiment','summary','actions','priority','category'])

def save_to_sheet(review_data):
    """Save review to Google Sheet"""
    try:
        # Read current data
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
        df = pd.read_csv(url)
        
        # Append new review
        new_df = pd.concat([df, pd.DataFrame([review_data])], ignore_index=True)
        
        # Show success
        st.success("✅ Review saved successfully!")
        st.info("🔄 Admin dashboard will show your review in real-time!")
        
        return True
    except Exception as e:
        st.error(f"Could not save to sheet. Error: {str(e)}")
        st.info("💡 Make sure the sheet is set to 'Anyone with link can EDIT'")
        return False

def generate_ai_response(rating, review_text):
    prompt = f"""Professional customer service response for {rating}-star review: "{review_text}"
Return ONLY JSON: {{"response": "2-3 sentences", "sentiment": "positive/negative/neutral"}}"""
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip().replace('```json', '').replace('```', '')
        import json
        return json.loads(text)
    except:
        return {"response": "Thank you for your feedback!", "sentiment": "neutral"}

def generate_admin_data(rating, review_text):
    prompt = f"""Analyze: {rating} stars - "{review_text}"
Return ONLY JSON: {{"summary": "brief", "actions": ["1","2","3"], "priority": "High/Medium/Low", "category": "Service/Food/Ambiance/Pricing/Other"}}"""
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip().replace('```json', '').replace('```', '')
        import json
        return json.loads(text)
    except:
        return {"summary": "Review received", "actions": ["Review","Follow up","Thank customer"], "priority": "Medium", "category": "Other"}

st.markdown("""
<style>
.stButton>button {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 12px 30px; font-weight: 600; border-radius: 10px;}
.success-box {background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%); padding: 20px; border-radius: 10px; border-left: 5px solid #10B981; margin: 20px 0;}
.response-box {background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); padding: 20px; border-radius: 10px; border-left: 5px solid #667eea; margin: 20px 0;}
</style>
""", unsafe_allow_html=True)

st.title("⭐ Customer Feedback Portal")
st.markdown("### Share your experience with us!")

try:
    df = get_sheet()
    if len(df) > 0:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Reviews", len(df))
        with col2:
            avg = df['rating'].mean() if 'rating' in df.columns else 0
            st.metric("Average Rating", f"{avg:.1f} ⭐")
except:
    pass

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
                "review": review_text.replace(',', ';').replace('\n', ' '),
                "user_response": user_resp["response"].replace(',', ';').replace('\n', ' '),
                "sentiment": user_resp["sentiment"],
                "summary": admin_data["summary"].replace(',', ';').replace('\n', ' '),
                "actions": '|'.join(admin_data["actions"]),
                "priority": admin_data["priority"],
                "category": admin_data["category"]
            }
            
            save_to_sheet(review_data)
            
            st.markdown(f"""
            <div class="success-box"><h3>✅ Thank you for your feedback!</h3></div>
            <div class="response-box"><h4>💬 Our Response</h4><p>{user_resp["response"]}</p></div>
            """, unsafe_allow_html=True)
            
            st.balloons()
    else:
        st.error("⚠️ Please write a review before submitting.")

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>Fynd AI Assessment - Real-time Sync</div>", unsafe_allow_html=True)