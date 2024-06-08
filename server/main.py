from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import json
from time import sleep
from threading import Semaphore
from typing import TypedDict
from urllib.parse import urlparse, parse_qs
from handlers import get_stages, buy_ticket, get_my_tickets
import constants


class Handler(BaseHTTPRequestHandler):
    semaphoreStages = Semaphore(1)
    semaphoreTickets = Semaphore(1)

    # to allow cors
    def allow_cors(self): # berfungsi untuk mengizinkan CORS (Cross-Origin Resource Sharing) agar server bisa diakses oleh domain lain
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def create_response(self, status: int, content: str): # def create_response berfungsi untuk membuat response dari server, dengan status code dan content yang diberikan
        self.send_response(status)
        self.allow_cors()
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(content.encode('utf8')) 

    def create_response_error(self, error_obj: constants.responseErrorType): # def create_response_error berfungsi untuk membuat response error dari server, dengan error_obj yang diberikan
        self.send_response(error_obj['status'])
        self.allow_cors()
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(error_obj['content']).encode('utf8')) # response yang berupa json di encode ke utf8 agar bisa dibaca oleh client yang meminta response

    # OPTIONS request
    def do_OPTIONS(self): 
        self.send_response(200)
        self.allow_cors()
        self.end_headers()

    # GET request
    def do_GET(self): # def do_GET berfungsi untuk menangani request GET dari client
        parsed_url = urlparse(self.path)
        query = parse_qs(parsed_url.query)

        match parsed_url.path:
            case '/':
                self.create_response(200, json.dumps({"test": 'Hello world!'}))

            case "/stages":
                stages = get_stages(self.semaphoreStages)
                self.create_response(200, json.dumps(stages))

            case "/my-tickets":
                # get query "username"
                username = query.get('username', [None])[0]
                my_tickets = get_my_tickets(
                    username, self.semaphoreTickets)

                match my_tickets:
                    case constants.HANDLER_ERROR_NO_USERNAME:
                        self.create_response_error(constants.ERROR_NO_USERNAME)
                    case constants.HANDLER_ERROR_READ_FILE:
                        self.create_response_error(
                            constants.ERROR_INTERNAL_SERVER)
                    # success
                    case _:
                        self.create_response(200, json.dumps(my_tickets))

            case _:
                self.create_response_error(constants.ERROR_NOT_FOUND)

    # POST request
    def do_POST(self):
        parsed_url = urlparse(self.path)
        query = parse_qs(parsed_url.query)

        match self.path:
            case '/buy-tickets':
                # get body and parse json
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                post_data = json.loads(post_data)
                stage_id = post_data.get('stage_id', None)
                qty = post_data.get('qty', None)
                username = post_data.get('username', None)

                result = buy_ticket(
                    stage_id, qty, username, self.semaphoreStages, self.semaphoreTickets)

                match result:
                    case constants.HANDLER_ERROR_NO_USERNAME:
                        self.create_response_error(constants.ERROR_NO_USERNAME)
                    case constants.HANDLER_ERROR_NO_STAGE_ID:
                        self.create_response_error(constants.ERROR_NO_STAGE_ID)
                    case constants.HANDLER_ERROR_NO_QTY:
                        self.create_response_error(constants.ERROR_NO_QTY)
                    case constants.HANDLER_ERROR_QTY_NOT_INT:
                        self.create_response_error(constants.ERROR_QTY_NOT_INT)
                    case constants.HANDLER_ERROR_STAGE_ID_NOT_INT:
                        self.create_response_error(
                            constants.ERROR_STAGE_ID_NOT_INT)
                    case constants.HANDLER_ERROR_NOT_ENOUGH_TICKETS:
                        self.create_response_error(
                            constants.ERROR_NOT_ENOUGH_TICKET_LEFT)
                    case constants.HANDLER_ERROR_STAGE_NOT_FOUND:
                        self.create_response_error(
                            constants.ERROR_STAGE_NOT_FOUND)
                    # success
                    case _:
                        self.create_response(200, json.dumps(result))

            case _:
                self.create_response_error(constants.ERROR_NOT_FOUND)


def run():
    server = ThreadingHTTPServer(('0.0.0.0', 4444), Handler) # server dijalankan pada port 4444
    server.serve_forever()


if __name__ == '__main__':
    run()
