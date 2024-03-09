from django import forms
from django.forms import ModelMultipleChoiceField
from django.contrib.auth import get_user_model


class MyModelMultipleChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.username

class CreateChatForm(forms.Form):
    title = forms.CharField(label="Chat Name")
    members = MyModelMultipleChoiceField(
                        queryset=get_user_model().objects.all().order_by('username'),
                        widget=forms.CheckboxSelectMultiple,
                        to_field_name='username',
                        label="Active users"
                )

class CreateMessageForm(forms.Form):
    message = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea,
    )
    message.widget.attrs.update({
        'class': 'form-control',
        'rows': 1
    })
    author = forms.CharField(widget=forms.HiddenInput)
    chat = forms.CharField(widget=forms.HiddenInput)
    message_id = forms.CharField(widget=forms.HiddenInput, required=False)