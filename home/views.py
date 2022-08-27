from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.db.models import Avg, Count
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import translation

from home.forms import SearchForm
from home.models import Setting, ContactForm, ContactMessage, Faq, SettingLang
from place.models import Category, Place, Images, Comment, CategoryLanguage, PlaceLanguage, wishist


# Create your views here.

# @register.simple_tag
def categoryTree(id, menu, lang):
    default_language = settings.LANGUAGE_CODE[0:2]
    if id <= 0:
        if lang == default_language:
            query = Category.objects.filter(parent_id__isnull=True).order_by('id')
        else:
            query = Category.objects.raw('SELECT c.id,l.title,l.keyword,l.description,l.slug'
                                         ' FROM place_category as c'
                                         ' INNER JOIN place_categorylanguage as l'
                                         ' ON c.id=l.category_id'
                                         ' WHERE parent_id IS NULL and lang=%s ORDER BY c.id', [lang])
        queryCount = Category.objects.filter(parent_id__isnull=True).count()
    else:
        if lang == default_language:
            query = Category.objects.filter(parent_id=id)
        else:
            query = Category.objects.raw('SELECT c.id,l.title,l.keyword,l.description,l.slug'
                                         ' FROM place_category as c'
                                         ' INNER JOIN place_categorylanguage as l'
                                         ' ON c.id=l.category_id'
                                         ' WHERE parent_id=%s and lang=%s ORDER BY c.id', [id, lang])
        queryCount = Category.objects.filter(parent_id__isnull=True).count()
    if queryCount > 0:
        for q in query:
            subcount = Category.objects.filter(parent_id=q.id).count()
            if subcount > 0:
                menu += '\t<li class="dropdown side-dropdown">\n'
                menu += '\t<a class="dropdown-toggle" data-toggle="dropdown" aria-expanded="true" >' + q.title + '<i class="fa fa-angle-right"></i></a>\n'
                menu += '\t\t<div class="custom-menu">\n'
                menu += '\t\t<ul class="list-links">\n'
                menu += categoryTree(int(q.id), '', lang)
                menu += '\t\t\t</ul>\n'
                menu += '\t\t</div>\n'
                menu += '\t</li>\n\n'
            else:
                menu += '\t\t\t\t <li><a href="' + reverse('category_places',args=(q.id, q.slug)) + '" >' + q.title + '</a></li>\n'
    return menu


def index(request):
    place_newest = Place.objects.all().order_by('-id')[:10]
    place_latest = Place.objects.all().order_by('id')[:10]
    place_slider = Place.objects.all().order_by('-id')[:3]

    setting = Setting.objects.all()
    default_language = settings.LANGUAGE_CODE[0:2]
    current_language = request.LANGUAGE_CODE[0:2]
    category = categoryTree(0, '', default_language)
    category1 = Category.objects.all()
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
        category = categoryTree(0, '' , current_language)
        category1 = Category.objects.raw('SELECT c.id,l.title,l.keyword,l.description,l.slug,c.parent_id,c.level'
                                         ' FROM place_category as c'
                                         ' INNER JOIN place_categorylanguage as l'
                                         ' ON c.id=l.category_id'
                                         ' WHERE lang=%s ORDER BY c.id', [current_language])
        setting = SettingLang.objects.filter(lang=current_language)
        place_slider=Place.objects.raw(' SELECT p.id as id,p.image,l.title,l.description,l.detail,p.city,p.country,p.location'
                                       ' FROM place_place as p'
                                       ' INNER JOIN place_placelanguage as l'
                                       ' ON p.id=l.place_id'
                                       ' WHERE  l.lang=%s', [current_language])


        place_newest =Place.objects.raw('SELECT p.id,l.title,l.keyword,l.description,l.slug,p.image,p.city,p.country,p.location'
                                         ' FROM place_place as p'
                                         ' INNER JOIN place_placelanguage as l'
                                         ' ON p.id=l.place_id'
                                         ' WHERE lang=%s ORDER BY p.create_at Desc', [current_language])

        place_latest =Place.objects.raw('SELECT p.id,l.title,l.keyword,l.description,l.slug,p.image,p.city,p.country,p.location'
                                         ' FROM place_place as p'
                                         ' INNER JOIN place_placelanguage as l'
                                         ' ON p.id=l.place_id'
                                         ' WHERE lang=%s ORDER BY p.create_at Asc', [current_language])
        wishlist = Place.objects.raw('SELECT p.id,l.title,l.keyword,l.description,l.slug,p.image,p.city,p.country,p.location'
                                         ' FROM home_wishist as w'
                                         ' JOIN place_place as p'
                                         ' ON w.place_id=p.id'
                                         ' JOIN place_placelanguage as l'
                                         ' ON p.id=l.place_id'
                                         ' WHERE l.lang=%s and w.user_id=%s', [current_language,request.user.id])
        #return HttpResponse(wishlist)

    context = {'category': category,
               'place_slider': place_slider,
               'place_newest': place_newest,
               'place_latest': place_latest,
               'category1':category1,
               'setting': setting,
               'wishlist':wishlist,
               'wishlistcount':wishlistcount,
               'wishlist1':wishlist1
               }
    return render(request, 'index.html', context)


def about(request):
    setting = Setting.objects.get(pk=1)
    default_language = settings.LANGUAGE_CODE[0:2]
    current_language = request.LANGUAGE_CODE[0:2]
    category =categoryTree(0,'',default_language)
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
        setting = SettingLang.objects.filter(lang=current_language)
        category = categoryTree(0, '', current_language)
    context = {'setting': setting, 'category': category,'wishlist':wishlist,
               'wishlistcount':wishlistcount,
               'wishlist1':wishlist1
               }
    return render(request, 'aboutus.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()
            data.name = request.user.first_name
            data.email = request.user.email
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, 'Your message has been successfully sent.Thanks!')
            return HttpResponseRedirect('/contact')
    setting = Setting.objects.get(pk=1)
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
        setting = SettingLang.objects.filter(lang=current_language)
        category = categoryTree(0, '', current_language)
    form = ContactForm
    context = {'category': category, 'form': form, 'setting': setting,
               'wishlist':wishlist,
               'wishlistcount':wishlistcount,
               'wishlist1':wishlist1
               }
    return render(request, 'contactus.html', context)


def references(request):
    setting = Setting.objects.get(pk=1)
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
        setting = SettingLang.objects.filter(lang=current_language)
        category = categoryTree(0, '', current_language)
    place_slider = Place.objects.all().order_by('-id')[:3]
    wishlist = wishist.objects.filter(user_id=request.user.id)
    context = {'category': category, 'setting': setting,'wishlist':wishlist,
               'wishlistcount':wishlistcount,
               'wishlist1':wishlist1}

    return render(request, 'references.html', context)


def category_places(request, id, slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    category_place = Place.objects.filter(category_id=id)
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
        category = categoryTree(0, '',current_language )
        setting = SettingLang.objects.filter(lang=current_language)
        try:
            category_place = Place.objects.raw(
                ' SELECT p.id,p.image,pl.title,pl.description,pl.keyword,p.city,p.country,p.location,p.slug'
                ' FROM place_place AS p'
                ' LEFT JOIN place_placelanguage AS pl'
                ' ON p.id=pl.place_id'
                ' WHERE  p.category_id=%s AND pl.lang=%s', [id,current_language])

        except:
            pass

    title = CategoryLanguage.objects.get(category_id=id,lang=current_language).title
    context = {'setting': setting, 'category': category, 'category_place': category_place, 'title': title,'wishlist':wishlist,
               'wishlistcount':wishlistcount,
               'wishlist1':wishlist1}
    # return HttpResponse(places)
    return render(request, 'category_place.html', context)


def place_detail(request, id, slug):
    query = request.GET.get('q')
    default_language = settings.LANGUAGE_CODE[0:2]
    current_language = request.LANGUAGE_CODE[0:2]
    category = categoryTree(0,'',default_language)
    place = Place.objects.get(pk=id)
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
        try:
            prolang = Place.objects.raw(
                'SELECT p.id,p.image,l.title,l.description,l.detail,p.city,p.country,p.location'
                ' FROM place_place as p'
                ' INNER JOIN place_placelanguage as l'
                ' ON p.id=l.place_id'
                ' WHERE p.id=%s and l.lang=%s', [id, current_language])
            place = prolang[0]
        except:
            pass


    setting = Setting.objects.get(pk=1)
    comments = Comment.objects.filter(place_id=id)
    images = Images.objects.filter(place_id=id)
    wishlist = wishist.objects.filter(user_id=request.user.id)
    context = {
        'setting': setting,
        'place': place,
        'images': images,
        'category': category,
        'comments': comments,
        'wishlist':wishlist,
               'wishlistcount':wishlistcount,
               'wishlist1':wishlist1
    }

    return render(request, 'place_detail.html', context)


def search(request):
    default_language = settings.LANGUAGE_CODE[0:2]
    current_language = request.LANGUAGE_CODE[0:2]
    category = categoryTree(0, '', default_language)
    category1 = Category.objects.all()
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
        category1 = CategoryLanguage.objects.filter(lang=current_language)
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                places = Place.objects.filter(title__icontains=query)
            else:
                places = Place.objects.filter(title__icontains=query, category_id=catid)
            #category = Category.objects.all()
            context = {'category': category,'category1': category1, 'places': places, 'query': query,'wishlist':wishlist,
               'wishlistcount':wishlistcount,
               'wishlist1':wishlist1 }
            return render(request, 'searchPlace.html', context)
    return HttpResponseRedirect('/'+current_language)


def faq(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    default_language = settings.LANGUAGE_CODE[0:2]
    current_language = request.LANGUAGE_CODE[0:2]
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
        faqs = Faq.objects.filter(status='True', lang=default_language).order_by('ordered')
    else:
        faqs = Faq.objects.filter(status='True', lang=current_language).order_by('ordered')
    # f_id = faqs.get(pk=1).ordered
    context = {'setting': setting,
               'category': category,
               'faqs': faqs,
                'wishlist':wishlist,
               'wishlistcount':wishlistcount,
               'wishlist1':wishlist1
               }
    return render(request, 'Faq.html', context)


def selectLanguage(request):

    if request.method == 'POST':
        url = request.META.get('HTTP_REFERER')
        user_language = translation.get_language()
        lang = request.POST['language']
        # translation.activate(user_language)
        translation.activate(lang)
        response = HttpResponse(lang)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
        return HttpResponseRedirect("/" + lang)
