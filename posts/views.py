from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Perfil, Follow, Like
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib import messages


@login_required
def feed(request):
    user = Follow.objects.filter(follower=request.user)
    followings_id = user.values_list("following", flat=True)
    mode = request.GET.get("mode", "all")

    if mode == "all":
        posts = Post.objects.all().order_by("-created_at")
    elif mode == "following":
        posts = Post.objects.filter(author__in=followings_id).order_by("-created_at")
    else:
        posts = Post.objects.all().order_by("-created_at")
        messages.add_message(request, messages.ERROR, "Erro")

    for post in posts:
        Perfil.objects.get_or_create(profile_user=post.author)
    return render(request, "posts/feed.html", {"posts": posts, "mode": mode})


def ini(request):
    return render(request, "posts/index.html")


@login_required
def create_post(request):
    if request.method == "POST":
        user_request = request.user
        message = request.POST.get("message")

        if message and message.strip() != "":
            Post.objects.create(author=user_request, message=message)
            messages.add_message(request, messages.SUCCESS, "Post criado com sucesso!")
            return redirect("feed")
        messages.add_message(request, messages.ERROR, "Mensagem vazia.")

    return render(request, "posts/create_post.html")


@login_required
def post_detail(request, id):
    post_detail_id = get_object_or_404(Post, id=id)
    user_request = request.user
    comments = Comment.objects.filter(from_post=post_detail_id)
    like_count = Like.objects.filter(post=post_detail_id).count()
    user_liked = Like.objects.filter(post=post_detail_id, profile_user=user_request).exists()
    Perfil.objects.get_or_create(profile_user=post_detail_id.author)
    for comment in comments:
        Perfil.objects.get_or_create(profile_user=comment.author)

    if request.method == "POST":
        new_comment = request.POST.get("comment_message")

        if new_comment and new_comment.strip() != "":
            Comment.objects.create(author=user_request, message=new_comment, from_post=post_detail_id)
            messages.add_message(request, messages.SUCCESS, "Comentario criado com sucesso!")
            return redirect("post_detail", id=id)

        messages.add_message(request, messages.ERROR, "Comentario Vazio!")
        return redirect("post_detail", id=id)

    return render(
        request,
        "posts/post_details.html",
        {
            "id_post": post_detail_id,
            "comments_post": comments,
            "like_count": like_count,
            "user_liked": user_liked,
        },
    )


@login_required
def view_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(author=profile_user)
    profile_perfil, created = Perfil.objects.get_or_create(profile_user=profile_user)
    followers_count = Follow.objects.filter(following=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()
    already_following = Follow.objects.filter(following=profile_user, follower=request.user).exists()

    return render(
        request,
        "posts/profile.html",
        {
            "profile_user": profile_user,
            "user_posts": user_posts,
            "profile_perfil": profile_perfil,
            "followers_count": followers_count,
            "following_count": following_count,
            "already_following": already_following,
        },
    )


@login_required
def edit_profile(request, username):
    user = request.user
    user_perfil, created = Perfil.objects.get_or_create(profile_user=user)

    if request.method == "POST":
        bio_att = request.POST.get("new_bio")
        foto_att = request.FILES.get("new_pfp")

        if bio_att:
            user_perfil.bio = bio_att

        if foto_att:
            user_perfil.profile_picture = foto_att

        if bio_att or foto_att:
            user_perfil.save()
            messages.add_message(request, messages.SUCCESS, "Perfil atualizado com sucesso!")
            return redirect("view_profile", username=user.username)

    if request.method == "GET":
        return render(request, "posts/edit_profile.html", {"user_perfil": user_perfil})


@login_required
@require_POST
def delete_comment(request, post_id, comment_id):
    target_comment = get_object_or_404(Comment, id=comment_id, from_post_id=post_id)

    if request.user == target_comment.author:
        target_comment.delete()
        messages.add_message(request, messages.SUCCESS, "Comentario excluido com sucesso!")
    else:
        messages.add_message(request, messages.ERROR, "Voce nao tem permissao pra isso")

    return redirect("post_detail", id=post_id)


@login_required
@require_POST
def delete_post(request, post_id):
    target_post = get_object_or_404(Post, id=post_id)

    if request.user == target_post.author:
        target_post.delete()
        messages.add_message(request, messages.SUCCESS, "Post excluido com sucesso!")
    else:
        messages.add_message(request, messages.ERROR, "Voce nao tem permissao pra isso")

    return redirect("feed")


@login_required
@require_POST
def follow(request, username):
    follower = request.user
    following = get_object_or_404(User, username=username)
    already_following = Follow.objects.filter(following=following, follower=follower)
    if following == follower:
        messages.add_message(request, messages.ERROR, "Voce nao pode seguir a si mesmo")
        return redirect("view_profile", username=username)

    if already_following.exists():
        messages.add_message(request, messages.ERROR, "Voce ja segue este usuario")
        return redirect("view_profile", username=username)

    Follow.objects.create(follower=follower, following=following)
    messages.add_message(request, messages.SUCCESS, "Seguido com sucesso")
    return redirect("view_profile", username=username)


@login_required
@require_POST
def unfollow(request, username):
    follower = request.user
    unfollowing = get_object_or_404(User, username=username)

    if unfollowing == follower:
        messages.add_message(request, messages.ERROR, "Voce nao pode parar de seguir a si mesmo")
        return redirect("view_profile", username=username)

    relation = Follow.objects.filter(follower=follower, following=unfollowing)

    if relation.exists():
        relation.delete()
        messages.add_message(request, messages.SUCCESS, "Parou de seguir com sucesso")
    else:
        messages.add_message(request, messages.ERROR, "Nao foi possivel realizar esta acao")

    return redirect("view_profile", username=username)


@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    already_liked = Like.objects.filter(post=post, profile_user=user).exists()

    if already_liked:
        like = Like.objects.get(post=post, profile_user=user)
        like.delete()
        messages.add_message(request, messages.SUCCESS, "Curtida removida com sucesso")
    else:
        Like.objects.create(post=post, profile_user=user)
        messages.add_message(request, messages.SUCCESS, "Curtido")

    return redirect("post_detail", id=post_id)
