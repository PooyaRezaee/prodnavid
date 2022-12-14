from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from apps.beat.models import Beat,Category
from .models import SiteSettings

__all__ = [
    'CreateBeatForm',
    'CreateCategoryForm',
    'SendEmailForm',
    'SettingSiteForm',
    'UpdateBeatForm',
    'UpdateCategoryForm',
]

class CreateBeatForm(forms.ModelForm):
    class Meta:
        model = Beat

        exclude = ('code','time_audio','hits')

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Add Beat', css_class='btn btn-primary w-100'))
    helper.form_method = 'POST'

class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category

        fields = '__all__'

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Add Category', css_class='btn btn-primary w-100'))
    helper.form_method = 'POST'

class SendEmailForm(forms.Form):
    subject = forms.CharField(label='Subject')
    message = forms.CharField(widget=forms.Textarea(),label='Message')

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Send', css_class='btn btn-primary w-100'))
    helper.form_method = 'POST'

class SettingSiteForm(forms.ModelForm):
    class Meta:
        model = SiteSettings

        fields = '__all__'

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Update Information Site', css_class='btn btn-primary w-100'))
    helper.form_method = 'POST'


class UpdateBeatForm(forms.ModelForm):
    class Meta:
        model = Beat

        exclude = ('hits',)

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Update', css_class='btn btn-primary w-100'))
    helper.form_method = 'POST'

class UpdateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category

        fields = '__all__'

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Update', css_class='btn btn-primary w-100'))
    helper.form_method = 'POST'