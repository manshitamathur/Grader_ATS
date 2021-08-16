from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('home/',views.my_func,name='home'),
    #path('Results/',views.results,name='results'),
    path('ATS/',views.ATS_HomePage1,name='ATS'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)