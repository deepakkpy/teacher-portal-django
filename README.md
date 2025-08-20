# 📘 Teachers Portal – Django Project

A lightweight Django web app for teachers to **manage student records** with a **custom authentication system** (no Django sessions, no Django auth).  
This project uses a **custom middleware-based session system** powered by in-memory storage.

---

## 🚀 Features
- 🔑 **Custom authentication**
  - Teachers log in with username & password.
  - Secure password hashing with `bcrypt`.
  - Cookie-based sessions (via custom middleware).
- 👨‍🏫 **Teacher Dashboard**
  - List of students.
  - CRUD operations (create, update, delete).
- 👩‍🎓 **Student Management**
  - Add new students.
  - Update student details.
  - Delete students (AJAX enabled).
- 🛡️ **Custom Middleware**
  - In-memory session store with expiration (default 1 hour).
  - Rolling sessions (auto-refresh TTL on each request).
- 📦 **Lightweight structure**
  - No reliance on Django’s built-in auth/session framework.
  - Easy to extend for custom use cases.

---

## 📂 Project Structure
```
teacher_portal/                 # Django project root
│── manage.py                   # Entry point
│
├── django_teacher_portal/       # Project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/                        # Main app
│   ├── __init__.py
│   ├── models.py                # Student, Teacher models
│   ├── forms.py                 # StudentForm, TeacherLoginForm
│   ├── views.py                 # Views (login, dashboard, CRUD)
│   ├── urls.py                  # App URLs
│   ├── middleware.py            # Custom session middleware
│   ├── utils/
│   │   └── security.py          # Password hashing helpers
│   └── templates/core/
│       ├── login.html
│       └── student/dashboard.html
```

---

## ⚙️ Installation

### 1. Clone the repo
```bash
git clone https://github.com/your-username/teachers-portal.git
cd teachers-portal
```

### 2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install django bcrypt
```

### 4. Apply migrations
```bash
python manage.py migrate
```

### 5. Create a teacher account (manually for now)
Run Django shell:
```bash
python manage.py shell
```
```python
from core.models import Teacher
from core.utils.security import generate_password_hash

Teacher.objects.create(
    username="admin",
    password=generate_password_hash("admin123")
)
```
Exit shell:
```python
exit()
```

### 6. Run the server
```bash
python manage.py runserver
```

Go to 👉 http://127.0.0.1:8000/

---

## 🔑 Authentication Flow

1. Teacher logs in → `views.login_view`  
   - Validates username/password.  
   - Generates a **secure random token**.  
   - Stores token in `SESSION_STORE`.  
   - Sets cookie `session_token`.  

2. **Custom Middleware** (`CustomSessionMiddleware`)  
   - Reads cookie → verifies token.  
   - Extends TTL if active.  
   - Attaches `request.teacher`.  

3. Views decorated with `@teacher_required`  
   - If no `request.teacher` → redirect to login.  
   - Otherwise → allow access.  

---

## 🖥️ Endpoints

### Auth
- `/login/` → Teacher login.  
- `/logout/` → Logout + clear cookie.  

### Students
- `/students/create/` → Create student (POST).  
- `/students/<pk>/update/` → Update student (POST).  
- `/students/<pk>/delete/` → Delete student (POST).  

### Dashboard
- `/` → Teacher dashboard with student list.  

---

## 🔒 Security Notes
- Passwords are hashed with `bcrypt` (`generate_password_hash` & `verify_password`).  
- Session tokens are stored in-memory, not DB (good for dev/testing).  
- Cookies are:
  - `HttpOnly` → prevents JS access.  
  - `SameSite=Lax` → prevents CSRF in most cases.  
  - `Secure=True` when `DEBUG=False`.  

For production:
- Use **Redis or database** for session storage instead of memory.  
- Enable **HTTPS** to secure cookies.  

---

## 🛠️ Tech Stack
- **Backend**: Django  
- **Auth**: Custom middleware + bcrypt  
- **Frontend**: Django templates + AJAX (for student CRUD)  

---

## 📌 Next Steps
- Add teacher registration.  
- Replace in-memory session store with Redis.  
- Add pagination and search for students.  
- Write unit tests.  

---

## 👨‍💻 Author
Built by [Your Name] 💻  
