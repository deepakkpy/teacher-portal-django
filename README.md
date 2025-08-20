# 🏫 Teacher Portal – Django Project  

A secure teacher portal built with **Django**, allowing authenticated teachers to manage a list of students with inline editing and deletion. This project implements **manual authentication and session management for learning purposes.  

---

## 🚀 Features  

- **Teacher Authentication**  
  - Custom login system using **manual password hashing with salt**.  
  - Manual session handling using **secure cookies** (no Django auth).  

- **Student Management**  
  - View list of students (Name, Subject, Marks).  
  - Add new students.  
  - Inline editing of student marks.  
  - Delete student records.  

- **Security**  
  - Inputs validated both client-side and server-side.  
  - Passwords stored in **hashed + salted** format.  
  - Protection against **SQL Injection** (via Django ORM).  
  - Protection against **XSS** (via Django’s auto HTML escaping).  
  - Protection against **CSRF** (via Django’s CSRF middleware).  

---

## 🛠️ Setup Instructions  

### 1. Clone Repository  
```bash
git clone https://github.com/deepakkpy/teacher-portal-django.git
cd teacher-portal-django
```

### 2. Create Virtual Environment  
```bash
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On Linux/Mac
```

### 3. Install Dependencies  
```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations  
```bash
python manage.py migrate
```

### 5. Create Teacher User (superuser equivalent)  
```bash
python manage.py shell
```
Inside the shell, run:
```python
from portal.models import Teacher
from portal.utils import hash_password

salt, pw = hash_password("admin123")
Teacher.objects.create(username="teacher1", password_salt=salt, password_hash=pw)
exit()
```

### 6. Start Development Server  
```bash
python manage.py runserver
```

Open in browser: **http://127.0.0.1:8000/login/**  

Login with:  
- **Username:** `teacher1`  
- **Password:** `admin123`  

---

## 🔒 Security Considerations  

✔️ Custom password hashing using **salt + hash**.  
✔️ No plain-text passwords stored.  
✔️ **SQL Injection prevention** via Django ORM (parameterized queries).  
✔️ **XSS Protection** using Django’s template auto-escaping.  
✔️ **CSRF Protection** using Django CSRF tokens.  
✔️ **Session Handling** via manual secure cookies.  

---

## ⚡ Challenges Faced  

- Implementing **manual authentication** instead of Django’s built-in auth.  
- Handling **custom cookies securely** for session management.  
- Designing **inline editing & deletion** with AJAX without reloading the page.  
- Ensuring **security best practices** (CSRF, XSS, password hashing).  

---

## ⏱️ Time Taken  

Approx. **10–12 hours** including:  
- Project setup & authentication logic → 3 hrs  
- Student management (CRUD) → 4 hrs  
- Security hardening → 2 hrs  
- Debugging & testing → 2 hrs  
- Documentation & GitHub setup → 1 hr  

---

## 📂 Project Structure  

```
teacher-portal-django/
│── portal/              # Main app
│   ├── models.py        # Teacher & Student models
│   ├── views.py         # Views for login & student APIs
│   ├── urls.py          # App routes
│   ├── utils.py         # Password hashing & session utils
│   ├── templates/
│   │    ├── login.html
│   │    └── home.html
│
│── teacher_portal/      # Django project settings
│── manage.py
│── requirements.txt
│── README.md
```
