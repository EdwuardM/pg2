from django.urls import path

from . import views

app_name = "Apps.sales"
urlpatterns = [
    path('', views.SalesListView, name='sales_list'),
    path('add', views.SalesAddView, name='sales_add'),
    path('close', views.SalescloseView, name='sales_close'),
    path('details/<str:sale_id>',
        views.SalesDetailsView, name='sales_details'),
    path("pdf/<str:sale_id>",
        views.ReceiptPDFView, name="sales_receipt_pdf"),
]