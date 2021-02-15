import argparse

from . import OC, run, start_server
# from .data import get_chunk
import flowsim.client as c


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default="localhost", help='Host name')
    parser.add_argument('--port', default="32211", help='Port of the current bubbles service')
    parser.add_argument('--simport', default="8080", help='Port of the data simulation service')
    args = parser.parse_args()

    model = OC(init_k=1, b=1, amp=.2, mcmc_iter=100, frame_size=60)
    run(model,
        c.get_chunk(host=args.host, port=args.simport),
        start_server(host=args.host, port=args.port, quiet=False))
