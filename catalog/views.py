from django.shortcuts import render
from catalog.models import Product, Contact

def home(request):
    print(Product.objects.order_by("-pk")[:5])
    return render(request, 'catalog/home.html', {'products': Product.objects.order_by("-pk")[:5]})

def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        text = request.POST.get('text')
        print(name, phone, text)
    return render(request, 'catalog/contacts.html', {'contacts': Contact.objects.all()[:5]})