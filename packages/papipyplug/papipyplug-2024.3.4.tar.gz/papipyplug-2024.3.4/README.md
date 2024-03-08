# papipyplug
Process-API Python Plugin

A lightweight wrapper for converting python functions into plugins for use in the [process-api](https://github.com/Dewberry/process-api) implementation of the [OGC API-Proceses](https://docs.ogc.org/is/18-062r2/18-062r2.html#toc0) standard. 

---

### Usage

*See the [example](example) for a complete implementation of this library for creating a demo plugin.* 

1. Define a main function with the following signature:

```python
# my_module.py
def main(params: dict) -> dict:
    pass
```

2. Add a constant `PLUGIN_PARAMS` describing the params that are required and/or optional to for the main function. the dictionary must, at a minimum, contain a `required` key returning a list of parameters for the funcion to recieve on execution.

```python
# my_module.py
PLUGIN_PARAMS = {"required": ["first_param", "second_param"], "optional": ["additioan_param"]}
```

3. Create a new file importing the `main` function above and the `PLUGIN_PARAMS`. Format the script to use the utilities from this library to prepare the data and format the results:
```python
import sys

from .my_module import  main, PLUGIN_PARAMS

from papipyplug import parse_input, print_results, plugin_logger, git_meta

if __name__ == "__main__":
    # Start plugin logger
    plugin_logger()

    # Read, parse, and verify input parameters
    input_params = parse_input(sys.argv, PLUGIN_PARAMS)

    # Add main function here
    results = main(input_params)

    # Print Results
    print_results(results)
```

4. Containerize your python code including the file created in 3. See `build_and_test_plugin.sh` in the `example` for details.
