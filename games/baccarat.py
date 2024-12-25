from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress
import random
import time

console = Console()

def create_deck():
    suits = ['♥️', '♦️', '♣️', '♠️']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    return [(rank, suit) for suit in suits for rank in ranks]

def card_value(card):
    rank = card[0]
    if rank in ['10', 'J', 'Q', 'K']:
        return 0
    elif rank == 'A':
        return 1
    return int(rank)

def calculate_total(hand):
    return sum(card_value(card) for card in hand) % 10

def dramatic_card_deal(card, is_banker=False):
    console.print("\n[cyan]Distribuzione carta...[/cyan]")
    with Progress() as progress:
        task = progress.add_task("[cyan]", total=100)
        while not progress.finished:
            progress.update(task, advance=2)
            time.sleep(0.01)

    prefix = "[red]Il Banchiere[/red]" if is_banker else "[cyan]Il Punto[/cyan]"
    rank, suit = card
    console.print(f"{prefix} riceve: [white]{rank}{suit}[/white]")
    time.sleep(0.5)

def display_hand(hand, hide=False):
    if hide:
        return "[red]?? ?[/red] " * len(hand)
    return " ".join(f"[white]{rank}{suit}[/white]" for rank, suit in hand)

def should_draw_third_card(total, is_banker=False, player_third=None):
    if is_banker:
        if total <= 2:
            return True
        elif total == 3 and player_third != 8:
            return True
        elif total == 4 and player_third in [2, 3, 4, 5, 6, 7]:
            return True
        elif total == 5 and player_third in [4, 5, 6, 7]:
            return True
        elif total == 6 and player_third in [6, 7]:
            return True
        return False
    else:  # Player drawing rules
        return total <= 5

def play_punto_banco(state, banker):
    banker.game_taunt('baccarat')

    while True:
        console.print("\n[green]===== BACCARAT - PUNTO BANCO =====[/green]")
        console.print(f"[yellow]Le tue fiches: {state.chips}[/yellow]")

        # Scommessa
        console.print("\n[yellow]Su chi vuoi scommettere?[/yellow]")
        console.print("1. Punto (Paga 1:1)")
        console.print("2. Banco (Paga 0.95:1)")
        console.print("3. Pareggio (Paga 8:1)")
        
        bet_choice = Prompt.ask("Scegli", choices=["1", "2", "3"])
        bet = Prompt.ask("Inserisci la tua puntata", default="100")
        
        try:
            bet = int(bet)
            if bet > state.chips:
                console.print("[red]Non hai abbastanza fiches![/red]")
                continue
        except ValueError:
            console.print("[red]Puntata non valida![/red]")
            continue

        deck = create_deck()
        random.shuffle(deck)

        # Distribuzione iniziale
        player_hand = []
        banker_hand = []

        # Prima carta per ciascuno
        card = deck.pop()
        dramatic_card_deal(card)
        player_hand.append(card)

        card = deck.pop()
        dramatic_card_deal(card, is_banker=True)
        banker_hand.append(card)

        # Seconda carta per ciascuno
        card = deck.pop()
        dramatic_card_deal(card)
        player_hand.append(card)

        card = deck.pop()
        dramatic_card_deal(card, is_banker=True)
        banker_hand.append(card)

        # Mostra i totali iniziali
        player_total = calculate_total(player_hand)
        banker_total = calculate_total(banker_hand)

        console.print(f"\n[cyan]Mano del Punto:[/cyan] {display_hand(player_hand)} = {player_total}")
        console.print(f"[red]Mano del Banco:[/red] {display_hand(banker_hand)} = {banker_total}")

        # Regole per la terza carta
        player_third = None
        if should_draw_third_card(player_total):
            card = deck.pop()
            dramatic_card_deal(card)
            player_hand.append(card)
            player_third = card_value(card)
            player_total = calculate_total(player_hand)
            console.print(f"[cyan]Nuovo totale del Punto:[/cyan] {player_total}")

        if should_draw_third_card(banker_total, True, player_third):
            card = deck.pop()
            dramatic_card_deal(card, is_banker=True)
            banker_hand.append(card)
            banker_total = calculate_total(banker_hand)
            console.print(f"[red]Nuovo totale del Banco:[/red] {banker_total}")

        # Determina il vincitore
        console.print("\n[yellow]Risultato finale:[/yellow]")
        console.print(f"[cyan]Punto:[/cyan] {player_total}")
        console.print(f"[red]Banco:[/red] {banker_total}")

        if bet_choice == "1":  # Punto
            if player_total > banker_total:
                console.print(f"\n[green]Hai vinto {bet} fiches![/green]")
                banker.win_response()
                state.update_chips(bet)
            else:
                console.print("\n[red]Hai perso![/red]")
                banker.lose_response()
                state.update_chips(-bet)
        elif bet_choice == "2":  # Banco
            if banker_total > player_total:
                winnings = int(bet * 0.95)
                console.print(f"\n[green]Hai vinto {winnings} fiches![/green]")
                banker.win_response()
                state.update_chips(winnings)
            else:
                console.print("\n[red]Hai perso![/red]")
                banker.lose_response()
                state.update_chips(-bet)
        else:  # Pareggio
            if player_total == banker_total:
                console.print(f"\n[green]Hai vinto {bet * 8} fiches![/green]")
                banker.win_response('big_win')
                state.update_chips(bet * 8)
            else:
                console.print("\n[red]Hai perso![/red]")
                banker.lose_response()
                state.update_chips(-bet)

        if not Prompt.ask("\nVuoi giocare ancora?", choices=["s", "n"]) == "s":
            break

    state.save_game()
