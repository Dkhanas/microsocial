# coding=utf-8
from django import forms
from django.utils.translation import ugettext as _
from dialogs.models import Message
from microsocial.forms import BootstrapFormMixin


class MessageForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Message
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(
                attrs={"class": " form-control",
                       "cols": "40", "id": "id_text",
                       "maxlength": "2000", "name": "text",
                       "rows": "4", "style": "margin-bottom: 10px;",
                       'placeholder': _(u'введіть повідомлення')})
                    }

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        BootstrapFormMixin.__init__(self)

    def clean_text(self):
        return self.cleaned_data['text'].strip()
