from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home),
    path('show_contacts/', show_contacts, name='show_contacts'),
    path('show_contacts/edit_contact/<int:contact_id>/', edit_contact, name='edit_contact'),
    path('show_contacts/delete/<int:contact_id>/', delete_contact, name='delete_contact'),
    path('edit_last_name_table/', edit_last_name_table, name='edit_last_name_table'),
    path('edit_last_name_table/delete_last_name/<int:last_name_id>/', delete_last_name, name='delete_last_name'),
    path('edit_last_name_table/edit_last_name/<int:last_name_id>/', edit_last_name, name='edit_last_name'),
    path('edit_first_name_table/', edit_first_name_table, name='edit_first_name_table'),
    path('edit_first_name_table/delete_first_name/<int:first_name_id>/', delete_first_name, name='delete_first_name'),
    path('edit_first_name_table/edit_first_name/<int:first_name_id>/', edit_first_name, name='edit_first_name'),
    path('edit_patronymic_table/', edit_patronymic_table, name='edit_patronymic_table'),
    path('edit_patronymic_table/delete_patronymic/<int:patronymic_id>/', delete_patronymic, name='delete_patronymic'),
    path('edit_patronymic_table/edit_patronymic/<int:patronymic_id>/', edit_patronymic, name='edit_patronymic'),
    path('edit_street_table/', edit_street_table, name='edit_street_table'),
    path('edit_street_table/delete_street/<int:street_id>/', delete_street, name='delete_street'),
    path('edit_street_table/edit_street/<int:street_id>/', edit_street, name='edit_street')
]
