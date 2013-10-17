from django.conf.urls.defaults import patterns, include, url
from django.views.generic import RedirectView
from django.conf.urls.static import static

import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     # Examples:
     # url(r'^$', 'vikiticket.views.home', name='home'),
     # url(r'^vikiticket/', include('vikiticket.foo.urls')),

#    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

     # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     
     # Django Tinymce
     url(r'^tinymce/', include('tinymce.urls')),

     # Custom urls


#     url(r'^$', RedirectView.as_view(url='/event/home/')),
     url(r'^', include('core.urls')),
)

# Handlers for 404 and 500
#handler400 = 'core.views.custom_404_view'
handler500 = 'core.views.custom_500_view'

if settings.SERVE_STATIC_FILES:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)    
