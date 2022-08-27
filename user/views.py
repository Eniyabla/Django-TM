from django.contrib import messages
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from TM import settings
from home.models import Setting, ContactMessage, SettingLang
from home.views import categoryTree
from place.models import Category, Comment, Images, Place, PlaceForm, ImageForm,  PlaceLanguage,wishist

from user.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm, PlaceUpdateForm
from user.models import UserProfile


@login_required(login_url='/login')
def index(request):
    category = Category.objects.all()
    setting = Setting.objects.all()
    default_language = settings.LANGUAGE_CODE[0:2]
    current_language = request.LANGUAGE_CODE[0:2]
    place_slider = Place.objects.all().order_by('-id')[:3]
    wishlist = wishist.objects.filter(user_id=request.user.id)
    wishlist1 = wishist.objects.filter(user_id=request.user.id)
    wishlistcount = wishlist.count()
    if default_language != current_language:
        wishlist = Place.objects.raw(
            'SELECT p.id,l.title,l.keyword,l.description,l.slug,p.image,p.city,p.country,p.location'
            ' FROM home_wishist as w'
            ' JOIN place_place as p'
            ' ON w.place_id=p.id'
            ' JOIN place_placelanguage as l'
            ' ON p.id=l.place_id'
            ' WHERE l.lang=%s and w.user_id=%s', [current_language, request.user.id])
        category = categoryTree(0, '', current_language)
        setting = SettingLang.objects.filter(lang=current_language)
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {
        'category': category,
        'profile': profile,
        'wishlist': wishlist,
        'wishlistcount': wishlistcount,
        'wishlist1': wishlist1
    }
    return render(request, 'UserProfile.html', context)


def loginForm(request):
    setting = Setting.objects.get(pk=1)
    default_language = settings.LANGUAGE_CODE[0:2]
    current_language = request.LANGUAGE_CODE[0:2]
    category = categoryTree(0, '', default_language)
    place_slider = Place.objects.all().order_by('-id')[:3]
    wishlist = wishist.objects.filter(user_id=request.user.id)
    wishlist1 = wishist.objects.filter(user_id=request.user.id)
    wishlistcount = wishlist.count()
    if default_language != current_language:
        wishlist = Place.objects.raw(
            'SELECT p.id,l.title,l.keyword,l.description,l.slug,p.image,p.city,p.country,p.location'
            ' FROM home_wishist as w'
            ' JOIN place_place as p'
            ' ON w.place_id=p.id'
            ' JOIN place_placelanguage as l'
            ' ON p.id=l.place_id'
            ' WHERE l.lang=%s and w.user_id=%s', [current_language, request.user.id])
        category = categoryTree(0, '', current_language)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, 'Wrong username or password, try again')
            return HttpResponseRedirect('/login')
    context = {
        'setting': setting,
        'category': category,
        'wishlist': wishlist,
        'wishlistcount': wishlistcount,
        'wishlist1': wishlist1
    }

    return render(request, 'login_form.html', context)


def signUpForm(request):
    default_language = settings.LANGUAGE_CODE[0:2]
    current_language = request.LANGUAGE_CODE[0:2]
    category = categoryTree(0, '', default_language)
    place_slider = Place.objects.all().order_by('-id')[:3]
    wishlist = wishist.objects.filter(user_id=request.user.id)
    wishlist1 = wishist.objects.filter(user_id=request.user.id)
    wishlistcount = wishlist.count()
    if default_language != current_language:
        wishlist = Place.objects.raw(
            'SELECT p.id,l.title,l.keyword,l.description,l.slug,p.image,p.city,p.country,p.location'
            ' FROM home_wishist as w'
            ' JOIN place_place as p'
            ' ON w.place_id=p.id'
            ' JOIN place_placelanguage as l'
            ' ON p.id=l.place_id'
            ' WHERE l.lang=%s and w.user_id=%s', [current_language, request.user.id])
        category = categoryTree(0, '', current_language)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            curr_user = request.user
            data = UserProfile()
            data.user_id = curr_user.id
            data.image = 'images/user/default.jpg'
            data.save()
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/register')
    setting = Setting.objects.get(pk=1)
    form = SignUpForm()
    context = {
        'setting': setting,
        'category': category,
        'form': form,
        'wishlist': wishlist,
        'wishlistcount': wishlistcount,
        'wishlist1': wishlist1
    }
    return render(request, 'signUp_Form.html', context)


@login_required(login_url='/login')
def user_update(request):
    default_language = settings.LANGUAGE_CODE[0:2]
    current_language = request.LANGUAGE_CODE[0:2]
    category = categoryTree(0, '', default_language)
    place_slider = Place.objects.all().order_by('-id')[:3]
    wishlist = wishist.objects.filter(user_id=request.user.id)
    wishlist1 = wishist.objects.filter(user_id=request.user.id)
    wishlistcount = wishlist.count()
    if default_language != current_language:
        wishlist = Place.objects.raw(
            'SELECT p.id,l.title,l.keyword,l.description,l.slug,p.image,p.city,p.country,p.location'
            ' FROM home_wishist as w'
            ' JOIN place_place as p'
            ' ON w.place_id=p.id'
            ' JOIN place_placelanguage as l'
            ' ON p.id=l.place_id'
            ' WHERE l.lang=%s and w.user_id=%s', [current_language, request.user.id])
        category = categoryTree(0, '', current_language)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been succesfully updated')
            return HttpResponseRedirect('/user')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form,
            'wishlist': wishlist,
            'wishlistcount': wishlistcount,
            'wishlist1': wishlist1
        }
        return render(request, 'user_update.html', context)


@login_required(login_url='/login')
def user_password(request):
    default_language = settings.LANGUAGE_CODE[0:2]
    current_language = request.LANGUAGE_CODE[0:2]
    category = categoryTree(0, '', default_language)
    place_slider = Place.objects.all().order_by('-id')[:3]
    wishlist = wishist.objects.filter(user_id=request.user.id)
    wishlist1 = wishist.objects.filter(user_id=request.user.id)
    wishlistcount = wishlist.count()
    if default_language != current_language:
        wishlist = Place.objects.raw(
            'SELECT p.id,l.title,l.keyword,l.description,l.slug,p.image,p.city,p.country,p.location'
            ' FROM home_wishist as w'
            ' JOIN place_place as p'
            ' ON w.place_id=p.id'
            ' JOIN place_placelanguage as l'
            ' ON p.id=l.place_id'
            ' WHERE l.lang=%s and w.user_id=%s', [current_language, request.user.id])
        category = categoryTree(0, '', current_language)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your account has been succesfully updated')
            return HttpResponseRedirect('/user')
        else:
            messages.success(request, 'Wrong:' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:

        form = PasswordChangeForm(request.user)
        context = {
            'category': category,
            'form': form,
            'wishlist': wishlist,
            'wishlistcount': wishlistcount,
            'wishlist1': wishlist1
        }
        return render(request, 'user_password.html', context)


@login_required(login_url='/login')
def user_comments(request):
    curr_user = request.user
    comments = Comment.objects.filter(user_id=curr_user.id)
    wishlist = wishist.objects.filter(user_id=request.user.id)
    wishlist1 = wishist.objects.filter(user_id=request.user.id)
    wishlistcount = wishlist.count()
    default_language = settings.LANGUAGE_CODE[0:2]
    current_language = request.LANGUAGE_CODE[0:2]
    category=categoryTree(0,'',default_language)
    if default_language != current_language:
        wishlist = Place.objects.raw(
            'SELECT p.id,l.title,l.keyword,l.description,l.slug,p.image,p.city,p.country,p.location'
            ' FROM home_wishist as w'
            ' JOIN place_place as p'
            ' ON w.place_id=p.id'
            ' JOIN place_placelanguage as l'
            ' ON p.id=l.place_id'
            ' WHERE l.lang=%s and w.user_id=%s', [current_language, request.user.id])
        category=categoryTree(0,'',current_language)
    context = {
        'category': category,
        'comments': comments,
        'wishlist': wishlist,
        'wishlistcount': wishlistcount,
        'wishlist1': wishlist1
    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')
def user_places(request):
    default_language = settings.LANGUAGE_CODE[0:2]
    current_language = request.LANGUAGE_CODE[0:2]
    category = categoryTree(0, '', default_language)
    place_slider = Place.objects.all().order_by('-id')[:3]
    wishlist = wishist.objects.filter(user_id=request.user.id)
    wishlist1 = wishist.objects.filter(user_id=request.user.id)
    wishlistcount = wishlist.count()
    places = Place.objects.filter(user_id=request.user.id)
    if default_language != current_language:
        wishlist = Place.objects.raw(
            'SELECT p.id,l.title,l.keyword,l.description,l.slug,p.image,p.city,p.country,p.location'
            ' FROM home_wishist as w'
            ' JOIN place_place as p'
            ' ON w.place_id=p.id'
            ' JOIN place_placelanguage as l'
            ' ON p.id=l.place_id'
            ' WHERE l.lang=%s and w.user_id=%s', [current_language, request.user.id])
        category = categoryTree(0, '', current_language)
        places=Place.objects.raw('SELECT p.id,l.title,l.keyword,l.description,l.slug,p.image,p.city,p.country,p.location'
                                         ' FROM place_place as p'
                                         ' INNER JOIN place_placelanguage as l'
                                         ' ON p.id=l.place_id'
                                         ' WHERE lang=%s', [current_language])
    # curr_user = request.user

    context = {
        'category': category,
        'places': places,
        'wishlist': wishlist,
        'wishlistcount': wishlistcount,
        'wishlist1': wishlist1
    }
    return render(request, 'user_places.html', context)


@login_required(login_url='/login')
def user_wishlist(request):
    default_language = settings.LANGUAGE_CODE[0:2]
    current_language = request.LANGUAGE_CODE[0:2]
    category = categoryTree(0, '', default_language)
    wishlist = wishist.objects.filter(user_id=request.user.id)
    wishlist1 = wishist.objects.filter(user_id=request.user.id)
    wishlistcount = wishlist.count()
    if default_language != current_language:
        wishlist = Place.objects.raw(
            'SELECT p.id,l.title,l.keyword,l.description,l.slug,p.image,p.city,p.country,p.location'
            ' FROM home_wishist as w'
            ' JOIN place_place as p'
            ' ON w.place_id=p.id'
            ' JOIN place_placelanguage as l'
            ' ON p.id=l.place_id'
            ' WHERE l.lang=%s and w.user_id=%s', [current_language, request.user.id])
        category = categoryTree(0, '', current_language)
        setting = SettingLang.objects.filter(lang=current_language)
    places = wishist.objects.filter(user_id=request.user.id)
    context = {
        'category': category,
        'places': places,
        'wishlist': wishlist,
        'wishlistcount': wishlistcount,
        'wishlist1': wishlist1
    }
    return render(request, 'user_wishlist.html', context)


@login_required(login_url='/login')
def user_delete_comment(request, id):
    category = Category.objects.all()
    curr_user = request.user
    comments = Comment.objects.filter(id=id, user_id=curr_user.id).delete()
    messages.success(request, 'comment is deleted')
    return HttpResponseRedirect('/user/comments')


@login_required(login_url='/login')
def user_delete_place(request, id):
    default_language = settings.LANGUAGE_CODE[0:2]
    current_language = request.LANGUAGE_CODE[0:2]
    category = categoryTree(0, '', default_language)
    wishlist = wishist.objects.filter(user_id=request.user.id)
    wishlist1 = wishist.objects.filter(user_id=request.user.id)
    wishlistcount = wishlist.count()
    if default_language != current_language:
        wishlist = Place.objects.raw(
            'SELECT p.id,l.title,l.keyword,l.description,l.slug,p.image,p.city,p.country,p.location'
            ' FROM home_wishist as w'
            ' JOIN place_place as p'
            ' ON w.place_id=p.id'
            ' JOIN place_placelanguage as l'
            ' ON p.id=l.place_id'
            ' WHERE l.lang=%s and w.user_id=%s', [current_language, request.user.id])
        category = categoryTree(0, '', current_language)
        setting = SettingLang.objects.filter(lang=current_language)
    curr_user = request.user
    places = Place.objects.filter(id=id, user_id=curr_user.id).delete()
    messages.success(request, 'place is deleted')
    return HttpResponseRedirect('/user/places')


from django.utils.text import slugify
@login_required(login_url='/login')
def user_add_place(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST, request.FILES)
        if form.is_valid():
            data = Place()
            data.image = form.cleaned_data['image']
            data.title = form.cleaned_data['title']
            data.slug = slugify(form.cleaned_data['title'])
            data.keyword = form.cleaned_data['keyword']
            data.description = form.cleaned_data['description']
            data.detail = form.cleaned_data['detail']
            data.city = form.cleaned_data['city']
            data.country = form.cleaned_data['country']
            data.location = form.cleaned_data['location']
            data.user_id = request.user.id
            data.category_id = form.cleaned_data['category'].id
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, 'Your item has been successfully inserted.Thanks!')
            return HttpResponseRedirect('/user/places')
    category = Category.objects.all()
    setting = Setting.objects.all()
    default_language = settings.LANGUAGE_CODE[0:2]
    current_language = request.LANGUAGE_CODE[0:2]
    place_slider = Place.objects.all().order_by('-id')[:3]
    wishlist = wishist.objects.filter(user_id=request.user.id)
    wishlist1 = wishist.objects.filter(user_id=request.user.id)
    wishlistcount = wishlist.count()
    if default_language != current_language:
        wishlist = Place.objects.raw(
            'SELECT p.id,l.title,l.keyword,l.description,l.slug,p.image,p.city,p.country,p.location'
            ' FROM home_wishist as w'
            ' JOIN place_place as p'
            ' ON w.place_id=p.id'
            ' JOIN place_placelanguage as l'
            ' ON p.id=l.place_id'
            ' WHERE l.lang=%s and w.user_id=%s', [current_language, request.user.id])
        category = categoryTree(0, '', current_language)
        setting = SettingLang.objects.filter(lang=current_language)
    # setting = Setting.objects.get(pk=1)
    form = PlaceForm
    form1 = ImageForm
    category = Category.objects.all()
    context = {'category': category, 'form': form, 'form1': form1, 'setting': setting,'wishlist':wishlist,
               'wishlistcount':wishlistcount,
               'wishlist1':wishlist1}

    return render(request, 'user_add_place.html', context)


@login_required(login_url='/login')
def user_update_place(request, id):
    default_language = settings.LANGUAGE_CODE[0:2]
    current_language = request.LANGUAGE_CODE[0:2]
    category = categoryTree(0, '', default_language)
    place_slider = Place.objects.all().order_by('-id')[:3]
    wishlist = wishist.objects.filter(user_id=request.user.id)
    wishlist1 = wishist.objects.filter(user_id=request.user.id)
    wishlistcount = wishlist.count()
    if default_language != current_language:
        wishlist = Place.objects.raw(
            'SELECT p.id,l.title,l.keyword,l.description,l.slug,p.image,p.city,p.country,p.location'
            ' FROM home_wishist as w'
            ' JOIN place_place as p'
            ' ON w.place_id=p.id'
            ' JOIN place_placelanguage as l'
            ' ON p.id=l.place_id'
            ' WHERE l.lang=%s and w.user_id=%s', [current_language, request.user.id])
        category = categoryTree(0, '', current_language)
    if request.method == 'POST':
        place = Place.objects.get(id=id)
        user_form = PlaceUpdateForm(request.POST, request.FILES, instance=place)
        # profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid():  # and profile_form.is_valid():
            user_form.save()
            # profile_form.save()
            messages.success(request, 'Your item has been succesfully updated')
            return HttpResponseRedirect('/user/places')
    else:
        place = Place.objects.get(id=id)
        user_form = PlaceUpdateForm(instance=place)
        # profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'user_form': user_form,
            'wishlist': wishlist,
            'wishlistcount': wishlistcount,
            'wishlist1': wishlist1
        }
        return render(request, 'user_update_place.html', context)


@login_required(login_url='/login')
def user_add_image(request, id):
    images = Images.objects.filter(place_id=id)
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = Images()
            data.image = form.cleaned_data['image']
            data.title = form.cleaned_data['title']
            if (data.image):
                data.place_id = id
                data.save()
            messages.success(request, 'Your image has been successfully inserted.Thanks!')
            return HttpResponseRedirect(url)
    setting = Setting.objects.all()
    default_language = settings.LANGUAGE_CODE[0:2]
    current_language = request.LANGUAGE_CODE[0:2]
    category = categoryTree(0, '', default_language)
    place_slider = Place.objects.all().order_by('-id')[:3]
    wishlist = wishist.objects.filter(user_id=request.user.id)
    wishlist1 = wishist.objects.filter(user_id=request.user.id)
    wishlistcount = wishlist.count()
    if default_language != current_language:
        wishlist = Place.objects.raw(
            'SELECT p.id,l.title,l.keyword,l.description,l.slug,p.image,p.city,p.country,p.location'
            ' FROM home_wishist as w'
            ' JOIN place_place as p'
            ' ON w.place_id=p.id'
            ' JOIN place_placelanguage as l'
            ' ON p.id=l.place_id'
            ' WHERE l.lang=%s and w.user_id=%s', [current_language, request.user.id])
        category = categoryTree(0, '', current_language)
        setting = SettingLang.objects.filter(lang=current_language)

    place = Place.objects.get(id=id)
    form = ImageForm
    context = {'category': category,
               'form': form,
               'images': images,
               'setting': setting,
               'place': place,
               'wishlist': wishlist,
               'wishlistcount': wishlistcount,
               'wishlist1': wishlist1
               }
    return render(request, 'user_add_image.html', context)


@login_required(login_url='/login')
def user_delete_image(request, place_id, image_id):
    default_language = settings.LANGUAGE_CODE[0:2]
    current_language = request.LANGUAGE_CODE[0:2]
    category = categoryTree(0, '', default_language)
    wishlist = wishist.objects.filter(user_id=request.user.id)
    wishlist1 = wishist.objects.filter(user_id=request.user.id)
    wishlistcount = wishlist.count()
    if default_language != current_language:
        wishlist = Place.objects.raw(
            'SELECT p.id,l.title,l.keyword,l.description,l.slug,p.image,p.city,p.country,p.location'
            ' FROM home_wishist as w'
            ' JOIN place_place as p'
            ' ON w.place_id=p.id'
            ' JOIN place_placelanguage as l'
            ' ON p.id=l.place_id'
            ' WHERE l.lang=%s and w.user_id=%s', [current_language, request.user.id])
        category = categoryTree(0, '', current_language)
        setting = SettingLang.objects.filter(lang=current_language)
    image = Images.objects.filter(id=image_id, place_id=place_id).delete()
    messages.success(request, 'image is deleted')
    return HttpResponseRedirect("/user/add_image/"+image.place_id)


def logoutF(request):
    logout(request)
    default_language = settings.LANGUAGE_CODE[0:2]
    current_language = request.LANGUAGE_CODE[0:2]
    category = categoryTree(0, '', default_language)
    wishlist = wishist.objects.filter(user_id=request.user.id)
    wishlist1 = wishist.objects.filter(user_id=request.user.id)
    wishlistcount = wishlist.count()
    if default_language != current_language:
        wishlist = Place.objects.raw(
            'SELECT p.id,l.title,l.keyword,l.description,l.slug,p.image,p.city,p.country,p.location'
            ' FROM home_wishist as w'
            ' JOIN place_place as p'
            ' ON w.place_id=p.id'
            ' JOIN place_placelanguage as l'
            ' ON p.id=l.place_id'
            ' WHERE l.lang=%s and w.user_id=%s', [current_language, request.user.id])
        category = categoryTree(0, '', current_language)
        setting = SettingLang.objects.filter(lang=current_language)
        url='/'+current_language
    url='/'+default_language
    return HttpResponseRedirect(url)


@login_required(login_url='/login')
def user_messages(request):
    curr_user = request.user
    wishlist = wishist.objects.filter(user_id=request.user.id)
    wishlist1 = wishist.objects.filter(user_id=request.user.id)
    wishlistcount = wishlist.count()
    default_language = settings.LANGUAGE_CODE[0:2]
    current_language = request.LANGUAGE_CODE[0:2]
    category=categoryTree(0,'',default_language)
    if default_language != current_language:
        category=categoryTree(0,'',current_language)
        wishlist = Place.objects.raw(
            'SELECT p.id,l.title,l.keyword,l.description,l.slug,p.image,p.city,p.country,p.location'
            ' FROM home_wishist as w'
            ' JOIN place_place as p'
            ' ON w.place_id=p.id'
            ' JOIN place_placelanguage as l'
            ' ON p.id=l.place_id'
            ' WHERE l.lang=%s and w.user_id=%s', [current_language, request.user.id])
    messages = ContactMessage.objects.filter(email=curr_user.email)
    context = {
        'category': category,
        'messages': messages,
        'wishlist': wishlist,
        'wishlistcount': wishlistcount,
        'wishlist1': wishlist1
    }
    return render(request, 'user_messages.html', context)


@login_required(login_url='/login')
def likeplace(request, id):
    url = request.META.get('HTTP_REFERER')
    default_language = settings.LANGUAGE_CODE[0:2]
    current_language = request.LANGUAGE_CODE[0:2]
    if request.method == 'POST':
        if wishist.objects.filter(user_id=request.user.id,place_id=id):
            wishist.objects.filter(user_id=request.user.id, place_id=id).delete()
        else:
            data = wishist()
            data.place_id = id
            data.user_id = request.user.id
            data.isLike = not (data.isLike)
            data.save()
    wishlist = wishist.objects.filter(user_id=request.user.id)
    wishlist1 = wishist.objects.filter(user_id=request.user.id)
    wishlistcount = wishlist.count()
    default_language = settings.LANGUAGE_CODE[0:2]
    current_language = request.LANGUAGE_CODE[0:2]
    if default_language != current_language:
        wishlist = Place.objects.raw(
            'SELECT p.id,l.title,l.keyword,l.description,l.slug,p.image,p.city,p.country,p.location'
            ' FROM home_wishist as w'
            ' JOIN place_place as p'
            ' ON w.place_id=p.id'
            ' JOIN place_placelanguage as l'
            ' ON p.id=l.place_id'
            ' WHERE l.lang=%s and w.user_id=%s', [current_language, request.user.id])
        return HttpResponseRedirect('/'+current_language)
    return HttpResponseRedirect('/')



@login_required(login_url='/login')
def user_add_place_multilang(request, id):
    if request.method == 'POST':
        url = request.META.get('HTTP_REFERER')
        form1 = PlaceLangForm(request.POST)
        if form1.is_valid():
            data = PlaceLanguage()
            data.title = form1.cleaned_data['title']
            data.lang = form1.cleaned_data['lang']
            data.slug = slugify(form.cleaned_data['title'])
            data.keyword = form1.cleaned_data['keyword']
            data.description = form1.cleaned_data['description']
            data.detail = form1.cleaned_data['detail']
            data.place_id = id
            if (data.title and data.lang):
                data.save()
            messages.success(request, 'Your item has been successfully inserted.Thanks!')
            return HttpResponseRedirect(url)

    setting = Setting.objects.all()
    default_language = settings.LANGUAGE_CODE[0:2]
    current_language = request.LANGUAGE_CODE[0:2]
    category = categoryTree(0, '', default_language)
    wishlist = wishist.objects.filter(user_id=request.user.id)
    wishlist1 = wishist.objects.filter(user_id=request.user.id)
    wishlistcount = wishlist.count()
    if default_language != current_language:
        wishlist = Place.objects.raw(
            'SELECT p.id,l.title,l.keyword,l.description,l.slug,p.image,p.city,p.country,p.location'
            ' FROM home_wishist as w'
            ' JOIN place_place as p'
            ' ON w.place_id=p.id'
            ' JOIN place_placelanguage as l'
            ' ON p.id=l.place_id'
            ' WHERE l.lang=%s and w.user_id=%s', [current_language, request.user.id])
        category = categoryTree(0, '', current_language)
        setting = SettingLang.objects.filter(lang=current_language)
    form1 = PlaceLangForm
    place = Place.objects.get(pk=id)
    places = PlaceLanguage.objects.filter(place_id=id)
    langcount = Language.objects.all().count() - 1
    placecount = places.count()
    context = {'category': category,
               'form1': form1,
               'setting': setting,
               'place': place,
               'places': places,
               'langcount': langcount,
               'placecount': placecount,
               'wishlist': wishlist,
               'wishlistcount': wishlistcount,
               'wishlist1': wishlist1
               }

    return render(request, 'user_add_place_multi.html', context)


@login_required(login_url='/login')
def user_update_multilang_place(request, place_id, id):
    default_language = settings.LANGUAGE_CODE[0:2]
    current_language = request.LANGUAGE_CODE[0:2]
    category = categoryTree(0, '', default_language)
    wishlist = wishist.objects.filter(user_id=request.user.id)
    wishlist1 = wishist.objects.filter(user_id=request.user.id)
    wishlistcount = wishlist.count()
    if default_language != current_language:
        wishlist = Place.objects.raw(
            'SELECT p.id,l.title,l.keyword,l.description,l.slug,p.image,p.city,p.country,p.location'
            ' FROM home_wishist as w'
            ' JOIN place_place as p'
            ' ON w.place_id=p.id'
            ' JOIN place_placelanguage as l'
            ' ON p.id=l.place_id'
            ' WHERE l.lang=%s and w.user_id=%s', [current_language, request.user.id])
        category = categoryTree(0, '', current_language)
        setting = SettingLang.objects.filter(lang=current_language)
    if request.method == 'POST':
        place = PlaceLanguage.objects.get(place_id=place_id, id=id)
        user_form = PlaceLangUpdateForm(request.POST, instance=place)
        # profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your item has been succesfully updated')
            url = "/user/add_place_multilang/"
            url += str(place_id)
            return HttpResponseRedirect(url)
    else:
        place = PlaceLanguage.objects.get(id=id, place_id=place_id)
        user_form = PlaceLangUpdateForm(instance=place)

        context = {
            'category': category,
            'user_form': user_form,
            'wishlist': wishlist,
            'wishlistcount': wishlistcount,
            'wishlist1': wishlist1
        }
        return render(request, 'user_update_multiLang_place.html', context)
