from logger import Logger
from UI import ChattWindow


if __name__ == "__main__":
    try:
        logger = Logger()
        ChattWindow(logger).run()
        
        
    except Exception as e:
        print(f"Exception caught in main: {e}!")
        logger.log.error(f"Exception caught in main: {e}!")

    print("Terminated!")
    input("Enter any key to exit... ")