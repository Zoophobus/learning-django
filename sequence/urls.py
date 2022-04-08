from django.urls import path
from . import views

app_name = 'sequence'
urlpatterns = [
        path('',views.index, name='index'),
        path('results/',views.results,name='results'),
        path('add/',views.add,name='add'),
        path('select/',views.select,name='select'),
#        path('<int:seq_id>/delete/',views.delete,name='delete'),
        ]
