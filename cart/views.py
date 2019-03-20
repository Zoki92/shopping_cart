from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from accounts.models import Profile
from product.models import Product
from django.contrib import messages
from .models import OrderItem, Order
from .extras import generate_order_id
import datetime
from django_ajax.decorators import ajax
import json
from django.http import Http404, HttpResponse
# Create your views here.

def get_user_pending_order(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        return order[0]
    return 0



@login_required
def add_to_cart(request, **kwargs):
    user_profile = get_object_or_404(Profile, user=request.user)
    product = Product.objects.filter(id=kwargs.get('item_id', "")).first()

    if product in request.user.profile.ebooks.all():
        messages.info(request, "You already own this ebook")
        return redirect('product-list')
    order_item, status = OrderItem.objects.get_or_create(product=product)
    user_order, status = Order.objects.get_or_create(owner = user_profile, is_ordered=False)
    user_order.items.add(order_item)
    if status:
        user_order.ref_code = generate_order_id()
        user_order.save()
    messages.info(request, "Item added to cart")
    return redirect('product-list')


# @login_required()
# def delete_from_cart(request, item_id):
#     item_to_delete = OrderItem.objects.filter(pk=item_id)
#     if item_to_delete.exists():
#         item_to_delete[0].delete()
#         messages.info(request, "Item has been deleted")
#     return redirect('order_summary')

@ajax
@login_required()
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
    orders = Order.objects.all();
    final_price = orders[0].get_cart_total();
    data = json.dumps(final_price)
    return HttpResponse(data, content_type='application/json')




@login_required
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'order_summary.html', context)


@login_required
def process_payment(request, order_id):
    return redirect('update_records', kwargs={
        'order_id': order_id
    })

@login_required
def update_transaction_records(request, order_id):
    order_to_purchase = get_object_or_404(Order, pk=order_id)
    order_to_purchase.is_ordered=True
    order_to_purchase.date_ordered=datetime.datetime.now()
    order_to_purchase.save()

    order_items = order_to_purchase.items.all()
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    user_profile = get_object_or_404(Profile, user=request.user)
    order_products = [item.product for item in order_items]
    user_profile.ebooks.add(*order_products)
    user_profile.save()
    messages.info(request, "Thank you! Your items have been added to your product list")
    return redirect('my_profile')

def success(request, **kwargs):
    return render(request, 'purchase_success.html', {})