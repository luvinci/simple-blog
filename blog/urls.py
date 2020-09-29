from django.conf.urls import url
from blog import views


urlpatterns = [
    url(r"backend/categoryid/(?P<id>\d+)/$", views.backend_article),
    url(r"article/delete/$", views.delete_article),
    url(r"article/add/$", views.add_article),
    url(r"upload/$", views.upload_image),
    url(r"article/edit/(?P<id>\d+)$", views.edit_article),
    url(r"settings/$", views.setting),

    url(r"backend/category/$", views.backend_category),
    url(r"category/delete/$", views.delete_category),
    url(r"category/add/$", views.add_category),
    url(r"category/edit/$", views.edit_category),

    url(r"backend/tag/$", views.backend_tag),
    url(r"tag/delete/$", views.delete_tag),
    url(r"tag/add/$", views.add_tag),
    url(r"tag/edit/$", views.edit_tag),

    url(r"backend/$", views.backend_article),
    url(r"comment/$", views.article_comment),
    url(r"updown/$", views.article_up_down),
    url(r"(?P<username>\w+)/articles/(?P<article_id>\d+)/$", views.article_detail),
    url(r"(?P<username>\w+)/?(?P<condition>tagid|categoryid|archive)/(?P<param>.*)/$", views.user_home),
    url(r"(?P<username>\w+)/$", views.user_home),
]
