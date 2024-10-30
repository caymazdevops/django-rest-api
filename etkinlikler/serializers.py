# etkinlikler/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Kategori, Etkinlik, Resim, Yorum, Favorite
from .models import UserProfile

class ResimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resim
        fields = ['id', 'resim']

class YorumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yorum
        fields = ['id','icerik', 'tarih']

class EtkinlikSerializer(serializers.ModelSerializer):
    resimler = ResimSerializer(many=True, read_only=True)
    yorumlar = YorumSerializer(many=True, read_only=True)
    kategori_isim = serializers.CharField(source='kategori.isim', read_only=True)  # Kategori ismini alıyoruz
    
    class Meta:
        model = Etkinlik
        fields = ['id','isim', 'icerik', 'tarih', 'baslangic_tarihi', 'bitis_tarihi', 'saat', 'konum', 'ucretli_mi', 'resimler', 'yorumlar', 'kategori_isim']

class KategoriSerializer(serializers.ModelSerializer):
    etkinlikler = EtkinlikSerializer(many=True, read_only=True)
    
    class Meta:
        model = Kategori
        fields = ['id','isim', 'etkinlikler']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_image']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        user.set_password(validated_data['password'])  # Şifreyi hash’le
        user.save()
        return user
        

class FavoriteSerializer(serializers.ModelSerializer):
    etkinlik = EtkinlikSerializer()  # İlişkili etkinliği göster

    class Meta:
        model = Favorite
        fields = ['id', 'etkinlik']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user