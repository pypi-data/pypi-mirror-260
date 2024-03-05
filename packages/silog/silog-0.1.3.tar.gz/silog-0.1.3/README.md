# silog

silog is a simple logging library for Python. Designed to no worries about the underlying log file management.

## Features

- Automatic rotation of log files based on the date, ensuring that log files are organized by day.
- Singleton pattern to ensure only one instance of the logger is created, making it easy to use across your application.
- Simple interface for logging messages at various severity levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).

## Installation

You can install silog directly from PyPI:

```bash
pip install silog
```

## Usage

To use silog in your project, import the 'Silog' class and initialize it with your desired log directory.
```python
from silog import Silog

# initialize logger
logger = Silog("logs")

# log message
logger.info("log message")
```