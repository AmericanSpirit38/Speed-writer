# SpeedWriter

A terminal typing speed game built with Python, Rich, and Faker.

## Features

- Random sentence generation
- Countdown and timed typing session
- WPM, mistakes, and accuracy output
- Saved settings in `settings.json`
- Replay prompt after each round

## Requirements

- Python 3.9+
- Windows (input uses `msvcrt`)

## Project Files

- `start.py`: game logic
- `speedwriter/__main__.py`: package entry point
- `requirements.txt`: dependency list
- `pyproject.toml`: package metadata and console script

## Quick Start

Install from source and run the command:

```powershell
python -m pip install .
speedwriter
```

For development mode (editable install):

```powershell
python -m pip install -e .
speedwriter
```

If you only want dependencies without installing the package:

```powershell
python -m pip install -r requirements.txt
python .\start.py
```

## How It Works

1. Choose existing settings or enter new values.
2. Press Enter to begin.
3. Type until time runs out or you press Enter.
4. Review results and choose whether to play again.

## Notes

- `console.input()` is line-based, so Enter submits the line.
- Real-time key capture is handled with `msvcrt.kbhit()` + `msvcrt.getwch()`.
