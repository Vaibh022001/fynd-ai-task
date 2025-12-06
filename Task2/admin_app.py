import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Admin Dashboard", page_icon="📊", layout="wide")

def get_gsheet_client():
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
    try:
        sheet = get_gsheet_client()
        if sheet:
            data = sheet.get_all_records()
            return pd.DataFrame(data)
        return pd.DataFrame()
    except:
        return pd.DataFrame()

st.markdown("""
<style>
.priority-high {background-color: #FEE2E2; color: #991B1B; padding: 5px 10px; border-radius: 5px; font-weight: bold;}
.priority-medium {background-color: #FEF3C7; color: #92400E; padding: 5px 10px; border-radius: 5px; font-weight: bold;}
.priority-low {background-color: #D1FAE5; color: #065F46; padding: 5px 10px; border-radius: 5px; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

st.title("📊 Admin Dashboard - Customer Feedback")

col1, col2 = st.columns([1, 5])
with col1:
    if st.button("🔄 Refresh", type="primary"):
        st.rerun()
with col2:
    st.write(f"⏰ {datetime.now().strftime('%H:%M:%S')}")

df = load_reviews()

if df.empty or len(df) == 0:
    st.info("📭 No reviews yet! Submit your first review from the User Dashboard.")
    st.stop()

if 'timestamp' in df.columns:
    df['timestamp'] = pd.to_datetime(df['timestamp'])
if 'rating' in df.columns:
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

tab1, tab2, tab3 = st.tabs(["📋 All Submissions", "📈 Analytics", "💡 Insights"])

with tab1:
    st.markdown("### All Customer Reviews")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Average Rating", f"{df['rating'].mean():.1f} ⭐")
    with col2:
        high = len(df[df['priority'] == 'High'])
        st.metric("High Priority", high)
    with col3:
        pos = len(df[df['sentiment'] == 'positive'])
        st.metric("Positive", f"{pos/len(df)*100:.0f}%")
    with col4:
        st.metric("Total Reviews", len(df))
    
    st.markdown("---")
    
    for _, row in df.sort_values('timestamp', ascending=False).iterrows():
        with st.expander(f"⭐ {row['rating']} stars - {pd.to_datetime(row['timestamp']).strftime('%Y-%m-%d %H:%M')} - **{row['category']}**"):
            st.write(f"**Customer Review:**")
            st.write(f"> {row['review']}")
            st.write(f"**AI Summary:** {row['summary']}")
            
            priority_class = f"priority-{row['priority'].lower()}"
            st.markdown(f"<span class='{priority_class}'>{row['priority']} Priority</span> | **Sentiment:** {row['sentiment']}", unsafe_allow_html=True)
            
            st.write("**Recommended Actions:**")
            if '|' in str(row['actions']):
                for action in str(row['actions']).split('|'):
                    st.write(f"- {action}")

with tab2:
    st.markdown("### Analytics Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.bar(df['rating'].value_counts().sort_index(), title="Rating Distribution")
        st.plotly_chart(fig1, use_container_width=True)
        
        fig3 = px.pie(df, names='priority', title="Priority Distribution")
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        fig2 = px.pie(df, names='category', title="Category Breakdown")
        st.plotly_chart(fig2, use_container_width=True)
        
        fig4 = px.bar(df['sentiment'].value_counts(), title="Sentiment Analysis")
        st.plotly_chart(fig4, use_container_width=True)

with tab3:
    st.markdown("### Key Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        excellent = len(df[df['rating'] >= 4])
        st.success(f"**Excellent (4-5★):** {excellent} reviews")
    with col2:
        good = len(df[df['rating'] == 3])
        st.info(f"**Good (3★):** {good} reviews")
    with col3:
        poor = len(df[df['rating'] < 3])
        st.warning(f"**Needs Attention (<3★):** {poor} reviews")
    
    csv = df.to_csv(index=False)
    st.download_button("📥 Download All Reviews", csv, f"feedback_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>Real-time Dashboard</div>", unsafe_allow_html=True)