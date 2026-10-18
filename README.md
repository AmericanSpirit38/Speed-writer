# SpeedWriter

A terminal-based typing speed game built with **Python** and **Rich**.

SpeedWriter generates random sentences and lets you type them under a time limit, then shows:

- **WPM (Words Per Minute)**
- **Mistakes**
- **Accuracy**

## Features

- Colorful terminal UI using [`rich`](https://github.com/Textualize/rich)
- Random sentence generation using [`faker`](https://faker.readthedocs.io/)
- Configurable:
  - game length (seconds)
  - number of sentences
  - sentence length (words)
- Settings persistence in `settings.json`
- Character-by-character typing input (Windows) via `msvcrt`
- Replay prompt after each game

## Project Structure

- `start.py` - main game script
- `settings.json` - saved game settings (created/updated automatically)

## Requirements

- Python **3.9+** (recommended)
- Windows (current input implementation uses `msvcrt`)

Python packages:

- `rich`
- `faker`

## Installation

Install dependencies:

```powershell
pip install rich faker