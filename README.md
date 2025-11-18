# 🌐 SubSphere — Smart Subscription Tracker

Take control of your digital spending.  
SubSphere helps users track recurring subscriptions like Netflix, Spotify, iCloud & more — beautifully and efficiently.

📍 *Portfolio Project – Built with Flask & SQLAlchemy*

---

## ✨ Features

| Category            | Description                                      |
|---------------------|--------------------------------------------------|
| 🔐 Authentication   | Secure login & registration (hashed passwords)   |
| 📊 Dashboard        | Monthly cost, yearly projection & insights       |
| ➕ CRUD             | Add, edit & delete subscriptions                 |
| 👁 Modern UI        | Clean, futuristic dashboard with smooth UX       |
| 💾 SQLite Database  | Lightweight local persistence                    |
| 🧠 User-specific    | Each user only sees **their** subscriptions      |
| 📱 Responsive Design| Works nicely on desktop & smaller screens        |

---

## 🚀 Tech Stack

| Technology       | Usage                         |
|------------------|------------------------------|
| Python (Flask)   | Web backend / routing        |
| SQLAlchemy       | ORM & database modeling      |
| SQLite           | Local database               |
| HTML + Jinja2    | Templates & rendering        |
| CSS3 (custom)    | Modern, light UI             |

---

## 📂 Project Structure

subsphere/  
├── app.py  
├── auth.py  
├── data_manager.py  
├── models.py  
├── requirements.txt  
├── data/  
│   └── .keep     ← ensures folder exists, DB gets created on first run  
├── static/  
│   ├── images/  
│   │   ├── logo.png  
│   │   └── favicon.png  
│   └── style.css  
└── templates/  
    ├── base.html  
    ├── index.html  
    ├── dashboard.html  
    ├── subscriptions.html  
    ├── edit_subscription.html  
    ├── login.html  
    └── register.html  

---

## 🛠️ Installation & Setup

```bash
# Clone repository
git clone https://github.com/ilyassuelen/SubSphere.git
cd SubSphere

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate      # Mac / Linux
# .venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py