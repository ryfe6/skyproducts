import slugify
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify

from catalog.models import Product, BlogWrite


# Create your views here.

class CatalogListView(ListView):
    model = Product


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'


class ProductsDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = 'item'


class BlogListView(ListView):
    model = BlogWrite

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = BlogWrite


    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
    model = BlogWrite
    fields = ('heading', 'slug', 'content', 'photo', 'created_at', 'is_published', "views_count")
    success_url = reverse_lazy('catalog:blog')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.heading)
            new_blog.save()
        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = BlogWrite
    fields = ('heading', 'slug', 'content', 'photo', 'created_at', 'is_published', "views_count")


    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.heading)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:blog_detail', args=[(self.kwargs.get('pk'))])


class BlogDeleteView(DeleteView):
    model = BlogWrite
    success_url = reverse_lazy('catalog:blog')


