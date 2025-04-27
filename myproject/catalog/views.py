from django.shortcuts import render
from .forms import ContactForm


def home(request):
    return render(request, 'catalog/home.html')

def contacts(request):
    return render(request, 'catalog/contacts.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # После успешной обработки перенаправляем на страницу успеха
            print(form.cleaned_data)  # Выводим данные в консоль

            return render(request, 'catalog/contact_success.html')
    else:
        form = ContactForm()

    return render(request, 'catalog/contacts.html', {'form': form})
