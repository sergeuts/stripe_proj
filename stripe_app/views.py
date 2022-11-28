from django.shortcuts import render, redirect
import stripe
from stripe_app.utils_db import get_table_values
from .forms import *

stripe.api_key = "sk_test_51M7QWiJ60IW64VVywW9xeqI08Erecj9gwoGTkWRluPJWG1swCcRgc46EMTu8CDThoPWDixwBfeFJYbYMB9ByzJ60004LHU0Fdt"
# "pk_test_51M7QWiJ60IW64VVyU4Ly3ONDB6LC8bApJf7rO33jbzekeNAPiWtU5ZwbvpzR0SRXnkHbagzmlXqk1fJKko01PeMS008wn0m37O"


def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'T-shirt',
                    },
                    'unit_amount': 2000,
                },
                'quantity': 1,
            },
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'iphone 14',
                    },
                    'unit_amount': 100000,
                },
                'quantity': 1,
            },


            ],
            mode='payment',
            success_url='http://localhost/success',
            cancel_url='http://localhost/cancel',
        )
    except Exception as e:
        return str(e)
    return session


def index(request):
    fields = ['item_id', 'name',  'price', 'currency']
    table = get_table_values(Item, filter='', fields=fields)
    formset = CatalogTableFormSet()
    for row in range(len(table)):
        table[row]['form'] = formset[row]
    return render(request, 'index.html', {'table': table, 'currency': PaymentCurrency(initial={'currency': Currency.objects.filter(id='1')})})


def make_order(request):
    cat_form = CatalogForm(request.POST)
    if cat_form.is_valid():
        amounts = cat_form.cleaned_data.get("amount")
    fields = ['item_id', 'name',  'price', 'currency']
    table = get_table_values(Item, filter='', fields=fields)
    return render(request, 'index.html', {'table': table, 'currency': PaymentCurrency()})


def payment(request):
    if request.method == 'POST':
        session = create_checkout_session()
        return redirect(session.url)
    else:
        return render(request, 'index.html', {})


def cancel(request):
    return render(request, 'cancel.html', {})


def success(request):
    return render(request, 'success.html', {})


def buy_items(request, item_id):
    session = create_checkout_session()
    return render(request, 'buy_items.html', {'item_id': item_id, 'url': session.url})