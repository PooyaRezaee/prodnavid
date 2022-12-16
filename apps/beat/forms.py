from django import forms
from apps.PanelNavid.models import Message
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3

class MessageForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'bg-dark text-light'

    class Meta:
        model = Message
        exclude = ("meta","user","seen")

        widgets = {
            'message': forms.Textarea(attrs={'id':'message'}),
        }
    
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Send Message', css_class='btn btn-primary w-100'))
    helper.form_method = 'POST'
