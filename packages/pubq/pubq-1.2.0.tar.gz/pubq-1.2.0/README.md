# PUBQ Python SDK

[PUBQ](https://pubq.io) is a pub/sub channels cloud and this is the official Python client library including both real-time and REST interfaces.

To meet PUBQ and see more info and examples, please read the [documentation](https://pubq.io/docs).

# Getting Started

Follow these steps to just start building with PUBQ in Python or see the [Quickstart guide](https://pubq.io/docs/getting-started/quickstart) which covers more programming languages.

## Install with package manager

The Python SDK is available as PyPI package:

```bash
pip install pubq
```

## Interacting with PUBQ

Get your application id and key from [PUBQ dashboard](https://dashboard.pubq.io) by [creating a new app](https://dashboard.pubq.io/applications/create) or use existing one.

Connect to PUBQ:

```python
import asyncio
from pubq import Pubq

async def main():
    def on_connected(state):
        print("Connected to PUBQ!")

    realtime = Pubq.RealTime({"key": "YOUR_API_KEY"})

    realtime.connection.on('connected', on_connected)

asyncio.run(main())
```

Subscribe a channel and listen for any data publish to receive:

```python
def on_message(msg):
    print("Received new data: '" + str(msg.data))

channel = realtime.channels.get("my-channel")
channel.subscribe(on_message)
```

Publish a message:

```python
channel.publish("Hello!")
```

Publish a message with REST interface:

```python
import asyncio
from pubq import Pubq

async def main():
    rest = Pubq.REST({"key": "YOUR_API_KEY"})
    channel = rest.channels.get("my-channel")
    channel.publish("Hello!")
asyncio.run(main())
```

# Development

Please, read the [contribution guide](https://pubq.io/docs/basics/contribution).

## Setup

```bash
git clone git@github.com:pubqio/pubq-python.git
cd ./pubq-python/
poetry install
```

## Build

```bash
poetry build
```

## Tests

To run tests using pytest:

```bash
poetry run pytest
```

## Example

To run pubsub example:

```bash
cd examples/
python pubsub.py
```
