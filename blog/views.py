from pipes import Template
from django.shortcuts import render
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
