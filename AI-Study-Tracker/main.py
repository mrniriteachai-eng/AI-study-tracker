import pandas as pd
import os
from datetime import datetime, timedelta

# CSV file name
CSV_FILE = "study_data.csv"

# Subject list
SUBJECTS = ["Math", "Physics", "Digital Logic", "Microprocessor", "Python", "DSA"]

def initialize_csv():
    """CSV file बनाऊ यदि छैन"""
    if not os.path.exists(CSV_FILE):
        # Empty DataFrame with columns
        df = pd.DataFrame(columns=["Date", "Subject", "Hours"])
        df.to_csv(CSV_FILE, index=False)
        print(f" {CSV_FILE} file created!")

def load_data():
    """CSV से data load गर"""
    try:
        df = pd.read_csv(CSV_FILE)
        return df
    except:
        return pd.DataFrame(columns=["Date", "Subject", "Hours"])

def save_data(df):
    """Data को CSV मा save गर"""
    df.to_csv(CSV_FILE, index=False)

def add_study_record():
    """नयाँ study record add गर"""
    print("\n" + "="*50)
    print(" ADD STUDY RECORD")
    print("="*50)
    
    # Date selection
    print("\nDate Option:")
    print("1. Today (Auto)")
    print("2. Manual Entry (YYYY-MM-DD)")
    date_choice = input("Choose (1/2): ").strip()
    
    if date_choice == "1":
        date = datetime.now().strftime("%Y-%m-%d")
        print(f" Date: {date} (Today)")
    elif date_choice == "2":
        date = input("Enter Date (YYYY-MM-DD): ").strip()
        # Validate date format
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print(" Invalid date format! Try again.")
            return
    else:
        print(" Invalid choice!")
        return
    
    # Subject selection
    print("\nChoose Subject:")
    for i, subject in enumerate(SUBJECTS, 1):
        print(f"{i}. {subject}")
    
    subject_choice = input("Enter Choice (1-6): ").strip()
    
    try:
        subject_idx = int(subject_choice) - 1
        if subject_idx < 0 or subject_idx >= len(SUBJECTS):
            print(" Invalid choice!")
            return
        subject = SUBJECTS[subject_idx]
    except:
        print(" Invalid input!")
        return
    
    # Hours input
    try:
        hours = float(input("Enter Hours Studied: ").strip())
        if hours <= 0:
            print(" Hours must be positive!")
            return
    except:
        print(" Invalid hours input!")
        return
    
    # Load current data and add new record
    df = load_data()
    new_record = pd.DataFrame({
        "Date": [date],
        "Subject": [subject],
        "Hours": [hours]
    })
    
    df = pd.concat([df, new_record], ignore_index=True)
    save_data(df)
    
    print(f"\n Record Added Successfully!")
    print(f"    Date: {date}")
    print(f"    Subject: {subject}")
    print(f"     Hours: {hours}")

def view_records():
    """सबै records देखाऊ"""
    print("\n" + "="*50)
    print("📋 YOUR STUDY RECORDS")
    print("="*50)
    
    df = load_data()
    
    if df.empty:
        print("\n No records found! Add some records first.")
        return
    
    print("\n")
    print(df.to_string(index=False))
    print(f"\n Total Records: {len(df)}")

def daily_total():
    """हरेक दिनमा कति घण्टा पढियो"""
    print("\n" + "="*50)
    print(" DAILY STUDY HOURS")
    print("="*50)
    
    df = load_data()
    
    if df.empty:
        print("\n No records found!")
        return
    
    # Convert Hours to numeric
    df['Hours'] = pd.to_numeric(df['Hours'], errors='coerce')
    
    daily_hours = df.groupby('Date')['Hours'].sum().sort_index()
    
    print("\n")
    for date, hours in daily_hours.items():
        print(f" {date}: {hours} hours")

def weekly_total():
    """यो हप्ता कति घण्टा पढियो"""
    print("\n" + "="*50)
    print("📊 WEEKLY STUDY HOURS")
    print("="*50)
    
    df = load_data()
    
    if df.empty:
        print("\n No records found!")
        return
    
    # Convert to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    df['Hours'] = pd.to_numeric(df['Hours'], errors='coerce')
    
    # Get this week's data
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    week_df = df[(df['Date'] >= pd.Timestamp(week_start)) & 
                 (df['Date'] <= pd.Timestamp(week_end))]
    
    if week_df.empty:
        print(f"\n Week: {week_start.date()} to {week_end.date()}")
        print(" No study records this week!")
        return
    
    total_hours = week_df['Hours'].sum()
    
    print(f"\n Week: {week_start.date()} to {week_end.date()}")
    print(f"  Total Hours: {total_hours} hours")
    
    # Daily breakdown
    daily = week_df.groupby('Date')['Hours'].sum()
    print("\nDaily Breakdown:")
    for date, hours in daily.items():
        print(f"  {date.date()}: {hours} hours")

def subject_analysis():
    """कुन subject धेरै पढियो"""
    print("\n" + "="*50)
    print(" SUBJECT-WISE ANALYSIS")
    print("="*50)
    
    df = load_data()
    
    if df.empty:
        print("\n No records found!")
        return
    
    df['Hours'] = pd.to_numeric(df['Hours'], errors='coerce')
    
    subject_hours = df.groupby('Subject')['Hours'].sum().sort_values(ascending=False)
    
    print("\n")
    for i, (subject, hours) in enumerate(subject_hours.items(), 1):
        print(f"{i}. {subject}: {hours} hours")
    
    print(f"\n Total Study Hours: {subject_hours.sum()} hours")

def goal_tracking():
    """Goal पूरा भयो कि भएन"""
    print("\n" + "="*50)
    print(" WEEKLY GOAL TRACKING")
    print("="*50)
    
    # Set weekly goal
    print("\nSet your weekly goal (hours):")
    try:
        goal = float(input("Enter Weekly Goal (e.g., 35): ").strip())
    except:
        print("❌ Invalid input!")
        return
    
    df = load_data()
    
    if df.empty:
        print("\n❌ No records found!")
        print(f" Goal: {goal} hours")
        print(f" Current: 0 hours")
        print(f"❌ Remaining: {goal} hours")
        return
    
    # Get this week's data
    df['Date'] = pd.to_datetime(df['Date'])
    df['Hours'] = pd.to_numeric(df['Hours'], errors='coerce')
    
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    week_df = df[(df['Date'] >= pd.Timestamp(week_start)) & 
                 (df['Date'] <= pd.Timestamp(week_end))]
    
    current = week_df['Hours'].sum() if not week_df.empty else 0
    remaining = goal - current
    
    print(f"\n Weekly Goal: {goal} hours")
    print(f" Current: {current} hours")
    
    if remaining <= 0:
        print(f" CONGRATULATIONS! Goal Achieved! 🎉")
        print(f"   Extra: {abs(remaining)} hours")
    else:
        print(f" Remaining: {remaining} hours")
        percentage = (current / goal) * 100
        print(f" Progress: {percentage:.1f}%")

def main_menu():
    """मुख्य menu"""
    while True:
        print("\n" + "="*50)
        print("🎓 AI STUDY TRACKER")
        print("="*50)
        print("\n1. ➕ Add Study Record")
        print("2.  View All Records")
        print("3.  Daily Total")
        print("4.  Weekly Total")
        print("5.  Subject-wise Analysis")
        print("6.  Goal Tracking")
        print("7.  Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            add_study_record()
        elif choice == "2":
            view_records()
        elif choice == "3":
            daily_total()
        elif choice == "4":
            weekly_total()
        elif choice == "5":
            subject_analysis()
        elif choice == "6":
            goal_tracking()
        elif choice == "7":
            print("\n Thank you for using AI Study Tracker!")
            print("Keep studying! ")
            break
        else:
            print(" Invalid choice! Try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    print(" Starting AI Study Tracker...")
    initialize_csv()
    main_menu()