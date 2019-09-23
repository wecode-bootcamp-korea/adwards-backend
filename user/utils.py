import jwt

from .models          import User, Advertiser
from adwards.settings import SECRET_KEY

from django.http      import JsonResponse

def user_login_required(func):
    def decorated_function(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization', None)

        if access_token:
            try:
                payload = jwt.decode(access_token, SECRET_KEY, 'HS256')
                user_type = payload['user_type']

                if user_type == 'advertiser':
                    return JsonResponse({"ERROR":"INVALID_USER"}, status=401)

                request.user = User.objects.get(email=payload['user_email'])

                return func(self, request, *args, **kwargs)
            except jwt.DecodeError:
                return JsonResponse({"ERROR":"INVALID_TOKEN"}, status=401)
            except User.DoesNotExist:
                return JsonResponse({"ERROR":"ID_NOT_EXIST"}, status=401)
        else:
            return JsonResponse({"ERROR":"LOGIN_REQUIERD"}, status=401)
    return decorated_function

def advertiser_login_required(func):
    def decorated_function(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization', None)

        if access_token:
            try:
                payload = jwt.decode(access_token, SECRET_KEY, 'HS256')
                user_type = payload['user_type']

                if user_type == 'user':
                    return JsonResponse({"ERROR":"INVALID_USER"}, status=401)

                request.user = Advertiser.objects.get(email=payload['user_email'])

                return func(self, request, *args, **kwargs)

            except jwt.DecodeError:
                return JsonResponse({"ERROR":"INVALID_TOKEN"}, status=401)
            except Advertiser.DoesNotExist:
                return JsonResponse({"ERROR":"ID_NOT_EXIST"}, status=401)

        else:
            return JsonResponse({"ERROR":"LOGIN_REQUIERD"}, status=401)
    return decorated_function
