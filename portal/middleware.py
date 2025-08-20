
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import SessionToken, Teacher
from .utils import user_agent_fingerprint

class CustomAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.teacher = None
        token = request.COOKIES.get('tw_session')
        if not token:
            return
        ua_hash = user_agent_fingerprint(request.META.get('HTTP_USER_AGENT'))
        try:
            st = SessionToken.objects.select_related('teacher').get(token=token, user_agent_hash=ua_hash)
        except SessionToken.DoesNotExist:
            return
        if st.expires_at < timezone.now():
            return
        request.teacher = st.teacher
        request.session_token = st
