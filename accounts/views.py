from django.shortcuts import render, redirect
from .models import *
from .forms import *


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {
        'delivered': delivered,
        'pending': pending,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'orders': orders,
        'customers': customers
    }
    return render(request, 'accounts/dashboard.html', context)


def product(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'accounts/products.html', context)

 
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()
    context = {
        'total_orders': total_orders,
        'orders': orders,
        'customer': customer
    }
    return render(request, 'accounts/customers.html', context)


def create_order(request, pk):
    customer = Customer.objects.get(id=pk)
    form = OrderForm()
    if request.method == 'POST':
        print("!!! PRINTING REQUEST POST:", request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'accounts/order_form.html', context)


def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == "POST":
        print("!!! PRINTING REQUEST POST:", request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'accounts/order_form.html', context)


def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        print("!!! PRINTING REQUEST POST:", request.POST)
        order.delete()
        return redirect('/')
    context = {
        'order': order
    }
    return render(request, 'accounts/delete_order.html', context)
