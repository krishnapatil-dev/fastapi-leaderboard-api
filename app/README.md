# 🏆 FastAPI Leaderboard API

A backend API built using FastAPI that allows user authentication, player management, score tracking, and leaderboard ranking.

---

## 🚀 Features

* 🔐 JWT Authentication (Signup & Login)
* 👤 Role-based Access (Admin / User)
* 🎮 Player Management
* 📊 Score Tracking
* 🏆 Leaderboard with Ranking
* 📈 Pagination & Filtering
* 🗑️ Admin Controls (Delete Players / Reset System)

---

## 🛠️ Tech Stack

* FastAPI
* SQLite
* JWT (python-jose)
* Passlib (bcrypt)
* Python

---

## 📂 Project Structure

```
app/
 ├── auth.py
 ├── database.py
 ├── models.py
 ├── utils.py
 ├── routes/
 │    └── leaderboard.py
```

---

## ⚙️ Installation

```bash
git clone https://github.com/YOUR_USERNAME/fastapi-leaderboard-api.git
cd fastapi-leaderboard-api
pip install -r requirements.txt
```

---

## ▶️ Run Server

```bash
uvicorn app.main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

## 🔐 Authentication Flow

1. Signup
2. Login → get JWT token
3. Click **Authorize** in Swagger
4. Paste token
5. Access protected endpoints

---

## 📌 API Endpoints

### Auth

* POST /signup
* POST /login

### Players

* POST /players
* GET /players
* DELETE /players/{id}

### Scores

* POST /scores
* GET /scores/{player_id}

### Leaderboard

* GET /leaderboard
* GET /rank/{player_id}

### Admin

* DELETE /admin/reset

---

## 🧠 Key Concepts Used

* JWT Authentication
* Password Hashing
* Dependency Injection (Depends)
* SQL Joins & Aggregation
* Pagination (limit & offset)
* Role-based Authorization

---

## 📈 Future Improvements

* PostgreSQL support
* Refresh tokens
* Logging system
* Docker support

---

## 👨‍💻 Author

Krishna Patil
