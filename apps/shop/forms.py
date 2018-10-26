from django import forms


class OrderForm(forms.Form):
    PAYMENT_CHOICES = (('invoice', 'Invoice'),)
    use_user_address = forms.BooleanField(initial=True,
                                          widget=forms.CheckboxInput(
                                              attrs={
                                                'id': 'delivery_bch',
                                                'class': 'posit_black posit checkbox '
                                                         'checkbox_disabled'
                                              }
                                          ))
    delivery_type = forms.BooleanField(initial=True,
                                       widget=forms.CheckboxInput(
                                           attrs={
                                               'id': 'ups_bch',
                                               'class': 'posit_black posit checkbox '
                                                        'checkbox_disabled'
                                           }
                                       ))
    payment_type = forms.BooleanField(initial='invoice',
                                      widget=forms.CheckboxInput(
                                          attrs={
                                              'id': 'invoice_bch',
                                              'class': 'posit_black posit checkbox '
                                                       'checkbox_disabled'
                                          }
                                      ))
    comments = forms.CharField(required=False,
                                 widget=forms.Textarea(
                                     attrs={
                                         'class': 'wd_text check_wd_text',
                                         'placeholder': 'Your order comments'
                                     }
                                 ))
    agree_terms = forms.BooleanField(required=False, initial=False,
                                     widget=forms.CheckboxInput(
                                         attrs={
                                             'id': 'teams_bch',
                                             'class': 'posit checkbox'
                                         }
                                     ))

    def clean_use_user_address(self):
        use_user_address = self.cleaned_data.get('use_user_address')
        if not use_user_address:
            raise forms.ValidationError('Check this field to continue')
        return use_user_address

    def clean_agree_terms(self):
        agree_terms = self.cleaned_data.get('agree_terms')
        if not agree_terms:
            raise forms.ValidationError('Check this field to continue')
        return agree_terms
