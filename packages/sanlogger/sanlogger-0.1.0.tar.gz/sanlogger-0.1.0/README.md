# slogger
A customized logger for my end to end project workflows

## Usage
```python
from slogger import SLogger

# setting up logging file location
from slogger.paths import TEMP_DIR
logfile = TEMP_DIR / 'logs'
# this log file location can be changed to custom log paths as well

logger = SLogger(__name__, logfile)

logger.critical("Santo")
```
