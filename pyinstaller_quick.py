# from logger_config import log_args_kwargs as print
import subprocess

def create_exe(file_path, single_file=False):
    command = ["pyinstaller", file_path]
    if single_file:
        command.extend(["--onefile", "--noconsole"])

    subprocess.run(command, check=True)


if __name__ == "__main__":
    file_path = "seperate_logger.py"
    single_file = True  
    create_exe(file_path, single_file)