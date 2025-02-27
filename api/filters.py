from django_filters import rest_framework as filters

from apps.sponsors.models import Sponsor
from apps.students.models import Student


class SponsorFilter(filters.FilterSet):
    created_at = filters.DateFromToRangeFilter(field_name="created_at")
    payment_amount = filters.RangeFilter(field_name="payment_amount")

    class Meta:
        model = Sponsor
        fields = ["created_at", "payment_amount"]


class StudentFilter(filters.FilterSet):
    student_type = filters.ChoiceFilter(
        field_name="student_type",
        choices=[("bachelor", "Bakalavr"), ("master", "Magistr")]
    )
    university = filters.CharFilter(field_name="OTM", lookup_expr="icontains")

    class Meta:
        model = Student
        fields = ["student_type", "university"]
