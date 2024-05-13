import datetime
import json
from threading import Semaphore
import uuid
import csv
import os
import constants

dirname = os.path.dirname(__file__)
STAGES_DB = os.path.join(dirname, "db/stages.json")
TICKETS_DB = os.path.join(dirname, "db/tickets.csv")


def get_stages(lockStages: Semaphore):
    lockStages.acquire()
    with open(STAGES_DB, "r") as f:
        stages = json.load(f)
    lockStages.release()
    return stages


def get_my_tickets(username: str, lockTickets: Semaphore):
    # check username
    if not username:
        return constants.HANDLER_ERROR_NO_USERNAME

    # CSV: ticket_id,stage_id,timestamp,username
    tickets = []
    lockTickets.acquire()
    with open(TICKETS_DB, "r") as f:
        reader = csv.reader(f, delimiter=",")
        next(reader, None)  # skip the headers
        try:
            for row in reader:
                if row[3] == username:
                    tickets.append(row)
        except csv.Error:
            lockTickets.release()
            return constants.HANDLER_ERROR_READ_FILE
    lockTickets.release()

    # convert to dict
    tickets = [{
        "ticket_id": ticket[0],
        "stage_id": int(ticket[1]),
        "timestamp": ticket[2],
        "username": ticket[3]
    } for ticket in tickets]

    return tickets


def buy_ticket(stage_id: int, qty: int, username: str, lockStages: Semaphore, lockTickets: Semaphore):
    if not username:
        return constants.HANDLER_ERROR_NO_USERNAME

    if not stage_id:
        return constants.HANDLER_ERROR_NO_STAGE_ID

    if not type(stage_id) == int:
        return constants.HANDLER_ERROR_STAGE_ID_NOT_INT

    if not qty:
        return constants.HANDLER_ERROR_NO_QTY

    if not type(qty) == int:
        return constants.HANDLER_ERROR_QTY_NOT_INT

    stage_id = int(stage_id)
    qty = int(qty)

    lockStages.acquire()
    with open(STAGES_DB, "r") as f:
        stages = json.load(f)

    # reduce ticket stock
    found = False

    for stage in stages:
        if stage["stage_id"] == stage_id:
            if (stage["ticket_stock"] < qty):
                lockStages.release()
                return constants.HANDLER_ERROR_NOT_ENOUGH_TICKETS

            stage["ticket_stock"] -= qty
            found = True
            break
    if not found:
        lockStages.release()
        return constants.HANDLER_ERROR_STAGE_NOT_FOUND

    with open(STAGES_DB, "w") as f:
        json.dump(stages, f)
    lockStages.release()

    tickets = [{
        "ticket_id": str(uuid.uuid4()),
        "stage_id": stage_id,
        "timestamp": datetime.datetime.now().isoformat(),
        "username": username
    } for _ in range(qty)]

    rows_to_write = [[ticket['ticket_id'], ticket['stage_id'],
                      ticket['timestamp'], ticket['username']] for ticket in tickets]

    # add to tickets db
    # CSV: ticket_id,stage_id,timestamp,username
    lockTickets.acquire()
    with open(TICKETS_DB, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows_to_write)
    lockTickets.release()

    return tickets
