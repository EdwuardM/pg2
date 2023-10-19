from django.urls import path
from . import views

app_name = "Apps.suppliers"
urlpatterns = [
      path('', views.suppliersListView, name='suppliers_list'),
      path('add', views.suppliersAddView, name='suppliers_add'),
      path('update/<str:supplier_id>',
            views.suppliersUpdateView, name='suppliers_update'),
      path('delete/<str:supplier_id>',
            views.suppliersDeleteView, name='suppliers_delete'),
]
