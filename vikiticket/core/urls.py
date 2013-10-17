from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView

from views import PageView
from vikiticket.core.views import OrderView
from core.models import Event

urlpatterns = patterns('',
     # Examples:
     # url(r'^$', 'vikiticket.views.home', name='home'),
     # url(r'^vikiticket/', include('vikiticket.foo.urls')),

     # Custom url
     url(r'^$', ListView.as_view(template_name="vikiticket_home.html",
                                 model=Event,
                                 context_object_name='events')),
     url(r'^(?P<event_slug>\w+)/(?P<slug>\w+)/$',
         PageView.as_view(), name='page_view'),
     url(r'^(?P<slug>\w+)/$', OrderView.as_view(), name='order_view'),
     # Redirect, should be removed
     url(r'^/event/(?P<slug>\w+)/order/$',
         OrderView.as_view(), name='order_view_slug'),
)
