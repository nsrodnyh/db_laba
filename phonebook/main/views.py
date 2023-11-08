from django.shortcuts import render, redirect
from .forms import NewContactForm, SearchForm, NewLastNameForm, FilterForm
from django.db.utils import IntegrityError
from django.db import connection


def home(request):
    return redirect('show_contacts')


def show_contacts(request):
    cursor = connection.cursor()
    cursor.execute(
        '''SELECT main_main.id, main_lastname.last_name, main_firstname.first_name, main_patronymic.patronymic,
        main_street.street, 
        main_main.number, main_main.building, main_main.apartment, main_main.phone_number 
        FROM main_main LEFT JOIN main_lastname ON main_main.last_name_id=main_lastname.id LEFT JOIN main_firstname ON 
        main_main.first_name_id=main_firstname.id 
        LEFT JOIN main_patronymic ON main_main.patronymic_id=main_patronymic.id LEFT JOIN main_street ON 
        main_main.street_id=main_street.id
        ORDER BY main_lastname.last_name''')
    full_table = cursor.fetchall()

    if request.method == 'POST':
        print(request.POST)
        add_form = NewContactForm(request.POST)
        if add_form.is_valid():
            variables = []
            values = []
            data = add_form.cleaned_data
            cursor = connection.cursor()
            if data['last_name_field']:
                last_name = tuple([data['last_name_field']])
                variables.append('last_name_id')
                try:
                    cursor.execute('INSERT INTO main_lastname VALUES (default, %s)', last_name)
                except IntegrityError as e:
                    print('Integrity Error occurred')
                    print(e)
                cursor.execute('SELECT id FROM main_lastname WHERE last_name = %s', last_name)
                selected_values = cursor.fetchone()[0]
                values.append(str(selected_values))
            if data['first_name_field']:
                first_name = tuple([data['first_name_field']])
                variables.append('first_name_id')
                try:
                    cursor.execute('INSERT INTO main_firstname VALUES (default, %s)', first_name)
                except IntegrityError:
                    pass
                cursor.execute('SELECT id FROM main_firstname WHERE first_name = %s', first_name)
                selected_values = cursor.fetchone()[0]
                values.append(str(selected_values))
            if data['patronymic_field']:
                patronymic = tuple([data['patronymic_field']])
                variables.append('patronymic_id')
                try:
                    cursor.execute('INSERT INTO main_patronymic VALUES (default, %s)', patronymic)
                except IntegrityError:
                    pass
                cursor.execute('SELECT id FROM main_patronymic WHERE patronymic = %s', patronymic)
                selected_values = cursor.fetchone()[0]
                values.append(str(selected_values))
            if data['street_field']:
                street = tuple([data['street_field']])
                variables.append('street_id')
                try:
                    cursor.execute('INSERT INTO main_street VALUES (default, %s)', street)
                except IntegrityError:
                    pass
                cursor.execute('SELECT id FROM main_street WHERE street = %s', street)
                selected_values = cursor.fetchone()[0]
                values.append(str(selected_values))

            if data['house_number_field']:
                variables.append('number')
                values.append(str(data['house_number_field']))
            if data['building_field']:
                variables.append('building')
                values.append("'" + data['building_field'] + "'")
            if data['apartment_field']:
                variables.append('apartment')
                values.append(str(data['apartment_field']))
            if data['phone_number_field']:
                variables.append('phone_number')
                values.append("'" + data['phone_number_field'] + "'")

            var_string = ', '.join(variables)
            val_string = ', '.join(values)
            cursor.execute(f"INSERT INTO main_main ({var_string}) VALUES ({val_string})")
            return redirect('show_contacts')
    else:
        add_form = NewContactForm()

    all_last_name = []
    all_first_name = []
    all_patronymic = []
    all_street = []
    try:
        cursor.execute("SELECT last_name FROM main_lastname")
        all_last_name = cursor.fetchall()
        cursor.execute("SELECT first_name FROM main_firstname")
        all_first_name = cursor.fetchall()
        cursor.execute("SELECT patronymic FROM main_patronymic")
        all_patronymic = cursor.fetchall()
        cursor.execute("SELECT street FROM main_street")
        all_street = cursor.fetchall()
    except IntegrityError as e:
        print(e)
    cursor.close()

    form = SearchForm()
    template = 'show_contacts.html'
    context = {
        'form': form,
        'add_form': add_form,
        'table': full_table,
        'all_last_name': all_last_name,
        'all_first_name': all_first_name,
        'all_patronymic': all_patronymic,
        'all_street': all_street
    }
    return render(request, template, context)


def edit_contact(request, contact_id):
    cursor = connection.cursor()
    cursor.execute('''SELECT main_lastname.last_name, main_firstname.first_name, main_patronymic.patronymic,
        main_street.street,
        main_main.number, main_main.building, main_main.apartment, main_main.phone_number 
        FROM main_main LEFT JOIN main_lastname ON main_main.last_name_id=main_lastname.id LEFT JOIN main_firstname ON 
        main_main.first_name_id=main_firstname.id 
        LEFT JOIN main_patronymic ON main_main.patronymic_id=main_patronymic.id LEFT JOIN main_street ON 
        main_main.street_id=main_street.id 
        WHERE main_main.id = %s''', (contact_id,))
    result = cursor.fetchone()
    if request.method == 'POST':
        form = NewContactForm(request.POST)
        if form.is_valid():
            variables = []
            values = []
            data = form.cleaned_data
            if data['last_name_field']:
                last_name = [data['last_name_field']]
                variables.append('last_name_id')
                try:
                    cursor.execute("INSERT INTO main_lastname VALUES (default, %s)", tuple(last_name))
                except IntegrityError:
                    pass
                try:
                    cursor.execute("SELECT id FROM main_lastname WHERE last_name = %s", tuple(last_name))
                    last_name_id = cursor.fetchone()[0]
                    values.append(str(last_name_id))
                except IntegrityError:
                    print(
                        'An error occurred during query execution. Possible problem: the last name was not found in main_lastname table')
            if data['first_name_field']:
                first_name = [data['first_name_field']]
                variables.append('first_name_id')
                try:
                    cursor.execute("INSERT INTO main_firstname VALUES (default, %s)", tuple(first_name))
                except IntegrityError:
                    pass
                try:
                    cursor.execute("SELECT id FROM main_firstname WHERE first_name = %s", tuple(first_name))
                    first_name_id = cursor.fetchone()[0]
                    values.append(str(first_name_id))
                except IntegrityError:
                    print(
                        'An error occurred during query execution. Possible problem: the first name was not found in main_firstname table')
            if data['patronymic_field']:
                patronymic = [data['patronymic_field']]
                variables.append('patronymic_id')
                try:
                    cursor.execute("INSERT INTO main_patronymic VALUES (default, %s)", tuple(patronymic))
                except IntegrityError:
                    pass
                try:
                    cursor.execute("SELECT id FROM main_patronymic WHERE patronymic = %s", tuple(patronymic))
                    patronymic_id = cursor.fetchone()[0]
                    values.append(str(patronymic_id))
                except IntegrityError:
                    print(
                        'An error occurred during query execution. Possible problem: the patronymic was not found in main_patronymic table')
            if data['street_field']:
                street = [data['street_field']]
                variables.append('street_id')
                try:
                    cursor.execute("INSERT INTO main_street VALUES (default, %s)", tuple(street))
                except IntegrityError:
                    pass
                try:
                    cursor.execute("SELECT id FROM main_street WHERE street = %s", tuple(street))
                    street_id = cursor.fetchone()[0]
                    values.append(str(street_id))
                except IntegrityError:
                    print(
                        'An error occurred during query execution. Possible problem: the street was not found in street table')

            if data['house_number_field']:
                variables.append('number')
                values.append(str(data['house_number_field']))
            if data['building_field']:
                variables.append('building')
                values.append("'" + data['building_field'] + "'")
            if data['apartment_field']:
                variables.append('apartment')
                values.append(str(data['apartment_field']))
            if data['phone_number_field']:
                variables.append('phone_number')
                values.append("'" + data['phone_number_field'] + "'")

            var_string = ', '.join(variables)
            val_string = ', '.join(values)
            cursor.execute(f"UPDATE main_main SET ({var_string}) = ({val_string}) WHERE id = {contact_id}")
            cursor.close()
            return redirect('show_contacts')

    else:
        form = NewContactForm()
        form.fields['last_name_field'].initial = result[0] if result[0] != 'None' else ''
        form.fields['first_name_field'].initial = result[1]
        form.fields['patronymic_field'].initial = result[2] if result[2] != 'None' else ''
        form.fields['street_field'].initial = result[3] if result[3] != 'None' else ''
        form.fields['house_number_field'].initial = result[4] if result[4] != 'None' else ''
        form.fields['building_field'].initial = result[5] if result[5] != 'None' else ''
        form.fields['apartment_field'].initial = result[6] if result[6] != 'None' else ''
        form.fields['phone_number_field'].initial = result[7]

    template = 'edit_contact.html'
    context = {
        'form': form
    }
    return render(request, template, context)


def delete_contact(request, contact_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM main_main WHERE id = %s", (contact_id,))
    cursor.close()

    return redirect('show_contacts')


def edit_last_name_table(request):
    cursor = connection.cursor()
    cursor.execute("SELECT id, last_name FROM main_lastname ORDER BY last_name")
    full_table = cursor.fetchall()

    if request.method == "POST":
        form = NewLastNameForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['new_last_name_field']:
                try:
                    cursor.execute("INSERT INTO main_lastname VALUES (default, %s)", (data['new_last_name_field'],))
                    cursor.close()
                except IntegrityError as e:
                    print(e)
            return redirect('edit_last_name_table')
        else:
            print('Form is not valid')
    else:
        form = NewLastNameForm()

    template = 'edit_last_name_table.html'
    context = {
        'table': full_table,
        'form': form
    }

    return render(request, template, context)


def delete_last_name(request, last_name_id):
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM main_lastname WHERE id = %s", (last_name_id, ))
        cursor.close()
    except IntegrityError as e:
        print(e)

    return redirect('edit_last_name_table')


def edit_last_name(request, last_name_id):
    cursor = connection.cursor()
    if request.method == "POST":
        form = NewLastNameForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                cursor.execute("UPDATE main_lastname SET last_name = %s WHERE id = %s", (data['new_last_name_field'], last_name_id))
            except IntegrityError as e:
                print(e)
            return redirect('edit_last_name_table')
    else:
        form = NewLastNameForm()
        cursor.execute("SELECT last_name FROM main_lastname WHERE id = %s", (last_name_id,))
        last_name = cursor.fetchone()[0]
        form.fields['new_last_name_field'].initial = last_name
    cursor.close()

    template = 'edit_last_name.html'
    context = {
        'form': form
    }
    return render(request, template, context)


def edit_first_name_table(request):
    cursor = connection.cursor()
    cursor.execute("SELECT id, first_name FROM main_firstname ORDER BY first_name")
    full_table = cursor.fetchall()

    if request.method == 'POST':
        form = NewLastNameForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['new_last_name_field']:
                try:
                    cursor.execute("INSERT INTO main_firstname VALUES (default, %s)", (data['new_last_name_field'],))
                    cursor.close()
                except IntegrityError as e:
                    print(e)
            return redirect('edit_first_name_table')
    else:
        form = NewLastNameForm()

    template = 'edit_first_name_table.html'
    context = {
        'table': full_table,
        'form': form
    }

    return render(request, template, context)


def edit_first_name(request, first_name_id):
    cursor = connection.cursor()
    if request.method == "POST":
        form = NewLastNameForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                cursor.execute("UPDATE main_firstname SET first_name = %s WHERE id = %s",
                               (data['new_last_name_field'], first_name_id))
            except IntegrityError as e:
                print(e)
            return redirect('edit_first_name_table')
    else:
        form = NewLastNameForm()
        cursor.execute("SELECT first_name FROM main_firstname WHERE id = %s", (first_name_id,))
        first_name = cursor.fetchone()[0]
        form.fields['new_last_name_field'].initial = first_name
    cursor.close()

    template = 'edit_first_name.html'
    context = {
        'form': form
    }
    return render(request, template, context)


def delete_first_name(request, first_name_id):
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM main_firstname WHERE id = %s", (first_name_id,))
        cursor.close()
    except IntegrityError as e:
        print(e)

    return redirect('edit_first_name_table')


def edit_street_table(request):
    cursor = connection.cursor()
    cursor.execute("SELECT id, street FROM main_street ORDER BY street")
    full_table = cursor.fetchall()

    if request.method == 'POST':
        form = NewLastNameForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['new_last_name_field']:
                try:
                    cursor.execute("INSERT INTO main_street VALUES (default, %s)", (data['new_last_name_field'],))
                    cursor.close()
                except IntegrityError as e:
                    print(e)
            return redirect('edit_street_table')
    else:
        form = NewLastNameForm()

    template = 'edit_street_table.html'
    context = {
        'table': full_table,
        'form': form
    }

    return render(request, template, context)


def edit_street(request, street_id):
    cursor = connection.cursor()
    if request.method == "POST":
        form = NewLastNameForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                cursor.execute("UPDATE main_street SET street = %s WHERE id = %s",
                               (data['new_last_name_field'], street_id))
            except IntegrityError as e:
                print(e)
            return redirect('edit_street_table')
    else:
        form = NewLastNameForm()
        cursor.execute("SELECT street FROM main_street WHERE id = %s", (street_id,))
        street = cursor.fetchone()[0]
        form.fields['new_last_name_field'].initial = street
    cursor.close()

    template = 'edit_street.html'
    context = {
        'form': form
    }
    return render(request, template, context)


def delete_street(request, street_id):
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM main_street WHERE id = %s", (street_id,))
        cursor.close()
    except IntegrityError as e:
        print(e)

    return redirect('edit_street_table')


def edit_patronymic_table(request):
    cursor = connection.cursor()
    cursor.execute("SELECT id, patronymic FROM main_patronymic ORDER BY patronymic")
    full_table = cursor.fetchall()

    if request.method == 'POST':
        form = NewLastNameForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['new_last_name_field']:
                try:
                    cursor.execute("INSERT INTO main_patronymic VALUES (default, %s)", (data['new_last_name_field'],))
                    cursor.close()
                except IntegrityError as e:
                    print(e)
            return redirect('edit_patronymic_table')
    else:
        form = NewLastNameForm()

    template = 'edit_patronymic_table.html'
    context = {
        'table': full_table,
        'form': form
    }

    return render(request, template, context)


def edit_patronymic(request, patronymic_id):
    cursor = connection.cursor()
    if request.method == "POST":
        form = NewLastNameForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                cursor.execute("UPDATE main_patronymic SET patronymic = %s WHERE id = %s",
                               (data['new_last_name_field'], patronymic_id))
            except IntegrityError as e:
                print(e)
            return redirect('edit_first_name_table')
    else:
        form = NewLastNameForm()
        cursor.execute("SELECT patronymic FROM main_patronymic WHERE id = %s", (patronymic_id,))
        patronymic = cursor.fetchone()[0]
        form.fields['new_last_name_field'].initial = patronymic
    cursor.close()

    template = 'edit_patronymic.html'
    context = {
        'form': form
    }
    return render(request, template, context)


def delete_patronymic(request, patronymic_id):
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM main_patronymic WHERE id = %s", (patronymic_id,))
        cursor.close()
    except IntegrityError as e:
        print(e)

    return redirect('edit_patronymic_table')
