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


def get_stages(lockStages: Semaphore): # def get_stages berfungsi untuk mengambil data stages dari file stages.json, dan lockstage Semaphore digunakan sebagai handle proses read dan write file stages.json
    with open(STAGES_DB, "r") as f: 
        stages = json.load(f) 
    lockStages.release() # berfungsi untuk melepaskan lock pada file stages.json agar bisa diakses oleh proses lain
    return stages


def get_my_tickets(username: str, lockTickets: Semaphore): # def get_my_tickets berfungsi untuk mengambil data tiket yang dimiliki oleh user berdasarkan username, dan lockTickets Semaphore digunakan sebagai handle proses read dan write file tickets.csv
    if not username:
        return constants.HANDLER_ERROR_NO_USERNAME

    # CSV: ticket_id,stage_id,timestamp,username
    tickets = []
    lockTickets.acquire() # berfungsi untuk mengunci file tickets.csv agar tidak bisa diakses oleh proses lain
    with open(TICKETS_DB, "r") as f:
        reader = csv.reader(f, delimiter=",")
        next(reader, None)  # skip the headers
        try: 
            for row in reader:
                if row[3] == username:
                    tickets.append(row) 
        except csv.Error:
            lockTickets.release() # berfungsi untuk melepaskan lock pada file tickets.csv agar bisa diakses oleh proses lain
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


def buy_ticket(stage_id: int, qty: int, username: str, lockStages: Semaphore, lockTickets: Semaphore): # def buy_ticket berfungsi untuk membeli tiket berdasarkan stage_id, qty, dan username, dan lockStages dan lockTickets Semaphore digunakan sebagai handle proses read dan write file stages.json dan tickets.csv
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
