import logging
import socketserver

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.request.sendall(
            b"Hi there on the server from thomas: " + self.client_address[0].encode("utf-8") + b"\n"
        )
        self.request.sendall(b"Type 'quit' to quit.\n")
        while True:
            self.data = self.request.recv(1024).strip()
            logger.debug("Received from %s: %s", self.client_address[0], self.data)

            # Zählen der Anzahl der 'o's in der Anfrage
            count_o = self.data.decode('utf-8').lower().count('o')

            # Eingang in umgekehrter Reihenfolge
            reversed_data = self.data.decode('utf-8')[::-1].encode('utf-8')
            
            # Antwort, die die Anzahl der 'o's und die umgekehrte Eingabe enthält
            response = (
                b"thomas server sagt: " + self.data + 
                b" is in upper case: " + self.data.upper() +
                b"\nReversed input: " + reversed_data +
                b"\nNumber of 'o's: " + str(count_o).encode("utf-8") + b"\n"
            )
            self.request.sendall(response)

            if self.data.upper() == b"QUIT":
                break
        logger.debug("Client %s left", self.client_address[0])


class MyTCPServer(socketserver.ThreadingTCPServer):

    HOST, PORT = "0.0.0.0", 9999

    def __init__(self):
        self.allow_reuse_address = True
        super().__init__((MyTCPServer.HOST, MyTCPServer.PORT), MyTCPHandler)

    def serve_forever(self, poll_interval=0.5):
        logging.debug(f"Listening to: {MyTCPServer.HOST}:{MyTCPServer.PORT}")
        super().serve_forever(poll_interval)


def main():

    with MyTCPServer() as server:

        server.serve_forever()


if __name__ == "__main__":
    main()
