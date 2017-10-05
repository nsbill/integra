#!/usr/local/bin/python3
from http.server import BaseHTTPRequestHandler
from urllib import parse
import integra

class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = parse.urlparse(self.path)
        print(parsed_path)
        if parsed_path.path == "/check":
            message_parts = ['TEST',
            format(parsed_path.query),
            format(parsed_path.plain),
            ]
            message = '\n\r'.join(message_parts)
            self.send_response(200)
            self.send_header('Content-Type',
                             'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(message.encode('utf-8'))
        else:
            parsed_path = parse.urlparse(self.path)
            print(parsed_path.path)
            print(parse.urlparse(self.path))
            message_parts = [
                'CLIENT VALUES:',
                'client_address={} ({})'.format(
                        self.client_address,
                        self.address_string()),
                'command={}'.format(self.command),
                'path={}'.format(self.path),
                'real path={}'.format(parsed_path.path),
                'query={}'.format(parsed_path.query),
                'request_version={}'.format(self.request_version),
                '',
                'SERVER VALUES:',
                'server_version={}'.format(self.server_version),
                'sys_version={}'.format(self.sys_version),
                'protocol_version={}'.format(self.protocol_version),
                '',
                'HEADERS RECEIVED:',
            ]
            for name, value in sorted(self.headers.items()):
                message_parts.append(
                        '{}={}'.format(name, value.rstrip())
                        )
            print('-===-')
            print(parsed_path)
            value = message_parts[5]
            print(''.join(value))
            value=value.replace('query=','').split('&')
            print(value)
#            message_parts.append(value)
            message_parts.append('')
            message = '\r\n'.join(message_parts)
            print(message)
            self.send_response(200)
            self.send_header('Content-Type',
                             'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(message.encode('utf-8'))


if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('127.0.0.10', 6969), GetHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()