from django.contrib import admin

from .models import *

# MODEL : ShopItems
class ShopItemsClass(admin.ModelAdmin):
	list_display = ('id','title','description','price','category','image')
admin.site.register(ShopItems ,ShopItemsClass)

# MODEL : COUPONS
class CouponClass(admin.ModelAdmin):
	list_display = ('id','coupon_code','discount','expiry_date')
admin.site.register(Coupon ,CouponClass)

# MODEL : Customer
class CustomerClass(admin.ModelAdmin):
	list_display = ('id','firstname','lastname','email','password','contact_no')
admin.site.register(Customer ,CustomerClass)

# MODEL : CART
class CartClass(admin.ModelAdmin):
	list_display = ('id','fk_customer','fk_shop_item','created_date')
admin.site.register(Cart ,CartClass)

# MODEL : ORDER
class OrderClass(admin.ModelAdmin):
	list_display = ('id','fk_customer','fk_shop_item','order_no','price','payment','fk_coupon')
admin.site.register(Order ,OrderClass)


