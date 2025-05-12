from rest_framework import serializers
from others.models.user_report import UserReport


class UserReportSerializer(serializers.ModelSerializer):
    report_by = serializers.SerializerMethodField()

    class Meta:
        model = UserReport
        fields = ['id', 'reason', 'description', 'date_created', 'report_by', 'report_to']

    def get_report_by(self, obj):
        if obj.report_by:
            return f"{obj.report_by.id}"
        return None
