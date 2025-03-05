from django.db import models
from apps.donations.models import Donation
from apps.shared.models import DateTimeBasedModel


class StudentType(models.TextChoices):
    BACHELOR = "bachelor", "Bakalavr"
    MASTER = "master", "Magistr"


class Student(DateTimeBasedModel):
    type = models.CharField(choices=StudentType.choices, default=StudentType.BACHELOR, max_length=10)
    full_name = models.CharField(max_length=255)
    university = models.ForeignKey('shared.University', on_delete=models.CASCADE, related_name='students')
    contract_amount = models.PositiveIntegerField()
    donated_amount = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Talaba'
        verbose_name_plural = 'Talabalar'
        db_table = 'students'

    def __str__(self):
        return self.full_name

    def update_donation_amount(self):
        """Talabaning umumiy olgan homiylik mablag'ini yangilaydi"""
        total_donated = Donation.objects.filter(student=self).aggregate(models.Sum('amount'))['amount__sum'] or 0
        self.donated_amount = total_donated
        self.save(update_fields=['donated_amount'])
