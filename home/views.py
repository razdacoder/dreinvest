from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, template_name="site/index.html")


def about(request):
    return render(request, template_name="site/about.html")


def plans(request):
    return render(request, template_name="site/plan.html")


def faqs(request):
    return render(request, template_name="site/faqs.html")


def contact(request):
    return render(request, template_name="site/contact.html")


def terms(request):
    return render(request, template_name="site/terms.html")


def policy(request):
    return render(request, template_name="site/policy.html")
