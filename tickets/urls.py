from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('create/', views.ticket_create, name='ticket_create'),
    path('update/<int:id>/', views.ticket_update, name='ticket_update'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('', views.login_view, name='login'),
    path('my_tickets/', views.my_tickets, name='my_tickets'),
    path('tickets/files/<int:ticket_id>/', views.serve_ticket_file, name='serve_ticket_file'),

]
