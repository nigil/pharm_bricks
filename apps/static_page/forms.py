from django import forms


class QuestionForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Name'}))
    email = forms.EmailField(max_length=100,
                             error_messages={'invalid': 'Please enter a valid email address'},
                             widget=forms.TextInput(
                                attrs={'placeholder': 'Email'}
                             ))
    question = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Question',
        'class': 'adres',
        'rows': 2}))
