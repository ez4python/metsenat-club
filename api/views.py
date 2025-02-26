from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, filters, status, parsers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.serializers import SponsorModelSerializer, DonationSerializer, StudentModelSerializer, UserTokenSerializer
from apps.donations.models import Donation
from apps.sponsors.models import Sponsor
from apps.students.models import Student
from utils.captcha import verify_recaptcha, get_recaptcha_token


# Create your views here.
@extend_schema(tags=["Sponsors"])
class SponsorViewSet(viewsets.ModelViewSet):
    queryset = Sponsor.objects.all().order_by("id")
    serializer_class = SponsorModelSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["full_name", "phone_number"]
    filterset_fields = ["sponsor_type", "payment_type", "spent_amount"]

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]


@extend_schema(tags=["Students"])
class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_filters = ["full_name", "university__name"]
    filterset_fields = ["contract_amount", "donated_amount"]


@extend_schema(tags=["Donation"])
class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["sponsor__full_name", "student__full_name"]
    filterset_fields = ["amount"]


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
