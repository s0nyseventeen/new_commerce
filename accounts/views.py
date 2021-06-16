from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter


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
    my_filter_order = OrderFilter(request.GET, queryset=orders)
    orders = my_filter_order.qs
    context = {
        'total_orders': total_orders,
        'orders': orders,
        'customer': customer,
        'my_filter_order': my_filter_order
    }
    return render(request, 'accounts/customers.html', context)


def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order,
                                        fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        print("!!! PRINTING REQUEST POST:", request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        # if form.is_valid():
            # form.save()
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {
        'formset': formset
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


def register_page(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)
