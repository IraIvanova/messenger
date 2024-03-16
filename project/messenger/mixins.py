from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.contrib import messages
from django.utils import timezone
import secrets
import json


class SuperuserOrPermissionRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and not request.user.has_perm(self.permission_required):
            return HttpResponseForbidden("Доступ заборонено")
        return super().dispatch(request, *args, **kwargs)


class MyLoginRequiredMixin(LoginRequiredMixin):
    login_url = '/users/login/'


class AjaxRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'error': 'This view is only accessible via AJAX.'}, status=400)
        return super().dispatch(request, *args, **kwargs)


class CreateSuccessMessageMixin:
    success_message = 'Success!'

    def processed_successfully(self, request):
        messages.add_message(request, messages.SUCCESS, self.success_message)


class ReadOnlyMixin:
    def dispatch(self, *args, **kwargs):
        if self.request.method != 'GET':
            return HttpResponseNotAllowed(['GET'])
        return super().dispatch(*args, **kwargs)


class IPAccessMixin:
    allowed_ips = ['127.0.0.1']

    def dispatch(self, request, *args, **kwargs):
        if request.META.get('REMOTE_ADDR') not in self.allowed_ips:
            return HttpResponseForbidden("Access denied")
        return super().dispatch(request, *args, **kwargs)


class RandomTokenMixin:
    def generate_token(self, length=20):
        return secrets.token_hex(length)


class JSONSerializeMixin:
    def to_json(self):
        return json.dumps(self.__dict__)


class UserActivityTrackingMixin:
    def track_user_activity(self, user):
        user.last_activity = timezone.now()
        user.save()


class UserLanguagePreferenceMixin:
    def set_language_preference(self, user, language):
        user.language_preference = language
        user.save()
