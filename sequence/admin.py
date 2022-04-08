from django.contrib import admin

from .models import Sequence, Alignment
# Register your models here.

admin.site.register(Sequence)
admin.site.register(Alignment)
