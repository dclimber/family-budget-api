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

    class Meta:
        ordering = ('name',)
        verbose_name = _('Budget')
        verbose_name_plural = _('Budgets')

    def __str__(self):
        return _('Budget "{}"').format(self.name)


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

    class Meta:
        ordering = ('name',)
        verbose_name = _('Income for budget')
        verbose_name_plural = _('Incomes for budget')
        constraints = (
            models.UniqueConstraint(
                fields=['budget', 'name'], name='unique_income_for_budget'
            ),
        )

    def __str__(self):
        return _('Income "{}" for {}').format(self.name, self.budget)


class ExpenseCategory(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid_4, editable=False
    )
    name = models.CharField(
        _('Category name'), max_length=150
    )

    class Meta:
        ordering = ('name',)
        verbose_name = _('Expense category')
        verbose_name_plural = _('Expense categories')

    def __str__(self):
        return _('Expense category: {}').format(self.name)


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

    class Meta:
        ordering = ('name',)
        verbose_name = _('Expense')
        verbose_name_plural = _('Expenses')
        constraints = (
            models.UniqueConstraint(
                fields=['budget', 'name', 'category'],
                name='unique_expense_for_budget_and_category'
            ),
        )

    def __str__(self):
        return _('Expense "{}" for {}').format(self.name, self.budget)
