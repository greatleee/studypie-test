"""studypie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from graphene_django.views import GraphQLView

from apps.users.views import login_view, logout_view
from studypie.schema import schema


@ensure_csrf_cookie
def get_csrf(request):
    if (request.method == 'GET'):
        return HttpResponse('Ok', status=200)
    else:
        return HttpResponse('Method not allowed', status=405)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('csrf/', get_csrf, name="csrf"),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('graphql', GraphQLView.as_view(graphiql=True, schema=schema)),
]
