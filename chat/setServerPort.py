import PySimpleGUI as sg
from typing import Optional


class ServerPortUI:

    def __init__(self) -> None:
        self.window = self.__make_window()

    @staticmethod
    def __make_window() -> sg.Window:

        layout =    [
                        [sg.Text("Server port:"), 
                        sg.Input(key="PORT", size=(10,1))],

                        [sg.Submit("Set port"), sg.Cancel()]
                    ]

        return sg.Window("Set server port", layout, finalize=True
                            , element_justification='center')

    def run(self) -> Optional[int]:

        while True:
            event, values = self.window.read()

            if event == sg.WINDOW_CLOSED or event == "Cancel":
                self.window.close()
                return None

            if event == "Set port" and values["PORT"] == "":
                self.window.close()
                return 1500

            if event == "Set port" and values["PORT"] != "":
                self.window.close()
                return int(values["PORT"])

