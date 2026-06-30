import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

# Page config
st.set_page_config(
    page_title="🎓 AI Study Tracker",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5em;
        margin-bottom: 10px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success {
        color: #28a745;
        font-weight: bold;
    }
    .warning {
        color: #ff6b6b;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Constants
CSV_FILE = "study_data.csv"
SUBJECTS = ["Math", "Physics", "Digital Logic", "Microprocessor", "Python", "DSA"]

# Initialize session state
if 'data_updated' not in st.session_state:
    st.session_state.data_updated = False

def initialize_csv():
    """CSV file बनाऊ यदि छैन"""
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=["Date", "Subject", "Hours"])
        df.to_csv(CSV_FILE, index=False)

def load_data():
    """CSV से data load गर"""
    try:
        df = pd.read_csv(CSV_FILE)
        df['Date'] = pd.to_datetime(df['Date'])
        df['Hours'] = pd.to_numeric(df['Hours'], errors='coerce')
        return df
    except:
        return pd.DataFrame(columns=["Date", "Subject", "Hours"])

def save_data(df):
    """Data को CSV मा save गर"""
    df['Date'] = df['Date'].astype(str)
    df.to_csv(CSV_FILE, index=False)

def page_add_record():
    """Add Record Page"""
    st.header(" Add Study Record")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date_option = st.radio(
            " Date Option:",
            ["Today (Auto)", "Manual Entry"],
            horizontal=False
        )
        
        if date_option == "Today (Auto)":
            selected_date = datetime.now().date()
        else:
            selected_date = st.date_input("Select Date:")
    
    with col2:
        subject = st.selectbox(
            " Select Subject:",
            SUBJECTS
        )
    
    with col3:
        hours = st.number_input(
            "⏱ Hours Studied:",
            min_value=0.0,
            max_value=24.0,
            step=0.5,
            value=1.0
        )
    
    if st.button(" Add Record", use_container_width=True):
        if hours <= 0:
            st.error("❌ Hours must be positive!")
        else:
            df = load_data()
            new_record = pd.DataFrame({
                "Date": [selected_date],
                "Subject": [subject],
                "Hours": [hours]
            })
            df = pd.concat([df, new_record], ignore_index=True)
            save_data(df)
            st.success(f" Record Added!\n📅 {selected_date} | 📖 {subject} | ⏱️ {hours} hours")
            st.session_state.data_updated = True

def page_view_records():
    """View Records Page"""
    st.header(" Your Study Records")
    
    df = load_data()
    
    if df.empty:
        st.warning("❌ No records found! Add some records first.")
    else:
        # Display table
        display_df = df.copy()
        display_df['Date'] = display_df['Date'].dt.strftime("%Y-%m-%d")
        st.dataframe(display_df, use_container_width=True)
        
        st.info(f" Total Records: {len(df)}")
        
        # Filter options
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(" Delete Last Record"):
                if len(df) > 0:
                    df = df.iloc[:-1]
                    save_data(df)
                    st.success(" Last record deleted!")
                    st.rerun()
        
        with col2:
            if st.button("🔄 Refresh"):
                st.rerun()

def page_analytics():
    """Analytics Page"""
    st.header(" Analytics & Insights")
    
    df = load_data()
    
    if df.empty:
        st.warning(" No data to analyze!")
        return
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["Daily", "Weekly", "Subject", "Goal"])
    
    # Daily Total
    with tab1:
        st.subheader(" Daily Study Hours")
        daily = df.groupby('Date')['Hours'].sum().sort_index()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig, ax = plt.subplots(figsize=(12, 5))
            daily.plot(kind='bar', ax=ax, color='#1f77b4')
            ax.set_title('Daily Study Hours', fontsize=14, fontweight='bold')
            ax.set_xlabel('Date')
            ax.set_ylabel('Hours')
            plt.xticks(rotation=45)
            st.pyplot(fig)
        
        with col2:
            st.metric(" Total Hours", f"{daily.sum():.1f}h")
            st.metric(" Study Days", len(daily))
            st.metric(" Average/Day", f"{daily.mean():.1f}h")
    
    # Weekly Total
    with tab2:
        st.subheader(" Weekly Study Progress")
        
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        
        week_df = df[(df['Date'] >= pd.Timestamp(week_start)) & 
                     (df['Date'] <= pd.Timestamp(week_end))]
        
        if not week_df.empty:
            daily_week = week_df.groupby('Date')['Hours'].sum()
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig, ax = plt.subplots(figsize=(12, 5))
                daily_week.plot(kind='bar', ax=ax, color='#2ca02c')
                ax.set_title(f'Weekly Hours: {week_start.date()} to {week_end.date()}', 
                            fontsize=14, fontweight='bold')
                ax.set_xlabel('Date')
                ax.set_ylabel('Hours')
                plt.xticks(rotation=45)
                st.pyplot(fig)
            
            with col2:
                st.metric(" Week Total", f"{daily_week.sum():.1f}h")
                st.metric(" Days Studied", len(daily_week))
                st.metric(" Average/Day", f"{daily_week.mean():.1f}h")
        else:
            st.info("No study records this week!")
    
    # Subject Analysis
    with tab3:
        st.subheader("📚 Subject-wise Analysis")
        
        subject_hours = df.groupby('Subject')['Hours'].sum().sort_values(ascending=False)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig, ax = plt.subplots(figsize=(12, 5))
            subject_hours.plot(kind='barh', ax=ax, color='#ff7f0e')
            ax.set_title('Study Hours by Subject', fontsize=14, fontweight='bold')
            ax.set_xlabel('Total Hours')
            st.pyplot(fig)
        
        with col2:
            st.metric("📊 Total Hours", f"{subject_hours.sum():.1f}h")
            top_subject = subject_hours.index[0]
            st.metric("🏆 Top Subject", f"{top_subject}\n{subject_hours.iloc[0]:.1f}h")
    
    # Goal Tracking
    with tab4:
        st.subheader("🎯 Weekly Goal Tracking")
        
        goal = st.slider("Set Weekly Goal (hours):", 10, 100, 35)
        
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        
        week_df = df[(df['Date'] >= pd.Timestamp(week_start)) & 
                     (df['Date'] <= pd.Timestamp(week_end))]
        
        current = week_df['Hours'].sum() if not week_df.empty else 0
        remaining = goal - current
        percentage = (current / goal) * 100 if goal > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Goal", f"{goal}h")
        
        with col2:
            st.metric("📈 Current", f"{current:.1f}h")
        
        with col3:
            if remaining <= 0:
                st.metric("✅ Status", "Achieved!", delta=f"+{abs(remaining):.1f}h")
            else:
                st.metric("⏳ Remaining", f"{remaining:.1f}h")
        
        with col4:
            st.metric("📉 Progress", f"{percentage:.0f}%")
        
        # Progress bar
        st.progress(min(percentage / 100, 1.0))
        
        if remaining <= 0:
            st.success("🎉 Congratulations! Weekly goal achieved!")
        else:
            st.info(f"Study {remaining:.1f} more hours to reach your goal!")

def page_settings():
    """Settings Page"""
    st.header("⚙️ Settings & Help")
    
    tab1, tab2, tab3 = st.tabs(["About", "Data", "Help"])
    
    with tab1:
        st.subheader("🎓 AI Study Tracker v1.0")
        st.write("""
        एक शक्तिशाली study tracker जो तिम्रो अध्ययन को समय ट्र्याक गर्न मदत गर्छ।
        
        **Features:**
        - Daily study tracking
        - Weekly progress analysis
        - Subject-wise analytics
        - Goal setting & tracking
        - Data visualization
        """)
    
    with tab2:
        st.subheader("📊 Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Download Data as CSV", use_container_width=True):
                df = load_data()
                if not df.empty:
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "Download CSV",
                        csv,
                        "study_data.csv",
                        "text/csv"
                    )
        
        with col2:
            if st.button("🗑️ Clear All Data", use_container_width=True):
                if st.button("⚠️ Confirm Delete", key="confirm_delete"):
                    df = pd.DataFrame(columns=["Date", "Subject", "Hours"])
                    save_data(df)
                    st.success("✅ All data cleared!")
                    st.rerun()
    
    with tab3:
        st.subheader("❓ Help & Tips")
        st.write("""
        **Tips for better tracking:**
        
        1. **Daily Entry**: हरेक दिन record add गर
        2. **Subject Balance**: सबै subjects मा समय दे
        3. **Weekly Goals**: Realistic goals set गर
        4. **Review Weekly**: आफ्नो progress review गर
        5. **Stay Consistent**: रोज अध्ययन गर
        
        **Format Guidelines:**
        - Date: Automatically set (Today or Manual)
        - Hours: 0.5 to 24 hours
        - Subject: Choose from dropdown
        
        **Data Storage:**
        - Data CSV file मा save हुन्छ
        - Backup लिन सक्छौ
        - Excel मा खोल सक्छौ
        """)

# Main App
def main():
    initialize_csv()
    
    st.markdown("<h1 class='main-title'>🎓 AI Study Tracker</h1>", unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.title("📚 Navigation")
        page = st.radio(
            "Select Page:",
            ["Dashboard", "Add Record", "View Records", "Analytics", "Settings"],
            label_visibility="collapsed"
        )
    
    # Pages
    if page == "Dashboard":
        st.header("📊 Dashboard")
        
        df = load_data()
        
        if df.empty:
            st.warning("🚀 Welcome! Add your first study record to get started.")
            st.info("""
            **How to use:**
            1. Go to 'Add Record' tab
            2. Select date (Today or Manual)
            3. Choose subject
            4. Enter hours studied
            5. Click 'Add Record'
            
            Then come back here to see your analytics!
            """)
        else:
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Hours", f"{df['Hours'].sum():.1f}")
            
            with col2:
                st.metric(" Total Records", len(df))
            
            with col3:
                st.metric(" Days Studied", df['Date'].nunique())
            
            with col4:
                st.metric("⏱ Average/Day", f"{df['Hours'].mean():.1f}")
            
            # Quick chart
            st.subheader(" Recent Activity")
            
            daily = df.groupby('Date')['Hours'].sum().sort_index().tail(10)
            
            fig, ax = plt.subplots(figsize=(12, 4))
            daily.plot(kind='line', marker='o', ax=ax, color='#1f77b4')
            ax.set_title('Last 10 Days - Study Hours', fontsize=12, fontweight='bold')
            ax.set_xlabel('Date')
            ax.set_ylabel('Hours')
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            st.pyplot(fig)
    
    elif page == "Add Record":
        page_add_record()
    
    elif page == "View Records":
        page_view_records()
    
    elif page == "Analytics":
        page_analytics()
    
    elif page == "Settings":
        page_settings()

if __name__ == "__main__":
    main()