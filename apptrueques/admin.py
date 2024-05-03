from django.contrib import admin
from .models import Sucursal
from .models import Usuario
from .models import Publicacion
from .models import Comentario
from .models import Solicitud

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Sucursal)
admin.site.register(Publicacion)
admin.site.register(Comentario)
admin.site.register(Solicitud)