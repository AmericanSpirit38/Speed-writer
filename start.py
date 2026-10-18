from pygments.lexer import words
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
    global sentences
    sentences = generate_sentences(num_sentence=int(num_sentence), len_sentence=int(len_sentence))
    layout = Layout()
    layout.split_row(Layout(name='game', ratio=1))
    layout["game"].update(
            Panel(
                "[bold blue]SpeedWriter[/bold blue]\n\n" + f"You have {game_length} seconds to type the following sentences:\n"
                + "Start typing fast!!\n\n" + "[bold yellow]Sentences: [/bold yellow]\n" + "".join([f"{sentence}\n" for sentence in sentences]),
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
def calculate_mistakes(inp, sentences):
    mistakes = 0
    splitsentence = [sentence.replace('.', '').replace(',', '').split(' ') for sentence in sentences]
    words = []
    for sentence in splitsentence:
        words.extend(sentence)
    inp = inp.lower().split()
    for i, wrd in enumerate(inp):
        if wrd != words[i].lower() and wrd not in words[i].lower():
            mistakes += 1
    return mistakes

def evaluate(inp, game_length, sentences):
    wpm = (len(inp)/5) / (game_length/60)
    console.clear()
    console.print(f"[bold green]Your WPM: {wpm:.2f}[/bold green]")
    mistakes = calculate_mistakes(inp, sentences)
    accuracy = mistakes / len(inp.split(" ")) * 100
    console.print(f"[bold red]Mistakes: {mistakes}[/bold red]")
    console.print(f"[bold blue]Accuracy: {accuracy:.2f}%[/bold blue]")

    console.clear()

def play_again_question():
    return console.input("[yellow]Do you want to play again? (y/n): [/yellow] ").lower() in ['y', 'yes', '1']

def start():
    console.input("[yellow]Press Enter to start.[/yellow] ")
    countdown(3)
    create_game_screen()
    start_time = time.time()
    typed_text = get_user_input(start_time=start_time, time_limit=float(game_length))
    time_typed = measure_time(start_time=start_time)
    console.print(f"\n[bold cyan]You typed: [/bold cyan] {typed_text}")
    evaluate(typed_text, float(time_typed), sentences=sentences)
    if play_again_question():
        setup()
        start()


# CODE 
setup()
start()