import imp
from threading import Thread
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

    def connect(self, s_port: int, c_port: int) -> None:

        """
            Creates a server and client object and runs their open_connection
            methods.
        """

        self.server = Server(self.window, self.logger, s_port)
        
        self.server_thread = Thread(target=self.server.open_connection)
        self.server_thread.start()
        
        print("Pre temp short delay between server start and client start")
        time.sleep(0.5)
        print("Post temp short delay between server start and client start")

        """
            Note To Self:
            Client will later run startup in a separate thread, both server
            and client will take result flag as a variable; the flag will
            be set to True if connected, False if it could not connect and
            None if no result yet.
        """

        self.client = Client(self.window, self.logger, c_port)
        self.client.open_connection(time.perf_counter())
        
    def run(self) -> None:

        """
            Main event loop for chat window.
        """

        active = False
        while True:
            try:
                # If not connected only run loop on event
                if not active:
                    event, values = self.window.read()

                # Else continuously run the loop
                else:
                    event, values = self.window.read(10)


                # Break loop when window is closed
                if event == sg.WIN_CLOSED:
                    break

                if event == 'Connect' and active == False:
                    self.window['MESSAGES'].update("Connected")

                    active = True

                    s_port, c_port = values['MY_MESSAGE'].split() # Temp

                    self.connect(int(s_port), int(c_port))

                    self.window['MY_MESSAGE'].update("")

                if event == 'Disconnect' and active:
                    self.window['MESSAGES'].update("Disconnected")

                    active = False
                    
                    self.client.close_connection()
                    self.server.close_connection()

                if event == 'Send' and active:
                    self.window['MESSAGES'].update(values['MESSAGES'] + '\n' 
                                                    + self.time_stamp.get_time()
                                                    + ' ME: ' 
                                                    + values['MY_MESSAGE'])

                    self.client.send(values['MY_MESSAGE'])

                    self.window['MY_MESSAGE'].update("")

                if active:
                    resp = self.server.get_msg(values['MESSAGES'])
                    if resp == "Close":
                        
                        self.window['MESSAGES'].update("Disconnected")
                        
                        active = False
                        
                        self.client.close_connection()
                        self.server.close_connection()

                        print("Connection ended by other user")

            # except AttributeError as e:
            #     pass
            except Exception as e:
                self.logger.log.error(f"Exception in chatwindow run: {e}!")

            # Handle connection timeout exception 
            # (+ create a connection timeout exception)