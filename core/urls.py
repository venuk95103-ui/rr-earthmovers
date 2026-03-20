from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('bills/', views.bills, name='bills'),
    path('add-bill/', views.add_bill, name='add_bill'),
    path('edit-bill/<int:id>/', views.edit_bill, name='edit_bill'),
    path('delete-bill/<int:id>/', views.delete_bill, name='delete_bill'),
    path('export-bills/', views.export_bills, name='export_bills'),

    path('expenses/', views.expenses, name='expenses'),
    path('edit-expense/<int:id>/', views.edit_expense, name='edit_expense'),
    path('delete-expense/<int:id>/', views.delete_expense, name='delete_expense'),
    path('export-expenses/', views.export_expenses, name='export_expenses'),

    path('add-farmer/', views.add_farmer, name='add_farmer'),
    path('farmer/<int:id>/', views.farmer_detail, name='farmer_detail'),
]