from . import OC, run, start_server
from .data import get_chunk

if __name__ == "__main__":
    model = OC(init_k=1, b=1, amp=.2, mcmc_iter=100, frame_size=60)
    run(model, get_chunk, start_server(port=32211))
