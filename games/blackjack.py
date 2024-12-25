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
    if rank in ['K', 'Q', 'J']:
        return 10
    elif rank == 'A':
        return 11
    return int(rank)

def hand_value(hand):
    value = 0
    aces = 0

    for card in hand:
        if card[0] == 'A':
            aces += 1
        else:
            value += card_value(card)

    for _ in range(aces):
        if value + 11 <= 21:
            value += 11
        else:
            value += 1

    return value

def display_hand(hand, hide_first=False):
    cards = []
    for i, (rank, suit) in enumerate(hand):
        if i == 0 and hide_first:
            cards.append('[red]?? ?[/red]')
        else:
            cards.append(f'[white]{rank}{suit}[/white]')
    return ' '.join(cards)

def dramatic_card_deal(card, is_dealer=False, hide_card=False):
    console.print("\n[cyan]Distribuzione carta...[/cyan]")
    with Progress() as progress:
        task = progress.add_task("[cyan]", total=100)
        while not progress.finished:
            progress.update(task, advance=2)
            time.sleep(0.01)

    prefix = "[red]Il Banchiere[/red]" if is_dealer else "[cyan]Tu[/cyan]"
    if hide_card:
        console.print(f"{prefix} riceve: [red]?? ?[/red]")
    else:
        rank, suit = card
        console.print(f"{prefix} riceve: [white]{rank}{suit}[/white]")
    time.sleep(0.5)

def get_cash_out_percentage(score):
    """
    Calcola la percentuale di rimborso in base al punteggio della mano
    """
    if score >= 20:
        return 0.9  # 90% della puntata
    elif score >= 19:
        return 0.8  # 80% della puntata
    elif score >= 18:
        return 0.7  # 70% della puntata
    elif score >= 17:
        return 0.6  # 60% della puntata
    elif score >= 16:
        return 0.5  # 50% della puntata
    elif score >= 15:
        return 0.4  # 40% della puntata
    elif score >= 14:
        return 0.3  # 30% della puntata
    else:
        return 0.2  # 20% della puntata

def play(state, banker):
    deck = create_deck()
    random.shuffle(deck)

    banker.game_taunt('blackjack')

    while True:
        console.print("\n[green]===== BLACKJACK =====[/green]")
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

        # Distribuzione carte iniziali con animazione
        console.print("\n[cyan]Il Banchiere distribuisce le carte...[/cyan]")
        time.sleep(1)

        player_hand = []
        dealer_hand = []

        # Distribuisci prima carta al giocatore
        new_card = deck.pop()
        dramatic_card_deal(new_card)
        player_hand.append(new_card)

        # Prima carta al banchiere (nascosta)
        new_card = deck.pop()
        dramatic_card_deal(new_card, is_dealer=True, hide_card=True)
        dealer_hand.append(new_card)

        # Seconda carta al giocatore
        new_card = deck.pop()
        dramatic_card_deal(new_card)
        player_hand.append(new_card)

        # Seconda carta al banchiere (visibile)
        new_card = deck.pop()
        dramatic_card_deal(new_card, is_dealer=True)
        dealer_hand.append(new_card)

        while True:
            console.print("\n[purple]Mano del Banchiere:[/purple]", display_hand(dealer_hand, hide_first=True))
            console.print("[cyan]La tua mano:[/cyan]", display_hand(player_hand))

            player_value = hand_value(player_hand)
            console.print(f"[green]Il tuo punteggio totale: {player_value}[/green]")

            if player_value == 21:
                console.print("[green]Blackjack![/green]")
                banker.win_response('big_win')
                state.update_chips(int(bet * 1.5))
                break
            elif player_value > 21:
                console.print("[red]Sballato![/red]")
                banker.lose_response('big_loss')
                state.update_chips(-bet)
                break

            action = Prompt.ask("Cosa vuoi fare", choices=["carta", "stai", "cash_out"])

            if action == "carta":
                new_card = deck.pop()
                dramatic_card_deal(new_card)
                player_hand.append(new_card)
            elif action == "cash_out":
                cash_out_percentage = get_cash_out_percentage(player_value)
                cash_out_value = int(bet * cash_out_percentage)
                console.print(f"\n[yellow]Con un punteggio di {player_value}, puoi ottenere il {int(cash_out_percentage * 100)}% della tua puntata ({cash_out_value} fiches)[/yellow]")
                if Prompt.ask(f"\nVuoi incassare {cash_out_value} fiches?", choices=["s", "n"]) == "s":
                    console.print(f"[green]Hai incassato {cash_out_value} fiches![/green]")
                    state.update_chips(-bet + cash_out_value)  # Sottrai la puntata e aggiungi il valore del cash out
                    break
                continue
            else:
                # Turno del Banchiere
                console.print("\n[purple]Mano del Banchiere:[/purple]", display_hand(dealer_hand))
                while hand_value(dealer_hand) < 17:
                    new_card = deck.pop()
                    dramatic_card_deal(new_card, is_dealer=True)
                    dealer_hand.append(new_card)
                    console.print("[purple]Mano del Banchiere:[/purple]", display_hand(dealer_hand))
                    time.sleep(1)

                dealer_value = hand_value(dealer_hand)
                if dealer_value > 21:
                    console.print("[green]Il Banchiere ha sballato! Hai vinto![/green]")
                    banker.win_response()
                    state.update_chips(bet)
                elif dealer_value > player_value:
                    console.print("[red]Il Banchiere vince![/red]")
                    banker.lose_response()
                    state.update_chips(-bet)
                elif dealer_value < player_value:
                    console.print("[green]Hai vinto![/green]")
                    banker.win_response()
                    state.update_chips(bet)
                else:
                    console.print("[yellow]Pareggio![/yellow]")
                break

        if not Prompt.ask("\nVuoi giocare ancora?", choices=["s", "n"]) == "s":
            break

    state.save_game()