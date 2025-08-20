import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teacher_portal.settings")  # change if your settings module is different
django.setup()

from portal.models import Teacher
from portal.utils import hash_password

def create_teacher(username, password):
    salt, pw = hash_password(password)
    Teacher.objects.create(username=username, password_salt=salt, password_hash=pw)
    print(f"Teacher '{username}' created successfully!")

if __name__ == "__main__":
    create_teacher("deepak", "admin123")
