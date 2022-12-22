from django.shortcuts import render, redirect
from django.http import HttpResponse
from luaas.models import User

FLAG = "CJ2022{PLACEHOLDER_VALUE}"

def my_custom_page_not_found_view(request,exception):
    return render(request,'404.html',status=404)

def my_custom_page_not_found_view(request,exception):
    return render(request,'500.html',status=500)

def home(request):
    return redirect("/list_accounts/")

def list_accounts(request):
    sort = request.GET.get("sorted", "")
    limit_param = request.GET.get("limit", 10)
    users = list(User.objects.all())
    
    if limit_param:
        if (int(limit_param) <= len(users)) and (int(limit_param) >= 1):
            limit = int(limit_param)

    data = []
    for user in users:
        data.append({'user': user})
    
    ctx = {'users': data[:limit], 'sorted': sort}
    return render(request, 'users.html', ctx)

def get_flag(request):
    password = request.GET.get("password", "")

    admin = User.objects.get(username="admin")

    if password == admin.password:
        return HttpResponse(FLAG)
    else:
        return HttpResponse("not good enough")

