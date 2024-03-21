import time
import logging

logger = logging.getLogger('request_time_logger')


class CalculateRequestProcessingTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()
        duration = (end_time - start_time) * 1000
        logger.info(f"Request to {request.path} took {duration:.2f} ms")
        return response
