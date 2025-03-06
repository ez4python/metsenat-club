from drf_spectacular.utils import extend_schema_serializer, extend_schema_field
from rest_framework import serializers

from apps.donations.models import Donation
from apps.shared.models import University
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


class UniversityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = "__all__"


class SponsorSerializer(serializers.ModelSerializer):
    donated_amount = serializers.IntegerField(source="donation.amount")

    class Meta:
        model = Sponsor
        fields = ["id", "full_name", "donated_amount"]


class StudentDetailModelSerializer(serializers.ModelSerializer):
    university = serializers.CharField(source="university.name")
    sponsors = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ["id", "full_name", "type", "university", "contract_amount", "donated_amount", "sponsors"]

    @extend_schema_field(SponsorSerializer(many=True))
    def get_sponsors(self, user):
        return (
            Sponsor.objects.filter(donation__student=user).values("id", "full_name", "donation__amount")
        )


class GrowthStatsSerializer(serializers.Serializer):
    date = serializers.DateField()
    sponsors = serializers.IntegerField()
    students = serializers.IntegerField()


class DashboardStats(serializers.Serializer):
    total_paid = serializers.IntegerField()
    total_requested = serializers.IntegerField()
    total_due = serializers.IntegerField()
