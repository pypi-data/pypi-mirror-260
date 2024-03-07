# telegramtk

**Telegram utilities**

This package provides easy (and sync) access for the Telegram Bot API.

## Installation

```console
pip install telegramtk
```

## Setup

```python
import telegramtk

telegramtk.init('<your-telegram-bot-token-here>')
```

## Send message

```python
import telegramtk

telegramtk.send_message(to, msg)
```

→ `msg` can be "Markdown" formatted.
