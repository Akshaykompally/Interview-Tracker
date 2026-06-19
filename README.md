# Interview-Tracker
# 🎯 Interview Tracker

Interview Tracker is a full-stack web application that helps job seekers organize, track, and analyze their interview journey. Users can record interview details, monitor progress through dashboards, review interview history, and gain insights into their performance.

## 🚀 Features

### 🔐 User Authentication
- User Registration
- Secure Login & Logout
- Password hashing using Bcrypt
- Session management with Flask-Login

### 📋 Interview Management
- Add interview records
- Track:
  - Company Name
  - Applied Role
  - Interview Date
  - Interview Status
  - Rounds Attended
  - Personal Notes & Mistakes

### 📊 Analytics Dashboard
- Total Interviews Count
- Accepted Interviews
- Rejected Interviews
- Pending Interviews
- Pie Chart for interview status distribution
- Bar Chart for rounds attended statistics

### 📜 Interview History
- View all interview records
- Delete interview entries
- Review interview notes and feedback

### 🤖 AI Chatbot
- Integrated chatbot using Groq API
- Provides interview-related assistance and guidance

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript
- Chart.js

### Backend
- Python
- Flask

### Database
- MySQL

### Authentication
- Flask-Login
- Flask-Bcrypt

---

## 📂 Project Structure

Interview-Tracker/
│
├── app.py
│
├── templates/
│ ├── Main.html
│ ├── Login.html
│ ├── Register.html
│ ├── MenuBar.html
│ ├── add.html
│ ├── History.html
│ └── To-do-list.html
│
├── static/
│ ├── main.css
│ ├── login.css
│ ├── register.css
│ ├── MenuBar.css
│ ├── add.css
│ ├── History.css
│ └── to-do-list.css
│
└── README.md

