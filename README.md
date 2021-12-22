# Foobartory

Building an automated `foobar` factory in Python for a coding challenge. It uses `asyncio` for multiprocessing.

## Docs

The full instructions (in French) are available [here](docs/instructions).

## Usage

To use this package, you need to run Python 3.7 or newer.

```sh
python3 start.py
```

## Configuration

All variables are located in the [configuration file](foobartory/config.py), from the target number of robots to the cost of each item.

You can play with the "speed" of the Foobartory by changing the `DURATION_MODIFIER` variable. Use `1` for actual seconds, default is `0.01`.

Note that duration shown in the logs has been adjusted for actual speed, regardless of the `DURATION_MODIFIER` in your configuration.

## Improvement ideas

- Add unit tests
- Improve the logic for robots to choose their next task
- Specialize the robots to avoid losing time when switching activities

## Meta

Nicolas Spehler – [@NSpehler](https://twitter.com/NSpehler)
