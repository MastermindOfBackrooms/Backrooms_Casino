from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress
from rich.table import Table
import random
import time
from games.poker import create_deck, display_hand, dramatic_card_deal

console = Console()

def compare_hands(hand1_score, hand2_score):
    """Confronta due mani di poker restituendo True se la prima è migliore"""
    rank1, values1 = hand1_score
    rank2, values2 = hand2_score
    if rank1 != rank2:
        return rank1 > rank2
    for v1, v2 in zip(values1, values2):
        if v1 != v2:
            return v1 > v2
    return False

def evaluate_hand(cards):
    """
    Valuta una mano di poker con supporto specifico per il Level 777
    """
    if len(cards) < 5:
        return (-1, [])

    # Prendi le migliori 5 carte
    best_score = (-1, [])
    for hand in [cards[:5]]:  # In futuro potremmo aggiungere più combinazioni
        # Converti i valori delle carte
        values = []
        suits = []
        for card in hand:
            rank = card[0]
            if rank == 'A':
                values.append(14)
            elif rank == 'K':
                values.append(13)
            elif rank == 'Q':
                values.append(12)
            elif rank == 'J':
                values.append(11)
            else:
                values.append(int(rank))
            suits.append(card[1])

        values.sort(reverse=True)

        # Controlla combinazioni
        is_flush = len(set(suits)) == 1
        is_straight = all(values[i] - values[i+1] == 1 for i in range(len(values)-1))

        # Conta le occorrenze
        value_counts = {}
        for value in values:
            value_counts[value] = value_counts.get(value, 0) + 1
        counts = sorted(value_counts.values(), reverse=True)

        # Determina il rank della mano
        current_score = None
        if is_straight and is_flush:
            current_score = (9, values)
        elif 4 in counts:
            current_score = (8, values)
        elif counts == [3, 2]:
            current_score = (7, values)
        elif is_flush:
            current_score = (6, values)
        elif is_straight:
            current_score = (5, values)
        elif 3 in counts:
            current_score = (4, values)
        elif counts[:2] == [2, 2]:
            current_score = (3, values)
        elif 2 in counts:
            current_score = (2, values)
        else:
            current_score = (1, values)

        if compare_hands(current_score, best_score):
            best_score = current_score

    return best_score

def check_seven_bonus(cards):
    """Controlla e calcola i bonus speciali per le combinazioni con il 7"""
    sevens = sum(1 for card in cards if card[0] == '7')
    if sevens >= 3:
        return 77
    elif sevens == 2:
        return 7
    return 1

def play_seven_card_stud(state, banker):
    """
    Variante 777: Seven Card Stud con regole speciali del Level 777
    - 7 carte per giocatore
    - Bonus speciali per combinazioni con 7
    - Pot moltiplicato per 7 in caso di mani speciali
    """
    banker.game_taunt('poker_777')

    while True:
        console.print("\n[red]♠ SEVEN CARD STUD - LEVEL 777 EDITION ♠[/red]")
        console.print(f"[yellow]Le tue fiches: {state.chips}[/yellow]")

        # Puntata iniziale
        bet = Prompt.ask("Inserisci la tua puntata iniziale", default="77")
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

        player_hand = []
        dealer_hand = []
        player_visible = []
        dealer_visible = []

        # Distribuzione iniziale (3 carte coperte)
        console.print("\n[cyan]Distribuzione delle carte iniziali...[/cyan]")
        for _ in range(3):
            card = deck.pop()
            dramatic_card_deal(card)
            player_hand.append(card)

            card = deck.pop()
            dramatic_card_deal(card, is_dealer=True)
            dealer_hand.append(card)
            dealer_visible.append(card)

        # Quattro turni di carte scoperte
        for round in range(4):
            console.print(f"\n[purple]Round {round + 1}[/purple]")
            console.print("[cyan]Le tue carte:[/cyan]", display_hand(player_hand))
            console.print("[red]Carte visibili del Banchiere:[/red]", display_hand(dealer_visible))

            # Controllo per combinazioni con 7
            sevens_count = sum(1 for card in player_hand if card[0] == '7')
            if sevens_count >= 2:
                console.print("[yellow]Il potere del 7 cresce...[/yellow]")
                banker.special_message("777")

            current_bet = bet * (round + 1)
            action = Prompt.ask("Vuoi continuare?", choices=["s", "n"])

            if action == "n":
                console.print("[red]Ti sei ritirato![/red]")
                banker.lose_response()
                state.update_chips(-bet * round)
                break

            state.chips -= current_bet

            # Nuova carta
            card = deck.pop()
            dramatic_card_deal(card)
            player_hand.append(card)
            player_visible.append(card)

            card = deck.pop()
            dramatic_card_deal(card, is_dealer=True)
            dealer_hand.append(card)
            dealer_visible.append(card)

            # Bonus speciale per 777
            if len([c for c in player_visible if c[0] == '7']) == 3:
                console.print("[green]✨ TRIPLO 7 - BONUS SPECIALE! ✨[/green]")
                bonus = bet * 77
                state.chips += bonus
                banker.win_response('seven_related')

        # Showdown
        if len(player_hand) == 7:
            console.print("\n[yellow]♠ SHOWDOWN ♠[/yellow]")
            console.print("[cyan]La tua mano finale:[/cyan]", display_hand(player_hand))
            console.print("[red]Mano del Banchiere:[/red]", display_hand(dealer_hand))

            # Valutazione delle mani con bonus del 7
            player_score = evaluate_hand(player_hand)
            dealer_score = evaluate_hand(dealer_hand)

            # Applica bonus per 7
            player_multiplier = check_seven_bonus(player_hand)
            if player_multiplier > 1:
                player_score = (player_score[0] + 1, player_score[1])

            if compare_hands(player_score, dealer_score):
                winnings = bet * player_multiplier
                console.print(f"[green]Hai vinto {winnings} fiches![/green]")
                banker.win_response('big_win')
                state.update_chips(winnings)
            else:
                console.print("[red]Il Banchiere vince![/red]")
                banker.lose_response('big_loss')
                state.update_chips(-bet)

        if not Prompt.ask("\nVuoi giocare ancora?", choices=["s", "n"]) == "s":
            break

def play_seven_devils(state, banker):
    """
    Variante esclusiva del Level 777: Seven Devils Poker
    - 7 giocatori virtuali controllati dal Banchiere
    - Ogni 7 ottenuto moltiplica le vincite
    - Bonus speciali per sconfiggere tutti i "diavoli"
    """
    banker.game_taunt('poker_777')
    console.print("\n[red]♠ SEVEN DEVILS POKER - LA SFIDA SUPREMA ♠[/red]")
    console.print("[yellow]Sfida 7 emanazioni del Banchiere in una partita all'ultimo sangue![/yellow]")

    while True:
        console.print(f"\n[yellow]Le tue fiches: {state.chips}[/yellow]")

        # Puntata iniziale
        bet = Prompt.ask("Inserisci la tua puntata per sfidare i Seven Devils", default="777")
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

        player_hand = []
        devil_hands = [[] for _ in range(7)]

        # Distribuzione iniziale
        console.print("\n[cyan]Il Banchiere distribuisce le carte del destino...[/cyan]")
        time.sleep(1)

        # Due carte coperte per tutti
        for _ in range(2):
            card = deck.pop()
            dramatic_card_deal(card)
            player_hand.append(card)

            for i in range(7):
                card = deck.pop()
                dramatic_card_deal(card, is_dealer=True)
                devil_hands[i].append(card)

        # Cinque carte comuni
        community_cards = []
        devil_names = [
            "Il Primo Diavolo del 7",
            "Il Secondo Demone",
            "La Terza Ombra",
            "Il Quarto Spettro",
            "Il Quinto Tormento",
            "La Sesta Perdizione",
            "Il Settimo Sigillo"
        ]

        devils_defeated = 0

        # Fasi di gioco
        for phase in range(3):
            if phase == 0:
                # Flop
                console.print("\n[red]✧ IL FLOP DEI DANNATI ✧[/red]")
                for _ in range(3):
                    card = deck.pop()
                    dramatic_card_deal(card, is_dealer=True)
                    community_cards.append(card)
            elif phase == 1:
                # Turn
                console.print("\n[red]✧ IL TURN DEL TORMENTO ✧[/red]")
                card = deck.pop()
                dramatic_card_deal(card, is_dealer=True)
                community_cards.append(card)
            else:
                # River
                console.print("\n[red]✧ IL RIVER DELLA DANNAZIONE ✧[/red]")
                card = deck.pop()
                dramatic_card_deal(card, is_dealer=True)
                community_cards.append(card)

            console.print("\n[purple]Carte sul tavolo:[/purple]", display_hand(community_cards))
            console.print("[cyan]La tua mano:[/cyan]", display_hand(player_hand))

            current_bet = bet * (phase + 1)
            if not Prompt.ask("\nVuoi continuare la sfida?", choices=["s", "n"]) == "s":
                console.print("[red]Ti ritiri dalla sfida dei Seven Devils![/red]")
                banker.lose_response('big_loss')
                state.update_chips(-bet * phase)
                break

            state.chips -= current_bet

            # Sfida contro ogni diavolo ancora in gioco
            for i in range(7):
                if len(devil_hands[i]) > 0:  # Diavolo ancora in gioco
                    console.print(f"\n[red]Sfida contro {devil_names[i]}[/red]")

                    # Valuta le mani con le carte comuni
                    all_player_cards = player_hand + community_cards
                    all_devil_cards = devil_hands[i] + community_cards

                    player_score = evaluate_hand(all_player_cards)
                    devil_score = evaluate_hand(all_devil_cards)

                    # Applica bonus per 7
                    player_multiplier = check_seven_bonus(all_player_cards)
                    if player_multiplier > 1:
                        player_score = (player_score[0] + 1, player_score[1])

                    if compare_hands(player_score, devil_score):
                        console.print(f"[green]Hai sconfitto {devil_names[i]}![/green]")
                        devils_defeated += 1
                        devil_hands[i] = []  # Rimuovi il diavolo sconfitto

                        # Bonus per 7
                        if player_multiplier > 1:
                            bonus = current_bet * player_multiplier
                            console.print(f"[yellow]Bonus del 7: +{bonus} fiches![/yellow]")
                            state.chips += bonus
                            banker.special_message("777")
                    else:
                        console.print(f"[red]{devil_names[i]} ti ha sconfitto![/red]")
                        banker.lose_response('normal')

            if devils_defeated == 7:
                console.print("\n[green]✨ HAI SCONFITTO TUTTI I SEVEN DEVILS! ✨[/green]")
                final_bonus = bet * 777
                state.chips += final_bonus
                banker.win_response('seven_related')
                break

        if devils_defeated < 7:
            console.print("\n[red]Non sei riuscito a sconfiggere tutti i Seven Devils![/red]")
            banker.lose_response('big_loss')

        if not Prompt.ask("\nVuoi sfidare ancora i Seven Devils?", choices=["s", "n"]) == "s":
            break

    state.save_game()