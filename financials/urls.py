from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='financials.dashboard'),
    path("transactions/", views.transactions_list, name='financials.transactions-list'),
    path("add-transaction/", views.add_transaction, name='financials.add_transaction'),
    path('edit-transaction/<int:transaction_id>/', views.edit_transaction, name='financials.edit_transaction'),
    path('delete/<int:transaction_id>/', views.delete_transaction, name='financials.delete_transaction')
]