from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import BlogModel
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User


# Create your views here.

# it will list all posts or save post post to database
def list_view(request):
    posts = []
    if request.POST:
        # data = request.POST
        # new_Post = BlogModel(title=data.get('title'), image=data.get("image"), description=data.get('description'))
        # new_Post.save()
        # or
        new_post = BlogModel()
        new_post.title = request.POST.get('title')

        # image upload code start
        uploaded_image = request.FILES['image']
        # fs = FileSystemStorage()
        # image_file = fs.save(uploaded_image.name, uploaded_image)
        # uploaded_image_url = fs.url(image_file)
        new_post.image = uploaded_image

        # end
        new_post.description = request.POST.get('description')
        new_post.author = request.user
        new_post.save()
        # return render(request, 'home.html', {"posts": posts})
        return redirect('index')
    else:
        try:
            search_string = request.GET['search']
            posts = BlogModel.objects.filter(title__contains=search_string)
        except:
            posts = BlogModel.objects.all()

    return render(request, 'home.html', {"posts": posts})


# it will show form to create post
@login_required
def new_view(request):
    return render(request, 'new.html')


# it will show particular post or update particular post
def show_edit_view(request, id):
    if request.POST:
        post = BlogModel.objects.get(pk=id)
        post.title = request.POST.get('title')
        try:
            uploaded_image = request.FILES['image']
            post.image.delete()
            post.image = uploaded_image
        except:
            pass
        post.description = request.POST.get('description')
        post.save()
        return redirect('user_posts', id=request.user.id)
    else:
        post = get_object_or_404(BlogModel, pk=id)
        return render(request, 'show.html', {"post": post})


# it will show edit form
@login_required
def edit_form_view(request, id):
    post = get_object_or_404(BlogModel, pk=id)
    return render(request, 'edit.html', {"post": post})


# it will delete post from database
@login_required
def delete_view(request, id):
    if request.POST:
        post = get_object_or_404(BlogModel, pk=id)
        post.delete()
        return redirect('user_posts', id=request.user.id)
    else:
        return redirect('show_edit', id=id)


# it will send message(comment) to author with post title
def comment_view(request, id):
    post = get_object_or_404(BlogModel, pk=id)
    subject = 'Comment on post "{}"'.format(post.title)
    message_body = '''{} has commented on your post "{}"
       
       "{}" '''.format(request.GET['name'], post.title, request.GET['message'])
    sender = request.GET['email']
    receiver = post.author.email

    send_mail(subject, message_body, sender, [receiver])
    return redirect('show_edit', id=id)


# it will show all posts of logged in user
def user_posts(request, id):
    user = get_object_or_404(User, pk=id)
    return render(request, 'posts.html', {'found_user': user})
