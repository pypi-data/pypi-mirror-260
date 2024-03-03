from fumedev import env
from fumedev.language_servers.javascript_server import JavaScriptLanguageServer
from fumedev.language_servers.python_server import PythonLanguageServer
def check_error(file_path):
    extension = file_path.split('.')[-1]

    if extension == 'py':
        
        jls = PythonLanguageServer(file_path)
        errors = jls.has_syntax_error()
        return errors
    
    elif extension == 'js' or extension == 'ts' or extension == 'jsx' or extension == 'tsx':
        
        jsls = JavaScriptLanguageServer(env.absolute_path('codebase'))
        jsls.start_lsp_server()
        errors = jsls.find_syntax_errors(file_path)
        jsls.cleanup()
        return errors