from typing import TypedDict


# Handler error responses
HANDLER_ERROR_NO_USERNAME = "Username is required"
HANDLER_ERROR_NO_STAGE_ID = "Stage ID is required"
HANDLER_ERROR_NO_QTY = "Quantity is required"
HANDLER_ERROR_QTY_NOT_INT = "Quantity must be an integer"
HANDLER_ERROR_STAGE_ID_NOT_INT = "Stage ID must be an integer"

HANDLER_ERROR_READ_FILE = "Internal server error"
HANDLER_ERROR_NOT_ENOUGH_TICKETS = "Not enough tickets in stock"
HANDLER_ERROR_STAGE_NOT_FOUND = "Stage not found"


responseErrorType = TypedDict('ErrorType', {'status': int, 'content': dict})
# HTTP Error responses
ERROR_NOT_ENOUGH_TICKET_LEFT: responseErrorType = {"status": 400,
                                                   "content": {"error": "Not enough tickets in stock!"}}
ERROR_STAGE_NOT_FOUND: responseErrorType = {"status": 400,
                                            "content": {"error": "Stage not found!"}}
ERROR_INTERNAL_SERVER: responseErrorType = {"status": 500,
                                            "content": {"error": "Internal server error"}}
ERROR_NOT_FOUND: responseErrorType = {"status": 404,
                                      "content": {"error": "Not found!"}}

ERROR_NO_USERNAME: responseErrorType = {"status": 400,
                                        "content": {"error": "Username required in query!"}}
ERROR_NO_STAGE_ID: responseErrorType = {"status": 400,
                                        "content": {"error": "Stage ID required in query!"}}
ERROR_NO_QTY: responseErrorType = {"status": 400,
                                   "content": {"error": "Quantity required in query!"}}
ERROR_QTY_NOT_INT: responseErrorType = {"status": 400,
                                        "content": {"error": "Quantity must be an integer!"}}
ERROR_STAGE_ID_NOT_INT: responseErrorType = {"status": 400,
                                             "content": {"error": "Stage ID must be an integer!"}}
