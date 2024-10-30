# etkinlikler/models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import date, time

class Kategori(models.Model):
    id = models.AutoField(primary_key=True)  # Otomatik artan birincil anahtar
    isim = models.CharField(max_length=100)

    def __str__(self):
        return self.isim

class Etkinlik(models.Model):
    id = models.AutoField(primary_key=True)
    kategori = models.ForeignKey(Kategori, related_name='etkinlikler', on_delete=models.CASCADE)
    isim = models.CharField(max_length=255)
    icerik = models.TextField()
    baslangic_tarihi = models.DateField(default=date.today)  # Etkinlik başlangıç tarihi
    bitis_tarihi = models.DateField(default=date.today)      # Etkinlik bitiş tarihi
    saat = models.TimeField(default=time(12))              # Etkinlik saati
    tarih = models.DateTimeField()
    konum = models.CharField(max_length=255)
    ucretli_mi = models.BooleanField(default=False)

    def __str__(self):
        return self.isim
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    etkinlik = models.ForeignKey(Etkinlik, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'etkinlik')  # Aynı etkinliği birden fazla kez favoriye eklemeyi önler

    def __str__(self):
        return f"{self.user.username} - {self.etkinlik.isim}"

class Resim(models.Model):
    id = models.AutoField(primary_key=True)
    etkinlik = models.ForeignKey(Etkinlik, related_name='resimler', on_delete=models.CASCADE)
    resim = models.ImageField(upload_to='etkinlik_resimleri/')

    def __str__(self):
        return f"{self.etkinlik.isim} Resmi"

class Yorum(models.Model):
    id = models.AutoField(primary_key=True)
    etkinlik = models.ForeignKey(Etkinlik, related_name='yorumlar', on_delete=models.CASCADE)
    icerik = models.TextField()
    tarih = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Yorum {self.etkinlik.isim} - {self.tarih}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  # Profil resmi

    def __str__(self):
        return self.user.username