from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from . models import *
import bcrypt

# Create your views here.
def reg_log(request):
    return render(request, 'registro_login.html')



def inicio(request):
    usuario = User.objects.filter(username=request.POST['username'])
    errores = User.objects.validar_login(request.POST, usuario)

    if len(errores) > 0:
        for key, msg in errores.items():
            messages.error(request, msg)
        return redirect('/')
    else:
        request.session['id'] = usuario[0].id
        return redirect("/travels")

def registro(request):
    #validacion de parametros
    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, msg in errors.items():
            messages.error(request, msg)
        return redirect('/')
    else:
        #encriptar password
        password = User.objects.encriptar(request.POST['password'])
        decode_hash_pw = password.decode('utf-8')
        #crear usuario
        user = User.objects.create(
        name=request.POST['name'],
        username=request.POST['username'],
        password=decode_hash_pw,
        )
        request.session['id'] = user.id
    return redirect("/travels")

def login(request):
    return HttpResponse('login')

def home(request):
    reg_user = User.objects.get(id=request.session['id'])
    trips = Trip.objects.filter(joined_user=User.objects.get(id=request.session['id']))
    other_trips = Trip.objects.exclude(joined_user=User.objects.get(id=request.session['id']))
    context={
        'trips':trips,
        'active_user': reg_user,
        'other_trips':other_trips,
    }
    return render(request,'home.html',context)

def destination_id(request,id):
    trip=Trip.objects.get(id=id)
    context={
        'trip':trip,
    }
    return render(request, 'destination.html',context)


def destination_add(request):
    return render(request, 'add_trip.html')


def succes_add(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['id'])
        destination = request.POST['destination']
        description = request.POST['description']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        errors = Trip.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, msg in errors.items():
                messages.error(request, msg)
            return redirect('travels/add')
        else:
            #Pongo al usuario creador como unido al viaje
            trip=Trip.objects.create(destination=destination, description=description, start_date=start_date, end_date=end_date,creator=user)
            trip.joined_user.add(User.objects.get(id=request.session['id']))
            return redirect("/travels")


def join_trip(request,id):
    #Para unir al Usuario en un viaje
    trip=Trip.objects.get(id=id)
    trip.joined_user.add(User.objects.get(id=request.session['id']))
    return redirect("/travels")

def logout(request):
    request.session.flush()
    return redirect('/')