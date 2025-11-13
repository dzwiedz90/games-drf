from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from users.models import User

def match_authenticated_user(request):
    try:
        request_token = request.META['HTTP_AUTHORIZATION'][6:]
        token = Token.objects.get(key=request_token)
        user = User.objects.get(pk=token.user_id)
        if token.key == request_token:
            return True, user
        return False, None
    except (User.DoesNotExist, Token.DoesNotExist):
        return Response({'message': 'authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)