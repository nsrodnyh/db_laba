from django import forms


# class DatalistTextInput(forms.TextInput):
#     def __init__(self, datalist_choices, attrs=None):
#         self.datalist_choices = datalist_choices
#         super().__init__(attrs)
#
#     def render(self, name, value, attrs=None, renderer=None):
#         datalist_choices = ''
#         for item in self.datalist_choices:
#             datalist_choices += f'<option value="{item}">{item}</option>'
#         # datalist_choices = ' '.join(self.datalist_choices)
#         # output = super().render(name, value, attrs, renderer)
#         return f'<input type="text" list="last_name_datalist" name="last_name_field"><datalist id="last_name_datalist">{datalist_choices}</datalist>'


class DatalistWidget(forms.TextInput):
    def __init__(self, datalist_id, *args, **kwargs):
        self.datalist_id = datalist_id
        super().__init__(*args, **kwargs)

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs['list'] = self.datalist_id
        return attrs
