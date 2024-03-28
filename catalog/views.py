import slugify
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify
from django.forms import inlineformset_factory
from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, BlogWrite, Version


# Create your views here.

class CatalogListView(ListView):
    """Класс для вывода главной страницы."""
    model = Product


class ContactsView(TemplateView):
    """Класс для вывода страницы - контактная информация."""
    template_name = 'catalog/contacts.html'


class ProductsDetailView(DetailView):
    """Класс для вывода детальной информации о продукте."""
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = 'item'


class ProductCreateView(CreateView):
    """Класс для создания продукта."""
    model = Product
    form_class = ProductForm
    # fields = ('name', 'description', 'img', 'category', 'price', 'created_at', 'updated_at')
    success_url = reverse_lazy('catalog:product_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset()
        else:
            context_data['formset'] = VersionFormset()
        return context_data


class ProductUpdateView(UpdateView):
    """Класс для редактирования продукта и его версий"""
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
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super(ProductUpdateView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class ProductDeleteView(DeleteView):
    """Класс для удаления карточек с продуктами."""
    model = Product
    success_url = reverse_lazy('catalog:product_list')


class BlogListView(ListView):
    """Класс для вывода главной страницы раздела - блог."""
    model = BlogWrite

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    """Класс для вывода детальной информации о статье."""
    model = BlogWrite

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
    """Класс для создания карточки со статьей."""
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
    """Класс для редактирования карточки со статьей."""
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
    """Класс для удаления карточки со статьей."""
    model = BlogWrite
    success_url = reverse_lazy('catalog:blog')

