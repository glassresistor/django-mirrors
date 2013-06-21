from tastypie import fields
from mirrors import widgets

class ByteaField(fields.CharField):
    """
    Half filefield half binary field so much TODO here.
    """
    dehydrated_type = 'string'
    help_text = 'Unicode string data. Ex: "Hello World"'

    def convert(self, value):
        import ipdb; ipdb.set_trace()
        return None
