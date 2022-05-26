import PySimpleGUI as sg
import csv
from typing import Optional

class Contact:
    
    """
        Contact object contains name, address and port
    """

    def __init__(self, name: str, address: str, port: int = 1500) -> None:
        
        assert isinstance(name, str), (f"The given name {name} is not of type"
                                        " string!")

        assert isinstance(address, str), (f"The given address {address} is"
                                            " not of type string!")

        assert isinstance(port, int), (f"The given port number {port} is not"
                                        " of type int!")

        self.name = name

        self.address = address

        self.port = port

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        assert isinstance(name, str), (f"The given name {name} is not of type"
                                        " string!")

        self.__name = name

    @property
    def address(self) -> str:
        return self.__address

    @address.setter
    def address(self, address: str) -> None:
        assert isinstance(address, str), (f"The given address {address} is not"
                                        " of type string!")
                                        
        self.__address = address

    @property
    def port(self) -> int:
        return self.__port

    @port.setter
    def port(self, port: int) -> None:
        assert isinstance(port, int), (f"The given port {port} is not of type"
                                        " int!")                     
        self.__port = port

    @property
    def contact_connection(self) -> tuple:
        """
            This is used to get name address and port to connect to.
        """
        return (self.__name, self.__address, self.__port)

    def __repr__(self) -> str:
        """
            Used when writing contact to csv file
        """
        return f"{self.name},{self.address},{self.port}"

    def __str__(self) -> str:
        return f"{self.name}: \n{self.address}:{self.port}"


class SelectContactUI:

    """
        A window to select a contact to try and connect to. 
    """

    def __init__(self) -> None:
        self.contacts = []
        self.window = self.make_window()

    @staticmethod
    def make_window() -> sg.Window:
        layout =    [
                        [sg.Listbox(values=[], key="CONTACT_DISPLAY", 
                         expand_x=True, expand_y=True)],
                         [sg.Button("Connect to selected")]
                    ]

        return sg.Window("Contacts", layout, size=(300, 400))

    def get_contacts(self) -> None:
        with open(".\Code\src\contacts.csv", "r") as csv_file:
            reader = csv.reader(csv_file)

            for row in reader:
                if row != []:
                    self.contacts.append(Contact(row[0], row[1], int(row[2])))

    def run(self) -> Optional[tuple]:
        """
            This method should be called by UI. It will return a typle
            (NAME, IP, PORT_NUMBER) if contact is selected, otherwise NoneType
            is returned.
        """
        self.get_contacts()
        init = False
        while True:
            if init is True:
                event, values = self.window.read()
            else:
                event, values = self.window.read(10)

            if init is False:

                self.window["CONTACT_DISPLAY"].update(values = self.contacts)
                init = True
                continue

            if event == sg.WIN_CLOSED:
                break

            if (event == "Connect to selected" 
                            and len(values["CONTACT_DISPLAY"]) == 1):
                                
                contact = values["CONTACT_DISPLAY"][0]
                
                self.window.close()
                return contact.contact_connection


class ShowContactsUI:
    
    """
        A window to display contacts in list.
    """

    def __init__(self) -> None:
        self.contacts = []
        self.window = self.make_window()

    @staticmethod
    def make_window() -> sg.Window:
        layout =    [
                        [sg.Listbox(values=[], key="CONTACT_DISPLAY", 
                         expand_x=True, expand_y=True)]
                    ]

        return sg.Window("Contacts", layout, size=(300, 400))

    def get_contacts(self) -> None:
        with open(".\Code\src\contacts.csv", "r") as csv_file:
            reader = csv.reader(csv_file)

            for row in reader:
                if row != []:
                    self.contacts.append(Contact(row[0], row[1], int(row[2])))

    def run(self) -> None:
        self.get_contacts()
        init = False
        while True:
            if init is True:
                event, values = self.window.read()
            else:
                event, values = self.window.read(10)

            if init is False:

                self.window["CONTACT_DISPLAY"].update(values = self.contacts)
                self.window["CONTACT_DISPLAY"].update(disabled = True)
                init = True
                continue

            if event == sg.WIN_CLOSED:
                break


class NewContactUI:

    """
        A window to create a new contact.
    """

    def __init__(self) -> None: # Pass in theme later?
        self.window = self.make_window()

    @staticmethod
    def make_window() -> sg.Window:
        
        layout =    [
                        [sg.Text("Name:", size=(7,1)),
                         sg.Input(expand_x=True, key="NAME")],

                        [sg.Text("Address:", size=(7,1)), 
                         sg.Input(expand_x=True, key="ADDRESS")],

                        [sg.Text("Port:", size=(7,1)), 
                         sg.Input(expand_x=True, key="PORT")],

                         [sg.Button("Create"), sg.Text("", key="OUTPUT")]
                    ]    

        return sg.Window("New Contact", layout, size=(300, 125))  

    @staticmethod
    def save_contact(contact: Contact) -> None:
        """
            Writes the new contact to file.
        """
        with open(".\Code\src\contacts.csv", "a") as csv_file:
            writer = csv.writer(csv_file)
            row = [fld for fld in repr(contact).split(",")]
            writer.writerow(row)

    def run(self) -> None:
        """
            Runs the new contact window.
        """
        while True:
            event, values = self.window.read()

            self.window["OUTPUT"].update("")

            if event == sg.WIN_CLOSED:
                break

            if event == "Create":
                if (values["NAME"] != "" 
                    and values["ADDRESS"] != "" 
                    and values["PORT"] != ""):
                    try:
                        new_contact = Contact(values["NAME"], 
                                                values["ADDRESS"],
                                                int(values["PORT"]))
                        
                        self.save_contact(new_contact)

                        self.window["OUTPUT"].update("New contact added")
                    except ValueError:
                        self.window["OUTPUT"].update("Port needs to be integer")
                else:
                    self.window["OUTPUT"].update("All fields needs to be "
                                                 "filled out")