from django.forms import fields
from mirrors import widgets

class ByteaField(fields.FileField):
    widget = widgets.ByteaInput
    
    def clean(self, data, initial=None):
        if initial and not data:
            return initial
        else:
            return data
