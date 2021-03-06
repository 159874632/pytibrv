##
# tibrvlisten.py
#   rewrite TIBRV example: tibrvlisten.c
#   using Python Object Model
#
# LAST MODIFIED: V1.0 2016-12-22 ARIEN arien.chen@gmail.com
#
import sys
import getopt
from pytibrv.events import *

def usage() :
    print()
    print("tibrvlisten.py [--service service] [--network network]")
    print("               [--daemon daemon] <subject> ")
    print()
    sys.exit(1)


def get_params(argv):

    try:
        opts, args = getopt.getopt(argv, '', ['service=', 'network=', 'daemon='])

    except getopt.GetoptError:
        usage()

    service = None
    network = None
    daemon = None

    for opt, arg in opts:
        if opt == '--service':
            service = arg
        elif opt == '--network':
            network = arg
        elif opt == '--daemon':
            daemon = arg
        else:
            usage()

    if len(args) != 1:
        usage()

    return service, network, daemon, args[0]

def my_callback(event, msg, closure):

    localTime, gmtTime = TibrvMsg.nowString()

    if msg.replySubject is not None:
        print("{} ({}): subject={}, reply={}, message={}".format(
               localTime, gmtTime, msg.sendSubject, msg.replySubject, str(msg)));
    else:
        print("{} ({}): subject={}, message={}".format(
               localTime, gmtTime, msg.sendSubject, str(msg)));


# MAIN PROGRAM
def main(argv):

    progname = argv[0]

    service, network, daemon, subj = get_params(argv[1:])

    err = Tibrv.open()
    if err != TIBRV_OK:
        print('{}: Failed to open TIB/RV: {}'.format('', progname, TibrvStatus.text(err)))
        sys.exit(1);

    tx = TibrvTx()

    err = tx.create(service, network, daemon)
    if err != TIBRV_OK:
        print('{}: Failed to initialize transport: {}'.format('', progname, TibrvStatus.text(err)))
        sys.exit(1)

    tx.description = progname

    print("tibrvlisten: Listening to subject {}".format(subj))

    def_que = TibrvQueue()
    listener = TibrvListener()

    err = listener.create(def_que, TibrvMsgCallback(my_callback), tx, subj, None)
    if err != TIBRV_OK:
        print('{}: Error {} listening to {}'.format('', progname, TibrvStatus.text(err), subj))
        sys.exit(2)

    while def_que.dispatch() == TIBRV_OK:
        pass

    # In Linux/OSX
    # CTRL-C will not interrupt the process
    # CTRL-\ (SIGQUIT) would work

    del listener
    del tx

    Tibrv.close()

    sys.exit(0)


    return

if __name__ == "__main__":
    main(sys.argv)



