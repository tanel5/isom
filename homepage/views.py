from django.shortcuts import render
from .models import LeadForm
# Create your views here.


def get_data(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'homepage/success.html', {'form': form})
    else:
        form = LeadForm()
    return render(request, 'homepage/homepage.html', {'form': form})


def cgu(request):
    return render(request, "homepage/cgu.html", {})
