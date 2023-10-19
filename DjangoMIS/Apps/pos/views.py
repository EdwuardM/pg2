from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, FloatField, F
from django.db.models.functions import Coalesce
from django.shortcuts import render
from Apps.products.models import Product, Category
from Apps.sales.models import Sale
import json

@login_required
def index(request):
    today = date.today()
    year = today.year

    # Crear una lista para almacenar las ganancias mensuales
    monthly_earnings = []

    # Crear una lista para almacenar las ganancias anuales
    annual_earnings = []

    # Crear una lista para almacenar las ganancias semanales
    weekly_earnings = []

    for month in range(1, 13):
        # Calcular las ganancias mensuales
        earning = Sale.objects.filter(date_added__year=year, date_added__month=month).aggregate(
            total_variable=Coalesce(Sum(F('grand_total')), 0.0, output_field=FloatField())).get('total_variable')
        monthly_earnings.append(earning)

    # Calcular las ganancias anuales
    annual_earnings = Sale.objects.filter(date_added__year=year).aggregate(total_variable=Coalesce(
        Sum(F('grand_total')), 0.0, output_field=FloatField())).get('total_variable')
    annual_earnings = format(annual_earnings, '.2f')

    # Calcular las ganancias semanales
    one_year_ago = today - timedelta(days=365)
    current_date = one_year_ago
    while current_date <= today:
        next_week = current_date + timedelta(weeks=1)
        earning = Sale.objects.filter(
            date_added__gte=current_date,
            date_added__lt=next_week
        ).aggregate(
            total_variable=Coalesce(Sum(F('grand_total')), 0.0, output_field=FloatField())
        ).get('total_variable')
        weekly_earnings.append(earning)
        current_date = next_week

    avg_month = format(sum(monthly_earnings) / 12, '.2f')

    top_products = Product.objects.annotate(quantity_sum=Sum(
        'saledetail__quantity')).order_by('-quantity_sum')[:3]

    top_products_names = []
    top_products_quantity = []

    for p in top_products:
        top_products_names.append(p.name)
        top_products_quantity.append(p.quantity_sum)

    context = {
        "active_icon": "dashboard",
        "products": Product.objects.all().count(),
        "categories": Category.objects.all().count(),
        "annual_earnings": annual_earnings,
        "monthly_earnings": json.dumps(monthly_earnings),
        "weekly_earnings": format(weekly_earnings[-1], '.2f'),  # Mostramos la ganancia de la semana actual
        "avg_month": avg_month,
        "top_products_names": json.dumps(top_products_names),
        "top_products_names_list": top_products_names,
        "top_products_quantity": json.dumps(top_products_quantity),
    }
    return render(request, "pos/index.html", context)
