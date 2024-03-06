from django.urls import path

from giant_search import views

app_name = "giant_search"

urlpatterns = [
    path("", views.SearchView.as_view(), name="index"),
]
