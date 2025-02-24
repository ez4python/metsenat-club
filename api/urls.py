from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import SponsorViewSet, StudentsViewSet, DonationViewSet, UserTokenAPIView

app_name = 'api'

router = DefaultRouter()
router.register(r"sponsors", SponsorViewSet)
router.register(r"students", StudentsViewSet)
router.register(r"donations", DonationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('test-token/', UserTokenAPIView.as_view(), name='user-token-api')
]
