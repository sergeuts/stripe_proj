from django.shortcuts import render, redirect
import stripe
from .utils_db import get_table_values
from .forms import *
from .models import *
from stripe_proj.env_vars import *
from django.http import HttpResponse
from stripe_proj.settings import DEBUG

if DEBUG:
    success_url = 'http://localhost:8000/success'
    cancel_url = 'http://localhost:8000/cancel'
else:
    success_url = SUCCESS_URL
    cancel_url = CANCEL_URL

stripe.api_key = API_KEY
active_order = ''

def create_checkout_session(line_items):
    # if type(items) == int:
    #     pass
    # elif type(items) == list:
    #     line_items = [
    #                      {
    #                          'price_data': {
    #                              'currency': 'usd',
    #                              'product_data': {
    #                                  'name': 'T-shirt',
    #                              },
    #                              'unit_amount': 2000,
    #                          },
    #                          'quantity': 1,
    #                      },
    #                      {
    #                          'price_data': {
    #                              'currency': 'usd',
    #                              'product_data': {
    #                                  'name': 'iphone 14',
    #                              },
    #                              'unit_amount': 100000,
    #                          },
    #                          'quantity': 1,
    #                      },
    #
    #                  ],

    try:
        session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )
    except Exception as e:
        return str(e)
    return session


def index(request):
    fields = ['item_id', 'name', 'price', 'currency']
    table = get_table_values(Item, filter='', fields=fields)
    formset = CatalogTableFormSet()
    for row in range(len(table)):
        table[row]['form'] = formset[row]
    return render(request, 'index.html', {'table': table, 'currency': PaymentCurrency()})
    # initial={'currency': Currency.objects.filter(id='1')}


def make_order(request):
    fields = ['item_id', 'name', 'price', 'currency']
    table = get_table_values(Item, filter='', fields=fields)
    for row in range(len(table)):
        table[row]['amount'] = int(request.POST[f'form-{row}-amount'])
    amount_list = []
    for row in range(len(table) - 1, -1, -1):
        if not table[row]['amount']:
            table.pop(row)
        else:
            amount_list.append(round(table[row]['amount']*table[row]['price'], 2))

    order = 0
    line_items = []
    if table:
        order = Order.objects.create(sum=sum(amount_list), discount_id=1)
        order.save()
        currency_obj = Currency.objects.filter(pk=int(request.POST['currency'])).first()
        order.currency = currency_obj
        currency = currency_obj.name
        if currency == 'usd':
            rate = 1
        else:
            rate = Currency.objects.filter(name=currency).first().rate
        sum_calc_price = 0
        descr = '№ -- Items -- Amount --  Price /n'
        pos_no = 0
        for row in table:
            fields = {'order_no': order, 'item': Item.objects.filter(item_id=row['item_id'])[0],
                      'quantity': row['amount'], 'sum': row['price'] * row['amount']}
            # fields = {'order_no': order, 'item': row[1], 'quantity': row['amount'], 'sum': 1, 'discount_id': 1, 'tax_id': 1}
            oil = OrderItemsList.objects.create(**fields)
            oil.save()

            if row['currency'] == currency:
                row['calc_price'] = row['price']
            elif row['currency'] == 'usd':
                row['calc_price'] = round(row['price']*rate, 2)
            else:
                cur_rate = Currency.objects.filter(name=row['currency']).first().rate
                row['calc_price'] = round(row['price']/cur_rate*rate, 2)
            sum_calc_price += row['calc_price']
            pos_no += 1
            descr += f"{pos_no}  {row['name']}  {row['amount']}  {row['calc_price']}" + '/n'
            line_items.append({'price_data': {
                'currency': currency,
                'product_data': {
                    'name': row['name']
                },
                'unit_amount': int(row['calc_price'] * row['amount'] * 100),
            },
                'quantity': row['amount'],
            })
        order.sum = sum_calc_price
        order.description = descr
        order.save()

    session = create_checkout_session(line_items)
    return render(request, 'buy_items.html', {'table': table, 'currency': currency, 'order': order, 'url': session.url})
    #return render(request, 'buy_items.html', {'table': table, 'currency': currency, 'order': order, 'url': 'session.url'})


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


def buy_item(request, item_id):
    item_set = Item.objects.filter(item_id=item_id)
    if not item_set.count():
        return HttpResponse(f"<h1>Item with id={item_id} not found in catalog.</h1>")
    item = item_set[0]
    line_items = [{'price_data': {
        'currency': item.currency.name,
        'product_data': {
            'name': item.name,
        },
        'unit_amount': int(item.price * 100),
    },
        'quantity': 1,
    }]
    session = create_checkout_session(line_items)
    if 'item' in request.path:
        return render(request, 'item.html', {'item_id': item_id, 'item': item, 'url': session.url})
    elif 'buy' in request.path:
        txt = f'<h1><a href="{session.url}">Session id for payment:</a> <br> {session.id} </h1>'
        return HttpResponse(txt)
