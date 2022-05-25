from logger import Logger
from UI import ChattWindow


if __name__ == "__main__":
    try:
        logger = Logger() # Create log object
        ChattWindow(logger).run() # Start program
        
        
    except Exception as e:
        print(f"Exception caught in main: {e}!")
        logger.log.error(f"Exception caught in main: {e}!")
    finally:
        print("Terminated!")
        input("Enter any key to exit... ")

#package as exe using: pyinstaller --onefile main.py