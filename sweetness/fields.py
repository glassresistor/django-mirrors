from django.db import models

class ContentField(models.ForeignKey):    
    
    def __init__(self, *args, **kwargs):
        self.encodings = kwargs.pop('encodings')
        self.required_fields = set(kwargs.pop('required_fields'))
        args = list(args)
        args.insert(0, 'asset.Asset')
        super(ContentField, self).__init__(*args,**kwargs)
