from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules
from material.frontend.apps import ModuleMixin

class ApiConfig(AppConfig):
    """Application config for api."""
    name = 'api'
    
    def __init__(self, app_name, app_module):
        super(ApiConfig, self).__init__(app_name, app_module)
        self._registry = []

    def register(self, flow_class):
        if flow_class not in self._registry:
            self._registry.append(flow_class)

    def ready(self):
        autodiscover_modules('flows', register_to=self)

    @property
    def flows(self):
        return self._registry
