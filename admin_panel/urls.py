from django.urls import path, re_path
from .views import *


urlpatterns = [
	path('', login, name='login'),
	path('logout', logout, name='logout'),
	path('dashboard', dashboard, name='dashboard'),
	path('change-password-page', change_password_page, name='change-password-page'),
	path('puc', page_under_construction, name='page_under_construction'),

	path('shop-items', shop_items, name='shop-items'),
	path('order-items', order_items, name='order-items'),
	path('shop-item/add', shop_item_add, name='shop-item-add'),
	re_path('shop-item/(?P<id>[0-9]+)/edit', shop_item_edit, name='shop-item-edit'),
	re_path('shop-item/(?P<id>[0-9]+)', shop_item_detail, name='shop-item-detail'),
	re_path('order-item/(?P<id>[0-9]+)', order_item_detail, name='order-item-detail'),
	path('coupons', coupons, name='coupons'),
	path('admin_panel/change_password', change_password, name='change-password'),
	
]  

# API URL
urlpatterns += [
	path('api/login',api_admin_login, name='api_admin_login'),
	
	path('api/shop_item_add',api_shop_item_add, name='api_shop_item_add'),
	path('api/shop_item_edit',api_shop_item_edit, name='api_shop_item_edit'),
	path('api/shop_item_delete',api_shop_item_delete, name='api_shop_item_delete'),
	
	path('api/coupon_add',api_coupon_add, name='api_coupon_add'),
	path('api/coupon_edit',api_coupon_edit, name='api_coupon_edit'),
	path('api/coupon_delete',api_coupon_delete, name='api_coupon_delete'),
]