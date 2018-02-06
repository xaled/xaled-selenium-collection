import argparse
DEFAULT_DRIVER_TYPE = "Firefox"
DEFAULT_DRIVER_PATH = "./geckodriver"

def parse_args(additional_argument=None, args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument( "--driver-type", default=DEFAULT_DRIVER_TYPE)
    parser.add_argument( "--driver-path", default=DEFAULT_DRIVER_PATH)
    # TODO: headless, useragent, proxy, json_server
    for aa in additional_argument:
        parser.add_argument(*aa[0], **aa[1])
    if args is None:
        return parser.parse_args()
    else:
        return parser.parse_args(args)

def get_additional_argument(*args, **kwargs):
    return args, kwargs
