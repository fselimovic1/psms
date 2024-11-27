# docstring

"""
"""


def psms_message(msg_id, msg_cont):

    # Print error message
    if msg_id == 1:
        print("\033[31m");
        print("ERROR!\n" + msg_cont);
        print("\033[0m");

    # Print warning message
    if msg_id == 2:
        print("\033[33;1m");
        print("WARNING!\n" + msg_cont);
        print("\033[0m");

    # Print success message
    if msg_id == 10:
        print("\033[32m");
        print("SUCCESS!\n" + msg_cont);
        print("\033[0m");