default_app_config = 'api.apps.ApiConfig'

def register(flow_class):
    """Register a flow class at api"""
    from django.apps import apps
    apps.get_app_config('api').register(flow_class)
    return flow_class
