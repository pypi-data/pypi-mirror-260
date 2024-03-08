import sys
import json
import logging


def parse_input(sysargs: list, plugin_params: dict) -> dict:
    if (not isinstance(plugin_params, dict)) or (set(plugin_params.keys()) != {"required", "optional"}):
        logging.error(
            f"Plugin improperly configured. Params definition must be a dict with exact keys `required` and `optional`. Provided: {plugin_params}"
        )
        sys.exit(1)

    # Verify user input parameters are consistent with plugin_params
    if len(sysargs) != 2:
        logging.error(f"error reading sys args `{sysargs}`. Expected 2 arguments (e.g. prgoram_name param_dict_as_string). Exiting.")
        sys.exit(1)

    # Read parameters in to dict to verify and pass to the plugin for execution
    try:
        params = json.loads(sysargs[1])
    except Exception as e:
        logging.error(f"Failed to parse `{params}` to JSON. Error: {str(e)}")
        sys.exit(1)
    if not isinstance(params, dict):
        logging.error(f"Input JSON must be a dict. Provided: {params}")
        sys.exit(1)

    # Verify parameters
    input_errs = []

    # Check for missing inputs
    missing_inputs = []
    for p in plugin_params["required"]:
        if p not in params.keys():
            missing_inputs.append(p)
    if len(missing_inputs) > 0:
        input_errs.append(f"Missing required inputs: {missing_inputs}")

    # Check for unexpected inputs
    unexpected_inputs = set(params.keys()) - set(plugin_params["required"] + plugin_params["optional"])
    if unexpected_inputs:
        input_errs.append(f"Unexpected inputs: {sorted(unexpected_inputs)}")

    # Exit if any errors were found
    if input_errs:
        for msg in input_errs:
            logging.error(msg)
        logging.error(
            f"Input error(s) encountered. Required: {plugin_params['required']}. Optional: {plugin_params['optional']}. Provided: {params}"
        )
        sys.exit(1)

    logging.info("successfully verified input parameters")
    return params


def plugin_logger():
    logging.root.handlers = []
    return logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%dT%H:%M:%SZ",
        format="""{"time": "%(asctime)s" , "level": "%(levelname)s", "msg": "%(message)s"}""",
        handlers=[logging.StreamHandler()],
    )


def print_results(results: dict):
    print(json.dumps({"plugin_results": results}))
