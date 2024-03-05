from .edb import ServiceEdb, ServiceEdbHttp


_SERVICE_EDB = {
    'name': 'http',
    'class_obj': ServiceEdbHttp,
    'option': dict()
}


def set_service_edb(name: str, class_obj: ServiceEdb, option: dict):
    global _SERVICE_EDB
    _SERVICE_EDB['name'] = name
    _SERVICE_EDB['class_obj'] = class_obj
    _SERVICE_EDB['option'] = option


def get_service_edb():
    global _SERVICE_EDB
    return _SERVICE_EDB
