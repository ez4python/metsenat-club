from django.core.validators import MinValueValidator
from django.db import models

from apps.donations.models import Donation


# Create your models here.
class StudentType(models.TextChoices):
    BACHELOR = "bachelor", "Bachelor"
    MASTER = "master", "Master"


class Student(models.Model):
    type = models.CharField(choices=StudentType.choices, default=StudentType.BACHELOR, max_length=10)
    full_name = models.CharField(blank=True, max_length=255)
    university = models.ForeignKey('shared.University', on_delete=models.CASCADE, related_name='students')
    contract_amount = models.BigIntegerField()
    donated_amount = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'students'

    def __str__(self):
        return self.full_name

    def update_donation_amount(self):
        """Updates the total amount allocated to the student"""
        total_donated = Donation.objects.filter(student=self).aggregate(models.Sum('amount'))['amount__sum'] or 0
        self.donated_amount = total_donated
        self.save()
