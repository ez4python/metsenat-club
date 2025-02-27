from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import SponsorViewSet, StudentsViewSet, DonationViewSet, UserTokenAPIView, DashboardStatsView, \
    GrowthStatsAPIView

app_name = 'api'

router = DefaultRouter()
router.register(r"sponsors", SponsorViewSet)
router.register(r"students", StudentsViewSet)
router.register(r"donations", DonationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('growth-stats/', GrowthStatsAPIView.as_view(), name='growth-stats'),
    path('dashboard/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('test-token/', UserTokenAPIView.as_view(), name='user-token-api')
]
