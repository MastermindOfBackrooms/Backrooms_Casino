from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress
import random
import time

console = Console()

ROULETTE_WHEEL = """
  [red]3[/red]  [black]6[/black]  [red]9[/red]  [red]12[/red] [black]15[/black] [red]18[/red] [red]21[/red] [black]24[/black] [red]27[/red] [red]30[/red] [black]33[/black] [red]36[/red]
[black]2[/black]  [red]5[/red]  [black]8[/black] [black]11[/black] [red]14[/red] [black]17[/black] [black]20[/black] [red]23[/red] [black]26[/black] [black]29[/black] [red]32[/red] [black]35[/black]
 [red]1[/red]  [black]4[/black]  [red]7[/red]  [black]10[/black] [black]13[/black] [red]16[/red] [red]19[/red] [black]22[/black] [red]25[/red] [black]28[/black] [black]31[/black] [red]34[/red]
                         [green]0[/green]
"""

def get_bet_type():
    console.print("\n[yellow]Tipi di Puntata:[/yellow]")
    console.print("1. Numero Singolo (35:1)")
    console.print("2. Rosso/Nero (1:1)")
    console.print("3. Pari/Dispari (1:1)")
    console.print("4. 1-18/19-36 (1:1)")
    return Prompt.ask("Scegli il tipo di puntata", choices=["1", "2", "3", "4"])

def get_bet_details(bet_type):
    if bet_type == "1":
        number = Prompt.ask("Scegli un numero", default="0")
        try:
            number = int(number)
            if 0 <= number <= 36:
                return ("number", number)
        except ValueError:
            pass
        console.print("[red]Numero non valido![/red]")
        return None

    elif bet_type == "2":
        color = Prompt.ask("Scegli il colore", choices=["rosso", "nero"])
        return ("color", "red" if color == "rosso" else "black")

    elif bet_type == "3":
        parity = Prompt.ask("Scegli", choices=["pari", "dispari"])
        return ("parity", "even" if parity == "pari" else "odd")

    else:  # bet_type == "4"
        range_choice = Prompt.ask("Scegli l'intervallo", choices=["1-18", "19-36"])
        return ("range", range_choice)

def animate_spin():
    console.print("\n[cyan]La ruota della roulette gira...[/cyan]")
    with Progress() as progress:
        task = progress.add_task("[cyan]", total=100)
        while not progress.finished:
            progress.update(task, advance=1)
            time.sleep(0.05)

    # Animazione del rimbalzo della pallina
    console.print("\n[cyan]La pallina rimbalza...[/cyan]")
    bounces = ["[red]⚪[/red]", "[black]⚪[/black]", "[green]⚪[/green]"]
    for _ in range(5):
        for bounce in bounces:
            console.print(bounce, end="\r")
            time.sleep(0.2)

def check_win(bet_details, number):
    bet_type, value = bet_details

    if bet_type == "number":
        return value == number, 35

    elif bet_type == "color":
        red_numbers = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
        is_red = number in red_numbers
        return (value == "red" and is_red) or (value == "black" and not is_red), 1

    elif bet_type == "parity":
        if number == 0:
            return False, 1
        is_even = number % 2 == 0
        return (value == "even" and is_even) or (value == "odd" and not is_even), 1

    else:  # range
        if value == "1-18":
            return 1 <= number <= 18, 1
        else:
            return 19 <= number <= 36, 1

def play(state, banker):
    banker.game_taunt('roulette')

    while True:
        console.print("\n[green]===== ROULETTE =====[/green]")
        console.print(ROULETTE_WHEEL)
        console.print(f"[yellow]Le tue fiches: {state.chips}[/yellow]")

        bet = Prompt.ask("Inserisci la tua puntata", default="100")
        try:
            bet = int(bet)
            if bet > state.chips:
                console.print("[red]Non hai abbastanza fiches![/red]")
                continue
        except ValueError:
            console.print("[red]Puntata non valida![/red]")
            continue

        bet_type = get_bet_type()
        bet_details = get_bet_details(bet_type)

        if not bet_details:
            continue

        # Animazione del giro della ruota
        animate_spin()

        number = random.randint(0, 36)
        color = "red" if number in [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36] else "black"
        color = "green" if number == 0 else color
        console.print(f"\n[green]La pallina si ferma sul {number}![/green] [{color}]●[/{color}]")

        won, multiplier = check_win(bet_details, number)

        if won:
            winnings = bet * multiplier
            console.print(f"[green]Hai vinto {winnings} fiches![/green]")
            banker.win_response('big_win' if multiplier > 1 else 'normal')
            state.update_chips(winnings)
        else:
            console.print("[red]Hai perso![/red]")
            banker.lose_response('normal')
            state.update_chips(-bet)

        if not Prompt.ask("\nVuoi giocare ancora?", choices=["s", "n"]) == "s":
            break

    state.save_game()