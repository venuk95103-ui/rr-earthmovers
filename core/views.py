from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import pandas as pd

from .models import Farmer, Bill, Expense
from .forms import FarmerForm, BillForm, ExpenseForm


# 🔹 DASHBOARD
@login_required
def dashboard(request):
    total = Bill.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    cleared = Bill.objects.aggregate(Sum('cleared_amount'))['cleared_amount__sum'] or 0
    balance = total - cleared
    expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    profit = total - expenses

    # DATE-WISE
    bills = Bill.objects.all().order_by('date')
    dates = [str(b.date) for b in bills]
    totals = [b.total_amount for b in bills]

    # MONTHLY
    monthly_data = (
        Bill.objects
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('total_amount'))
        .order_by('month')
    )

    months = [m['month'].strftime('%Y-%m') for m in monthly_data]
    monthly_totals = [m['total'] for m in monthly_data]

    return render(request, 'dashboard.html', {
        'total': total,
        'cleared': cleared,
        'balance': balance,
        'expenses': expenses,
        'profit': profit,
        'dates': dates,
        'totals': totals,
        'months': months,
        'monthly_totals': monthly_totals
    })


# 🔹 BILLS
@login_required
def bills(request):
    return render(request, 'bills.html', {
        'bills': Bill.objects.all()
    })


# 🔹 ADD BILL
@login_required
def add_bill(request):
    form = BillForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('bills')
    return render(request, 'form.html', {'form': form})


# 🔹 EDIT BILL
@login_required
def edit_bill(request, id):
    bill = get_object_or_404(Bill, id=id)
    form = BillForm(request.POST or None, instance=bill)
    if form.is_valid():
        form.save()
        return redirect('bills')
    return render(request, 'form.html', {'form': form})


# 🔹 DELETE BILL
@login_required
def delete_bill(request, id):
    Bill.objects.get(id=id).delete()
    return redirect('bills')


# 🔹 EXPORT BILLS
@login_required
def export_bills(request):
    bills = Bill.objects.all()

    data = []
    for b in bills:
        data.append({
            'Farmer': b.farmer.name,
            'Total': b.total_amount,
            'Cleared': b.cleared_amount,
            'Balance': b.total_amount - b.cleared_amount,
            'Date': b.date.strftime('%d-%m-%Y') if b.date else ''   # ✅ FIXED
        })

    df = pd.DataFrame(data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=bills.xlsx'

    df.to_excel(response, index=False)
    return response


# 🔹 EXPENSES
@login_required
def expenses(request):
    form = ExpenseForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('expenses')

    return render(request, 'expenses.html', {
        'expenses': Expense.objects.all(),
        'form': form
    })


# 🔹 EDIT EXPENSE
@login_required
def edit_expense(request, id):
    expense = get_object_or_404(Expense, id=id)
    form = ExpenseForm(request.POST or None, instance=expense)
    if form.is_valid():
        form.save()
        return redirect('expenses')
    return render(request, 'form.html', {'form': form})


# 🔹 DELETE EXPENSE
@login_required
def delete_expense(request, id):
    Expense.objects.get(id=id).delete()
    return redirect('expenses')


# 🔹 EXPORT EXPENSES
@login_required
def export_expenses(request):
    expenses = Expense.objects.all()

    data = []
    for e in expenses:
        data.append({
            'Date': e.date.strftime('%d-%m-%Y') if e.date else '',  # ✅ FIXED
            'Amount': e.amount,
            'Type': e.expense_type
        })

    df = pd.DataFrame(data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=expenses.xlsx'

    df.to_excel(response, index=False)
    return response


# 🔹 ADD FARMER
@login_required
def add_farmer(request):
    form = FarmerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('bills')
    return render(request, 'form.html', {'form': form})


# 🔹 FARMER DETAIL
@login_required
def farmer_detail(request, id):
    farmer = get_object_or_404(Farmer, id=id)
    bills = Bill.objects.filter(farmer=farmer)

    return render(request, 'farmer_detail.html', {
        'farmer': farmer,
        'bills': bills
    })