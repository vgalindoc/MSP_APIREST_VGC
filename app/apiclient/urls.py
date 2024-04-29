from django.urls import(
    path,
    include
)

from rest_framework.routers import DefaultRouter
from apiclient import views

#VERBOS FRAMEWORK REST
#/recipes/
router = DefaultRouter()
router.register('apiclients',views.apiclientViewSet)

app_name='apiclient'

urlpatterns = [   
    path('', include(router.urls)),
    
]