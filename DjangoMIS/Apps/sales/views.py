from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from Apps.customers.models import Customer
from Apps.products.models import Product
from django.db import transaction
from .models import Sale, SaleDetail, CashRegisterOpening
from django.db.models import Sum
from datetime import datetime
from xhtml2pdf import pisa
from io import BytesIO

import json


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@login_required(login_url="/accounts/login/")
def SalesListView(request):
    today = datetime.now()
    opening = CashRegisterOpening.objects.filter(user=request.user, opening_date__date=today).first()
    if not opening:
        if request.method == 'POST':
            initial_amount = request.POST.get('initial_amount')
            opening = CashRegisterOpening.objects.create(user=request.user, initial_amount=initial_amount, opening_date=today)
        else:
            return render(request, 'sales/open_cash_register.html')
    context = {
        "active_icon": "sales",
        "sales": Sale.objects.all(),  
        "opening": opening,
    }
    return render(request, "sales/sales.html", context=context)

@login_required(login_url="/accounts/login/")
def SalesAddView(request):
    today = datetime.now().date()
    opening = CashRegisterOpening.objects.filter(opening_date__date=today).first()
    context = {
        "active_icon": "sales",
        "customers": [c.to_select2() for c in Customer.objects.all()],
    }
    if request.method == 'POST':
        if is_ajax(request=request):
            cash_register_opening_id = opening.id
            cash_register_opening_instance = CashRegisterOpening.objects.get(id=cash_register_opening_id)
            data = json.loads(request.body)
            sale_attributes = {
                "customer": Customer.objects.get(id=int(data['customer'])),
                "sub_total": float(data["sub_total"]),
                "grand_total": float(data["grand_total"]),
                "tax_amount": float(data["tax_amount"]),
                "tax_percentage": float(data["tax_percentage"]),
                "amount_payed": float(data["amount_payed"]),
                "amount_change": float(data["amount_change"]),
                "cashRegisterOpening": cash_register_opening_instance,
            }
            try:
                with transaction.atomic():
                    new_sale = Sale.objects.create(**sale_attributes)
                    new_sale.save()
                    customer = Customer.objects.get(id=int(data['customer']))
                    customer.debts += float(data["grand_total"])
                    customer.save()
                products = data["products"]
                for product in products:
                    detail_attributes = {
                        "sale": Sale.objects.get(id=new_sale.id),
                        "product": Product.objects.get(id=int(product["id"])),
                        "price": product["price"],
                        "quantity": product["quantity"],
                        "total_detail": product["total_product"]
                    }
                    sale_detail_new = SaleDetail.objects.create(
                        **detail_attributes)
                    sale_detail_new.save()
                    product_instance = Product.objects.get(id=int(product["id"]))
                    product_instance.quantity -= product["quantity"]
                    product_instance.save()
                messages.success(
                    request, '¡Venta creada con éxito!', extra_tags="success")
            except Exception as e:
                messages.success(
                    request, '¡Hubo un error al obtener la venta!', extra_tags="danger")
        return redirect('Apps.sales:sales_list')
    return render(request, "sales/sales_add.html", context=context)

@login_required(login_url="/accounts/login/")
def SalesDetailsView(request, sale_id):
    try:
        sale = Sale.objects.get(id=sale_id)
        print(sale)
        details = SaleDetail.objects.filter(sale=sale)
        context = {
            "active_icon": "sales",
            "sale": sale,
            "details": details,
        }
        return render(request, "sales/sales_details.html", context=context)
    except Exception as e:
        messages.success(
            request, '¡Hubo un error al obtener la venta!', extra_tags="danger")
        return redirect('Apps.sales:sales_list')

@login_required(login_url="/accounts/login/")
def SalescloseView(request):
    if request.method == 'POST':
        today = datetime.now().date()
        closing = CashRegisterOpening.objects.filter(opening_date__date=today).first()
        if closing:
            final_amount = request.POST.get('final_amount')
            closing.final_amount = final_amount
            total_sesion = Sale.objects.filter(cashRegisterOpening=closing.id).aggregate(total_grand_total=Sum('grand_total'))['total_grand_total']
            closing.total_sesion = total_sesion
            closing.save()
            return render(request, 'sales/cash_register_closing_summary.html', {
                'closing': closing,
                'user': request.user,
                'closing_date': closing.opening_date,
            })
        else:
            return HttpResponse("No se encontró una apertura de caja para el día actual.")
    return render(request, 'sales/close_cash_register.html')

@login_required(login_url="/accounts/login/")
def ReceiptPDFView(request, sale_id):
    sale = Sale.objects.get(id=sale_id)
    details = SaleDetail.objects.filter(sale=sale)
    template = get_template("sales/sales_receipt_pdf.html")
    context = {
        "sale": sale,
        "details": details
    }
    html_template = template.render(context)
    buffer = BytesIO()
    pisa.CreatePDF(
        src=html_template,
        dest=buffer
    )
    pdf_data = buffer.getvalue()
    buffer.close()
    pdf_filename = "ReciboEdcar.pdf"
    response = HttpResponse(pdf_data, content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
    return response
