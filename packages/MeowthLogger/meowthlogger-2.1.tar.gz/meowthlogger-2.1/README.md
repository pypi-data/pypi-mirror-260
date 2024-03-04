# MeowthPxnk Cxstom logger for python!
---
### How this works:

Logs will be steram to console and save to rollover every hour at 00 minutes:
***savepath ->*** ./Logs/`YYYY-MM-DD`/`HH.00-HH.00`.log

---
### Usage:
```python
from MeowthLogger import Logger

logger = Logger()

# usage logger ---->

logger.info("INFO")
logger.error("ERROR")
logger.debug("DEBUG")
logger.warning("WARNING")
logger.critical("CRITICAL")
```
---
### Initialisation arguments:
- **logger_level** - level of logging
- **use_files** - bool argument, if u don't need use logging files
- **path** - logs folder path
- **filename** - logging filename
- **encoding** - encoding for log ro files
- **use_uvicorn** - bool argument, need to use logger with uvicorn
##### Example:
```python
logger = Logger(
    path="user/logs",
    filename="logging.log",
    encoding="utf-8"
)
```
---
### Logs parsing:
###### Can use if active file system
```python
date_from: datetime.datetime = ...
date_to: datetime.datetime.now()

logs: bytes = logger.parse_logs(date_from, date_to)
```
or without date_to
```python
logs: bytes = logger.parse_logs(date_from)
```
---
### Usage without file system:
```python
logger = Logger(use_files=False)
```
---
### Usage with dependencies:
##### Uvicorn - 
```python
logger = Logger(use_uvicorn=True)
```
---
$XOXO$
*meowthpxnk*