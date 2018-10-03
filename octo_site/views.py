from django.shortcuts import render,redirect
from octo_site.models import *
from django.http import HttpResponseRedirect
from octo_site.forms import *
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import mysql.connector
import sys
from octo_site.db_conf import pull_data
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
# Create your views here
def log_in(request):

    print("loging doging")
    user = None
    try:
        user = authenticate(username=request.POST['user'], password=request.POST['password'])
    except:
        None
    if request.method == 'POST':
        if user is not None:
            request.session['username'] = user.username
            request.session['guest'] = True
            request.session['logged'] = True
            login(request, user)
        else:
            messages.warning(request,'Wrong credentials, please try again.')
        return redirect('index')
    else:
        return render(request, 'octo_site/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, password=password)
        user.save()
        print(user.username)
        messages.warning(request, 'Account Created.')
        return redirect('index')
    return render(request, 'octo_site/register.html')
def page_sensor(request):
    return render(request, 'octo_site/settings/sensor_page.html')
def page_venue(request):
    if request.method == 'POST':

        if request.POST['type'] == "room":
            if RoomForm(request.POST, request.FILES).is_valid():
                room = Room(room_name=request.POST['room_name'], branch_id=request.POST['branch_id'], header_img=request.FILES['header_img'])
                room.save()
        elif request.POST['type'] == "room_edit":
            room = Room.objects.filter(branch_id=request.POST['room_id'])
            room.room_name = request.POST['room_name']
            room.branch_id = request.POST['branch_id']
            room.save()
        elif request.POST['type'] == "room_delete":
            room = Room.objects.filter(room_id=request.POST['room_id'])
            room.delete()
        # -------------------- # -------------------- # -------------------- # --------------------
        elif request.POST['type'] == "branch":
            branch = Branch(name=request.POST['name'], address=request.POST['address'])
            branch.save()
        elif request.POST['type'] == "branch_edit":
            branch = Branch.objects.filter(branch_id=request.POST['branch_id'])
            branch.name=request.POST['name']
            branch.address=request.POST['address']
            branch.save()
        elif request.POST['type'] == "branch_delete":
            branch = Branch.objects.filter(branch_id=request.POST['branch_id'])
            branch.delete()

        return HttpResponseRedirect(reverse('page_venue'))
    return render(request, 'octo_site/settings/venue_page.html',
                  {"branches":Branch.objects.all(),"rooms":Room.objects.all(),"room_form":RoomForm()})
@csrf_exempt
def upload_process(request):
    print("waw ngaleng")
    return JsonResponse({'filename':"kapiha"})
def add_room(request):
    return render(request, 'octo_site/settings/venue_page.html')
def dashboard(request):
    return render(request,'octo_site/dashboard.html')
def signout(request):
    logout(request)
    return redirect('index')
def index(request):
    print("gago")
    return render(request,'octo_site/dashboard.html')
def sensor_data():
    return pull_data()

