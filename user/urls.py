from django.urls import path

from user import views
from django.utils.translation import gettext_lazy as _
urlpatterns = [
    path('', views.index, name='user_index'),
    path('editer', views.user_update, name='user_update'),
    path('mot-de-passe', views.user_password, name='user_password'),
    path('commentaires', views.user_comments, name='user_comments'),
    path('messages', views.user_messages, name='user_messages'),

    path('produits', views.user_places, name='user_places'),
    path('list-de-souhaits', views.user_wishlist, name='user_wishlist'),
    path('supprimer-un-commentaire/<int:id>', views.user_delete_comment, name='user_delete_comment'),
    path('supprimer-un-message/<int:id>', views.user_delete_message, name='user_delete_message'),
    path('supprimer-un-produit/<int:id>', views.user_delete_place, name='user_delete_place'),
    path('editer-un-produit/<int:id>', views.user_update_place, name='user_update_place'),
    path('version-arabe-dun-produit/<int:place_id>/<int:id>', views.user_update_multilang_place, name='user_update_multilang_place'),
    path('aimer-un-produit/<int:id>', views.likeplace, name='likeplace'),
    path('ajouter-un-produit',views.user_add_place,name='user_add_place'),
    path('ajouter-sa-version-arabe/<int:id>',views.user_add_place_multilang,name='user_add_place_multilang'),
    path('ajouter-une-image/<int:id>',views.user_add_image,name='user_add_image'),
    path('supprimer-une-image/<int:place_id>/<int:image_id>', views.user_delete_image, name='user_delete_image'),

]
