from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_app, get_models
from djangojsonschema.jsonschema import DjangoFormToJSONSchema
from django import forms
from django.utils import simplejson as json

def model_form_factory(model_class):
    class MyForm(forms.ModelForm):
        class Meta:
            model = model_class
    return MyForm
    
class Command(BaseCommand):
    args = '<app_id app_id ...>'
    help = 'Prints the json schema for models users model forms.'

    def handle(self, *args, **options):
        for arg in args:
            app = get_app(arg)
            for model in get_models(app):
                form_class = model_form_factory(model)
                schema_repr = DjangoFormToJSONSchema().convert_form(form_class)
                self.stdout.write('var %s_%s = %s;' % (arg, model.__name__.lower(),
                    json.dumps(schema_repr, sort_keys=True, indent=4)))
                self.stdout.write('\n')
