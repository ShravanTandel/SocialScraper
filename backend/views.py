from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from .models import ModelWithImage
from .forms import UserForm
from django.http import HttpResponseRedirect, HttpResponse, response
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required                   #view required to user to logged in this decorator is used

import time
import instabot
import twitterbot
import requests
import tempfile
import csv
import json

from django.core import files
from .models import ModelWithImage,ModelForTwitter
from django.core.files import File

import os

# Create your views here.

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def user_login(request):
    i = ModelWithImage.objects.filter(user = request.user.id)
    if i.exists:
        for j in i:
            j.delete()
    t = ModelForTwitter.objects.filter(user = request.user.id)
    t.delete()
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)

                if 'next' in request.POST:
                    return HttpResponseRedirect(request.POST.get('next'))
                else:
                    return HttpResponseRedirect('/')
            
            else:
                return HttpResponse('User not active')

        else:
            # messages.info(request, "Invalid credentials")
            return render(request, 'login.html')

    else:
        return render(request, 'login.html')



def index(request):
    i = ModelWithImage.objects.filter(user = request.user.id)
    if i.exists:
        for j in i:
            j.delete()
    t = ModelForTwitter.objects.filter(user = request.user.id)
    t.delete()
    return render(request,"index.html")

@login_required(login_url = '/login')
def twitter(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        search = request.POST.get("search")
        nooftweets = request.POST.get("nooftweets")
        user1 = get_object_or_404(User, username = request.user)
        data = twitterbot.tweetbot(username,password,nooftweets,search)
        length = len(data)
        m = ModelForTwitter()
        m.user = user1
        m.data = json.dumps(data)
        m.save()
        return render(request, "twitter.html",{"search":search,"length":length})
    i = ModelWithImage.objects.filter(user = request.user.id)
    if i.exists:
        for j in i:
            j.delete()
    t = ModelForTwitter.objects.filter(user = request.user.id)
    t.delete()
    return render(request,"twitter.html")

@login_required(login_url = '/login')
def downloadtweetscsv(request,filename):
    m = ModelForTwitter.objects.all()
    jsonDec = json.decoder.JSONDecoder()
    for i in m:
        datalist = jsonDec.decode(i.data)
    response = HttpResponse(content_type = "text/csv")
    writer = csv.writer(response)
    writer.writerow(['UserName', 'Handle', 'Timestamp', 'Text', 'Emojis', 'Comments', 'Likes', 'Retweets'])
    writer.writerows(datalist)
    response['Content-Disposition'] = f'attachment; filename={filename+".csv"}'
    return response

@login_required(login_url = '/login')
def instagram(request):
    user1 = get_object_or_404(User, id = request.user.id)
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        instaname = request.POST.get("instaname")
        image_urls = instabot.bot(username,password,instaname)
        user1 = get_object_or_404(User, id = request.user.id)
        username1 = get_object_or_404(User, username = request.user.username)

        print(request.user)
        l = len(image_urls)-1

        for i,image_url in enumerate(image_urls):
            if image_url.startswith("https:"):
                response = requests.get(image_url, stream=True)
                if response.status_code != requests.codes.ok:
                    continue
                file_name = str(i)
                lf = tempfile.NamedTemporaryFile()
                for block in response.iter_content(1024 * 8):
                    if not block:
                        break
                    lf.write(block)
                image = ModelWithImage()
                image.user = request.user
                image.url = image_url
                image.save()
                image.image.save(str(username1)+file_name+".jpg", files.File(lf))
        imagesindb = ModelWithImage.objects.filter(user = request.user)
        image_len = len(image_urls)
        time.sleep(1)
        return render(request, "instagram.html",{"imagesindb":imagesindb,"image_len":image_len,"instaname":instaname})
    i = ModelWithImage.objects.filter(user = request.user)
    if i.exists:
        for j in i:
            j.delete()
    t = ModelForTwitter.objects.filter(user = request.user)
    t.delete()
    return render(request,"instagram.html")

def register(request):
    form = UserForm()
    if request.method == "POST":
        userform = UserForm(request.POST)

        if userform.is_valid():
            print("Hello")
            user = userform.save()
            user.set_password(user.password)
            user.save()
        return HttpResponseRedirect('/')
    else:
        form = UserForm()
        return render(request, 'register.html', {'form':form})

@login_required(login_url = '/login')
def download(request,id,instaname):
    # save_as = f"C:\Users\91876\Downloads\{pk}.jpg"
    # wget.download(image, save_as)
    im = ModelWithImage.objects.filter(id=id)
    for i in im:
        url = i.url

    with requests.get(url, stream=True) as r:
        home = os.path.expanduser("~")
        path1 = os.path.join(home, "Downloads")
        print(path1)
        with open(path1+'/'+instaname+str(id)+'.jpg', "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    f.close()
    return redirect("/")

def profile(request):
    user1 = {'user':request.user}
    return render(request,"profile.html",user1)

        
