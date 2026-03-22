from django.shortcuts import render, redirect
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages


@login_required
def feed(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "posts/feed.html", {"posts": posts})

def ini (request):
    return render(request, "posts/index.html")

@login_required
def create_post(request):
    if request.method == "POST":

        user_request = request.user      
        message = request.POST.get('message')

        if message and message.strip() != "":
            Post.objects.create(author=user_request, message=message) 
            messages.add_message(request, messages.SUCCESS, "Post criado com sucesso!")
            return redirect("/feed")
        else:
            messages.add_message(request, messages.ERROR, "Mensagem vazia.")
    
    return render(request, "posts/create_post.html")

def post_detail(request, id):
    post_detail_id = Post.objects.get(id=id)
    comments = Comment.objects.filter(from_post=post_detail_id)
    return render(request, "posts/post_details.html", {"id_post": post_detail_id, "comments_post": comments})