from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.utils import generate_uuid_4


class Budget(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid_4, editable=False
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    name = models.CharField(
        _('Budget name'), max_length=150
    )
    categories = models.ManyToManyField(
        'budgets.ExpenseCategory',
        through='budgets.Expense',
        through_fields=('budget', 'category'),
        related_name='budgets'
    )


class Income(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid_4, editable=False
    )
    budget = models.ForeignKey(
        'budgets.Budget', on_delete=models.CASCADE, related_name='incomes'
    )
    name = models.CharField(
        _('Income name'), max_length=150
    )
    amount = models.DecimalField(
        _('amount'), max_digits=25, decimal_places=2,
        validators=(MinValueValidator(Decimal(0)),)
    )


class ExpenseCategory(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid_4, editable=False
    )
    name = models.CharField(
        _('Category name'), max_length=150
    )


class Expense(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid_4, editable=False
    )
    budget = models.ForeignKey(
        'budgets.Budget', on_delete=models.CASCADE,
        related_name='expenses'
    )
    category = models.ForeignKey(
        'budgets.ExpenseCategory', on_delete=models.PROTECT,
        related_name='expenses'
    )
    name = models.CharField(
        _('Expense name'), max_length=150
    )
    amount = models.DecimalField(
        _('amount'), max_digits=5, decimal_places=2,
        validators=(MinValueValidator(Decimal(0)),)
    )
