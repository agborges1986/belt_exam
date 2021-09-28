from django.db import models
import re
import bcrypt
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import datetime

#Model and manager for User model

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errores = {}
        if len(User.objects.filter(username=postData['username'])) > 0:
            errores['existe'] = "Usuario ya registrado"
        else:
            #Valido el nombre
            if len(postData['name']) < 3:
                errores['name'] = "Nombre debe ser al menos 3 caracteres"
            #Valido el username
            if len(postData['username']) < 3:
                errores['username'] = "Username debe ser al menos 3 caracteres"
            #Valido tamaño de password
            if len(postData['password']) < 9:
                errores['password'] = "Password debe ser mayor a 8 caracteres"
            if postData['password'] != postData['password2']:
                errores['password'] = "Password no son iguales"
        return errores

    def encriptar(self, password):
        password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return password

    def validar_login(self, postData, usuario ):
        errores = {}
        if len(usuario) > 0:
            pw_given = postData['password']
            pw_hash = usuario[0].password

            if bcrypt.checkpw(pw_given.encode(), pw_hash.encode()) is False:
                errores['pass_incorrecto'] = "password es incorrecto"
        else:
            errores['usuario_invalido'] = "Usuario no existe"
        return errores

class User(models.Model):
    #id = models.AutoField(db_column='user_id',primary_key=True)
    name = models.CharField(max_length=40)
    username = models.CharField(max_length=40)
    #email = models.CharField(max_length=40)
    password = models.CharField(max_length=255)
    #rol = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class TripManager(models.Manager):
    def basic_validator(self, postData):
        today = make_aware(timezone.now().today())

        errores = {}
        if len(postData['destination']) == 0:
            errores['destination'] = "Destination field cannot be empty"

        if len(postData['description']) == 0:
            errores['description'] = "Description field cannot be empty"

        if len(postData['start_date']) == 0:
            errores['start_date'] = "Starting travel date field cannot be empty"
            if len(postData['end_date']) == 0:
                errores['end_date'] = "Ending travel date field cannot be empty"
        else:
            start_date = make_aware(datetime.strptime(postData['start_date'], '%Y-%m-%d'))
            if start_date <= today:
                errores['start_date'] = "The starting date must be in the future"

            if len(postData['end_date']) == 0:
                errores['end_date'] = "Ending travel date field cannot be empty"
            else:
                end_date = make_aware(datetime.strptime(postData['end_date'], '%Y-%m-%d'))
                if end_date <= start_date:
                    errores['end_date'] = "Ending travel date field cannot be before the starting date"

        return errores

class Trip(models.Model):
    creator = models.ForeignKey(User, related_name="creator", on_delete=models.CASCADE)
    destination = models.CharField(max_length=40)
    description = models.CharField(max_length=200, default="")
    start_date = models.DateField()
    end_date = models.DateField()
    joined_user = models.ManyToManyField(User, related_name="join_users", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()

