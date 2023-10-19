from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Customer
from Apps.sales.models import SaleDetail, Sale
from decimal import Decimal, ROUND_DOWN

@login_required(login_url="/accounts/login/")
def CustomersListView(request):
    context = {
        "active_icon": "customers",
        "customers":Customer.objects.exclude(id=11)
    }
    return render(request, "customers/customers.html", context=context)

@login_required(login_url="/accounts/login/")
def CustomersAddView(request):
    context = {
        "active_icon": "customers",
    }
    if request.method == 'POST':
        data = request.POST
        attributes = {
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "address": data['address'],
            "phone": data['phone'],
        }
        if Customer.objects.filter(**attributes).exists():
            messages.error(request, '¡El cliente ya existe!',
                extra_tags="warning")
            return redirect('Apps.customers:customers_add')
        try:
            new_customer = Customer.objects.create(**attributes)
            new_customer.save()
            messages.success(request, '¡Cliente: ' + attributes["first_name"] + " " +
                attributes["last_name"] + ' Creado con éxito!', extra_tags="success")
            return redirect('Apps.customers:customers_list')
        except Exception as e:
            messages.success(
                request, '¡Hubo un error durante la creación!', extra_tags="danger")
            print(e)
            return redirect('Apps.customers:customers_add')
    return render(request, "customers/customers_add.html", context=context)

@login_required(login_url="/accounts/login/")
def CustomersUpdateView(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Exception as e:
        messages.success(
            request, '¡Hubo un error al intentar localizar al cliente!', extra_tags="danger")
        return redirect('Apps.customers:customers_list')
    context = {
        "active_icon": "customers",
        "customer": customer,
    }
    if request.method == 'POST':
        try:
            data = request.POST
            attributes = {
                "first_name": data['first_name'],
                "last_name": data['last_name'],
                "address": data['address'],
                "phone": data['phone'],
            }
            if Customer.objects.filter(**attributes).exists():
                messages.error(request, '¡El cliente ya existe!',
                    extra_tags="warning")
                return redirect('Apps.customers:customers_add')
            customer = Customer.objects.filter(
                id=customer_id).update(**attributes)
            customer = Customer.objects.get(id=customer_id)
            messages.success(request, '¡Cliente: ' + customer.get_full_name() +
                ' actualizado exitosamente!', extra_tags="success")
            return redirect('Apps.customers:customers_list')
        except Exception as e:
            messages.success(
                request, '¡Hubo un error durante la actualización!', extra_tags="danger")
            return redirect('Apps.customers:customers_list')
    return render(request, "customers/customers_update.html", context=context)

@login_required(login_url="/accounts/login/")
def CustomersDeleteView(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        customer.delete()
        messages.success(request, '¡Cliente: ' + customer.get_full_name() +
            ' Eliminado!', extra_tags="success")
        return redirect('Apps.customers:customers_list')
    except Exception as e:
        messages.success(
            request, '¡Hubo un error durante la eliminación!', extra_tags="danger")
        return redirect('Apps.customers:customers_list')

@login_required(login_url="/accounts/login/")
def CustomerDetailsView(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        sales = Sale.objects.filter(customer=customer)
        details = SaleDetail.objects.filter(sale__in=sales)
        total_amount_payed = Decimal('0.0')
        tax_discount = Decimal('0.0') 
        tax_discount_porcentaje = Decimal('0.0') 
        detail_total= Decimal('0.0')
        for detail in details:
            detail_total += Decimal(detail.total_detail)
        for sale in sales:
            total_amount_payed += Decimal(sale.grand_total)
            tax_discount += Decimal(sale.tax_amount)
            tax_discount_porcentaje += Decimal(sale.tax_percentage)
        tax_discount = tax_discount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        total_amount_payed = total_amount_payed.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        context = {
            "active_icon": "customers",
            "sale": sales,
            "details": details,
            "customer": customer,
            "details_total": detail_total,
            "total_amount_payed": total_amount_payed,
            "tax_percentage": tax_discount_porcentaje,
            "tax_amount": tax_discount,
        }
        return render(request, "customers/customers_details.html", context=context)
    except Exception as e:
        messages.success(
            request, '¡Hubo un error al obtener cliente! ', extra_tags="danger")
        return redirect('Apps.customers:customers_list')

@login_required(login_url="/accounts/login/")    
def CustomersDebtsView(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        sales = Sale.objects.filter(customer=customer)
    except Exception as e:
        messages.error(
            request, '¡Hubo un error al intentar localizar al cliente!', extra_tags="danger")
        return redirect('Apps.customers:customers_list')
    if request.method == 'POST':
        try:
            customer.debts = 0
            customer.save()
            Sale.objects.filter(customer=customer).update(customer_id=11)
            messages.success(
                request, '¡Deuda del cliente ' + customer.get_full_name() + ' cancelada con éxito!', extra_tags="success")
            return redirect('Apps.customers:customers_list')
        except Exception as e:
            messages.error(
                request, '¡Hubo un error al pagar la deuda del cliente!', extra_tags="danger")
    context = {
        'customer': customer,
        'sales': sales,
    }
    return render(request, "customers/customers_update.html", context=context)
