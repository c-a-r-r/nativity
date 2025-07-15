# backend/users/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

# ——— Custom User Manager ———
class UsuarioManager(BaseUserManager):
    def create_user(self, usuario, email=None, password=None, **extra_fields):
        if not usuario:
            raise ValueError('Username (usuario) is required')
        user = self.model(usuario=usuario, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, usuario, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(usuario, email, password, **extra_fields)


# ——— Module ——— (maps to usuario_nivel)
class Module(models.Model):
    id     = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'usuario_nivel'
        managed  = False

    def __str__(self):
        return self.nombre


# ——— Role ——— (maps to usuario_grupo)
class Role(models.Model):
    id      = models.AutoField(primary_key=True)
    nombre  = models.CharField(max_length=100, unique=True)
    modules = models.ManyToManyField(
        Module,
        db_table='usuario_grupo_nivel',    # <-- your join table
        related_name='roles',
        blank=True,
    )

    class Meta:
        db_table = 'usuario_grupo'
        managed  = False

    def __str__(self):
        return self.nombre


# ——— Join table (if you need to customize it) ———
class RoleModule(models.Model):
    grupo  = models.ForeignKey(Role,   db_column='grupo_id', on_delete=models.CASCADE)
    nivel  = models.ForeignKey(Module, db_column='nivel_id', on_delete=models.CASCADE)

    class Meta:
        db_table  = 'usuario_grupo_nivel'
        managed   = False


# ——— User ——— (maps to usuario)
class Usuario(AbstractBaseUser, PermissionsMixin):
    id               = models.AutoField(primary_key=True)
    usuario          = models.CharField(max_length=45, unique=True)
    last_login       = models.DateTimeField(
       db_column='acceso_ultimo',
       null=True,
        blank=True,
    )
    password = models.CharField(max_length=128)
    grupo            = models.ForeignKey(Role,
                                         db_column='grupo_id',
                                         on_delete=models.SET_NULL,
                                         null=True,
                                         related_name='users')
    activo           = models.CharField(max_length=3,
                                        choices=[('NO','No'),('YES','Yes')],
                                        default='YES')
    nombre           = models.CharField(max_length=100, null=True, blank=True)
    u_first_name     = models.CharField(max_length=100, null=True, blank=True)
    u_last_name      = models.CharField(max_length=100, null=True, blank=True)
    email            = models.EmailField(null=True, blank=True)
    idioma           = models.CharField(max_length=15, default='ENGLISH')
    #acceso_ultimo    = models.DateTimeField(null=True, blank=True)
    acceso_intentos  = models.IntegerField(default=0)
    telefono_fijo    = models.CharField(max_length=50, null=True, blank=True)
    telefono_movil   = models.CharField(max_length=50, null=True, blank=True)
    comision         = models.DecimalField(max_digits=19,
                                           decimal_places=2,
                                           default=0.00)
    agent            = models.CharField(max_length=3,
                                        choices=[('NO','No'),('YES','Yes')],
                                        default='NO')

    # Django flags
    is_active        = models.BooleanField(default=True)
    is_staff         = models.BooleanField(default=False)

    USERNAME_FIELD   = 'usuario'
    REQUIRED_FIELDS  = []

    objects = UsuarioManager()

    class Meta:
        db_table = 'usuario'
        managed  = False

    def __str__(self):
        return self.usuario
    def get_full_name(self):
    # Adjust 'nombre' to your actual full name field
        return getattr(self, 'nombre', '') or getattr(self, 'username', '') or str(self)