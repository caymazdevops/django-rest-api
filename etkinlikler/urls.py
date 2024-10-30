# etkinlikler/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KategoriViewSet, EtkinlikViewSet
from .views import register, login
from .views import register, get_user_profile
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import add_to_favorites, remove_from_favorites, list_favorites, search_events
from .views import update_user_profile

router = DefaultRouter()
router.register(r'kategoriler', KategoriViewSet)
router.register(r'etkinlikler', EtkinlikViewSet)

urlpatterns = [
    path('', include(router.urls)),
     path('register/', register, name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token yenileme
    path('me/', get_user_profile, name='user_profile'),  # Yeni uç nokta
    path('favorites/', list_favorites, name='list_favorites'),
    path('favorites/add/', add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<int:etkinlik_id>/', remove_from_favorites, name='remove_from_favorites'),
    path('profile/update/', update_user_profile, name='update_user_profile'),
    path('search/', search_events, name='search_events'),
]