from django.urls import path, include
from rest_framework import routers
# from rest_framework.documentation import include_docs_urls
from . import views

router = routers.DefaultRouter()
router.register(r'images', views.DatasetView, 'images')

urlpatterns = [
    path('', views.index),
    path('hello/<str:username>', views.hello),
    path('about/', views.about),
    path('datasets/', include(router.urls)),
    path('datasets/count/', views.DatasetView.as_view({'get': 'count'}), name='dataset-count')
]
