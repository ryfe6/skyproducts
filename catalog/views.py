import slugify
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify
from django.forms import inlineformset_factory
from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, BlogWrite, Version


# Create your views here.

class CatalogListView(ListView):
    model = Product


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'


class ProductsDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = 'item'


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    # fields = ('name', 'description', 'img', 'category', 'price', 'created_at', 'updated_at')
    success_url = reverse_lazy('catalog:product_list')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self, *args, **kwargs):
        return reverse('catalog:product_update', args=[self.get_object().pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            form.save()

        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')


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

