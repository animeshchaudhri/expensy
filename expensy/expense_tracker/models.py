from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return self.user.email

class Expense(models.Model):
    SPLIT_CHOICES = [
        ('EQUAL', 'Equal Split'),
        ('EXACT', 'Exact Amount'),
        ('PERCENTAGE', 'Percentage Split'),
    ]

    title = models.CharField(max_length=200)
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    paid_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='expenses_paid'
    )
    split_type = models.CharField(max_length=10, choices=SPLIT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"

class ExpenseSplit(models.Model):
    expense = models.ForeignKey(
        Expense, 
        on_delete=models.CASCADE, 
        related_name='splits'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        unique_together = ['expense', 'user']