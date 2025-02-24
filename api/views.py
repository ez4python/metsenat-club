from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, filters, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from api.serializers import SponsorModelSerializer, DonationSerializer, StudentModelSerializer
from apps.donations.models import Donation
from apps.sponsors.models import Sponsor
from apps.students.models import Student


# Create your views here.
@extend_schema(tags=["Sponsors"])
class SponsorViewSet(viewsets.ModelViewSet):
    queryset = Sponsor.objects.all().order_by("id")
    serializer_class = SponsorModelSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["full_name", "phone_number"]
    filterset_fields = ["sponsor_type", "payment_type", "spent_amount"]


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
    # permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password required!"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })
        else:
            return Response({"error": "Username or password wrong!"}, status=status.HTTP_401_UNAUTHORIZED)
