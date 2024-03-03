# Configure logging
import logging


def logging_config(log_level, log_file, log_stream, add_handler):
    handlerlist = [logging.StreamHandler(log_stream)]

    if log_file is not None:
        handlerlist.append(logging.FileHandler(log_file))

    if add_handler is not None:
        handlerlist.append(add_handler)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s:%(msecs)03d [%(filename)s - %(levelname)s] \t\t %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=handlerlist,
    )
