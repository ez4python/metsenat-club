from django.core.validators import MinValueValidator
from django.db import models
from apps.shared.models import DateTimeBasedModel
from apps.shared.validators import validate_phone_number


class SponsorType(models.TextChoices):
    LEGAL = "legal", "Jismoniy shaxs"
    INDIVIDUAL = "individual", "Yuridik shaxs"


class PaymentType(models.TextChoices):
    CASH = "cash", "Naqd pul"
    CARD = "card", "Plastik karta"
    TRANSFER = "transfer", "Pul o'tkazmasi"


class StatusType(models.TextChoices):
    NEW = "new", "Yangi"
    MODERATION = "moderation", "Moderatsiyada"
    APPROVED = "approved", "Tasdiqlangan"
    CANCELED = "canceled", "Bekor qilingan"


class Sponsor(DateTimeBasedModel):
    status = models.CharField(max_length=20, choices=StatusType.choices, default=StatusType.NEW)
    sponsor_type = models.CharField(max_length=10, choices=SponsorType.choices, default=SponsorType.INDIVIDUAL)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, validators=[validate_phone_number], unique=True)
    organization_name = models.CharField(max_length=255, blank=True, null=True)
    payment_amount = models.PositiveIntegerField(validators=[MinValueValidator(1000000)])
    payment_type = models.CharField(max_length=20, choices=PaymentType.choices, default=PaymentType.TRANSFER)
    spent_amount = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])  # 🆕 Default qo'shildi

    class Meta:
        verbose_name = "Homiy"
        verbose_name_plural = "Homiylar"
        db_table = "sponsors"

    def __str__(self):
        return f"{self.full_name} - {self.payment_amount} UZS - {self.organization_name}"
