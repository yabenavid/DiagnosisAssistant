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
    path('dataset/', views.list_files_view),
    path('dataset/view', views.show_images),
    # path('upload-image/', views.upload_images_view, name='upload_image'),
    # path('docs/', include_docs_urls(title='Management Dataset API'))
    path('api/v1/datasets/', include(router.urls)),
    path('api/v1/datasets/count/', views.DatasetView.as_view({'get': 'count'}), name='dataset-count')
]
