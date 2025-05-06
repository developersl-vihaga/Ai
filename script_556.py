"""
Event handling system
Every "major" event in Empire (loosely defined as everything you'd want to
go into a report) is logged to the database. This file contains functions
which help manage those events - logging them, fetching them, etc.
"""
import json
from pydispatch import dispatcher
def agent_rename(old_name, new_name):
    """
    Helper function for reporting agent name changes.
    old_name - agent's old name
    new_name - what the agent is being renamed to
    """
    message = "[*] Agent {} has been renamed to {}".format(old_name, new_name)
    signal = json.dumps({
        'print': False,
        'message': message,
        'old_name': old_name,
        'new_name': new_name,
        'event_type' : 'rename'
    })
    dispatcher.send(signal, sender="agents/{}".format(old_name))
    dispatcher.send(signal, sender="agents/{}".format(new_name))
def log_event(cur, name, event_type, message, timestamp, task_id=None):
    """
    Log arbitrary events
    cur        - a database connection object (such as that returned from
                 `get_db_connection()`)
    name       - the sender string from the dispatched event
    event_type - the category of the event - agent_result, agent_task,
                 agent_rename, etc. Ideally a succinct description of what the
                 event actually is.
    message    - the body of the event, WHICH MUST BE JSON, describing any
                 pertinent details of the event
    timestamp  - when the event occurred
    task_id    - the ID of the task this event is in relation to. Enables quick
                 queries of an agent's task and its result together.
    """
    cur.execute(
        "INSERT INTO reporting (name, event_type, message, time_stamp, taskID) VALUES (?,?,?,?,?)",
        (
            name,
            event_type,
            message,
            timestamp,
            task_id
        )
    )