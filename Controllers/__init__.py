import importlib
import pkgutil
import flask_restx

namespaces = []

for _, module_name, _ in pkgutil.iter_modules(__path__):
    module = importlib.import_module(f".{module_name}", package=__name__)
    if (hasattr(module, 'ns') and
            isinstance(getattr(module, 'ns'), flask_restx.Namespace)):
        namespaces.append(getattr(module, 'ns'))


__all__ = ["namespaces"]
