from django.urls import path

from user import views
from django.utils.translation import gettext_lazy as _
urlpatterns = [
    path('', views.index, name='user_index'),
    path('update', views.user_update, name='user_update'),
    path('password', views.user_password, name='user_password'),
    path('comments', views.user_comments, name='user_comments'),
    path('messages', views.user_messages, name='user_messages'),

    path('places', views.user_places, name='user_places'),
    path('wishlist', views.user_wishlist, name='user_wishlist'),
    path('delete_comment/<int:id>', views.user_delete_comment, name='user_delete_comment'),
    path('delete_place/<int:id>', views.user_delete_place, name='user_delete_place'),
    path('update_place/<int:id>', views.user_update_place, name='user_update_place'),
    path('update_multilang_place/<int:place_id>/<int:id>', views.user_update_multilang_place, name='user_update_multilang_place'),
    path('like/<int:id>', views.likeplace, name='likeplace'),
    path('add_place',views.user_add_place,name='user_add_place'),
    path('add_place_multilang/<int:id>',views.user_add_place_multilang,name='user_add_place_multilang'),
    path('add_image/<int:id>',views.user_add_image,name='user_add_image'),
    path('delete_image/<int:place_id>/<int:image_id>', views.user_delete_image, name='user_delete_image'),

]
