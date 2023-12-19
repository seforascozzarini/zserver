from rest_framework.response import Response


class HTTPException(Exception):
    def __init__(self, error='Generic Error', status=500):
        self.error = error
        self.status = status
        super().__init__(self.error)

    def get_response(self):
        return Response(self.error, self.status)