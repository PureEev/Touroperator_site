from django import forms


class ContactForm(forms.Form):
    From_Name = forms.CharField(
        min_length = 2,
        widget = forms.TextInput(
            attrs={'placeholder': 'Откуда'}
        )
    )
    To_Name = forms.CharField(
        min_length=2,
        widget=forms.TextInput(
            attrs={'placeholder': 'Куда'}
        )
    )
    my_date_field = forms.DateField(
        widget=forms.DateInput(
            attrs={'placeholder': 'Дата'}
        ))
