from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='financials.index'),
    path("transactions/", views.transactions_list, name='financials.transactions-list'),
    path("add-transaction/", views.add_transaction, name='financials.add_transaction'),
    path('edit-transaction/<int:transaction_id>/', views.edit_transaction, name='financials.edit_transaction')
]