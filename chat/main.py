from logger import Logger
from UI import ChatWindow


def main():
    try:
        logger = Logger() # Create log object
        ChatWindow(logger).run() # Start program
        
        
    except Exception as e:
        print(f"Exception caught in main: {e}!")
        logger.log.error(f"Exception caught in main: {e}!")
    finally:
        print("Terminated!")
        input("Enter any key to exit... ")


if __name__ == "__main__":
    main()

#package as exe using: pyinstaller --onefile main.py