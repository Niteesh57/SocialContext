# 🚀 Social Context API (FastAPI)

## 📖 Overview

Social Context API is a **FastAPI**-based application that provides **user authentication**, **role management**, and **post creation** features. It supports **JWT authentication** and **role-based access control (RBAC)** to secure endpoints.

## 📦 Features
✅ **User Authentication (JWT)**  
✅ **Role-Based Access Control (Admin/User)**  
✅ **CRUD Operations for Users, Roles, and Posts**  
✅ **Swagger UI Documentation**  
✅ **Token-Based Authorization**  

---

## ⚡ Installation Guide

### 1️⃣ Clone the Repository

git clone https://github.com/yourusername/social-context-api.git
cd Path

### 2️⃣ Create a Virtual Environment

python -m venv env
env\Scripts\activate  (On Windows)(My Python Version 3.11)

### 3️⃣ Install Dependencies

pip install -r requirements.txt

### 4️⃣ Set Up Environment Variables (.env File)

POSTGRESQL_DATABASE_URL = "postgresql+psycopg2://postgres:(UserName)@(Password)/(DataBase)"

SECRET_KEY = (SECRET_KEY) "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" (My Config)<br>
ALGORITHM = (ALGORITHM) "HS256" (My Config)<br>
ACCESS_TOKEN_EXPIRE_MINUTES = (ACCESS_TOKEN_EXPIRE_MINUTES) 30 (My Config)<br>

###  5️⃣ DB schema
<img src="DB.jpg" alt="Screenshot DB Schema">

