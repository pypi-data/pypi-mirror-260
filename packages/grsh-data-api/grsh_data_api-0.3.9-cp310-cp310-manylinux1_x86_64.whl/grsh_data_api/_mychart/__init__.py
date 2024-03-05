_MPL_BACKEND = None


def set_mpl_backend(name: str = 'TkAgg'):
    assert name in ['agg', 'TkAgg']
    global _MPL_BACKEND
    _MPL_BACKEND = name


def get_mpl_backend():
    return _MPL_BACKEND
