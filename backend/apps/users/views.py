import json

from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse


def login_view(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        username = body.get('username', '')
        password = body.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_info = {
                username: user.get_username(),
            }
            return HttpResponse(json.dumps(user_info), status=200)
        else:
            return HttpResponse('Unauthorized', status=401)
    else:
        return HttpResponse('Method not allowed', status=405)

def logout_view(request):
    logout(request)
    return HttpResponse('Ok', status=200)
