from django.urls import path
from .views import *

urlpatterns = [

    path('', list_view, name="index"),
    path('new/', new_view),
    path('<int:id>/', show_edit_view, name='show_edit'),
    path('<int:id>/edit/', edit_form_view, name='edit_form'),
    path('<int:id>/delete', delete_view, name='delete'),
    path('<int:id>/comment/', comment_view, name='comment'),
    path('<int:id>/posts', user_posts, name='user_posts'),

]
