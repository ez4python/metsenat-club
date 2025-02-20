from django.db import models

from apps.shared.models import DateTimeBasedModel
from apps.shared.validators import validate_phone_number


# Create your models here.
class SponsorType(models.TextChoices):
    LEGAL = "legal", "Legal"
    INDIVIDUAL = "individual", "Individual"


class PaymentType(models.TextChoices):
    CASH = "cash", "Cash"
    CARD = "card", "Card"
    TRANSFER = "transfer", "Transfer"


class Sponsor(DateTimeBasedModel):
    sponsor_type = models.CharField(choices=SponsorType.choices, default=SponsorType.INDIVIDUAL, max_length=10)
    full_name = models.CharField(blank=True, max_length=255)
    organization = models.CharField(max_length=150, null=True)
    payment_type = models.CharField(choices=PaymentType.choices, default=PaymentType.CASH, max_length=10)
    balance = models.BigIntegerField()
    phone_number = models.CharField(max_length=20, validators=[validate_phone_number], unique=True)


class ApplicationStatusType(models.TextChoices):
    NEW = "new", "New"
    MODERATION = "moderation", "Moderation"
    APPROVED = "approved", "Approved"
    CANCELED = "canceled", "Canceled"


class Application(models.Model):
    status = models.CharField(choices=ApplicationStatusType.choices, default=ApplicationStatusType.NEW, max_length=10)
    sponsor_type = models.CharField(choices=SponsorType.choices, default=SponsorType.INDIVIDUAL, max_length=10)
    sponsor_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, validators=[validate_phone_number], blank=True, unique=True)
    payment_amount = models.BigIntegerField(blank=True)
    organization = models.CharField(blank=True, max_length=200)
    comment = models.TextField(null=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        db_table = 'applications'

    def __str__(self):
        return f"{self.sponsor_name} - {'Approved' if self.is_approved else 'Pending'}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # create or update sponsor info, if application will be approved
        if self.is_approved:
            sponsor, created = Sponsor.objects.get_or_create(
                full_name=self.sponsor_name,
                defaults={
                    'organization': self.organization,
                    'balance': self.payment_amount
                }
            )

            # update balance, if sponsor exists
            if not created:
                sponsor.balance += self.payment_amount

            sponsor.save()
