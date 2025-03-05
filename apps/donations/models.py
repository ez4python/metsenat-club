from django.db import models
from django.core.exceptions import ValidationError


class Donation(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    sponsor = models.ForeignKey('sponsors.Sponsor', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sponsor.full_name} -> {self.student.full_name} ({self.amount})"

    def save(self, *args, **kwargs):
        """
        Avtomatik holda homiyning sarflagan summasi va talabaning to'langan summasi qatorlarini yangilaydi
        """

        # Homiyning qolgan mablag'ini tekshiramiz
        remaining_sponsor_balance = self.sponsor.payment_amount - self.sponsor.spent_amount
        if self.amount > remaining_sponsor_balance:
            raise ValidationError("Homiyda yetarli mablag' mavjud emas!")

        # Talabaning kontrakt balansini tekshiramiz
        remaining_student_contract = self.student.contract_amount - self.student.donated_amount
        if self.amount > remaining_student_contract:
            raise ValidationError("To'lanadigan summa talabaning kontraktidan katta bo'lishi mumkin emas!")

        super().save(*args, **kwargs)

        # Homiy va talaba balansini yangilaymiz
        self.sponsor.spent_amount += self.amount
        self.sponsor.save(update_fields=['spent_amount'])

        self.student.update_donation_amount()

    class Meta:
        verbose_name = "Xayriya"
        verbose_name_plural = "Xayriyalar"
        db_table = "donations"
