from rest_framework import serializers

from apps.donations.models import Donation
from apps.sponsors.models import Sponsor
from apps.students.models import Student


class SponsorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = "__all__"


class StudentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = "__all__"


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    # recaptcha = serializers.CharField(help_text="Google reCAPTCHA token")


class DashboardStatisticsSerializer(serializers.Serializer):
    total_paid = serializers.IntegerField()
    total_requested = serializers.IntegerField()
    total_due = serializers.IntegerField()
