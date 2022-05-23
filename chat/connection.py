import socket
from threading import Thread
import PySimpleGUI
from timestamp import TimeStamp
from logger import Logger
import time


class Server:

    def __init__(self, win: PySimpleGUI.Window, logger: Logger,
                                                s_port: int = 1500) -> None:
       
        """
            Initializes a server connection object.          
        """
        # Parameter validation
        assert isinstance(win, PySimpleGUI.Window), (f"The given window {win}"
                                    " is not of type PySimpleWindow.Window!")

        assert isinstance(logger, Logger), (f"The given logger {logger}"
                                            " is not of type Logger!")

        assert isinstance(s_port, int), (f"The given server port {s_port}"
                                        " is not of type int!")

        # Setting instance arrtibutes
        self.host = socket.gethostname() # Exchange for host ip later
        self.server_port = s_port

        self.window = win
        self.time_stamp = TimeStamp() # Used to output message recieved time
        self.logger = logger    # Used to log errors
        
    def open_connection(self) -> None: # Se if it can return true if connected and false if not (also look into timout for accept()) [TEMP COMMENT]
        
        """
            Sets up a server socket and waits for client to connect.
        """

        try:
            print("Setting up server socket")
            self.server_soc = socket.socket()
            
            self.server_soc.bind((self.host, self.server_port))
            
            self.server_soc.listen(5)
            
            self.connection, addr = self.server_soc.accept()

            print ('New connection from', addr )

        except Exception as e:
            print(f"Exception during server connection: {e}!")
            self.logger.log.error(f"Exception during server connection: {e}!")

    def close_connection(self) -> None:

        """
            Terminates the server connection.
        """

        try:
            self.connection.close()
        
        except Exception as e:
            print(f"Exception during server closing: {e}!")
            self.logger.log.error(f"Exception during server closing: {e}!")

    def get_msg(self, pre: str) -> str:

        """
            Updates the 'MESSAGES' multiline box with incoming messages.
        """

        try:
            self.connection.settimeout(0.0001)
            msg = self.connection.recv(1024).decode()
            
            if msg == '<Terminating connection>':
                self.close_connection()
                print(msg)
                return "Close"
            else:
                self.window['MESSAGES'].update(pre + '\n' 
                                + self.time_stamp.get_time() + ' User: ' + msg)
                return "NONE"

        except Exception as e:
            #print(e)   # This prints time out
            self.logger.log.error(f"Exception during get_msg: {e}!")
            return "ERROR"


class Client:

    def __init__(self, win: PySimpleGUI.Window, logger: Logger,
                                                c_port: int = 1500) -> None:
        """
            Initializes a client connection object.           
        """

        # Parameter validation
        assert isinstance(win, PySimpleGUI.Window), (f"The given window {win}"
                                     " is not of type PySimpleWindow.Window!")

        assert isinstance(logger, Logger), (f"The given logger {logger}"
                                            " is not of type Logger!")

        assert isinstance(c_port, int), (f"The given client port {c_port}"
                                         " is not of type int!")

        # Setting instance attributes
        self.host = socket.gethostname()
        self.client_port = c_port


        self.logger = logger # Used to log errors
        self.window = win

    def open_connection(self, start_time: time.ctime) -> None:

        """
            Sets up a client socket and trys to connect to server
            for 30 seconds. After 30 seconds an exception is raised.
        """

        try:
            print("Setting up client socket")
            self.client_soc = socket.socket()

            self.client_soc.connect((self.host, self.client_port))
            print("Client has been setup and connected")
            
        except Exception as e:
            print(f"Exception during client connection: {e}!")
            self.logger.log.error(f"Exception during client connection: {e}!")

            # When 30 seconds has passed, stop trying to connect.
            if time.perf_counter() - start_time >= 30:
                raise Exception("Connection attempt timed out")

            self.open_connection(start_time)

    def close_connection(self) -> None:

        """
            Sends message to the server telling it to terminate the
            connection. 
        """

        try:
            
            self.client_soc.send('<Terminating connection>'.encode())

        except Exception as e:
            print(f"Exception during client close: {e}!")
            self.logger.log.error(f"Exception during client close: {e}!")

    def send(self, msg: str) -> None:

        """
            Sends a message to the connected server.
        """

        self.client_soc.send(msg.encode())

