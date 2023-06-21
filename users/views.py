from django.shortcuts import redirect
from django.views.generic import ListView
from .functions import f_post_user, f_get_users
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User

# Create your views here.


@csrf_exempt
def post_user(request):
    return JsonResponse(f_post_user(request.POST['name'],
                                    request.POST['email'],
                                    request.POST['preferences'],
                                    request.POST['affiliate']))

@csrf_exempt
def add_user(request):
    response =  f_post_user(request.POST['name'],
                            request.POST['email'],
                            request.POST['preferences'],
                            request.POST['affiliate'])
    
    if 'error' in response.keys():
        request.session['error'] = response['error']
    else:
        if 'error' in request.session:
            del request.session['error']
        request.session['name'] = response['name']
        request.session['email'] = response['email']
        request.session['preferences'] = response['preferences']
        request.session['affiliate'] = response['affiliate']

    return redirect(to='../', json=response)


def get_users(_):
    return JsonResponse(f_get_users())


class HomeView(ListView):
    model = User
    template_name = 'home.html'

    def get_queryset(self):
        return f_get_users()