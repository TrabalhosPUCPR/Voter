import math
import signal
from sys import argv

import Pyro5.server
import Pyro5.api

VOTER_NAME = "VOTER_123456789_987654321_RETOV"


class VoterService(object):
    def __init__(self, ve, to):
        self.msgs = []
        self.timeout_active = False
        self.timeout_to = to
        self.expect = ve
        signal.signal(signal.SIGALRM, lambda n, s: self.handle_timeout())

    def handle_timeout(self):
        msg_received = len(self.msgs)
        print(f"Timed out with {msg_received} messages received, verdict will be inconclusive!")
        self.cancel_timeout()
        self.vote(math.ceil((msg_received + 1) / 2))

    def cancel_timeout(self):
        signal.alarm(0)
        self.timeout_active = False

    def start_timeout(self):
        self.timeout_active = True
        signal.alarm(self.timeout_to)

    @Pyro5.server.expose
    @Pyro5.server.oneway
    def send(self, msg):
        if not self.timeout_active:
            self.start_timeout()
        self.msgs.append(msg)
        msgs_received = len(self.msgs)
        if msgs_received >= self.expect:
            print(f"{msgs_received} messages received! Voting...")
            self.cancel_timeout()
            self.vote(math.ceil((self.expect + 1) / 2))
        else:
            print(f"Message {msg} received")

    def vote(self, majority):
        highest = (None, 0)
        for m in self.msgs:
            count = self.msgs.count(m)
            if count >= majority:
                print(f"Voter final verdict: {m}, where it was received {count} times")
                self.msgs.clear()
                return m
            if highest[1] < count:
                highest = (m, count)
        print(f"Voter did not receive enough messages, verdict will be inconclusive!")
        print(f"Voter final verdict: {highest[0]}, where it was received {highest[1]} times")
        self.msgs.clear()
        return highest[0]


if __name__ == '__main__':
    if len(argv) < 3:
        print("Invalid parameter")
        exit(-1)
    arg_to = int(argv[2])
    arg_ve = int(argv[1])
    daemon = Pyro5.server.Daemon()
    voter = VoterService(arg_ve, arg_to)
    uri = daemon.register(voter)
    ns = Pyro5.api.locate_ns()
    ns.register(VOTER_NAME, uri)
    print("Voter is now active!")
    daemon.requestLoop()
