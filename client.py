import Pyro5.api
import Pyro5.errors
from voter import VOTER_NAME

voter = Pyro5.api.Proxy("PYRONAME:"+VOTER_NAME)

try:
    voter.send("pao")
except Pyro5.errors.CommunicationError as e:
    print(f"Could not connect: {e}")
