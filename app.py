import streamlit as st
import pandas as pd
import datetime
import sqlite3
import calendar

# -----------------------------------
# 🌈 App Config
# -----------------------------------
st.set_page_config(page_title="Campus Wellness Platform", page_icon="🎓", layout="wide")

# -----------------------------------
# 🗄️ Database Setup
# -----------------------------------
conn = sqlite3.connect("campus_wellness.db", check_same_thread=False)
cursor = conn.cursor()

# Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# Mood Logs Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS moods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    date TEXT,
    mood TEXT,
    intensity INTEGER,
    trigger TEXT,
    note TEXT
)
""")

# Productivity Logs Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS productivity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    date TEXT,
    study_hours INTEGER,
    energy_level INTEGER,
    comment TEXT
)
""")

conn.commit()

# -----------------------------------
# Mood + Trigger Options
# -----------------------------------
moods = ["Happy 😊", "Calm 😌", "Neutral 😐", "Sad 😔", "Angry 😡", "Anxious 😰"]
triggers = ["Exams 📚", "Assignments 📝", "Friends 💛", "Family 🏠",
            "Money Stress 💸", "Burnout 😵", "Other"]

# Mood Colors (Calendar)
mood_colors = {
    "Happy 😊": "🟩",
    "Calm 😌": "🟦",
    "Neutral 😐": "⬜",
    "Sad 😔": "🟪",
    "Angry 😡": "🟥",
    "Anxious 😰": "🟨"
}

# -----------------------------------
# Auth Functions
# -----------------------------------
def signup(username, password):
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except:
        return False

def login(username, password):
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return cursor.fetchone()

# -----------------------------------
# Session State
# -----------------------------------
if "user" not in st.session_state:
    st.session_state.user = None

# -----------------------------------
# LOGIN PAGE
# -----------------------------------
if st.session_state.user is None:
    st.title("🎓 Campus Wellness Platform")
    st.write("Track your mood, manage stress, and stay balanced in school 💛")

    tab1, tab2 = st.tabs(["🔑 Login", "🆕 Sign Up"])

    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login(username, password)
            if user:
                st.session_state.user = username
                st.success("Welcome back 🎉")
                st.rerun()
            else:
                st.error("Invalid login details")

    with tab2:
        new_user = st.text_input("Create Username")
        new_pass = st.text_input("Create Password", type="password")

        if st.button("Sign Up"):
            if signup(new_user, new_pass):
                st.success("Account created! Please login 💛")
            else:
                st.error("Username already exists")

# -----------------------------------
# MAIN PLATFORM
# -----------------------------------
else:
    user = st.session_state.user

    st.sidebar.success(f"👤 Logged in as {user}")

    menu = st.sidebar.radio("📌 Campus Navigation", [
        "Dashboard",
        "Log Mood",
        "Mood Calendar",
        "Study & Productivity",
        "Support Hub",
        "Logout"
    ])

    # -----------------------------------
    # DASHBOARD
    # -----------------------------------
    if menu == "Dashboard":
        st.title("🌈 Student Wellness Dashboard")

        mood_df = pd.read_sql("SELECT * FROM moods WHERE username=? ORDER BY date DESC",
                              conn, params=(user,))

        prod_df = pd.read_sql("SELECT * FROM productivity WHERE username=? ORDER BY date DESC",
                              conn, params=(user,))

        col1, col2, col3 = st.columns(3)

        if not mood_df.empty:
            col1.metric("🌤 Latest Mood", mood_df.iloc[0]["mood"])
            col2.metric("📊 Avg Mood Intensity", round(mood_df["intensity"].mean(), 1))
        else:
            col1.metric("🌤 Latest Mood", "No logs yet")
            col2.metric("📊 Avg Mood Intensity", "-")

        if not prod_df.empty:
            col3.metric("📚 Latest Study Hours", prod_df.iloc[0]["study_hours"])
        else:
            col3.metric("📚 Latest Study Hours", "No logs")

        st.divider()
        st.subheader("✨ Motivation for Students")
        st.info("You don’t have to do everything today. Small progress still counts 💛")

    # -----------------------------------
    # LOG MOOD
    # -----------------------------------
    elif menu == "Log Mood":
        st.title("📝 Log Your Mood Today")

        with st.form("mood_form"):
            mood = st.selectbox("How are you feeling?", moods)
            intensity = st.slider("Mood Intensity", 1, 10, 5)
            trigger = st.selectbox("Main Stress Trigger", triggers)
            note = st.text_area("Journal Note (optional)")
            submit = st.form_submit_button("✅ Save Mood")

            if submit:
                today = str(datetime.date.today())
                cursor.execute("""
                    INSERT INTO moods (username, date, mood, intensity, trigger, note)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user, today, mood, intensity, trigger, note))
                conn.commit()
                st.success("Mood entry saved 💛")

    # -----------------------------------
    # MOOD CALENDAR GRID
    # -----------------------------------
    elif menu == "Mood Calendar":
        st.title("📅 Mood Calendar View")

        df = pd.read_sql("SELECT date, mood FROM moods WHERE username=?", conn, params=(user,))

        if df.empty:
            st.info("Log moods to see your calendar 🌱")
        else:
            df["date"] = pd.to_datetime(df["date"])

            month = datetime.date.today().month
            year = datetime.date.today().year

            st.subheader(f"{calendar.month_name[month]} {year}")

            month_days = calendar.monthcalendar(year, month)

            mood_map = {
                row["date"].day: mood_colors.get(row["mood"], "⬜")
                for _, row in df.iterrows()
                if row["date"].month == month
            }

            # Display Calendar Grid
            st.write("🟩 Happy | 🟦 Calm | 🟨 Anxious | 🟥 Angry | 🟪 Sad")

            for week in month_days:
                cols = st.columns(7)
                for i, day in enumerate(week):
                    if day == 0:
                        cols[i].write(" ")
                    else:
                        emoji = mood_map.get(day, "⬜")
                        cols[i].markdown(f"**{day}** {emoji}")

    # -----------------------------------
    # STUDY + PRODUCTIVITY
    # -----------------------------------
    elif menu == "Study & Productivity":
        st.title("📚 Study & Productivity Check-in")

        with st.form("prod_form"):
            study_hours = st.slider("How many hours did you study today?", 0, 12, 2)
            energy = st.slider("Energy Level", 1, 10, 5)
            comment = st.text_area("How was school today?")

            submit = st.form_submit_button("✅ Save Productivity Log")

            if submit:
                today = str(datetime.date.today())
                cursor.execute("""
                    INSERT INTO productivity (username, date, study_hours, energy_level, comment)
                    VALUES (?, ?, ?, ?, ?)
                """, (user, today, study_hours, energy, comment))
                conn.commit()
                st.success("Productivity saved 🎉")

    # -----------------------------------
    # SUPPORT HUB
    # -----------------------------------
    elif menu == "Support Hub":
        st.title("💛 Campus Support Hub")

        st.subheader("You are not alone.")
        st.info("If school feels overwhelming, please reach out to someone 💛")

        st.write("### 📌 Student Support Options")
        st.write("✅ Talk to a trusted friend")
        st.write("✅ Reach out to your school counselor")
        st.write("✅ Join a campus community group")
        st.write("✅ Take breaks — burnout is real")

        st.subheader("✨ Quick Self-Care Tips")
        st.success("Drink water + take 5 deep breaths 🌱")
        st.success("Step outside for fresh air ☀️")
        st.success("Rest is productive too 💛")

    # -----------------------------------
    # LOGOUT
    # -----------------------------------
    elif menu == "Logout":
        st.session_state.user = None
        st.rerun()
