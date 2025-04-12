# Logging in Python

Examples of setting up **logger**: 

``` python
    from logger import Logger

    # Make format
    log_format: str = LoggerConfig.format(name=True, levelname=True, message=True)

    # Config and get logger
    log = LoggerConfig(name="test", level=10, log_file="test.log", formatter=log_format).get_logger()
```

### LoggerConfig

* Args:
    * **name**: Logger name (usually `__name__`)
    * **level**: Logging level constant (e.g., logging.INFO)
    * **log_file**: Filename for log output (__None for console only__)
    * **log_path**: Directory path for log files
    * **formatter**: Log message format string
    * **mode**: File mode ('a' for append, 'w' for overwrite)

### LoggerConfig.format

* Args:
    * **name**: Include logger name
    * **asctime**: Include timestamp
    * **levelname**: Include log level
    * **message**: Include message
    * ****additional_fields**: Extra format fields (e.g., lineno=True)
* Returns:
    * Format string (e.g., **"%(name)s %(levelname)s %(message)s"**)