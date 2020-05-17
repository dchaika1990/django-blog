from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # post views
    path(
        '',
        views.post_list,
        name='post_list'
    ),
    path(
        '<int:year>/<int:month>/<int:dat>/<slug:slug>',
        views.post_detail,
        name='post_detail'
    ),
]
