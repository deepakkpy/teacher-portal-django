
# Teacher Portal (Custom Auth + Secure CRUD)

This Django project demonstrates a **custom authentication** (no Django auth), a
**custom session token**, and a secure teacher portal to manage students records with
inline edit/delete and an "Add or Merge" modal.

## Features
- Custom password hashing (PBKDF2-HMAC-SHA256) with per-user salt.
- Custom session tokens stored in DB and set as `HttpOnly` cookie `tw_session`.
- CSRF protection via Django CSRF middleware.
- Input validation on client and server. Marks must be 0..100.
- Audit trail for create/update/delete/login actions.
- "Add New Student" modal merges with existing name+subject using `calculate_new_marks`.
- ORM usage to avoid SQL injection.

## Quick start
1. Create & activate a virtualenv, then install Django:
   ```bash
   pip install django
   ```
2. Migrate database and create a teacher:
   ```bash
   cd teacher_portal
   python manage.py makemigrations
   python manage.py migrate
   python manage.py shell
   >>> from portal.models import Teacher
   >>> from portal.utils import hash_password
   >>> salt, pw = hash_password("admin123")
   >>> Teacher.objects.create(username="teacher1", password_salt=salt, password_hash=pw)
   >>> exit()
   ```
3. (Optional) Load some sample students in shell:
   ```python
   from portal.models import Student
   Student.objects.create(name="Sean Abot", subject="Maths", marks=77)
   ```
4. Run the server:
   ```bash
   python manage.py runserver
   ```
5. Go to http://127.0.0.1:8000/login/ and sign in with the created teacher.

## Notes
- We intentionally do **not** enable Django's authentication/session frameworks.
- Cookie `tw_session` contains a random 32-byte hex string; we match it with the
  current user-agent fingerprint and expiry.
- `calculate_new_marks(existing, new)` returns sum; if the sum exceeds 100, the server rejects.
- Security: CSRF tokens, Django autoescape for templates, strict server-side validation,
  and ORM (parameterized) queries.
