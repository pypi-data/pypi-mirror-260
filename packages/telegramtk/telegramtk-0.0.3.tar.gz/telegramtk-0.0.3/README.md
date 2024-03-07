# tgutils

**Telegram utilities**

This package provides easy (and sync) access for the Telegram Bot API.

## Installation

```console
pip install tgutils
```

## Setup

```python
import tgutils

tgutils.init('<your-telegram-bot-token-here>')
```

## Send message

```python
import tgutils

tgutils.send_message(to, msg)
```

→ `msg` can be "Markdown" formatted.
