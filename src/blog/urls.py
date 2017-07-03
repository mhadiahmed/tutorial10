from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    url(r'^$',views.post_list,name='list' ),
    url(r'^create/',views.post_create ),
    url(r'^(?P<id>\d+)/$',views.post_detail , name='detail'),
    url(r'^(?P<id>\d+)/edit/$',views.post_update , name='update'),
    url(r'^(?P<id>\d+)/delete/$',views.post_delete , name='delete'),
    ]


if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)