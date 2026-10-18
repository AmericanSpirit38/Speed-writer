from rich.layout import Layout
from rich.console import Console
from rich.panel import Panel
from faker import Faker
import time
import json
import msvcrt

gen = Faker()
console = Console()
console.print(Panel.fit("SpeedWriter", style="bold blue"))

def countdown(num_sec):
    for i in range(num_sec, 0, -1):
        console.print(f'[bold yellow]{i}[/bold yellow]')
        time.sleep(1)
    console.print('[bold green]Go![/bold green]')
def generate_sentences(num_sentence: int, len_sentence: int) -> list:
    sentences: list = []
    for _ in range(num_sentence):
        sentences.append(gen.sentence(nb_words=len_sentence))
    return sentences
def check_valid_int(val) -> bool:
    try:
        int(val)
        return True
    except ValueError:
        return False
def check_json(path):
    try:
        with open(path) as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None
def check_yn_answer(val) -> bool:
    if val.lower() in ('y', 'yes', 'agree'):
        return True
    elif val.lower() in ('n', 'no', 'disagree'):
        return False
    else:
        console.print('[bold red]Invalid answer. Answer with only yes or no.[/bold red]')
        yn = console.input("[dim][Y/n] [/dim]")
        return check_yn_answer(yn)
def setup():
    global game_length, num_sentence, len_sentence
    settings = check_json('settings.json')
    if settings is not None:
        console.print('[bold yellow]Do you want to keep your previous setting?[/bold yellow]')
        yn = console.input("[dim][Y/n] [/dim]")
        if check_yn_answer(yn):
            console.print('[bold green]Keeping previous settings.[/bold green]')
            game_length = int(settings['time'])
            num_sentence = int(settings['num_sentence'])
            len_sentence = int(settings['len_sentence'])
            return None
        else:
            console.print('[bold green]Setting new settings.[/bold green]')
    console.print("[dim]Please enter positive integers[/dim]")
    game_length = console.input('Time in seconds: ')
    if not check_valid_int(game_length):
        console.print('[bold red]Invalid time. Please enter a positive integer.[/bold red]')
        return setup()
    num_sentence = console.input('Number of sentences: ')
    if not check_valid_int(num_sentence):
        console.print('[bold red]Invalid number of sentences. Please enter a positive integer.[/bold red]')
        return setup()
    len_sentence = console.input('Length of sentences: ')
    if not check_valid_int(len_sentence):
        console.print('[bold red]Invalid length of sentences. Please enter a positive integer.[/bold red]')
        return setup()
    game_length = int(game_length)
    num_sentence = int(num_sentence)
    len_sentence = int(len_sentence)
    data = {'time': int(game_length), 'num_sentence': int(num_sentence), 'len_sentence': int(len_sentence)}
    with open('settings.json', 'w') as file:
        json.dump(data, file)
        return None
def create_game_screen():
    layout = Layout()
    layout.split_row(Layout(name='game', ratio=1))
    layout["game"].update(
            Panel(
                "[bold blue]SpeedWriter[/bold blue]\n\n" + f"You have {game_length} seconds to type the following sentences:\n"
                + "Start typing fast!!\n\n" + "[bold yellow]Sentences: [/bold yellow]\n" + "".join([f"{sentence}\n" for sentence in generate_sentences(num_sentence=int(num_sentence), len_sentence=int(len_sentence))]),
                title="Game"
            )
        )
    console.print(layout)
def measure_time(start_time: float) -> float:
    return time.time() - start_time

def get_user_input(start_time: float, time_limit: float) -> list:
    chars = []
    while measure_time(start_time) < time_limit:
        if msvcrt.kbhit():
            ch = msvcrt.getwch()  # waits for one key
            if ch == '\r':  # Enter
                break
            elif ch == '\b':  # Backspace
                if chars:
                    chars.pop()
                    print('\b \b', end='', flush=True)
            else:
                chars.append(ch)
            print(ch, end='', flush=True)
    return ''.join(chars)

def start():
    console.input("[yellow]Press Enter to start.[/yellow] ")
    countdown(3)
    create_game_screen()
    typed_text = get_user_input(start_time=time.time(), time_limit=float(game_length))
    console.print(f"\n[bold cyan]You typed: [/bold cyan] {typed_text}")

# CODE 
setup()
start()