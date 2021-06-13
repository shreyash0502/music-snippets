from django.views import generic
from django import forms
from .models import Album, Song
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']


class IndexView2(generic.ListView):
    template_name = 'music/index2.html'
    context_object_name = 'songs'

    def get_queryset(self):
        return Song.objects.filter(user=self.request.user).order_by('-is_favorite')


class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = 'music:login_user'
    template_name = 'music/index.html'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return render(self.request, 'music/login.html')
        else:
            return Album.objects.filter(user=self.request.user).order_by('-is_favorite')

    def get_context_data(self):
        # else:
        #    return Album.objects.filter(user=self.request.user).order_by('-is_favorite')
        albums = Album.objects.filter(user=self.request.user).order_by('-is_favorite')
        song_results = Song.objects.filter(user=self.request.user).order_by('-is_favorite')
        query = self.request.GET.get("q")
        if query:
            albums = albums.filter(
                Q(album_title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()
            song_results = song_results.filter(
                Q(song_title__icontains=query) |
                Q(album__album_title__icontains=query) |
                Q(album__artist__icontains=query)
            ).distinct()
            return {'all_albums': albums, 'songs': song_results, }
        else:
            return {'all_albums': albums}


class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'
    # context_object_name = 'all_songs'

    # def get_queryset(self):
    #     album = Album.objects.get(pk=self.kwargs['pk'])
    #     songs = album.song_set.all()
    #     return {'all_songs': songs}


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'music/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # albums = Album.objects.filter(user=request.user)
                return redirect(reverse('music:index'))
                # return render(request, 'music/index.html', {'all_albums': albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')


def favourite_song(request,  album_pk, song_id):
    album = get_object_or_404(Album, pk=album_pk)
    song = album.song_set.get(pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return redirect(reverse('music:detail', kwargs={'pk': album_pk}))


def favourite_song_in_index(request,  album_pk, song_id):
    album = get_object_or_404(Album, pk=album_pk)
    song = album.song_set.get(pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favourite_album(request, album_id):
    # album = Album.objects.get(pk=album_id)
    # album.is_favorite = not album.is_favorite
    # album.save()
    # albums = Album.objects.filter(user=request.user)
    # return render(request, 'music/index.html', {'albums': albums})
    album = get_object_or_404(Album, pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


class AlbumCreate(CreateView):
    model = Album
    fields = ['user', 'artist', 'album_title', 'genre', 'album_logo']

    # fields['user'].widget.attrs['readonly'] = True
    def get_form(self, *args, **kwargs):
        form = super(AlbumCreate, self).get_form(*args, **kwargs)
        # form.fields['user'].required = False
        form.fields['user'].initial = self.request.user
        # form.fields['user'].widget.attrs = {'readonly': 'readonly'}
        form.fields['user'].widget.attrs['hidden'] = True
        return form


class SongCreate(CreateView):
    model = Song
    fields = ['user', 'album', 'audio_file', 'song_title']

    # def get_queryset(self):
    #     song = Song.objects.get(pk=self.kwargs['pk'])
    #     song.audio_file = request.FILES['audio_file']
    #     file_type = song.audio_file.url.split('.')[-1]
    #     file_type = file_type.lower()
    #     if file_type not in AUDIO_FILE_TYPES:
    #         context = {
    #             'album': song.album,
    #             'error_message': "Invalid file_type",
    #             }
    #     else:
    #         context = {'album': song.album}
    #     extra_context = context
    def get_form(self, *args, **kwargs):
        form = super(SongCreate, self).get_form(*args, **kwargs)
        form.fields['album'].queryset = Album.objects.filter(user=self.request.user)
        form.fields['user'].initial = self.request.user
        form.fields['album'].initial = Album.objects.get(pk=self.kwargs['pk'])
        form.fields['user'].widget.attrs['hidden'] = True
        return form

    # def get_initial(self):
    #     album = Album.objects.get(pk=self.kwargs['pk'])
    #     user = album.user
    #     return {'album': album, 'user': user}


class SongAdd(CreateView):
    model = Song
    fields = ['user', 'album', 'audio_file', 'song_title']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     albums = Album.objects.filter(user=self.request.user)
    #     # instance = kwargs.get("instance")
    #     self.fields['album'].queryset = albums
    # def get_queryset(self, *args, **kwargs):
    #     self.fields['album'].queryset = Album.objects.filter(user=self.request.user)
    #     return self.fields
    def get_form(self, *args, **kwargs):
        form = super(SongAdd, self).get_form(*args, **kwargs)
        form.fields['user'].initial = self.request.user
        form.fields['user'].widget.attrs['hidden'] = True
        form.fields['album'].queryset = Album.objects.filter(user=self.request.user)
        return form


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['user', 'artist', 'album_title', 'genre', 'album_logo']

    def get_form(self, *args, **kwargs):
        form = super(AlbumUpdate, self).get_form(*args, **kwargs)
        form.fields['user'].widget.attrs['hidden'] = True
        return form


class AlbumDelete(DeleteView):
    model = Album
    # the following line of code determines the page where the user is redirected to, on successful deletion of album
    success_url = reverse_lazy('music:index')


class SongDelete(DeleteView):
    model = Song

    # the following line of code determines the page where the user is redirected to, on successful deletion of album
    def get_success_url(self):
        return reverse_lazy('music:detail', kwargs={'pk': self.object.album_id})


class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # cleaned and normalized data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # to reset password: user.set_password(password) user.save()
            user.set_password(password)
            user.save()

            # returns User objects if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('music:index')

        return render(request, self.template_name, {'form': form})

