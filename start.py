import rich
from rich.layout import Layout
from rich.console import Console
from rich.panel import Panel
from faker import Faker
import time
import json

gen = Faker()
console = Console()
console.print(Panel.fit("SpeedWriter", style="bold blue"))

def countdown(num_sec):
    for second in range(num_sec, 0, -1):
        console.print(second)
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
    global time, num_sentence, len_sentence
    settings = check_json('settings.json')
    if settings is not None:
        console.print('[bold yellow]Do you want to keep your previous setting?[/bold yellow]')
        yn = console.input("[dim][Y/n] [/dim]")
        if check_yn_answer(yn):
            console.print('[bold green]Keeping previous settings.[/bold green]')
            time = settings['time']
            num_sentence = settings['num_sentence']
            len_sentence = settings['len_sentence']
            return
        else:
            console.print('[bold green]Setting new settings.[/bold green]')
    console.print("[dim]Please enter positive integers[/dim]")
    length = console.input('Time in seconds: ')
    if not check_valid_int(length):
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
    data = {'time': int(length), 'num_sentence': int(num_sentence), 'len_sentence': int(len_sentence)}
    with open('settings.json', 'w') as file:
        json.dump(data, file)
def create_game_screen():
    layout = Layout()
    layout.split_row(Layout(name='game', ratio=1))
    layout["game"].update(
            Panel(
                "[bold blue]SpeedWriter[/bold blue]\n\n" + f"You have {time} seconds to type the following sentences:\n"
                "Start typing fast!!\n\n" + "[bold yellow]Sentences: [/bold yellow]\n" + "".join([f"{sentence}\n" for sentence in generate_sentences(num_sentence=num_sentence, len_sentence=len_sentence)]),
                title="Game"
            )
        )
    console.print(layout)
def start():
    console.input("[yellow]Press Enter to start.[/yellow] ")
    create_game_screen()

setup()
start()