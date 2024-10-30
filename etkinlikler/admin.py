# etkinlikler/admin.py
from django.contrib import admin
from .models import Kategori, Etkinlik, Resim, Yorum

admin.site.register(Kategori)
admin.site.register(Etkinlik)
admin.site.register(Resim)
admin.site.register(Yorum)