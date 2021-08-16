from django.contrib.auth import authenticate,login as userlogin, logout as userlogout
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseForbidden,JsonResponse
from blog import models

from blog.decorators import login_required


def index(request):
    if request.user.is_authenticated:
        blogset = models.Blog.objects.filter(user__id__in=request.user.get_friend_idlist())
        blogs = [x.get_datadict(request.user) for x in blogset]
        return render(request, "home/home.html",{
            "blogs":blogs,
        })
    else:
        return render(request, "index/index.html")

def login(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        user = authenticate(username=request.POST.get("email").strip(),password=request.POST.get("password"))
        if user:
            userlogin(request, user)
            return redirect("/")
        else:
            return render(request, "index/index.html", {
                "message": "invalid Email or Password",
                "type": "err",
            })
    else:
        return  HttpResponse("failed")
def logout(request):
    userlogout(request)
    return redirect("/")
def register(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        post = request.POST
        try:
            if models.Users.objects.filter(email=post.get("email").strip).exists():
                return render(request,"index/index.html",{
                    "message" : "user with same email address already exists",
                    "type":"err",
                })
            else:
                user = models.Users.objects.create_user(
                    name=post.get("name").strip(),
                    username=post.get("email").strip(),
                    email=post.get("email").strip(),
                    password=post.get("password").strip(),
                    mobile=post.get("mobile").strip(),
                )
                return render(request,"index/index.html",{
                    "message" : "You are registered successfully. Please login to access your account",
                    "type":"success",
                })
        except:
            return render(request, "index/index.html", {
                "message": "oops! error",
                "type": "err",
            })

    else:
        return redirect("/")
def newPost(request):
    if request.method == "POST":
        try:
            post = request.POST
            blog = models.Blog()
            blog.user = request.user
            blog.text = request.POST.get("postText")
            if request.FILES.get("imagefile"):
                blog.picture = request.FILES.get("imagefile")
            print(request.FILES)
            blog.save()
            return redirect("/")
        except:
            return redirect("/")
    else:
        return HttpResponseForbidden
    return HttpResponse("got Post")

@login_required
def myProfile(request):
    return render(request,'profile/profile.html')

@login_required
def myFriends(request):

    return render(request,'friends/friends.html',{
        "friendList": request.user.get_friend_list,
    })

@login_required
def findFriends(request):
    return render(request,'friends/findFriends.html',{
        "friendList": request.user.find_friends,
    })

@login_required
def friendRequests(request):
    print(request.user.get_friend_requests)
    return render(request,'friends/friendRequests.html',{
        "requests": request.user.get_friend_requests
    })

@login_required
def updaterequest(request):
    user = request.user
    action = request.GET.get("action")
    userid = request.GET.get("userId")
    if action == "sendFrndRq":
        user.send_friend_rq(userid)
    elif action == "reject":
        user.reject_friend_rq(userid)
    elif action == "approve":
        user.accept_friend_rq(userid)
    elif action == "cancel":
        user.cancel_friend_rq(userid)
    else:
        return HttpResponseForbidden


    return JsonResponse({"status":"Success"})

