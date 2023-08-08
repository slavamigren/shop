from django.contrib.messages import success
from django.http import Http404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView, DeleteView, UpdateView

from blog.forms import BlogForm
from blog.models import Blog
from pytils.translit import slugify
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class BlogListView(ListView):
    model = Blog
    paginate_by = 3

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.object.owner != self.request.user:
            context_data['owner'] = False
        else:
            context_data['owner'] = True
        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        if self.object.views_count == 100:
            send_mail('Рекорд', f'Пост {self.object.title} просмотрен 100 раз', settings.EMAIL_HOST_USER, ['testtestsky@yandex.ru'])
        self.object.save()
        return self.object


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog')
    permission_required = 'blog.add_blog'

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.title)
            new_post.save()
        return super().form_valid(form)


class BlogDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog')
    permission_required = 'blog.delete_blog'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object



class BlogUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    permission_required = 'blog.change_blog'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.title)
            new_post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:view_post', args=[self.kwargs.get('pk')])