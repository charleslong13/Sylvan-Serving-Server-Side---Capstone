from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from sylvanapi.views.auth import register_user, login_user
from rest_framework import routers
from sylvanapi.views.comments import CommentView
from sylvanapi.views.deck import DeckViewSet
from sylvanapi.views.event import EventView
from sylvanapi.views.playStyle import PlayStyleView
from sylvanapi.views.player import PlayerView


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'decks', DeckViewSet, 'deck')
router.register(r'players', PlayerView, 'player')
router.register(r'MyDeckList', PlayerView, 'MyDeckList')
router.register(r'playStyle', PlayStyleView, 'playStyle')
router.register(r'events', EventView, 'events')
router.register(r'comments', CommentView, 'comments')
urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
   
    
    
]
