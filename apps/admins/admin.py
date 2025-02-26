from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin

from apps.admins.models import Admin
from apps.donations.models import Donation
from apps.shared.models import University
from apps.sponsors.models import Sponsor
from apps.students.models import Student


@admin.register(Admin)
class UserModelAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", "password1", "password2"),
            },
        ),
    )
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)
    filter_horizontal = ("user_permissions",)


@admin.register(Sponsor)
class SponsorModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentsModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Donation)
class DonationModelAdmin(admin.ModelAdmin):
    pass


@admin.register(University)
class University(admin.ModelAdmin):
    pass
