from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.get_analysis_page, name='analysis'),
    path('<int:query_id>', views.get_summary_page, name='summary'),
    path('create', views.create_analysis, name='analysis_creation'),
    path('all', views.get_all_results, name='all_results')
]
