from eoslib.util import state_machine

def key_state_map():
    #           State               Event                Next State
    stmap = [(None,                "rotate",             "active"),
             ("active",            "rotate",             "revoked"),
             ("active",            "graceful_rotate",    "depreciated")]
    return state_machine.state_transition_map(stmap)

