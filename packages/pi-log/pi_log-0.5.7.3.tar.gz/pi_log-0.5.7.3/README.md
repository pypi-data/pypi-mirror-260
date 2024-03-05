# A simple logging module that adds utility functions for using Python logging

## Example Usage

### Using in a typical module
```python
from pi_conf import logs
log = logs.getLogger(__name__)
log.info("Hello log world!")
```

### Set logging across entire application
```python
from pi_conf import logs
logs.set_app_logging("debug")
```
