from django import forms
from .models import Farmer, Bill, Expense

class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = '__all__'


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['farmer', 'total_amount', 'cleared_amount', 'date']


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'