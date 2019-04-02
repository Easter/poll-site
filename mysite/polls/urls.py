from django.urls import path
from . import views
app_name = 'polls'
urlpatterns=[
    path('',views.IndexView.as_view(),name="index"),
    path('<int:pk>',views.DetailView.as_view(),name = "detail"),#DetailView期望从url中获取名为"pk"的主键值，所以把question改为pk
    path('<int:pk>/results/',views.ResultsView.as_view(),name = "results"),
    path('<int:question_id>/vote/',views.vote,name = "vote"),
]
