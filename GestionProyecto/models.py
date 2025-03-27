from django.db import models

# Metodo "AbstractBaseUser" para crear tablas de usuarios personalizada y no usar el predeterminado de Django
# Metodo "BaseUserManager" permitirá definir métodos personalizados para la creación de usuarios.

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Para manejar la creacion de usuarios
class manageUsuario(BaseUserManager):
    
    def create_user(self, correo, nombre, apellido, password = None):
        
        if not correo:
            
            raise ValueError("Obligatorio Correo")
        
        user = self.model(
            correo=self.normalize_email(correo),
            nombre = nombre,
            apellido = apellido
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, correo, nombre, apellido, password = None):
        
        if not correo:
            raise ValueError("Obligatorio Correo")
        
        user = self.create_user(
            correo=self.normalize_email(correo),
            nombre = nombre,
            apellido = apellido,
            password=password,
        )
        
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    
    


# Creando la clase para usuarios personalizado y no usar el predeterminado de django
class Usuarios(AbstractBaseUser):
    
    correo = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'apellido']
    
    objects = manageUsuario()
    
    def __str__(self):
        return self.correo
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return self.is_superuser

class Proyectos(models.Model):
    
    id_proyecto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

class miembros_proyecto(models.Model):
    
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    
class categorias(models.Model):
    
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    
class categorias_proyecto(models.Model):
    
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE)
    id_categoria = models.ForeignKey(categorias, on_delete=models.CASCADE)
    indice = models.IntegerField()
    
class tareas(models.Model):
    
    OPCIONES_PRIORIDAD = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
    ]
    
    id_tarea = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    prioridad = models.CharField(max_length=5, choices=OPCIONES_PRIORIDAD)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    categoria = models.ForeignKey(categorias, on_delete=models.CASCADE)

class tareas_proyecto(models.Model):
    
    id_tarea = models.ForeignKey(tareas, on_delete=models.CASCADE)
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)