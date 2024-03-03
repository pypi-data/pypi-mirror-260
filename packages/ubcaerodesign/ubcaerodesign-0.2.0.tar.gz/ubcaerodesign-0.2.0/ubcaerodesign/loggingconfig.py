# Configure logging
import logging

def logging_config(log_level,log_file,log_stream,add_handler):
    
    if log_file is None:
        file_handler = None;
    else:
        file_handler = logging.FileHandler(log_file);

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s:%(msecs)03d [%(filename)s - %(levelname)s] \t\t %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(log_stream),
            file_handler,
            add_handler,
        ],
    )

