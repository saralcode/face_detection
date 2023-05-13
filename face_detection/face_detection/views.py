from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from profiles.models import Profile
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .helper.compare_images import compare_face
from logs.models import Log
from datetime import datetime
def login_view(request):
    if (request.method == "POST"):
        files = request.FILES
        if(files):
            profiles = Profile.objects.all()
            firstLog = Log.objects.create()
            firstLog.photo=files['file']
            firstLog.save()
            userProfile:Profile = None
            for profile in profiles:
                if(profile.photo):
                    try:
                        isMatched =  compare_face(firstLog.photo.url, profile.photo.url)
                        print(firstLog.photo.url, profile.photo.url)
                        print(isMatched)
                        if(isMatched):
                            userProfile= profile
                            break
                    except:
                        print("Error ")
            firstLog.delete()
            if(userProfile!=None):
                login(request=request, user= userProfile.user )
            return JsonResponse({"success":  False if userProfile==None else True })
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        user = authenticate(
            request=request, username=username, password=password)
        if user is not None:
            login(request=request, user=user)
            return redirect("home", permanent=True)
        else:
            return HttpResponse("Invalid Credentials")
    if (request.user.is_authenticated):
        return redirect("home")
    return render(request=request, template_name='login.html', context={})


def logout_view(request):
    logout(request=request)
    return redirect('login')


@login_required
def home_view(request):
    return render(request=request, template_name='main.html', context={})

def signup_view(request):
    data = {}
    if (request.user.is_authenticated):
        return redirect("home")
    if (request.method == "POST"):
        try:
            email = request.POST.get("email")
            username = request.POST.get("username")
            password = request.POST.get("password")
            confirmPass = request.POST.get("confirm-password")
            if (confirmPass == password):
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.save()
                login(request=request, user=user)
                return redirect("login", permanent=True,)
            data['error']="Password Doesn't Match"
        except Exception as e:
            print(e)
            data['error']=e

    return render(request=request, template_name="signup.html", context=data)


@login_required
def update_user(request):
    now = datetime.now()
    profile = Profile.objects.get(user=request.user)
    if (request.method == 'POST'):
        image = request.FILES['file']
        print(request.user)
        image.name=f"{request.user}.jpeg"
        if(profile.photo):
            profile.photo.delete()
        profile.photo = image
        profile.save()
        return JsonResponse({"success": True})

    return render(request=request, template_name="update-user.html", context={"image":f"{profile.photo.url}?lastmod=${now.timestamp()}" if profile.photo else "", "bio":profile.bio} )
