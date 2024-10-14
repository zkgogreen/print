from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('edit/<int:id>', views.edit, name="edit"),
    path('add', views.add, name="add"),
    path('addSub/<int:id>', views.addSub, name="addSub"),
    path('editSub/<int:id>', views.editSub, name="editSub"),
    path('deleteSub/<int:id>', views.deleteSub, name="deleteSub"),
]