from django.core.mail import EmailMessage
from django.conf import settings
import random
from django.core.cache import cache
from django.template.loader import render_to_string
import geoip2.database
import os


def generate_otp(user_id):
    otp=f"{random.randint(1000, 9999)}"
    key=f"otp:{user_id}"
    cache.set (key, otp, timeout=1200)
    return otp

def verify_otp(user_id, otp_input):
    key = f"otp:{user_id}"
    cached_otp = cache.get(key)
    if cached_otp and cached_otp == otp_input:
        cache.delete(key)
        return True
    return False


def send_otp_email(user_email, otp, fail_silently=True):
    subject = "Please Verify Your Email Address"
    message = render_to_string("email_template.html", {
        "user_email": user_email,
        "otp": otp
    })
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    email = EmailMessage(subject, message, from_email, recipient_list)
    email.content_subtype = 'html'
    email.send(fail_silently=fail_silently)


def extract_ip(request):
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR')

    # print("X-Real-IP", request.META)
    # ip_address = "45.87.213.228"
    # print("hhhhhhh", ip_address)
    if ip_address:
        ip_address = ip_address.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    # print("ip_address", ip_address)

    print("FORWARDED:", request.META.get("HTTP_X_FORWARDED_FOR"))
    print("REMOTE:", request.META.get("REMOTE_ADDR"))
    print("FINAL IP:", ip_address)
    return ip_address


def get_country_from_ip(ip_address):
    db_path = os.path.join(
        settings.BASE_DIR,
        'geoip',
        'GeoLite2-City_20250502',
        'GeoLite2-City_20250502',
        'GeoLite2-City.mmdb'
    )

    reader = geoip2.database.Reader(db_path)

    try:
        response = reader.city(ip_address)
        return response.country.name

    except geoip2.errors.AddressNotFoundError:
        return None
    finally:
        reader.close()