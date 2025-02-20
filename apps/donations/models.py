from django.db import models


# Create your models here.
class Donation(models.Model):  # used Many-to-Many table
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    sponsor = models.ForeignKey('sponsors.Sponsor', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sponsor.full_name} -> {self.student.full_name} ({self.amount})"

    def save(self, *args, **kwargs):
        """Automatically updates the student's allocated amount when a donation is saved"""
        super().save(*args, **kwargs)
        self.student.update_donation_amount()
