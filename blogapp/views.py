from django.shortcuts import render,HttpResponseRedirect
from .forms import SignUpForm,LoginForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post
from django.contrib.auth.models import Group

# Create your Home views here.
def home(request):
    posts = Post.objects.all()
    return render (request,'blogapp/home.html',{'posts':posts})

# Create about views here.
def about(request):
    return render (request,'blogapp/about.html')

def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()


        return render(request,'blogapp/dashboard.html',{'posts':posts,'full_name':full_name,'groups':gps})
    else:
        return HttpResponseRedirect('/login/')

def contact(request):
    return render (request,'blogapp/contact.html')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,"Congratulations!! Welcome Author")
            user=form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(request,'blogapp/signup.html',{'form':form})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request,data= request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user= authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged in Succesfully')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render (request,'blogapp/login.html',{'form':form})
    else:
     return HttpResponseRedirect('/dashboard')

#Add new Post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                pst = Post(title=title,description=description)
                pst.save()
                form = PostForm()
                #form.save()
        else:
            form = PostForm()

        return render(request,'blogapp/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

#update/edit post
def update_post(request,id):
    if request.user.is_authenticated:
        if request.method =='POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request,'blogapp/updatepost.html',{'form':form})

    else:
        return HttpResponseRedirect('/login/')

#delete post
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')