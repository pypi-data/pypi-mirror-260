from django.urls import include, path

from .views import demo_index, demo_list, demo_messages

urlpatterns = [
    path("rt_messages/", include("pluto_rt.urls")),
    path("list/", view=demo_list, name="demo_list"),
    path("messages/", view=demo_messages, name="demo_messages"),
    path("", view=demo_index),
]
