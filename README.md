# 🎓 Campus Wellness Platform

A fullstack student-focused wellness web application that helps university students track their mood, manage academic stress, and maintain productivity balance.

Built with **Streamlit + Python + SQLite**, this platform combines emotional check-ins, study tracking, calendar mood visualization, and campus support resources into one clean dashboard.

---

## 🌟 Project Overview

University life can be stressful — exams, deadlines, burnout, and emotional overload are common.  
The Campus Wellness Platform provides students with a private and supportive space to:

- Reflect daily
- Monitor emotional patterns
- Track academic stress triggers
- Balance study and wellbeing

---

## 🚀 Features

### 🔐 User Authentication
- Sign up and login system  
- Private mood entries saved per student  
- Session-based access control  

### 🌈 Mood Tracking
- Daily mood logging with intensity slider  
- Journaling notes for reflection  
- Academic stress trigger selection  

### 📅 Mood Calendar View
- Monthly mood grid visualization  
- Emoji-based mood indicators  
- Helps students spot emotional trends over time  

### 📚 Study & Productivity Check-ins
- Track daily study hours  
- Monitor energy levels  
- Record academic reflections  

### 💛 Campus Support Hub
- Self-care tips for students  
- Encouragement and wellness reminders  
- Support resources for overwhelming school periods  

---

## 🛠️ Tech Stack

| Layer        | Technology Used |
|-------------|----------------|
| Frontend UI | Streamlit      |
| Backend     | Python         |
| Database    | SQLite         |
| Auth System | Session Login  |
| Analytics   | Streamlit Charts |

---

## 📂 Database Structure

The application uses three main tables:

- **users** → Stores student login credentials  
- **moods** → Stores mood entries, triggers, notes  
- **productivity** → Stores study hours and energy check-ins  

---

## ▶️ How to Run the Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/chihunanya/campus-wellness-platform.git
cd campus-wellness-platform
