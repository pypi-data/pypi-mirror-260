from grsh_data_api import util
from grsh_data_api._service.edb import ServiceEdbHttp as __ServiceEdbHttp


__version__ = "0.3.9"
__release__ = f"{__version__}.20240305"


# http://patorjk.com/software/taag
LOGO = '''
   _____ _____   _____ _    _ 
  / ____|  __ \ / ____| |  | |
 | |  __| |__) | (___ | |__| |
 | | |_ |  _  / \___ \|  __  |
 | |__| | | \ \ ____) | |  | |
  \_____|_|  \_\_____/|_|  |_|    release=%s

''' % __release__


from .api import INIT, _get_global_var
