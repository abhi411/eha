from django.db import models
import datetime
import os
import random
from django_resized import ResizedImageField



# FUNCTION to Upload image
def shop_item_image(instance, filename):
	"""Rename file before upload"""
	basefilename, file_extension= os.path.splitext(filename)
	basename = "pic_"
	current = str(datetime.datetime.now().strftime('%Y-%m-%d'))
	random_number = '{:04}'.format(random.randrange(1, 10**4))
	return 'shop_item/{basename}{randomstring}{ext}'.format(basename= basename, randomstring= random_number + "_" + current, ext= file_extension)

# Function to upload PROFILE PICTURE(CUSTOMER)
def photo_path(instance, filename):
	basefilename, file_extension= os.path.splitext(filename)
	basename = "pic_"
	current = str(datetime.datetime.now().strftime('%Y-%m-%d'))
	random_number = '{:04}'.format(random.randrange(1, 10**4))
	return 'profile_picture/{basename}{randomstring}{ext}'.format(basename= basename, randomstring= random_number + "_" + current, ext= file_extension)

# ---------------------------------------------------------------------------------------



# SHOP ITEMS
class ShopItems(models.Model):
	title = models.TextField(null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	image = ResizedImageField(size=[500, 300], crop=['middle', 'center'], null=True, blank=True, upload_to = shop_item_image)
	price = models.CharField(max_length=100, null=True, blank=True)
	category = models.CharField(max_length=100, null=True, blank=True)
	created_date = models.DateField(null = True, blank = True,default = datetime.date.today)

	def __str__(self):
		return self.title



# COUPON
class Coupon(models.Model):
	coupon_code = models.CharField(max_length=100, null=True, blank=True)
	discount = models.CharField(max_length=50, null=True, blank=True)
	expiry_date = models.DateField(null = True, blank = True)
	created_date = models.DateField(null = True, blank = True,default = datetime.date.today)
	total_uses = models.CharField(max_length=50, null=True, blank=True)
	uses_remain = models.CharField(max_length=50, null=True, blank=True)
	def __str__(self):
		return self.coupon_code



# Customer
class Customer(models.Model):
	firstname = models.CharField(max_length=250, null=True, blank=True)
	lastname = models.CharField(max_length=250, null=True, blank=True)
	email = models.CharField(max_length=200, null=True, blank=True)
	password = models.CharField(max_length=200, null=True, blank=True)
	contact_no = models.CharField(max_length=50, null=True, blank=True)
	address = models.TextField(null=True, blank=True)
	profile_img = ResizedImageField(size=[300, 300], crop=['middle', 'center'], upload_to= photo_path, null=True, blank=True)
	reset_code = models.CharField(max_length=10, null=True, blank=True)
	created_date = models.DateField(null = True, blank = True,default = datetime.date.today)

	def __str__(self):
		return ' '.join(filter(None, (self.firstname, self.lastname)))



# CART
class Cart(models.Model):	
	fk_customer = models.ForeignKey(Customer, null = True, on_delete=models.CASCADE)
	fk_shop_item = models.ForeignKey(ShopItems , null = True, on_delete=models.CASCADE)
	created_date = models.DateField(null = True, blank = True,default = datetime.date.today)


class Order(models.Model):	
	fk_customer = models.ForeignKey(Customer,null = True,on_delete=models.CASCADE)
	fk_shop_item = models.ForeignKey(ShopItems ,null = True,on_delete=models.CASCADE)
	order_no = models.CharField(max_length=200, null=True, blank=True)
	price = models.CharField(max_length=100, null=True, blank=True)
	payment = models.CharField(max_length=100, null=True, blank=True)
	fk_coupon = models.ForeignKey(Coupon,null = True, blank=True, on_delete=models.CASCADE)
	address = models.TextField(null=True, blank=True)
	latitude = models.FloatField(null=True, blank=True)
	longitude = models.FloatField(null=True, blank=True)
	created_date = models.DateField(null = True, blank = True,default = datetime.date.today)
	stripe_session = models.CharField(max_length=500, null=True, blank=True)
