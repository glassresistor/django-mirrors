from datetime import date
from django.forms import widgets


class ByteaInput(widgets.FileInput):
    def value_from_datadict(self, data, files, name):
        return buffer(files.get(name, None).read())
