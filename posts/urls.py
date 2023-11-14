from django.urls import path
from . import views

urlpatterns=[

    path('homepage/',views.homepage,name='posts_home'),
    path('',views.PostListCreateView.as_view(),name="getall_posts"),
    path('<str:pk>/',views.PostRetrieveUpdateDeleteView.as_view(),name="post_details"),
    path('current_user/',views.get_posts_for_current_user,name="Current User"),
    path('post_currentuser/',views.ListPostsForAuthor.as_view(),name="post-currentuser"),
    # path('listall',views.list_posts),
    # path('update/<str:pk>/',views.updatePost),
    # path('delete/<str:pk>/',views.deletePost)

]