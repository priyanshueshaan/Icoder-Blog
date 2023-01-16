from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from blog.models import Post

def home(request):
    return render(request,'home/home.html')

def contact(request):
        if request.method=="POST":
            name=request.POST['name']
            email=request.POST['email']
            phone=request.POST['phone']
            issue=request.POST['query']
            if len(name)<2 or len(email)<3 or len(phone)<10 or len(issue)<4:
                messages.error[request,"Please fill the form correctly"]
            else:
                contact=Contact(name=name,email=email,phone=phone,content=issue)
                contact.save()
                messages.success(request,"Your message has been successfully sent")
        return render(request, 'home/contact.html')

def about(request):
    return render(request,'home/about.html')

def search(request):
    query=request.GET['query']
    if len(query)>78:
        allPosts=Post.objects.none()
    else:
        allPostsTitle=Post.objects.filter(title__icontains=query)
        allPostsAuthor=Post.objects.filter(author__icontains=query)
        allPostsContent=Post.objects.filter(content__icontains=query)
        allPosts=allPostsTitle.union(allPostsContent,allPostsAuthor)
    if allPosts.count()==0:
        messages.warning(request,"No Search Result Found. Please refine your query")
    params={'allPosts':allPosts,'query':query}
    return render(request,'home/search.html',params)

def signup(request):
    if request.method=="POST":
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        # create the user 
        myuser=User.objects.create_user(username,email,password1)
        myuser.first_name=fname 
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"User has been created")
        return redirect('home')
    
    else:
        return HttpResponse("404 Not Found")
    
def handlelogin(request):
    if request.method=="POST":
        loginUsername=request.POST['loginUsername']
        loginPassword=request.POST['loginPassword']
        user=authenticate(username=loginUsername,password=loginPassword)
        if user is not None:
            login(request,user)
            messages.success(request, "Succesfully Logged In")
            return redirect("home")
        else:
            messages.error(request,"Invalid Credentials ! Please try again")
            return redirect("home")
        
    return HttpResponse("404 Not Found")

def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')
            