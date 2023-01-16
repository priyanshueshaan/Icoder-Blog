from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post, BlogComment
from django.contrib import messages
from django.contrib.auth.models import User
from blog.templatetags import extras

def bloghome(request):
    allPosts = Post.objects.all()
    context = {'allPosts': allPosts}
    return render(request,'blog/bloghome.html', context)
    # return HttpResponse("hello i m bloghome")

def blogpost(request,slug):
    post = Post.objects.filter(slug=slug).first()
    post.views=post.views+1
    post.save()
    comments=BlogComment.objects.filter(post=post,parent=None)
    replies=BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context = {'post':post,'comments':comments,'user':request.user,'replyDict':replyDict}
    return render(request,"blog/blogpost.html", context)
    # return HttpResponse(f'This is Blogpost:{slug}')

def PostComment(request):
    if request.method=="POST":
        comment=request.POST.get('comment')
        user=request.user
        postsno=request.POST.get('postsno')
        post=Post.objects.get(sno=postsno)
        parentSno=request.POST.get('parentSno')
        if parentSno=="":
            comment=BlogComment(comment=comment,user=user,post=post)
            comment.save()
            messages.success(request,"Your Comment has been posted successfully")
        else:
            parent=BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comment=comment,post=post,user=user,parent=parent)
            comment.save()
            messages.success(request,"Your Reply has been posted successfully")
    return redirect(f"/blog{post.slug}")
   
    
    
