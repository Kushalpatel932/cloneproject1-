from pipes import Template
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
from .models import Post,Comment
from .forms import PostForm,CommentForm
from django.utils import timezone
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
# Create your views here.

class AboutView(TemplateView):
    template_name= 'about.html'


class PostListView(ListView,TemplateView):
    template_name: 'home.html'
    model = Post
    

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    
    model = Post

class CreatePostView(CreateView):
    login_url = '/login/'
    redirect_field_name = 'post_detail.html'

    form_class = PostForm

    model = Post

class PostUpdateView(UpdateView):
    login_url = '/login/'
    redirect_field_name = 'post_detail.html'

    form_class = PostForm

    model = Post

class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

class DraftListView(ListView):
    login_url = '/login/'
    redirect_field_name = 'post_draft_list.html'

    model = Post
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


def post_publish(request, pk):
    #use seesion 
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


def add_comment_to_post(request, pk):
    #session
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})

def comment_approve(request, pk):
#session
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


def comment_remove(request, pk):
    #session
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)