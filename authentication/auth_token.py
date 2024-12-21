import jwt # for jwt authentication
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from core.settings import SECRET_KEY

User = get_user_model()

class JwtAuthentication(BaseAuthentication):
    # here it will just get the authorization from header then extract the token
    # then decode it and return the user object
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
        else:
            try:
                token = auth_header.split(' ')[-1]
                payload = jwt.decode(token, key=SECRET_KEY, algorithms=['HS256'])
                # print('_____________________',payload)
            except jwt.InvalidAlgorithmError:
                raise AuthenticationFailed('Invalid algrothim')
            except jwt.InvalidTokenError:
                raise AuthenticationFailed('Invalid token')
            except jwt.InvalidKeyError:
                raise AuthenticationFailed('Invalid Key')
            
            if 'user_email' in payload and 'user_type' in payload:
                user = User.objects.get(email = payload['user_email'] , user_type = payload['user_type']) # this should be get not filter
                # as get returns a user object where a filter returns a queryset
                return (user, payload)
            else:
                raise AuthenticationFailed('Invalid payload data')

# to get the payload data from user we use Dispatch function and then call it in the class base api view 
class Dispatch: 
    def get_request(self , request):
        auth = JwtAuthentication()
        user, payload = auth.authenticate(request=request)
        if user is None:
            raise AuthenticationFailed('user not found')
        return (user, payload)