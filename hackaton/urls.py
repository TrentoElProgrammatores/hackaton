"""
URL configuration for hackaton project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from scambio import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    #path("__reload__/", include("django_browser_reload.urls")),
    path('', views.home, name='home'),
    path('aggiungi/item', views.addItem, name='addItem'),
    path('aggiungi/scatola', views.addScatola, name='addScatola'),
    path('prodotto/<str:id>', views.prodotto, name='prodotto'),
    path('aggiungi/location', views.addLocation, name='addLocation'),
    path('item/edit/<str:id>', views.editProduct, name='editProduct'),
    path('login/', views.sedeLogin, name="sedeLogin"),
    path('logout/', views.sedeLogout, name='sedeLogout'),
    path("confermaPrenotazione/<uuid:item_id>/", views.confermaPrenotazione, name="confermaPrenotazione"),
    path('api/locations/<str:id>', views.apiLocation),
    path('api/scatole/<str:id>', views.apiScatole),
    path('scatole/<str:id>', views.apiScatole,name='visualizzaScatola'),
    path('iMieiOggetti/', views.iMieiOggetti, name='iMieiOggetti'),
    path('api/aggetto/save', views.apiSaveItem),
    path('leMieScatole/', views.leMieScatole, name='leMieScatole'),
    path('scatola/<uuid:scatola_id>/', views.oggettiInScatola, name='oggettiInScatola'),
       path('scatola/<uuid:scatola_id>/aggiungi-oggetto/',
         views.aggiungi_oggetto_view,
         name='aggiungi_oggetto'),

    path('scatola/<uuid:scatola_id>/aggiungi-oggetto/<uuid:oggetto_id>/',
         views.aggiungi_oggetto_scatola,
         name='aggiungi_oggetto_scatola'),
         path('oggetto/<uuid:oggetto_id>/rimuovi/', views.rimuovi_dalla_scatola, name='rimuovi_dalla_scatola'),
    path('recupero/password', views.recupero_password, name='recupero_password'),
    path("oggetto/<uuid:pk>/elimina/", views.elimina_oggetto, name="elimina_oggetto"),
    path('scatola/<uuid:scatola_id>/elimina/', views.elimina_scatola, name='elimina_scatola'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


'''
    path('recupero/password/<str:id>', views.verifica_recupero, name='verifica_recupero'),'''