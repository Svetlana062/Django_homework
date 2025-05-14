from django.shortcuts import render, redirect
from .forms import ContactForm
from django.shortcuts import render, get_object_or_404
from .models import Product


def home(request):
    products = Product.objects.all()
    return render(request, 'catalog/home.html', {'products': products})

def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Обработка данных формы
            print(form.cleaned_data)  # Для теста
            return redirect('contact_success')  # Название URL для страницы успеха
    else:
        form = ContactForm()

    return render(request, 'catalog/contacts.html', {'form': form})

def contact_success(request):
    return render(request, 'catalog/contact_success.html')

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})

