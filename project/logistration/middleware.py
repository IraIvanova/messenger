import logging
import datetime

logger = logging.getLogger('auth_logger')


class UserLoginLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_anonymous:
            return self.get_response(request)

        user = request.user
        last_login = user.last_login
        response = self.get_response(request)
        current_time = datetime.datetime.now()

        if user and (not last_login or last_login != user.last_login):
            user.last_login = current_time
            user.save()
            logger.info(f"User {user.username} logged in at {current_time}.")

        return response
