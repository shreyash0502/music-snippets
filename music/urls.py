from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    # /music/
    path('', views.IndexView.as_view(), name='index'),
    # /music/songs/
    path('songs/', views.IndexView2.as_view(), name='songs'),
    # /music/register/
    path('register/', views.UserFormView.as_view(), name='register'),
    # /music/<pk>/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # music/1/favourite_album/
    path('<int:album_id>/favourite_album/', views.favourite_album, name='favourite_album'),
    # /music/<pk>/song-add/
    path('<int:pk>/song-add/', views.SongCreate.as_view(), name='song-add'),
    # /music/song/add/
    path('song/add/', views.SongAdd.as_view(), name='song2-add'),
    # /music/album/add/
    path('album/add/', views.AlbumCreate.as_view(), name='album-add'),
    # /music/album/2/
    path('album/<int:pk>/', views.AlbumUpdate.as_view(), name='album-update'),
    # /music/album/2/delete/
    path('<int:pk>/delete/', views.AlbumDelete.as_view(), name='album-delete'),
    # /music/1/delete-song/11/
    path('<int:album_pk>/delete-song/<int:pk>/', views.SongDelete.as_view(), name='delete-song'),
    # /music/1/favourite-song/11/
    path('<int:album_pk>/favourite-song/<int:song_id>/', views.favourite_song, name='favourite_song'),
    # /music/1/favourite-song/11/
    path('<int:album_pk>/favourite-song-in-index/<int:song_id>/', views.favourite_song_in_index, name='favourite_song_in_index'),
    # music/logout/
    path('logout/', views.logout_user, name='log-out'),
    # music/login/
    path('login_user/', views.login_user, name='login_user'),
]

