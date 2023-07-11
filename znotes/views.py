from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from . import forms, models
from django.contrib.auth.models import User

from django.core.paginator import Paginator

from django.views.generic import DeleteView
from django.urls import reverse_lazy

def home(request):
    notes = models.Note.objects.order_by("-id").all()

    p = Paginator(notes, 9)
    page = request.GET.get('page')
    mypage = p.get_page(page)

    return render(request, 'home.html', {'notes':mypage})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {"error":"Wrong Credentials"})
    return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    return redirect('home')

def register(request):
    form = forms.RegisterForm()
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request,username=username,password=password)
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'register.html', {"form":form})
        
    return render(request, 'register.html', {"form":form})


def shownotes(request, id):
    note = get_object_or_404(models.Note, id=id)
    myfiles = models.MyFile.objects.filter(noteid = note)
    return render(request, 'shownotes.html',{"note":note,"myfiles":myfiles})

def dept(request, deptname):
    notes = models.Note.objects.order_by("-id").filter(department=deptname.upper())
    p = Paginator(notes, 9)
    page = request.GET.get('page')
    mypage = p.get_page(page)

    return render(request, 'showdept.html',{'notes':mypage,'department':deptname.upper()})

def profile(request, id):
    myuser = get_object_or_404(models.Profile, id=id)
    userpost = models.Note.objects.filter(author = myuser.name).order_by('-id')[:6]
    userpostcount = models.Note.objects.filter(author = myuser.name).count()
    return render(request, 'profile.html',{'myuser':myuser,"userpost":userpost[:6],"userpostcount":userpostcount})

def uploadnotes(request):
    form = forms.UploadNotesForm()
    if request.method == 'POST':
        form = forms.UploadNotesForm(request.POST, request.FILES)
        
        if form.is_valid():
            data = form.save(commit=False)
            data.author = request.user
            # file = request.FILES["file"]
            # data.file=file
            files = request.FILES.getlist('myfiles')
          
            data.save()
            for attachment in files:
                models.MyFile.objects.create(file=attachment,author=request.user,noteid=data)
            return redirect('home')
    return render(request, 'uploadnotes.html',{'form':form})

def showall(request , id):
    myuser = get_object_or_404(models.Profile, id=id)
    notes = models.Note.objects.order_by('-id').filter(author = myuser.name)
    p = Paginator(notes, 9)
    page = request.GET.get('page')
    mypage = p.get_page(page)
    return render(request, 'showall.html', {"myuser":myuser.name,"notes":mypage})

def editprofile(request):
    if request.user.is_authenticated:
        curr_user = User.objects.get(id=request.user.id)
        profile_user = models.Profile.objects.get(name_id=request.user.id)
        userform = forms.UpdateUserForm(request.POST or None, request.FILES or None ,instance=curr_user)
        profileform = forms.ProfileImageForm(request.POST or None , request.FILES or None ,instance=profile_user )
        profilelinkform = forms.ProfileLinkForm(request.POST or None , request.FILES or None ,instance=profile_user )
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()
            profilelinkform.save()
            login(request,curr_user)
            return redirect('/profile/%d'%request.user.id)
        else:
            return render(request, 'editprofile.html', {"userform":userform,"profileform":profileform,"profilelinkform":profilelinkform})
        
    else:
        redirect('home')

class PostDeleteView(DeleteView):
    model = models.Note
    template_name = 'delete.html'
    success_url = reverse_lazy("home")

def search(request):
    if request.method == "POST":
        search = request.POST['search']
        note = models.Note.objects.order_by("-id").filter(title__contains = search)
        dept = models.Note.objects.order_by("-id").filter(department__contains = search)
        notes = note | dept
        p = Paginator(notes, 9)
        page = request.GET.get('page')
        mypage = p.get_page(page)

        return render(request,"search.html",{"notes":mypage,"search":search})
    else:
        return render(request,"search.html",{})
    
def error404(request,exception):
    return render(request,'404.html',{})