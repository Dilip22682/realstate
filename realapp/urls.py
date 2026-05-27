from django.urls import path

from .views import (
    home,
    register_view,
    login_view,
    logout_view,
    dashboard,
    create_property,
    property_list,
    property_detail,
    update_property,
    delete_property,
    contact,
    about
)

urlpatterns = [

    path('', home, name='home'),

    path('register/', register_view, name='register'),

    path('login/', login_view, name='login'),

    path('logout/', logout_view, name='logout'),

    path('dashboard/', dashboard, name='dashboard'),

    path('properties/', property_list, name='properties'),

    path('property/<int:id>/', property_detail, name='property_detail'),

    path('create-property/', create_property, name='create_property'),

    path('property/<int:pk>/edit/',update_property,name='update_property'),

    path('property/<int:pk>/delete/',delete_property,name='delete_property'),

    path('contact/',contact, name='contact'),
 
    path('about/',about, name='about'),
    

]


 