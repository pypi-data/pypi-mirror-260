# Configure logging
import logging


def logging_config(
    file_name, log_stream, log_file=None, log_level=logging.INFO, add_handler=None
):
    handlerlist = [logging.StreamHandler(log_stream)]

    if log_file is not None:
        handlerlist.append(logging.FileHandler(log_file))

    if add_handler is not None:
        handlerlist.append(add_handler)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s:%(msecs)03d [%(file_name)s - %(levelname)s] \t\t %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=handlerlist,
    )
