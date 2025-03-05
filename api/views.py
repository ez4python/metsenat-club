from datetime import timedelta

from django.contrib.auth import authenticate
from django.db import models
from django.db.models.functions import TruncDate
from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, filters, status, parsers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import SponsorFilter, StudentFilter
from api.pagination import CustomPagination
from api.serializers import SponsorModelSerializer, DonationSerializer, StudentModelSerializer, UserTokenSerializer, \
    UniversityModelSerializer, StudentDetailModelSerializer, GrowthStatsSerializer, DashboardStatisticsSerializer
from apps.donations.models import Donation
from apps.shared.models import University
from apps.sponsors.models import Sponsor
from apps.students.models import Student


# Create your views here.
@extend_schema(tags=["Sponsors"])
class SponsorViewSet(viewsets.ModelViewSet):
    queryset = Sponsor.objects.order_by("id")
    serializer_class = SponsorModelSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ["full_name", "phone_number"]
    filterset_class = SponsorFilter
    ordering_fields = ["created_at", "payment_amount"]
    ordering = "created_at"
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]


@extend_schema(tags=["Student"])
class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_filters = ["full_name", "university__name"]
    filterset_class = StudentFilter
    pagination_class = CustomPagination
    http_method_names = ['get', 'post', 'put', 'patch']


@extend_schema(tags=["Donation"])
class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["sponsor__full_name", "student__full_name"]
    filterset_fields = ["amount"]
    http_method_names = ["post", "get", "put", "patch"]


@extend_schema(tags=["Auth"])
class UserTokenAPIView(ObtainAuthToken):
    """
    JWT token for admins
    """
    parser_classes = [parsers.JSONParser]
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Auth"],
        request=UserTokenSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "access": {"type": "string"},
                    "refresh": {"type": "string"},
                }
            },
            400: {"description": "Invalid reCAPTCHA or missing fields"},
            401: {"description": "Invalid username or password"},
        }
    )
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        # recaptcha_token = request.data.get("recaptcha")

        # validate reCAPTCHA
        # if not recaptcha_token or not verify_recaptcha(recaptcha_token):
        #     return Response({"error": "Invalid reCAPTCHA"}, status=status.HTTP_400_BAD_REQUEST)

        # validate username & password
        if not username or not password:
            return Response({"error": "Username and password required!"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })
        else:
            return Response({"error": "Username or password wrong!"}, status=status.HTTP_401_UNAUTHORIZED)


@extend_schema(tags=["Dashboard"], responses=DashboardStatisticsSerializer)
class DashboardStatsView(APIView):
    """
    Dashboard uchun umumiy to'lov statistikasi
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_paid = Student.objects.aggregate(total=models.Sum("donated_amount"))["total"] or 0
        total_requested = Student.objects.aggregate(total=models.Sum("contract_amount"))["total"] or 0
        total_due = total_requested - total_paid

        data = {
            "total_paid": total_paid,
            "total_requested": total_requested,
            "total_due": total_due
        }
        return Response(data)


@extend_schema(tags=["Dashboard"], responses=GrowthStatsSerializer(many=True))
class GrowthStatsAPIView(APIView):
    """
    bu API homiylar va talabalarni vaqtga bog'langan grafigi uchun ma'lumot qaytaradi (limit= 1 yil)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_date = now() - timedelta(days=365)
        sponsors = Sponsor.objects.filter(created_at__gte=start_date) \
            .annotate(date=TruncDate('created_at')) \
            .values('date') \
            .annotate(count=models.Count('id')) \
            .order_by('date')

        students = Student.objects.filter(created_at__gte=start_date) \
            .annotate(date=TruncDate('created_at')) \
            .values('date') \
            .annotate(count=models.Count('id')) \
            .order_by('date')

        sponsor_data = {str(item['date']): item['count'] for item in sponsors}
        student_data = {str(item['date']): item['count'] for item in students}

        all_dates = sorted(set(sponsor_data.keys()) | set(student_data.keys()))

        result = []
        for date in all_dates:
            result.append({
                "date": date,
                "sponsors": sponsor_data.get(date, 0),
                "students": student_data.get(date, 0)
            })

        return Response(result)


@extend_schema(tags=["University"])
class UniversityListAPIView(ListAPIView):
    queryset = University.objects.order_by('name')
    serializer_class = UniversityModelSerializer
    pagination_class = None


@extend_schema(tags=["Student"])
class StudentDetailAPIView(RetrieveAPIView):
    queryset = Student.objects.prefetch_related("university", "donation_set__sponsor")
    serializer_class = StudentDetailModelSerializer
    lookup_field = "id"
