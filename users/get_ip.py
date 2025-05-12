# import geoip2.database
# from django.http import JsonResponse
# from .models import User
# import os
# from django.conf import settings
#
# def get_user_ip(request):
#     # ip_address = '103.252.24.1'
#     ip_address = request.META.get('REMOTE_ADDR', '0.0.0.0')
#
#     db_path = os.path.join(
#         settings.BASE_DIR,
#         'geoip',
#         'GeoLite2-City_20250502',
#         'GeoLite2-City_20250502',
#         'GeoLite2-City.mmdb'
#     )
#
#     reader = geoip2.database.Reader(db_path)
#
#     try:
#         response = reader.city(ip_address)
#
#         country = response.country.name
#
#         user = User.objects.get(email=request.user.email)
#         user.country = country
#         user.save()
#
#         location = {
#             'ip': ip_address,
#             'country': country
#         }
#
#     except geoip2.errors.AddressNotFoundError:
#         location = {'error': 'Location not found for this IP'}
#     except User.DoesNotExist:
#         location = {'error': 'User not found'}
#
#     reader.close()
#
#     return JsonResponse(location)




