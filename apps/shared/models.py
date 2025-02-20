from django.db import models


# Create your models here.
class University(models.Model):
    name = models.CharField(blank=True, max_length=100)

    class Meta:
        verbose_name_plural = 'Universities'
        db_table = 'universities'

    def __str__(self):
        return self.name


class DateTimeBasedModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
