# getting path
from django.urls import path

# getting path
from . import views

urlpatterns = [
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('', views.index, name='index'),
    path('api/check/<str:shortlink>', views.check, name="check"),
    path('api/create/', views.create, name="create"),
    path('api/clicky/<str:shortlink>', views.clicks, name="clicks"),
    path('api/getAllLinks', views.get_all_links, name="get_all"),
    path('<str:shortlink>', views.rediretor, name="redirector")

]


# get / send page
# get / api/check json
# post / api/make -> call check internal fn -> write to db
