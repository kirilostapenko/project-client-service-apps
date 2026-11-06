from django.db import connection
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    def get(self, request: Request) -> Response:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            db_status = "healthy"
        except Exception:
            db_status = "unhealthy"

        status_code = 200 if db_status == "healthy" else 503
        return Response({"status": "ok", "database": db_status}, status=status_code)