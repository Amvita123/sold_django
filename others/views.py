from others.serializers.user_report_serializers import UserReportSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from others.models.user_report import UserReport


class UserReportView(APIView):

    def get(self, request):
        reports = UserReport.objects.all().order_by('-date_created')
        serializer = UserReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserReportSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(report_by = request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
