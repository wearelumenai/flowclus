import argparse
from . import run

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default="localhost", help='Host name')
    parser.add_argument('--port', default="8080", help='Port')
    args = parser.parse_args()

    run(host=args.host, port=args.port, quiet=True)
