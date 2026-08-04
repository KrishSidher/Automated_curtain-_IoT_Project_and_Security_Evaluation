from motor import *

state = "CLOSED"

def open_curtain():
    global state
    if state != "OPEN":
        Backwards()
        state = "OPEN"
    return state

def close_curtain():
    global state
    if state != "CLOSED":
        Forwards()
        state = "CLOSED"
    return state

def stop_curtain():
    global state
    Stop()
    state = "STOPPED"
    return state

def get_state():
    return state
