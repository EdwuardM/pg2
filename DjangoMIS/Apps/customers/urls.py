from django.urls import path

from . import views

app_name = "Apps.customers"
urlpatterns = [
     path('', views.CustomersListView, name='customers_list'),
     path('add', views.CustomersAddView, name='customers_add'),
     path('details/<str:customer_id>',
          views.CustomerDetailsView, name='customers_details'),
     path('update/<str:customer_id>',
          views.CustomersUpdateView, name='customers_update'),
     path('delete/<str:customer_id>',
          views.CustomersDeleteView, name='customers_delete'),
     path('debts/<str:customer_id>',
          views.CustomersDebtsView, name='customers_debts'),
]
