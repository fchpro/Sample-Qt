import datetime
import logging
from global_signals import global_signals
from paths import Paths
from icecream import ic

debug_mode = True
global_signals.debug_mode.emit(debug_mode)


def clear_log_txt_file():
    """
    Clears the log.txt file.
    """
    try:
        with open(Paths.log_file, "w") as file:
            file.write("")
    except Exception as e:
        print("TJngI",f"An error occurred while clearing the log file: {e}")


def log_args_kwargs(*args, **kwargs):
    if not debug_mode:
        return

    print(args, kwargs)
    
    # try:
    #     separator = "_" * 10
    #     simple_log = f"\n{separator}\n {args} {kwargs}\n{separator}\n"
    #     with open(Paths.log_file, "a") as file:
    #         file.write(simple_log)
    # except Exception as e:
    #     print("ENvyJ", f"LoggingError writing to log file: {e}")

    # try:
    #     log_message = f" args = {args}, kwargs = {kwargs}\n"
    #     # global_signals.log_message.emit(log_message)
    # except Exception as e:
    #     print("LIZ3x",f"LoggingError emitting log message: {e}")

    # try:
    #     logger = setup_logger()
    # except Exception as e:
    #     print("2PwKG",f"LoggingError initializing logger: {e}")

    # try:
    #     args_str, kwargs_str = str(args), str(kwargs)
    #     logger.debug(f"Args: {args_str}, Kwargs: {kwargs_str}")
    # except Exception as e:
    #     print("zkW8k",f"LoggingError logging args and kwargs: {e}")

    # try:
    #     print(args, kwargs)
    # except Exception as e:
    #     print("GKvay",f"LoggingError printing args and kwargs: {e}")

    # try:
    #     ic(args, kwargs)
    # except Exception as e:
    #     print("GKvay",f"LoggingError printing args and kwargs: {e}")

    # try:
    #     formatted_time = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-4]
    #     log_message = f"{formatted_time}: args = {args}, kwargs = {kwargs}\n"
    # except Exception as e:
    #     print("82qFX",f"LoggingError formatting message: {e}")


    # try:

    #     seperator =  "_" * 100
    #     simple_log = f"{seperator} {args}{kwargs}"
        
    #     with open(Paths.log_file, "a") as file:
    #         file.write(simple_log)
    # except Exception as e:
    #     print("ENvyJ",f"LoggingError writing to log file: {e}")

    

# def setup_logger():
#     try:
#         logger = logging.getLogger('MyLogger')
#         logger.setLevel(logging.DEBUG)
#         if not logger.handlers:
#             file_handler = logging.FileHandler('log_folder\\output.txt')
#             file_handler.setLevel(logging.DEBUG)
#             console_handler = logging.StreamHandler()
#             console_handler.setLevel(logging.DEBUG)
#             formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#             file_handler.setFormatter(formatter)
#             console_handler.setFormatter(formatter)
#             logger.addHandler(file_handler)
#             logger.addHandler(console_handler)
#     except Exception as e:
#         print("TdrDs",f"Error setting up logger: {e}")
#     return logger
