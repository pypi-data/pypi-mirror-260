import subprocess
import threading
from pylspclient import JsonRpcEndpoint, LspEndpoint, LspClient

class JavaScriptLanguageServer:
    def __init__(self, project_path):
        self.project_path = project_path
        self.syntax_errors = []
        self.diagnostics_received = threading.Event()
        self.lsp_client, self.lsp_server_process = self.start_lsp_server()

    def handle_log_message(self, params):
        print(f"Log Message from LSP Server: {params['message']}")

    def handle_diagnostics(self, params):
        diagnostics = params['diagnostics']
        for diagnostic in diagnostics:
            if 'use of undeclared variable' in diagnostic['message']:
                continue
            error_message = f"{diagnostic['message']} between line {diagnostic['range']['start']['line']} - {diagnostic['range']['end']['line']}"
            self.syntax_errors.append(error_message)
        # Signal that diagnostics have been received
        self.diagnostics_received.set()

    def start_lsp_server(self):
        lsp_server_process = subprocess.Popen(
            ['npx', 'quick-lint-js', '--lsp'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        json_rpc_endpoint = JsonRpcEndpoint(lsp_server_process.stdin, lsp_server_process.stdout)

        notify_callbacks = {
            "window/logMessage": self.handle_log_message,
            "textDocument/publishDiagnostics": self.handle_diagnostics,
        }
        lsp_endpoint = LspEndpoint(json_rpc_endpoint, notify_callbacks=notify_callbacks)

        lsp_client = LspClient(lsp_endpoint)

        lsp_client.initialize(
            processId=None,
            rootPath=None,
            rootUri=f'file://{self.project_path}',
            initializationOptions=None,
            capabilities={},  # Populate as needed
            trace='off',
            workspaceFolders=None
        )

        return lsp_client, lsp_server_process

    def find_syntax_errors(self, file_path):
        self.syntax_errors.clear()  # Clear previous syntax errors
        self.diagnostics_received.clear()

        extension = file_path.split('.')[-1]

        language_name  = 'javascript' if extension in ['js', 'jsx'] else 'typescript'

        with open(file_path, 'r') as file:
            file_content = file.read()

        self.lsp_client.didOpen({
            'uri': f'file://{file_path}',
            'languageId': language_name,
            'version': 1,
            'text': file_content
        })

        # Wait for diagnostics to be received
        self.diagnostics_received.wait()

        # Send a didClose notification to the LSP server for the file
        self.didClose(f'file://{file_path}')

        return self.syntax_errors
    
    def didClose(self, uri):
        """
        Manually send a didClose notification to the LSP server using JSON RPC.
        """
        params = {
            "textDocument": {
                "uri": uri
            }
        }
        self.lsp_client.lsp_endpoint.send_notification("textDocument/didClose", params=params)

    def cleanup(self):
        self.lsp_client.shutdown()
        self.lsp_client.exit()
        self.lsp_client.lsp_endpoint.stop()
        self.lsp_client.lsp_endpoint.join()
        self.lsp_server_process.terminate()

# Example usage:
if __name__ == "__main__":
    file_path = '/Users/metehanoz/Downloads/codebase/src/components/Header/Header.js'
    project_path = '/Users/metehanoz/Downloads/codebase'
    syntax_error_finder = JavaScriptLanguageServer(project_path)
    errors = syntax_error_finder.find_syntax_errors(file_path)
    syntax_error_finder.cleanup()
    print(errors)
