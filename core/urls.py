from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("plan/", views.plans, name="plans"),
    path("faqs/", views.faqs, name="faqs"),
    path("contct/", views.contact, name="contact"),
    path("terms/", views.terms, name="terms"),
    path("policy/", views.policy, name="policy"),
    path("dashboard/", include("dashboard.urls")),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
