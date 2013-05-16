from tastypie.api import Api
from mirrors.api import resources

v1 = Api(api_name='v1')

v1.register(resources.AssetResource())
v1.register(resources.ContentResource())
v1.register(resources.ContentAttributeResource())
