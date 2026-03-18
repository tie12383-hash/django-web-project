from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from .models import Product, Category, Contact
from .forms import ProductForm, ContactForm
from .service import get_products_by_category


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'page_obj'
    paginate_by = 6
    ordering = ['-created_at']

    def get_queryset(self):
        # Показываем только опубликованные товары
        return Product.objects.filter(is_published=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        context['categories'] = Category.objects.all()[:4]
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление товара'
        return context


class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner


class ProductUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование товара'
        return context


class ModeratorCanDeleteMixin(UserPassesTestMixin):
    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner or self.request.user.has_perm('catalog.delete_product')


class ProductDeleteView(LoginRequiredMixin, ModeratorCanDeleteMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление товара'
        return context


class ModeratorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_perm('catalog.can_unpublish_product')


class ProductUnpublishView(LoginRequiredMixin, ModeratorRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['pk'])
        product.is_published = False
        product.save()
        messages.success(request, f'Товар "{product.name}" снят с публикации.')
        return redirect('catalog:product_detail', pk=product.pk)


class ContactsView(FormView):
    template_name = 'catalog/contacts.html'
    form_class = ContactForm
    success_url = reverse_lazy('catalog:contacts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        context['contact_info'] = Contact.objects.filter(is_active=True)
        return context

    def form_valid(self, form):
        print("\n" + "="*50)
        print("ДАННЫЕ ФОРМЫ ОБРАТНОЙ СВЯЗИ:")
        print("="*50)
        print(f"Имя: {form.cleaned_data['name']}")
        print(f"Email: {form.cleaned_data['email']}")
        print(f"Telegram: {form.cleaned_data['telegram']}")
        print(f"Сообщение: {form.cleaned_data['message']}")
        print("="*50 + "\n")
        messages.success(self.request, 'Спасибо за ваше сообщение! Мы свяжемся с вами в ближайшее время.')
        return super().form_valid(form)

class CategoryProductsView(ListView):
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        self.category = Category.objects.get(pk=self.kwargs['pk'])
        return get_products_by_category(self.category.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['title'] = f'Категория: {self.category.name}'
        return context
