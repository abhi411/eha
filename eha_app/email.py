from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import smtplib, ssl
from .models import * 
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import mail


# To reset PASSWORD
def reset_password(code, email, name):
	
	mail_subject = "EHA Email Verification"
	from_email = settings.EMAIL_HOST_USER
	html_message = render_to_string('emails/forgot_password.html', {"name":name,"code":code})
	message_to_send   = strip_tags(html_message)
	send_mail(mail_subject, message_to_send, from_email, [email], html_message = html_message)


# To send order confirmation mail
def order_confirmation(email, name, items, total, address):
	
	mail_subject = "Your EHA order #"+items[0].order_no
	from_email = settings.EMAIL_HOST_USER
	context = {
		'name' : name,
                'address' : address,
		'items' : items,
		'total' : total,
		'email' : email
	}
	html_message = render_to_string('emails/order_confirmation.html', context)
	message_to_send   = strip_tags(html_message)
	send_mail(mail_subject, message_to_send, from_email, [email], html_message = html_message)
	
	
	
def order_confirmation_admin(name, address, items, total,email):
	
	mail_subject = "Your EHA order #"+items[0].order_no
	from_email = settings.EMAIL_HOST_USER
	context = {
		'name' : name,
		'address' : address,
		'items' : items,
		'total' : total,
		'email' : email
	}
	html_message = render_to_string('emails/order_confirmation_admin.html', context)
	message_to_send   = strip_tags(html_message)
	send_mail(mail_subject, message_to_send, from_email, ['environmentalandhealth@gmail.com'], html_message = html_message)



#  to send contact-us mail
def email_contact_us(name, email, subject, message):
	
	mail_subject = "New enquiry from website"
	message = message
	from_email = settings.EMAIL_HOST_USER
	context = {
		"name" : name,
		"email" : email,
		"subject" : subject,
		"message" : message,
	} 
	html_message = render_to_string('emails/contact.html', context)
	message_to_send   = strip_tags(html_message)
	send_mail(mail_subject, message_to_send, from_email, ['environmentalandhealth@gmail.com'], html_message = html_message)



@csrf_exempt
def email_order_details(request):
    id = request.POST.get('id')
    if Order.objects.filter(id=id).exists():
        email_obj = Order.objects.get(id=id)
        mail_subject = "Your Order No :"+email_obj.order_no
        from_email = settings.EMAIL_HOST_USER
        f= open("order_details.txt", "w")
        f.write("Sold to :"+str(email_obj.fk_customer)+"\n")
        f.write("Address :"+str(email_obj.address))
        f.close()
        context = { 
        "address" : email_obj.address,
        "name" : email_obj.fk_customer,
        }
        # html_message = render_to_string('emails/order_details.html', context) 
        message_to_send   = render_to_string('emails/order_details.html', context) 
        email = EmailMessage(mail_subject, message_to_send, from_email,['environmentalandhealth@gmail.com'])
        email.content_subtype = "html"
        f = open('order_details.txt', 'r')
        email.attach('order_details.txt', f.read(), 'text/plain')
        email.send()
        
        response = "success"
    else:
        response = "error"
    return HttpResponse(response)
        
