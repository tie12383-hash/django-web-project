from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Product, Category, Contact
from .forms import ProductForm, ContactForm

class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'page_obj'
    paginate_by = 6
    ordering = ['-created_at']

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

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление товара'
        return context

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование товара'
        return context

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление товара'
        return context

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
