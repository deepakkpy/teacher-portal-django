

import json
import secrets
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect  
from django.db import transaction

from .models import Teacher, Student, AuditLog
from .forms import LoginForm, AddStudentForm
from .utils import verify_password, calculate_new_marks


SESSION_STORE = {}


def index_redirect(request):
    return redirect('home')


# -----------------------------
# Helpers for manual session auth
# -----------------------------
def _attach_teacher(request):
    """
    Reads the cookie 'session_token', looks up the teacher in SESSION_STORE,
    and sets request.teacher = Teacher or None.
    """
    token = request.COOKIES.get('session_token')
    teacher_id = SESSION_STORE.get(token)
    teacher = None
    if teacher_id:
        try:
            teacher = Teacher.objects.get(id=teacher_id)
        except Teacher.DoesNotExist:
            teacher = None
    request.teacher = teacher


def _require_login_page(request):
    """
    Enforce login for page views: redirect to login if not authenticated.
    """
    _attach_teacher(request)
    if not getattr(request, 'teacher', None):
        return redirect('login')
    return None


def _require_login_api(request):
    """
    Enforce login for API endpoints: return JSON 401 if not authenticated.
    """
    _attach_teacher(request)
    if not getattr(request, 'teacher', None):
        return _json_error('Unauthorized', status=401)
    return None


# -----------------------------
# Authentication (manual cookie session)
# -----------------------------
@csrf_protect
@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == 'GET':
        return render(request, 'portal/login.html', {'form': LoginForm()})

    form = LoginForm(request.POST)
    if not form.is_valid():
        return render(request, 'portal/login.html', {'form': form, 'error': 'Invalid input.'})

    username = form.cleaned_data['username'].strip()
    password = form.cleaned_data['password']

    try:
        t = Teacher.objects.get(username=username)
    except Teacher.DoesNotExist:
        return render(request, 'portal/login.html', {'form': form, 'error': 'Invalid credentials.'})

    if not verify_password(password, t.password_salt, t.password_hash):
        return render(request, 'portal/login.html', {'form': form, 'error': 'Invalid credentials.'})

    # Issue manual session token
    token = secrets.token_hex(32)
    SESSION_STORE[token] = t.id

    resp = redirect('home')
    # In production, set secure=True and samesite='Strict'
    resp.set_cookie('session_token', token, httponly=True, secure=False, samesite='Lax', max_age=60 * 60 * 12)
    # Optional audit log
    AuditLog.objects.create(teacher=t, action='login', details='Manual session login')
    return resp


def logout_view(request):
    token = request.COOKIES.get('session_token')
    if token and token in SESSION_STORE:
        del SESSION_STORE[token]
    resp = redirect('login')
    resp.delete_cookie('session_token')
    return resp


# -----------------------------
# Pages
# -----------------------------
def home(request):
    redir = _require_login_page(request)
    if redir:
        return redir
    students = Student.objects.all().order_by('name', 'subject')
    return render(request, 'portal/home.html', {'students': students, 'teacher': request.teacher})


# -----------------------------
# Utilities
# -----------------------------
def _json_error(msg, status=400):
    return JsonResponse({'ok': False, 'error': msg}, status=status)


def _validate_marks(marks):
    try:
        m = int(marks)
    except Exception:
        return None
    if m < 0 or m > 100:
        return None
    return m


# -----------------------------
# APIs (CSRF-protected)
# -----------------------------
@require_http_methods(["GET"])
def api_students(request):
    redir = _require_login_api(request)
    if redir:
        return redir
    items = list(Student.objects.values('id', 'name', 'subject', 'marks'))
    return JsonResponse({'ok': True, 'students': items})


@require_http_methods(["POST"])
@csrf_protect
def api_student_update(request, pk):
    redir = _require_login_api(request)
    if redir:
        return redir

    # Accept either form-encoded (from your inline edit) or JSON (if you choose)
    marks_raw = request.POST.get('marks')
    if marks_raw is None and request.body:
        try:
            body = json.loads(request.body.decode('utf-8'))
            marks_raw = body.get('marks')
        except Exception:
            marks_raw = None

    marks = _validate_marks(marks_raw)
    if marks is None:
        return _json_error('Marks must be an integer between 0 and 100.')

    try:
        with transaction.atomic():
            s = Student.objects.select_for_update().get(pk=pk)
            old = s.marks
            s.marks = marks
            s.save()
            AuditLog.objects.create(
                teacher=request.teacher,
                action='update',
                details=f'Updated student {s.id} marks: {old} -> {marks}'
            )
    except Student.DoesNotExist:
        return _json_error('Student not found.', status=404)

    return JsonResponse({'ok': True, 'id': s.id, 'marks': s.marks})


@require_http_methods(["POST"])
@csrf_protect
def api_student_delete(request, pk):
    redir = _require_login_api(request)
    if redir:
        return redir
    try:
        with transaction.atomic():
            s = Student.objects.select_for_update().get(pk=pk)
            s.delete()
            AuditLog.objects.create(
                teacher=request.teacher,
                action='delete',
                details=f'Deleted student {pk}'
            )
    except Student.DoesNotExist:
        return _json_error('Student not found.', status=404)
    return JsonResponse({'ok': True})


@require_http_methods(["POST"])
@csrf_protect
def api_student_add(request):
    redir = _require_login_api(request)
    if redir:
        return redir

    # Accept regular form POST (your current frontend uses FormData)
    form = AddStudentForm(request.POST)
    if not form.is_valid():
        return _json_error('Invalid input.')

    name = form.cleaned_data['name'].strip()
    subject = form.cleaned_data['subject'].strip()
    marks = form.cleaned_data['marks']

    with transaction.atomic():
        try:
            s = Student.objects.select_for_update().get(name=name, subject=subject)
            new_total = calculate_new_marks(s.marks, marks)
            if new_total > 100:
                return _json_error('Total marks cannot exceed 100.')
            old = s.marks
            s.marks = new_total
            s.save()
            AuditLog.objects.create(
                teacher=request.teacher,
                action='update',
                details=f'Incremented "{name}-{subject}" from {old} by {marks} -> {new_total}'
            )
            return JsonResponse({
                'ok': True, 'updated': True,
                'id': s.id, 'name': s.name, 'subject': s.subject, 'marks': s.marks
            })
        except Student.DoesNotExist:
            if marks > 100:
                return _json_error('Marks cannot exceed 100.')
            s = Student.objects.create(name=name, subject=subject, marks=marks)
            AuditLog.objects.create(
                teacher=request.teacher,
                action='create',
                details=f'Created "{name}-{subject}" with {marks}'
            )
            return JsonResponse({
                'ok': True, 'created': True,
                'id': s.id, 'name': s.name, 'subject': s.subject, 'marks': s.marks
            })

