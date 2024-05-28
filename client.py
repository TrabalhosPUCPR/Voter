import Pyro5.api
import Pyro5.errors
from voter import VOTER_NAME
from sys import argv

voter = Pyro5.api.Proxy("PYRONAME:"+VOTER_NAME)

if len(argv) < 2:
    print("No message passed in parameter")
    exit(-1)

try:
    voter.send(argv[1])
except Pyro5.errors.CommunicationError as e:
    print(f"Could not connect: {e}")
