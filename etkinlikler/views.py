# etkinlikler/views.py
from rest_framework import viewsets
from .models import Kategori, Etkinlik, Favorite
from .serializers import KategoriSerializer, EtkinlikSerializer, FavoriteSerializer
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer

class KategoriViewSet(viewsets.ModelViewSet):
    queryset = Kategori.objects.all()
    serializer_class = KategoriSerializer

class EtkinlikViewSet(viewsets.ModelViewSet):
    queryset = Etkinlik.objects.all()
    serializer_class = EtkinlikSerializer

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)  # Kullanıcı için JWT token'ları oluştur
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username})
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_favorites(request):
    user = request.user
    etkinlik_id = request.data.get('etkinlik_id')
    try:
        etkinlik = Etkinlik.objects.get(id=etkinlik_id)
        favorite, created = Favorite.objects.get_or_create(user=user, etkinlik=etkinlik)
        if created:
            return Response({"message": "Etkinlik favorilere eklendi."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Etkinlik zaten favorilerde."}, status=status.HTTP_200_OK)
    except Etkinlik.DoesNotExist:
        return Response({"error": "Etkinlik bulunamadı."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_favorites(request, etkinlik_id):
    user = request.user
    try:
        favorite = Favorite.objects.get(user=user, etkinlik_id=etkinlik_id)
        favorite.delete()
        return Response({"message": "Etkinlik favorilerden kaldırıldı."}, status=status.HTTP_204_NO_CONTENT)
    except Favorite.DoesNotExist:
        return Response({"error": "Bu etkinlik favorilerinizde değil."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_favorites(request):
    user = request.user
    favorites = Favorite.objects.filter(user=user)
    serializer = FavoriteSerializer(favorites, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def search_events(request):
    search_term = request.query_params.get('search_term', '').strip()  # Arama terimini al
    if search_term:
        etkinlikler = Etkinlik.objects.filter(isim__icontains=search_term)  # İsimde arama yap
    else:
        etkinlikler = Etkinlik.objects.all()  # Arama yoksa tüm etkinlikleri göster
    serializer = EtkinlikSerializer(etkinlikler, many=True)
    return Response(serializer.data)