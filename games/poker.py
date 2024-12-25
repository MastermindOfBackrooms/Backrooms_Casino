from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress
import random
import time
from itertools import combinations

console = Console()

def create_deck():
    suits = ['♥️', '♦️', '♣️', '♠️']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    return [(rank, suit) for suit in suits for rank in ranks]

def get_rank_value(rank):
    if rank == 'A':
        return 14
    elif rank == 'K':
        return 13
    elif rank == 'Q':
        return 12
    elif rank == 'J':
        return 11
    return int(rank)

def evaluate_hand(cards):
    """Valuta una mano di poker e restituisce un punteggio."""
    if len(cards) != 5:
        return (-1, [])  # Invalid hand

    ranks = [card[0] for card in cards]
    suits = [card[1] for card in cards]
    values = sorted([get_rank_value(rank) for rank in ranks], reverse=True)
    is_flush = len(set(suits)) == 1
    is_straight = all(values[i] - values[i+1] == 1 for i in range(len(values)-1))

    # Conta le occorrenze di ogni valore
    value_counts = {}
    for value in values:
        value_counts[value] = value_counts.get(value, 0) + 1
    counts = sorted(value_counts.values(), reverse=True)

    # Determina il tipo di mano
    if is_straight and is_flush:
        if values[0] == 14:  # Royal Flush
            return (10, values)
        return (9, values)  # Straight Flush
    elif counts[0] == 4:
        return (8, values)  # Four of a Kind
    elif counts == [3, 2]:
        return (7, values)  # Full House
    elif is_flush:
        return (6, values)  # Flush
    elif is_straight:
        return (5, values)  # Straight
    elif counts[0] == 3:
        return (4, values)  # Three of a Kind
    elif counts[:2] == [2, 2]:
        return (3, values)  # Two Pair
    elif counts[0] == 2:
        return (2, values)  # One Pair
    return (1, values)  # High Card

def find_best_hand(cards):
    """Trova la migliore mano di 5 carte tra tutte le possibili combinazioni."""
    best_hand = None
    best_score = (-1, [])

    for hand in combinations(cards, 5):
        score = evaluate_hand(hand)
        if score[0] > best_score[0] or (score[0] == best_score[0] and score[1] > best_score[1]):
            best_score = score
            best_hand = hand

    return best_hand, best_score

def dramatic_card_deal(card, is_dealer=False, is_community=False):
    console.print("\n[cyan]Distribuzione carta...[/cyan]")
    with Progress() as progress:
        task = progress.add_task("[cyan]", total=100)
        while not progress.finished:
            progress.update(task, advance=2)
            time.sleep(0.01)

    if is_community:
        prefix = "[yellow]Sul tavolo[/yellow]"
    else:
        prefix = "[red]Il Banchiere[/red]" if is_dealer else "[cyan]Tu[/cyan]"

    rank, suit = card
    console.print(f"{prefix} ricevi: [white]{rank}{suit}[/white]")
    time.sleep(0.5)

def display_hand(hand, hide=False):
    if hide:
        return "[red]?? ?[/red] " * len(hand)
    return " ".join(f"[white]{rank}{suit}[/white]" for rank, suit in hand)

def play(state, banker):
    banker.game_taunt('poker')

    while True:
        console.print("\n[green]===== POKER TEXAS HOLD'EM =====[/green]")
        console.print(f"[yellow]Le tue fiches: {state.chips}[/yellow]")

        # Puntata iniziale
        bet = Prompt.ask("Inserisci la tua puntata iniziale", default="100")
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

        # Distribuisci le carte iniziali
        console.print("\n[cyan]Il Banchiere distribuisce le carte iniziali...[/cyan]")
        time.sleep(1)

        player_hand = []
        dealer_hand = []
        community_cards = []
        pot = bet * 2  # Il dealer pareggia sempre la puntata

        # Hole cards
        for _ in range(2):
            card = deck.pop()
            dramatic_card_deal(card)
            player_hand.append(card)

            card = deck.pop()
            dramatic_card_deal(card, is_dealer=True)
            dealer_hand.append(card)

        # Pre-flop
        console.print("\n[purple]Mano del Banchiere:[/purple]", display_hand(dealer_hand, hide=True))
        console.print("[cyan]La tua mano:[/cyan]", display_hand(player_hand))

        # Flop
        if Prompt.ask("\nVuoi vedere il flop?", choices=["s", "n"]) == "s":
            console.print("\n[yellow]Il Banchiere distribuisce il flop...[/yellow]")
            time.sleep(1)
            for _ in range(3):
                card = deck.pop()
                dramatic_card_deal(card, is_community=True)
                community_cards.append(card)

            # Mostra le carte comuni
            console.print("\n[yellow]Carte sul tavolo:[/yellow]", display_hand(community_cards))

            # Turn
            if Prompt.ask("\nVuoi vedere il turn?", choices=["s", "n"]) == "s":
                bet = int(bet * 1.5)  # Aumenta la puntata
                if bet > state.chips:
                    console.print("[red]Non hai abbastanza fiches per continuare![/red]")
                    state.update_chips(-int(pot/2))
                    continue
                pot += bet * 2

                card = deck.pop()
                console.print("\n[yellow]Il Banchiere distribuisce il turn...[/yellow]")
                dramatic_card_deal(card, is_community=True)
                community_cards.append(card)
                console.print("[yellow]Carte sul tavolo:[/yellow]", display_hand(community_cards))

                # River
                if Prompt.ask("\nVuoi vedere il river?", choices=["s", "n"]) == "s":
                    bet = int(bet * 1.5)  # Aumenta ancora la puntata
                    if bet > state.chips:
                        console.print("[red]Non hai abbastanza fiches per continuare![/red]")
                        state.update_chips(-int(pot/2))
                        continue
                    pot += bet * 2

                    card = deck.pop()
                    console.print("\n[yellow]Il Banchiere distribuisce il river...[/yellow]")
                    dramatic_card_deal(card, is_community=True)
                    community_cards.append(card)

                    # Showdown
                    console.print("\n[yellow]Showdown![/yellow]")
                    console.print("[purple]Mano del Banchiere:[/purple]", display_hand(dealer_hand))
                    console.print("[cyan]La tua mano:[/cyan]", display_hand(player_hand))
                    console.print("[yellow]Carte sul tavolo:[/yellow]", display_hand(community_cards))

                    # Calcola il punteggio delle mani
                    all_cards = player_hand + community_cards
                    player_best_hand, player_score = find_best_hand(all_cards)

                    dealer_cards = dealer_hand + community_cards
                    dealer_best_hand, dealer_score = find_best_hand(dealer_cards)

                    console.print("\n[cyan]La tua migliore mano:[/cyan]", display_hand(player_best_hand))
                    console.print("[purple]Migliore mano del Banchiere:[/purple]", display_hand(dealer_best_hand))

                    if player_score > dealer_score:
                        console.print(f"\n[green]Hai vinto {pot} fiches![/green]")
                        banker.win_response('big_win')
                        state.update_chips(int(pot/2))
                    else:
                        console.print("\n[red]Il Banchiere vince![/red]")
                        banker.lose_response('big_loss')
                        state.update_chips(-int(pot/2))
                else:
                    console.print("\n[red]Ti sei ritirato![/red]")
                    banker.lose_response()
                    state.update_chips(-int(pot/2))
            else:
                console.print("\n[red]Ti sei ritirato![/red]")
                banker.lose_response()
                state.update_chips(-int(pot/2))
        else:
            console.print("\n[red]Ti sei ritirato![/red]")
            banker.lose_response()
            state.update_chips(-int(pot/2))

        if not Prompt.ask("\nVuoi giocare ancora?", choices=["s", "n"]) == "s":
            break

    state.save_game()