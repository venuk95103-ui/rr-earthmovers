from django.db import models
from django.utils.timezone import now

class Farmer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name


class Bill(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    cleared_amount = models.FloatField()
    balance_amount = models.FloatField(blank=True)
    date = models.DateField(default=now)

    def save(self, *args, **kwargs):
        self.balance_amount = self.total_amount - self.cleared_amount
        super().save(*args, **kwargs)


class Expense(models.Model):
    amount = models.FloatField()
    expense_type = models.CharField(max_length=50)
    date = models.DateField(default=now)