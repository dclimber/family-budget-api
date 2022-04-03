from django.contrib import admin

from .models import Budget, Expense, ExpenseCategory, Income


class BudgetIncomeInline(admin.TabularInline):
    model = Income
    extra = 0


class BudgetExpenseInline(admin.TabularInline):
    model = Expense
    extra = 0


class BudgetAdmin(admin.ModelAdmin):
    inlines = (BudgetIncomeInline, BudgetExpenseInline)


admin.site.register(Budget, BudgetAdmin)
admin.site.register(ExpenseCategory)
