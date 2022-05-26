import socket
from threading import Event
import PySimpleGUI
from src.timestamp import TimeStamp
from src.logger import Logger


class Server:

    def __init__(self, window: PySimpleGUI.Window, logger: Logger, name: str,
                                        s_port: int = 1500) -> None:

        """
            Initializes a server connection object.
        """
        # Parameter validation
        assert isinstance(window, PySimpleGUI.Window), (f"The given window"
                                    f" {window} is not of type"
                                     " PySimpleWindow.Window!")

        assert isinstance(logger, Logger), (f"The given logger {logger}"
                                            " is not of type Logger!")

        assert isinstance(name, str), (f"The given name {name} is not"
                                        " of type str!")

        assert isinstance(s_port, int), (f"The given server port {s_port}"
                                        " is not of type int!")

        # Setting instance arrtibutes
        self.connected_user_name = name

        self.host = socket.gethostbyname(socket.gethostname()) # Get device IP.
        self.server_port = s_port

        self.server = (self.host, s_port)

        self.window = window
        self.time_stamp = TimeStamp() # Used to output message recieved time
        self.logger = logger    # Used to log errors

    def open_connection(self, done: Event, err: Event) -> None:

        """
            Sets up a server socket and waits for 30 seconds for
            client to connect. If no connection server times out.
        """

        try:
            print("Setting up server socket")
            
            self.server_soc = socket.socket()

            self.server_soc.settimeout(30)

            self.server_soc.bind(self.server)

            self.server_soc.listen(5)

            self.connection, addr = self.server_soc.accept()

            print ('New connection from', addr )

            done.set() # Tells the main thread that server got a connection.

        except socket.timeout:
            print("Server timed out")
            err.set() # Tells main thread that error occured.

        except Exception as e:
            print(f"Exception during server connection: {e}!")
            self.logger.log.error(f"Exception during server connection: {e}!")
            err.set() # Tells main thread that error occured.

    def close_connection(self) -> None:

        """
            Terminates the server connection.
        """

        try:
            self.connection.close() # Try to close connection.

        except Exception as e:
            print(f"Exception during server closing: {e}!")
            self.logger.log.error(f"Exception during server closing: {e}!")

    def get_msg(self, previous_text: str) -> str:

        """
            Updates the 'MESSAGES' multiline box with incoming messages.
        """

        try:
            self.connection.settimeout(0.0001) # Does quick check
            msg = self.connection.recv(1024).decode()

            if msg == '<Terminating connection>':
                #self.close_connection()
                print(msg)
                return "Close"
            else:
                self.window['MESSAGES'].update(previous_text + '\n'
                                + self.time_stamp.get_time() 
                                + " " + self.connected_user_name + ": " + msg)
                return "NONE"

        except socket.timeout:
            # Ugly way to ignore the timeouts
            pass

        except Exception as e:
            self.logger.log.error(f"Exception during get_msg: {e}!")
            return "ERROR"


class Client:

    def __init__(self, window: PySimpleGUI.Window, logger: Logger,
                                        ip: str, c_port: int = 1500) -> None:
        """
            Initializes a client connection object.
        """

        # Parameter validation
        assert isinstance(window, PySimpleGUI.Window), (f"The given window"
                                     f" {window} is not of type"
                                     " PySimpleWindow.Window!")

        assert isinstance(logger, Logger), (f"The given logger {logger}"
                                            " is not of type Logger!")

        assert isinstance(ip, str), (f"The given server ip {ip}"
                                        " is not of type str!")

        assert isinstance(c_port, int), (f"The given client port {c_port}"
                                         " is not of type int!")

        # Setting instance attributes

        self.host = socket.gethostname()
        self.client_port = c_port

        if ip == "localhost":
            self.client = (self.host, c_port)
        else:
            self.client = (ip, c_port)

        self.logger = logger # Used to log errors
        self.window = window

    def open_connection(self, done: Event, err: Event) -> None:

        """
            Sets up a client socket and trys to connect to server
            for 30 seconds. After 30 seconds an exception is raised.
        """

        try:
            print("Setting up client socket")
            
            self.client_soc = socket.socket()

            self.client_soc.settimeout(30)

            self.client_soc.connect(self.client)

            print("Client has been setup and connected")

            done.set() # Tells main thread that client has connected to server.

        except socket.timeout:
            print("Client timed out")
            err.set() # Tells main thread that error occured.

        except Exception as e:
            print(f"Exception during client connection: {e}!")
            self.logger.log.error(f"Exception during client connection: {e}!")

            err.set() # Tells main thread that error occured.
            
    def close_connection(self) -> None:

        """
            Sends message to the server telling it to terminate the
            connection.
        """

        try:
            self.client_soc.settimeout(1)
            self.client_soc.send('<Terminating connection>'.encode())

        except Exception as e:
            print(f"Exception during client close: {e}!")
            self.logger.log.error(f"Exception during client close: {e}!")

    def send(self, msg: str) -> None:

        """
            Sends a message to the connected server.
        """

        self.client_soc.send(msg.encode())

