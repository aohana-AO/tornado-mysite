from django.urls import path
from app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('juusyomap/', views.JuusyoMapView.as_view(), name='juusyomap'),
    path('juusyocreatemap/', views.CreatePostMap.map, name='juusyocreatemap'),
    path('juusyocreatemap2/', views.CreatePostMap.post, name='juusyocreatemap2'),
    path('post/<int:pk>',views.PostDetailView.as_view(),name='post_detail'),
    path('post/new',views.CreatePostView.as_view(),name='post_new'),
    path('post/<int:pk>edit/',views.PostEditView.as_view(),name='post_edit'),
    path('post/<int:pk>delete/',views.PostDeleteView.as_view(),name='post_delete'),
]
