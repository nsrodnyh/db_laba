from django import forms
from django.db import connection
from django.db.utils import IntegrityError


class NewContactForm(forms.Form):
    last_name_field = forms.CharField(max_length=20, required=False, label='Фамилия',
                                      widget=forms.TextInput(attrs={'list': 'last-name-examples'}))
    first_name_field = forms.CharField(max_length=20, label='Имя',
                                       widget=forms.TextInput(attrs={'list': 'first-name-examples'}))
    patronymic_field = forms.CharField(max_length=30, required=False, label='Отчество',
                                       widget=forms.TextInput(attrs={'list': 'patronymic-examples'}))
    street_field = forms.CharField(max_length=50, required=False, label='Улица',
                                   widget=forms.TextInput(attrs={'list': 'street-examples'}))
    house_number_field = forms.IntegerField(label='Дом', required=False)
    building_field = forms.CharField(max_length=4, required=False, label='Корпус')
    apartment_field = forms.IntegerField(label='Квартира', required=False)
    phone_number_field = forms.CharField(max_length=14, label='Номер телефона')


class SearchForm(forms.Form):
    search_query_field = forms.CharField(required=False, label='')


class NewLastNameForm(forms.Form):
    new_last_name_field = forms.CharField(required=False, label='', max_length=20,
                                          widget=forms.TextInput(attrs={'placeholder': 'Введите новое значение'}))


class FilterForm(forms.Form):
    last_name_choice_field = forms.ChoiceField(choices=[], required=False, label='Фамилия')
    first_name_choice_field = forms.ChoiceField(choices=[], required=False, label='Имя')
    patronymic_choice_field = forms.ChoiceField(choices=[], required=False, label='Отчество')
    street_choice_field = forms.ChoiceField(choices=[], required=False, label='Улица')

    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT last_name FROM main_lastname")
            all_last_name = cursor.fetchall()
            all_last_name = [('', '')] + [(last_name, last_name) for last_name, in all_last_name]
            cursor.execute("SELECT first_name FROM main_firstname")
            all_first_name = cursor.fetchall()
            all_first_name = [('', '')] + [(first_name, first_name) for first_name, in all_first_name]
            cursor.execute("SELECT patronymic FROM main_patronymic")
            all_patronymic = cursor.fetchall()
            all_patronymic = [('', '')] + [(patronymic, patronymic) for patronymic, in all_patronymic]
            cursor.execute("SELECT street FROM main_street")
            all_street = cursor.fetchall()
            all_street = [('', '')] + [(street, street) for street, in all_street]

            self.fields['last_name_choice_field'].choices = all_last_name
            self.fields['first_name_choice_field'].choices = all_first_name
            self.fields['patronymic_choice_field'].choices = all_patronymic
            self.fields['street_choice_field'].choices = all_street
        except IntegrityError as e:
            print(e)
