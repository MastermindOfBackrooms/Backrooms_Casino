from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import random
import time

console = Console()

def roll_dice(num_dice=2):
    return [random.randint(1, 6) for _ in range(num_dice)]

def check_come_out_roll(total):
    if total in [7, 11]:
        return "win"
    elif total in [2, 3, 12]:
        return "lose"
    return "point"

def show_betting_options(point=None, chips=0):
    table = Table(title="Opzioni di Scommessa")
    table.add_column("Tipo", style="cyan")
    table.add_column("Descrizione", style="green")
    table.add_column("Pagamento", style="yellow")

    if point is None:
        table.add_row("1", "Pass Line", "1:1")
        table.add_row("2", "Don't Pass", "1:1")
        table.add_row("3", "Lucky 7 (Somma 7)", "7:1")
        table.add_row("4", "Seventh Sign (7 consecutivi)", "77:1")
        table.add_row("5", "Seven's Prophecy", "17:1")
        if chips >= 7777:
            table.add_row("6", "Banker's Doom (Richiede 7777+ fiches)", "777:1")
        table.add_row("7", "Triple Seven's Curse", "777:1")
        table.add_row("8", "Seven Devils' Dance", "7x-77x")
    else:
        table.add_row("1", f"Point è {point}", "1:1")
        table.add_row("2", "Field (2,3,4,9,10,11,12)", "1:1, 2:1 per 2/12")
        table.add_row("3", "Any Craps (2,3,12)", "7:1")
        table.add_row("4", "Seven's Heaven (7 in 7 tiri)", "77:1")
        table.add_row("5", "Mystical Field (7,17,27)", "27:1")

    console.print(table)

def animate_roll(banker):
    console.print("\n[cyan]I dadi danzano nell'aria...[/cyan]")
    time.sleep(1)
    banker.game_taunt('craps')
    time.sleep(1)

def play(state, banker):
    while True:
        console.print("\n[yellow]♠ CRAPS - Il Gioco dei Dadi ♠[/yellow]")
        console.print("\n[red]Level 777 Special Edition[/red]")
        console.print(f"\nLe tue fiches: {state.chips}")

        if state.chips <= 0:
            console.print("[red]Non hai abbastanza fiches per giocare![/red]")
            return

        # Nuove variabili per le varianti speciali
        seventh_sign_active = False
        seventh_sign_count = 0
        prophecy_active = False
        prophecy_numbers = []
        triple_seven_count = 0
        devils_dance_active = False
        devils_dance_multiplier = 7

        point = None
        show_betting_options(point, state.chips)

        bet_type = Prompt.ask("Scegli il tipo di scommessa", choices=["1", "2", "3", "4", "5", "6", "7", "8", "E"])
        if bet_type == "E":
            break

        bet_amount = int(Prompt.ask("Quanto vuoi scommettere?", default="10"))
        while bet_amount > state.chips or bet_amount <= 0:
            console.print("[red]Scommessa non valida![/red]")
            bet_amount = int(Prompt.ask("Quanto vuoi scommettere?", default="10"))

        state.chips -= bet_amount

        # Gestione delle varianti speciali
        if bet_type == "6" and state.chips >= 7777:  # Banker's Doom
            console.print("\n[red]⚠️ BANKER'S DOOM ATTIVATO ⚠️[/red]")
            banker.special_message("777")
            animate_roll(banker)
            rolls = [sum(roll_dice()) for _ in range(3)]
            if all(r == 7 for r in rolls):
                winnings = bet_amount * 777
                state.chips += winnings
                console.print(f"\n[green]🎲 BANKER'S DOOM! Hai vinto {winnings} fiches! 🎲[/green]")
                banker.win_response('devils_defeated')
            else:
                console.print("\n[red]Il Banchiere ride della tua sfortuna...[/red]")
                banker.lose_response('devils_defeat')
            continue

        if bet_type == "7":  # Triple Seven's Curse
            console.print("\n[purple]Triple Seven's Curse Attivata[/purple]")
            for i in range(3):
                animate_roll(banker)
                roll = sum(roll_dice())
                if roll == 7:
                    triple_seven_count += 1
                    console.print(f"[cyan]Seven #{triple_seven_count}![/cyan]")
                else:
                    break

            if triple_seven_count == 3:
                winnings = bet_amount * 777
                state.chips += winnings
                console.print(f"\n[green]🎲 TRIPLE SEVEN'S CURSE! Hai vinto {winnings} fiches! 🎲[/green]")
                banker.win_response('mystical_sequence')
            else:
                console.print("\n[red]La maledizione si è spezzata...[/red]")
                banker.lose_response('normal')
            continue

        if bet_type == "8":  # Seven Devils' Dance
            console.print("\n[red]Seven Devils' Dance Iniziata[/red]")
            devils_dance_active = True
            devils_dance_wins = 0

            for dance_round in range(7):
                console.print(f"\n[red]Danza #{dance_round + 1}[/red]")
                console.print(f"[yellow]Moltiplicatore attuale: x{devils_dance_multiplier}[/yellow]")

                animate_roll(banker)
                roll = sum(roll_dice())

                if roll == 7:
                    devils_dance_wins += 1
                    winnings = bet_amount * devils_dance_multiplier
                    state.chips += winnings
                    console.print(f"[green]Vittoria! +{winnings} fiches[/green]")
                    devils_dance_multiplier += 10
                    banker.win_response('streak')
                else:
                    console.print("[red]I demoni vincono questo round...[/red]")
                    banker.lose_response('devils_defeat')
                    devils_dance_multiplier = max(7, devils_dance_multiplier - 5)

                time.sleep(1)

            if devils_dance_wins >= 4:
                bonus = bet_amount * 77
                state.chips += bonus
                console.print(f"\n[green]BONUS DEVILS' DANCE! +{bonus} fiches[/green]")
                banker.win_response('devils_defeated')
            continue


        # Gestione delle varianti speciali pre-point
        if bet_type == "4" and point is None:  # Seventh Sign
            console.print("\n[cyan]Seventh Sign Attivato[/cyan]")
            seventh_sign_active = True
            seventh_sign_count = 0
        elif bet_type == "5" and point is None:  # Seven's Prophecy
            console.print("\n[cyan]Seven's Prophecy Attivata[/cyan]")
            prophecy_active = True
            prophecy_numbers = []

        # Prima fase: Come Out roll
        console.print("\n[cyan]Come Out Roll[/cyan]")
        dice = roll_dice()
        total = sum(dice)
        console.print(f"Dadi: {dice} (Totale: {total})")

        # Gestione Seven's Prophecy
        if prophecy_active:
            prophecy_numbers.append(total)
            if len(prophecy_numbers) == 3:
                if all(n % 7 == 0 for n in prophecy_numbers):
                    winnings = bet_amount * 17
                    state.chips += winnings
                    console.print(f"[green]Profezia del Sette completata! Hai vinto {winnings} fiches![/green]")
                    banker.special_message("777")
                else:
                    console.print("[red]La profezia è fallita![/red]")
                continue

        # Gestione Seventh Sign
        if seventh_sign_active:
            if total == 7:
                seventh_sign_count += 1
                console.print(f"[cyan]Seventh Sign: {seventh_sign_count}/7[/cyan]")
                if seventh_sign_count == 7:
                    winnings = bet_amount * 77
                    state.chips += winnings
                    console.print(f"[green]SEVENTH SIGN COMPLETATO! Hai vinto {winnings} fiches![/green]")
                    banker.special_message("777")
                    continue
            else:
                console.print("[red]Seventh Sign fallito![/red]")
                continue

        result = check_come_out_roll(total)

        if result == "win" and bet_type == "1" or result == "lose" and bet_type == "2":
            winnings = bet_amount * 2
            state.chips += winnings
            console.print(f"[green]Hai vinto {winnings} fiches![/green]")
            if total == 7:
                banker.special_message("777")
        elif result == "lose" and bet_type == "1" or result == "win" and bet_type == "2":
            console.print("[red]Hai perso![/red]")
        else:
            point = total
            console.print(f"\n[yellow]Point è {point}[/yellow]")

            seven_counter = 0
            rolls_remaining = 7
            heavens_bet = 0

            if Prompt.ask("\nVuoi tentare Seven's Heaven? (7 in 7 tiri)", choices=["s", "n"]) == "s":
                heavens_bet = int(Prompt.ask("Quanto vuoi scommettere su Seven's Heaven?", default="5"))
                while heavens_bet > state.chips or heavens_bet <= 0:
                    console.print("[red]Scommessa non valida![/red]")
                    heavens_bet = int(Prompt.ask("Quanto vuoi scommettere?", default="5"))
                state.chips -= heavens_bet

            while True:
                show_betting_options(point, state.chips)
                bet_choice = Prompt.ask("Vuoi fare una scommessa aggiuntiva?", choices=["1", "2", "3", "4", "5", "N"])

                if bet_choice == "N":
                    break

                side_bet = int(Prompt.ask("Quanto vuoi scommettere?", default="5"))
                while side_bet > state.chips or side_bet <= 0:
                    console.print("[red]Scommessa non valida![/red]")
                    side_bet = int(Prompt.ask("Quanto vuoi scommettere?", default="5"))

                state.chips -= side_bet
                dice = roll_dice()
                total = sum(dice)
                console.print(f"\nDadi: {dice} (Totale: {total})")

                # Conteggio per Seven's Heaven
                if heavens_bet > 0:
                    rolls_remaining -= 1
                    if total == 7:
                        seven_counter += 1
                        console.print(f"[cyan]Seven's Heaven: {seven_counter}/7 (Tiri rimasti: {rolls_remaining})[/cyan]")

                # Gestione scommesse aggiuntive
                if bet_choice == "2" and total in [2, 3, 4, 9, 10, 11, 12]:
                    multiplier = 2 if total in [2, 12] else 1
                    winnings = side_bet * (multiplier + 1)
                    state.chips += winnings
                    console.print(f"[green]Hai vinto {winnings} fiches sulla scommessa Field![/green]")
                elif bet_choice == "3" and total in [2, 3, 12]:
                    winnings = side_bet * 8
                    state.chips += winnings
                    console.print(f"[green]Hai vinto {winnings} fiches su Any Craps![/green]")
                elif bet_choice == "4" and total == 7 and heavens_bet > 0 and seven_counter == 7:
                    winnings = heavens_bet * 77
                    state.chips += winnings
                    console.print(f"[green]SEVEN'S HEAVEN! Hai vinto {winnings} fiches![/green]")
                    banker.special_message("777")
                elif bet_choice == "5" and total in [7, 17, 27]:  # Mystical Field
                    winnings = side_bet * 27
                    state.chips += winnings
                    console.print(f"[green]MYSTICAL FIELD! Hai vinto {winnings} fiches![/green]")
                    banker.special_message("777")
                else:
                    console.print("[red]Hai perso la scommessa aggiuntiva![/red]")

                if total == point:
                    if bet_type == "1":
                        winnings = bet_amount * 2
                        state.chips += winnings
                        console.print(f"[green]Hai vinto {winnings} fiches sulla scommessa principale![/green]")
                    break
                elif total == 7:
                    if bet_type == "2":
                        winnings = bet_amount * 2
                        state.chips += winnings
                        console.print(f"[green]Hai vinto {winnings} fiches sulla scommessa principale![/green]")
                    banker.special_message("777")
                    break

                # Verifica Seven's Heaven
                if heavens_bet > 0 and rolls_remaining == 0:
                    if seven_counter == 7:
                        winnings = heavens_bet * 77
                        state.chips += winnings
                        console.print(f"[green]SEVEN'S HEAVEN! Hai vinto {winnings} fiches![/green]")
                        banker.special_message("777")
                    else:
                        console.print("[red]Seven's Heaven fallito![/red]")
                    break

        if state.chips <= 0:
            console.print("[red]Hai finito le fiches![/red]")
            break

        if not Prompt.ask("\nVuoi continuare a giocare?", choices=["s", "n"]) == "s":
            break