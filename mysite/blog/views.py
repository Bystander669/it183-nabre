from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import HttpResponseRedirect,  Http404
from .forms import PostForm, CommentForm
from django.urls import reverse

# Create your views here.
def blog_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return HttpResponseRedirect('/')
    context = {
        'form':form,
        'form_type': 'Create',
    }
    return render(request, "blog/blog_create.html", context)
    
def blog_update(request, id):
    post = Post.objects.get(id=id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/')
    context = {
         'blog_detail': post,
        'form':form,
        'form_type': 'Update',
    }
    return render(request, "blog/blog_update.html", context)

def blog_list(request):
   post = Post.objects.all()
   context = {

       'blog_list':post
   }
   return render(request, "blog/blog_list.html",context)

def blog_detail(request, id):
    try:
        id = int(id)
    except ValueError:
        raise Http404("Invalid blog post ID")

    each_post = get_object_or_404(Post, id=id)
    total_likes = each_post.total_likes()
    liked = each_post.likes.filter(id=request.user.id).exists()

    # Handle comment form submission
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = each_post
            comment.name = request.user.username  # Use logged-in user's name
            comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    context = {
        'liked': liked,
        'total_likes': total_likes,
        'blog_detail': each_post,
        'comment_form': comment_form,
    }
    return render(request, "blog/blog_detail.html", context)

def blog_delete(request, id):
    each_post = Post.objects.get(id=id)
    each_post.delete()
    return HttpResponseRedirect('/')


def like_post(request, id):
    post = get_object_or_404(Post, id=id)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    return HttpResponseRedirect(reverse('blog_detail', args=[id]))

def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = CommentForm()
    
    context = {
        'post': post,
        'form': form,
    }
    return render(request, "blog/add_comment.html", context)