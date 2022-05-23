from threading import Thread, Event
import PySimpleGUI as sg
import time
from logger import Logger
from connection import Server, Client
from timestamp import TimeStamp


class ChattWindow:

    def __init__(self, logger: Logger) -> None:

        """
            Initializes chat window object.
        """

        # Validating given parameters
        assert isinstance(logger, Logger), (f"The given logger {logger} is not"
                                            " of type Logger!")

        # Setting instance attributes
        self.window = self.make_window()

        self.time_stamp = TimeStamp()
        self.logger = logger

    def make_window(self) -> sg.Window:

        """
            Creates and returns the window.
        """

        menu_layout =   [
                            ['Connection', ['Connect', 'Disconnect']]
                        ]

        layout =    [
                        [sg.Menu(menu_layout, key='MENU')],

                        [sg.Multiline(expand_x=True, expand_y=True, 
                        disabled=True, key='MESSAGES', autoscroll=True)],

                        [sg.Input(expand_x=True, do_not_clear=True, 
                        key='MY_MESSAGE'), sg.Button('Send')]
                    ]

        return sg.Window("Chat", layout, size=(800, 650), finalize=True)

    def connect(self, ip: str, port: str) -> None:

        """
            Creates a server and client object and runs their open_connection
            methods.
        """

        self.server = Server(self.window, self.logger, ip, port)
        
        self.server_thread = Thread(target=self.server.open_connection, 
                                    args=(self.server_connected_done,
                                            self.server_connected_err))
        self.server_thread.start()
        
        # print("Pre temp short delay between server start and client start")
        # time.sleep(0.5)
        # print("Post temp short delay between server start and client start")

        """
            Note To Self:
            Client will later run startup in a separate thread, both server
            and client will take result flag as a variable; the flag will
            be set to True if connected, False if it could not connect and
            None if no result yet.
        """

        self.client = Client(self.window, self.logger, ip, port)
        self.client_thread = Thread(target=self.client.open_connection, 
                                    args=(self.client_connected_done,
                                            self.client_connected_err))
        self.client_thread.start()

        #self.client.open_connection(time.perf_counter())
        
    def run(self) -> None:

        """
            Main event loop for chat window.
        """

        self.client_connected_done = Event()
        self.client_connected_err = Event()

        self.server_connected_done = Event()
        self.server_connected_err = Event()

        connecting = False
        connected = False

        while True:
            try:
                # If not connected only run loop on event
                if not connecting and not connected:
                    event, values = self.window.read()

                # Else continuously run the loop
                else:
                    event, values = self.window.read(10)

                # Break loop when window is closed
                if event == sg.WIN_CLOSED:
                    break

                # While trying to connect
                if connecting:
                    if (self.client_connected_err.is_set()
                        or self.server_connected_err.is_set()):

                        self.client.close_connection()
                        self.server.close_connection()

                        connected = False
                        connecting = False

                        self.client_connected_done.clear()
                        self.client_connected_err.clear()

                        self.server_connected_done.clear()
                        self.server_connected_err.clear()
                        
                        self.window['MESSAGES'].update("Connection failed!")

                    elif (self.client_connected_done.is_set()
                            and self.server_connected_done.is_set()):
                            
                            connected = True
                            connecting = False

                            self.client_connected_done.clear()
                            self.client_connected_err.clear()

                            self.server_connected_done.clear()
                            self.server_connected_err.clear()
                            
                            self.window['MESSAGES'].update("Connected!")
                    else:
                        
                        continue

                # When connected
                if event == 'Connect' and not connected:
                    self.window['MESSAGES'].update("Connecting...")

                    connecting = True

                    ip, port = values['MY_MESSAGE'].split(":") # Temp

                    self.connect(int(ip), int(port))

                    self.window['MY_MESSAGE'].update("")

                if event == 'Disconnect' and connected:
                    self.window['MESSAGES'].update("Disconnected")

                    connected = False
                    
                    self.client.close_connection()
                    self.server.close_connection()

                if event == 'Send' and connected:
                    self.window['MESSAGES'].update(values['MESSAGES'] + '\n' 
                                                    + self.time_stamp.get_time()
                                                    + ' ME: ' 
                                                    + values['MY_MESSAGE'])

                    self.client.send(values['MY_MESSAGE'])

                    self.window['MY_MESSAGE'].update("")

                if connected:
                    resp = self.server.get_msg(values['MESSAGES'])
                    if resp == "Close":
                        
                        self.window['MESSAGES'].update("Disconnected")
                        
                        connected = False
                        
                        self.client.close_connection()
                        self.server.close_connection()

                        print("Connection ended by other user")

            # except AttributeError as e:
            #     pass
            except Exception as e:
                self.logger.log.error(f"Exception in chatwindow run: {e}!")

            # Handle connection timeout exception 
            # (+ create a connection timeout exception)