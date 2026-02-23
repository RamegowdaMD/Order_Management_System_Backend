import uuid
import logging
import time

# creates logger for this file and also __name__ anodu current file name
logger = logging.getLogger(__name__)

class RequestIDMiddleware:
    

    def __init__(self,get_response):
        self.get_response = get_response

    
    def __call__(self,request):

        request_id = str(uuid.uuid4())

        request.request_id = request_id


        start_time = time.time()

        logger.info(
            f"[{request_id}]"
            f"Incoming request: {request.method}{request.path}"
        )


        response = self.get_response(request)


        duration = time.time() - start_time

        response["X-Request-ID"] =  request_id

        logger.info(
            f"[{request_id}]"
            f"Response status: {response.status_code}"
            f"Duration: {duration:.2f}s"
        )



        return response