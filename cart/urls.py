
from django.urls import path
from .views import add_to_cart, order_details, delete_from_cart, update_transaction_records, success

urlpatterns = [
    path('add-to-cart/<int:item_id>/', add_to_cart, name="add_to_cart"),
    path('order-summary/', order_details, name="order_summary"),
    path('success/', success, name="purchase_success"),
    path('item/delete/<int:item_id>/', delete_from_cart, name="delete_item"),
    path('update-transaction/<int:order_id>/', update_transaction_records, name="update_records")
]
