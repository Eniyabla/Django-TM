from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.db.models import Avg, Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting
from place.models import CommentForm, Category, Comment


def place(request):
    return HttpResponse('place views')


def ratePlace(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.place_id = id
            cur_user = request.user
            data.user_id = cur_user.id
            data.save()
            messages.success(request, 'Your review has been succesfully sent!')
            return HttpResponseRedirect(url)
    return HttpResponseRedirect('ratePlace')



# setting = Setting.objects.get(pk=1)
# category = Category.objects.all()
# context = {'category': category, 'form': form, 'setting': setting}
# return render(request, 'contactus.html', context)
