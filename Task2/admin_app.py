# """
# Task 2 - Admin Dashboard
# Fynd AI Intern Assessment

# View all submissions with AI-generated summaries and analytics.
# """

# import streamlit as st
# import json
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from datetime import datetime
# from pathlib import Path
# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Page config
# st.set_page_config(
#     page_title="Admin Dashboard - Customer Feedback",
#     page_icon="🔧",
#     layout="wide"
# )

# # Check API key (optional for admin, but good to verify)
# GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
# if not GEMINI_API_KEY:
#     st.warning("⚠️ GEMINI_API_KEY not found in .env file")

# # Data file
# DATA_FILE = 'reviews_data.json'

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

# # Custom CSS
# st.markdown("""
# <style>
#     .main {
#         background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
#     }
#     .metric-card {
#         background: white;
#         padding: 20px;
#         border-radius: 10px;
#         box-shadow: 0 4px 12px rgba(0,0,0,0.1);
#     }
#     .priority-high {
#         background: #FEE2E2;
#         color: #991B1B;
#         padding: 5px 10px;
#         border-radius: 5px;
#         font-weight: bold;
#     }
#     .priority-medium {
#         background: #FEF3C7;
#         color: #92400E;
#         padding: 5px 10px;
#         border-radius: 5px;
#         font-weight: bold;
#     }
#     .priority-low {
#         background: #D1FAE5;
#         color: #065F46;
#         padding: 5px 10px;
#         border-radius: 5px;
#         font-weight: bold;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Header
# st.title("🔧 Admin Dashboard - Customer Feedback Analysis")

# # Load data
# data = load_data()
# reviews = data["reviews"]

# if not reviews:
#     st.info("📭 No reviews yet. Waiting for customer feedback...")
#     st.stop()

# # Convert to DataFrame
# df = pd.DataFrame(reviews)
# df['timestamp'] = pd.to_datetime(df['timestamp'])

# # Tabs
# tab1, tab2, tab3 = st.tabs(["📋 All Submissions", "📊 Analytics", "🔍 Insights"])

# # ==================== TAB 1: ALL SUBMISSIONS ====================
# with tab1:
#     # Key Metrics
#     col1, col2, col3, col4 = st.columns(4)
    
#     with col1:
#         avg_rating = df['rating'].mean()
#         st.metric("Average Rating", f"{avg_rating:.2f} ⭐")
    
#     with col2:
#         high_priority = len(df[df['priority'] == 'High'])
#         st.metric("High Priority", high_priority, delta="Urgent" if high_priority > 0 else None)
    
#     with col3:
#         positive = len(df[df['sentiment'] == 'positive'])
#         positive_pct = (positive / len(df)) * 100
#         st.metric("Positive Reviews", f"{positive_pct:.0f}%")
    
#     with col4:
#         today = datetime.now().date()
#         today_reviews = len(df[df['timestamp'].dt.date == today])
#         st.metric("Today's Reviews", today_reviews)
    
#     st.markdown("---")
    
#     # Filters
#     st.subheader("🔍 Filters")
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         filter_rating = st.multiselect(
#             "Rating",
#             options=[1, 2, 3, 4, 5],
#             default=[1, 2, 3, 4, 5]
#         )
    
#     with col2:
#         filter_priority = st.multiselect(
#             "Priority",
#             options=['High', 'Medium', 'Low'],
#             default=['High', 'Medium', 'Low']
#         )
    
#     with col3:
#         filter_category = st.multiselect(
#             "Category",
#             options=df['category'].unique().tolist(),
#             default=df['category'].unique().tolist()
#         )
    
#     # Apply filters
#     filtered_df = df[
#         (df['rating'].isin(filter_rating)) &
#         (df['priority'].isin(filter_priority)) &
#         (df['category'].isin(filter_category))
#     ]
    
#     st.markdown(f"**Showing {len(filtered_df)} of {len(df)} reviews**")
#     st.markdown("---")
    
#     # Display reviews
#     for idx, review in filtered_df.sort_values('timestamp', ascending=False).iterrows():
#         with st.expander(
#             f"⭐ {review['rating']} stars - {review['category']} - "
#             f"{review['timestamp'].strftime('%Y-%m-%d %H:%M')}"
#         ):
#             col1, col2 = st.columns([2, 1])
            
#             with col1:
#                 st.markdown("**🔖 Customer Review:**")
#                 st.info(review['review'])
                
#                 st.markdown("**📝 AI Summary:**")
#                 st.success(review['summary'])
                
#                 st.markdown("**🎯 Recommended Actions:**")
#                 for i, action in enumerate(review['actions'], 1):
#                     st.markdown(f"{i}. {action}")
            
#             with col2:
#                 # Priority badge
#                 priority_class = f"priority-{review['priority'].lower()}"
#                 st.markdown(f"**Priority:** <span class='{priority_class}'>{review['priority']}</span>", 
#                           unsafe_allow_html=True)
                
#                 st.markdown(f"**Category:** {review['category']}")
#                 st.markdown(f"**Sentiment:** {review['sentiment'].title()}")
#                 st.markdown(f"**ID:** {review['id'][:8]}...")

# # ==================== TAB 2: ANALYTICS ====================
# with tab2:
#     col1, col2 = st.columns(2)
    
#     with col1:
#         # Rating Distribution
#         st.subheader("Rating Distribution")
#         rating_counts = df['rating'].value_counts().sort_index()
#         fig1 = px.bar(
#             x=rating_counts.index,
#             y=rating_counts.values,
#             labels={'x': 'Stars', 'y': 'Count'},
#             color=rating_counts.values,
#             color_continuous_scale='RdYlGn'
#         )
#         fig1.update_layout(showlegend=False)
#         st.plotly_chart(fig1, use_container_width=True)
        
#         # Priority Distribution
#         st.subheader("Priority Distribution")
#         priority_counts = df['priority'].value_counts()
#         fig3 = px.pie(
#             values=priority_counts.values,
#             names=priority_counts.index,
#             color=priority_counts.index,
#             color_discrete_map={'High': '#EF4444', 'Medium': '#F59E0B', 'Low': '#10B981'}
#         )
#         st.plotly_chart(fig3, use_container_width=True)
    
#     with col2:
#         # Category Distribution
#         st.subheader("Category Breakdown")
#         category_counts = df['category'].value_counts()
#         fig2 = px.pie(
#             values=category_counts.values,
#             names=category_counts.index,
#             hole=0.4
#         )
#         st.plotly_chart(fig2, use_container_width=True)
        
#         # Sentiment Analysis
#         st.subheader("Sentiment Analysis")
#         sentiment_counts = df['sentiment'].value_counts()
#         fig4 = px.bar(
#             x=sentiment_counts.index,
#             y=sentiment_counts.values,
#             labels={'x': 'Sentiment', 'y': 'Count'},
#             color=sentiment_counts.index,
#             color_discrete_map={'positive': '#10B981', 'neutral': '#6B7280', 'negative': '#EF4444'}
#         )
#         st.plotly_chart(fig4, use_container_width=True)
    
#     # Timeline
#     st.subheader("Reviews Over Time")
#     df['date'] = df['timestamp'].dt.date
#     daily_counts = df.groupby('date').size().reset_index(name='count')
#     fig5 = px.line(
#         daily_counts,
#         x='date',
#         y='count',
#         markers=True,
#         labels={'date': 'Date', 'count': 'Number of Reviews'}
#     )
#     st.plotly_chart(fig5, use_container_width=True)

# # ==================== TAB 3: INSIGHTS ====================
# with tab3:
#     st.subheader("🔍 Key Insights")
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.markdown("### 📈 Performance Overview")
        
#         avg_rating = df['rating'].mean()
        
#         if avg_rating >= 4:
#             st.success(f"""
#             ✅ **Excellent Performance**
            
#             Overall rating: **{avg_rating:.2f} stars**
            
#             Customer satisfaction is high. Keep up the great work!
#             """)
#         elif avg_rating >= 3:
#             st.info(f"""
#             📊 **Good Performance**
            
#             Overall rating: **{avg_rating:.2f} stars**
            
#             Performance is solid but there's room for improvement.
#             """)
#         else:
#             st.warning(f"""
#             ⚠️ **Needs Improvement**
            
#             Overall rating: **{avg_rating:.2f} stars**
            
#             Immediate action required to improve customer satisfaction.
#             """)
        
#         # Most common category
#         top_category = df['category'].mode()[0]
#         category_count = len(df[df['category'] == top_category])
#         st.info(f"🏷️ **Most common issue:** {top_category} ({category_count} reviews)")
    
#     with col2:
#         st.markdown("### ⚡ Action Items")
        
#         high_priority_count = len(df[df['priority'] == 'High'])
#         negative_count = len(df[df['sentiment'] == 'negative'])
        
#         st.error(f"🔴 **{high_priority_count}** high-priority items need immediate attention")
#         st.warning(f"⚠️ **{negative_count}** negative reviews need response")
        
#         # Recent critical reviews
#         critical = df[df['rating'] <= 2].sort_values('timestamp', ascending=False).head(3)
        
#         if len(critical) > 0:
#             st.markdown("### 🚨 Recent Critical Reviews")
#             for _, review in critical.iterrows():
#                 st.error(f"""
#                 **{review['rating']} ⭐** - {review['category']}
                
#                 {review['review'][:100]}...
                
#                 *Actions: {', '.join(review['actions'][:2])}*
#                 """)
#         else:
#             st.success("✅ No recent critical reviews!")
    
#     # Full data table
#     st.markdown("---")
#     st.subheader("📊 Complete Data Table")
    
#     display_df = df[['timestamp', 'rating', 'category', 'priority', 'sentiment', 'review', 'summary']].copy()
#     display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
#     display_df = display_df.sort_values('timestamp', ascending=False)
    
#     st.dataframe(
#         display_df,
#         use_container_width=True,
#         hide_index=True
#     )
    
#     # Download button
#     csv = df.to_csv(index=False)
#     st.download_button(
#         label="📥 Download Full Data (CSV)",
#         data=csv,
#         file_name=f"reviews_export_{datetime.now().strftime('%Y%m%d')}.csv",
#         mime="text/csv"
#     )

# # Footer
# st.markdown("---")
# st.markdown(
#     "<div style='text-align: center; color: gray;'>"
#     "Fynd AI Intern Assessment - Task 2 | Admin Dashboard"
#     "</div>",
#     unsafe_allow_html=True
# )

# # Refresh button
# if st.button("🔄 Refresh Data"):
#     st.rerun()










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