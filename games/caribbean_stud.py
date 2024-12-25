from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress
import random
import time
import sys

console = Console()

def create_deck():
    suits = ['♥️', '♦️', '♣️', '♠️']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    return [(rank, suit) for suit in suits for rank in ranks]

def hand_rank(hand):
    ranks = [card[0] for card in hand]
    suits = [card[1] for card in hand]

    rank_values = []
    for rank in ranks:
        if rank == 'A':
            rank_values.append(14)
        elif rank == 'K':
            rank_values.append(13)
        elif rank == 'Q':
            rank_values.append(12)
        elif rank == 'J':
            rank_values.append(11)
        else:
            rank_values.append(int(rank))

    rank_values.sort(reverse=True)

    is_flush = len(set(suits)) == 1
    is_straight = (max(rank_values) - min(rank_values) == 4) and len(set(rank_values)) == 5

    rank_counts = {}
    for rank in rank_values:
        rank_counts[rank] = rank_counts.get(rank, 0) + 1

    if is_straight and is_flush:
        return 8, rank_values  # Scala reale
    elif 4 in rank_counts.values():
        return 7, rank_values  # Poker
    elif set(rank_counts.values()) == {2, 3}:
        return 6, rank_values  # Full
    elif is_flush:
        return 5, rank_values  # Colore
    elif is_straight:
        return 4, rank_values  # Scala
    elif 3 in rank_counts.values():
        return 3, rank_values  # Tris
    elif list(rank_counts.values()).count(2) == 2:
        return 2, rank_values  # Doppia coppia
    elif 2 in rank_counts.values():
        return 1, rank_values  # Coppia
    else:
        return 0, rank_values  # Carta alta

def display_hand(hand, reveal=True):
    if not reveal:
        return "[red]?? ?[/red] " * len(hand)
    return " ".join(f"[white]{rank}{suit}[/white]" for rank, suit in hand)

def dramatic_card_reveal(card, delay=0.5):
    console.print("\n[cyan]Il destino rivela una carta...[/cyan]")
    with Progress() as progress:
        task = progress.add_task("[cyan]", total=100)
        while not progress.finished:
            progress.update(task, advance=2)
            time.sleep(0.01)
    rank, suit = card
    console.print(f"[white]{rank}{suit}[/white]")
    time.sleep(delay)

def challenge_banker(state, banker):
    console.print("\n[red]=============== SFIDA AL BANCHIERE - LEVEL 777 ===============[/red]")
    console.print("\n[yellow]Gli occhi del Banchiere brillano di una luce sovrannaturale mentre mischia le carte...[/yellow]")

    banker.challenge_taunt('start')

    total_rounds = 10
    rounds_won = 0
    current_round = 1
    total_bet = 0

    base_bet = 777  # Puntata base per round
    console.print(f"\n[red]Il Banchiere:[/red] La puntata base è di {base_bet} fiches per round...")

    while current_round <= total_rounds and state.chips >= base_bet:
        console.print(f"\n[red]╔════ Round {current_round} di {total_rounds} ════╗[/red]")
        console.print(f"[yellow]Round vinti: {rounds_won}[/yellow]")
        console.print(f"[yellow]Fiches rimanenti: {state.chips}[/yellow]")

        banker.challenge_taunt('during')

        current_bet = base_bet * (current_round // 3 + 1)  # La puntata aumenta ogni 3 round
        console.print(f"\n[red]Puntata per questo round: {current_bet} fiches[/red]")

        if current_bet > state.chips:
            console.print("[red]Non hai abbastanza fiches per continuare la sfida![/red]")
            banker.lose_response('bankruptcy')
            break

        if not Prompt.ask("\n[yellow]Vuoi affrontare questo round?[/yellow]", choices=["s", "n"]) == "s":
            console.print("\n[red]Ti ritiri dalla sfida...[/red]")
            banker.lose_response('devils_defeat')
            break

        state.chips -= current_bet
        total_bet += current_bet

        deck = create_deck()
        random.shuffle(deck)

        # Distribuzione carte con drammaticità
        console.print("\n[cyan]Il Banchiere distribuisce le carte con movimenti ipnotici...[/cyan]")
        time.sleep(1.5)

        player_hand = []
        banker_hand = []

        # Distribuisci le carte alternando
        for _ in range(5):
            card = deck.pop()
            dramatic_card_reveal(card, 0.3)
            player_hand.append(card)

            card = deck.pop()
            banker_hand.append(card)

        # Mostra le mani
        console.print("\n[cyan]La tua mano:[/cyan]")
        console.print(display_hand(player_hand))

        console.print("\n[red]La mano del Banchiere (prima carta):[/red]")
        console.print(display_hand([banker_hand[0]], reveal=True))
        console.print(display_hand(banker_hand[1:], reveal=False))

        # Decisione del giocatore
        if not Prompt.ask("\n[yellow]Vuoi continuare con questa mano?[/yellow]", choices=["s", "n"]) == "s":
            console.print("\n[red]Abbandoni la mano...[/red]")
            banker.lose_response('normal')
            current_round += 1
            continue

        # Rivela la mano del Banchiere
        console.print("\n[red]Il Banchiere rivela le sue carte...[/red]")
        for card in banker_hand[1:]:
            dramatic_card_reveal(card, 0.3)

        player_score = hand_rank(player_hand)
        banker_score = hand_rank(banker_hand)

        # Mostra i punteggi finali
        console.print("\n[cyan]La tua mano definitiva:[/cyan]", display_hand(player_hand))
        console.print("[red]La mano del Banchiere:[/red]", display_hand(banker_hand))

        if player_score > banker_score:
            # Bonus per mani speciali
            bonus_multiplier = 1
            if player_score[0] >= 5:  # Colore o meglio
                bonus_multiplier = player_score[0] - 3

            winnings = current_bet * bonus_multiplier
            console.print(f"\n[green]Hai vinto questo round! ({winnings} fiches)[/green]")
            if bonus_multiplier > 1:
                console.print(f"[yellow]Bonus x{bonus_multiplier} per la mano speciale![/yellow]")

            state.chips += winnings
            rounds_won += 1
            banker.win_response('challenge')

            # Evento speciale per 7
            sevens = sum(1 for card in player_hand if card[0] == '7')
            if sevens >= 2:
                bonus = current_bet * sevens
                console.print(f"\n[yellow]✨ BONUS DEL 7! +{bonus} fiches ✨[/yellow]")
                state.chips += bonus
                banker.special_message("777")
        else:
            console.print("\n[red]Il Banchiere vince questo round![/red]")
            banker.lose_response('challenge')

        current_round += 1

        if rounds_won >= 7:  # Vittoria anticipata con 7 round vinti
            console.print("\n[green]✨ HAI DOMINATO LA SFIDA! ✨[/green]")
            final_bonus = total_bet * 7
            state.chips += final_bonus
            console.print(f"[yellow]Bonus finale: {final_bonus} fiches![/yellow]")
            banker.challenge_taunt('victory')
            break

    # Risultato finale
    console.print("\n[red]════ RISULTATO FINALE ════[/red]")
    console.print(f"[yellow]Round vinti: {rounds_won} su {current_round - 1}[/yellow]")

    if rounds_won >= 6:  # Vittoria
        console.print("\n[green]Hai conquistato il rispetto del Banchiere![/green]")
        bonus = total_bet
        state.chips += bonus
        console.print(f"[yellow]Bonus di rispetto: {bonus} fiches[/yellow]")
        banker.challenge_taunt('victory')

        # Offerta della tessera onoraria
        console.print("\n[red]Il Banchiere si alza lentamente dal tavolo, i suoi occhi brillano di una luce sovrannaturale...[/red]")
        time.sleep(2)
        console.print("\n[red]'In 777 anni, solo pochi hanno dimostrato tale... abilità.'[/red]")
        time.sleep(2)
        console.print("\n[red]Il Banchiere estrae una tessera dorata che emana un'aura misteriosa.[/red]")
        time.sleep(2)
        console.print("\n[red]'Ti offro un posto tra i membri onorati del Level 777. Accetti?'[/red]")

        choice = Prompt.ask("\n[yellow]Accetti la tessera onoraria?[/yellow]", choices=["s", "n"])

        if choice == "s":
            # Finale 1: Accettazione della tessera
            state.special_endings['membership_accepted'] = True
            console.print("\n[yellow]Allunghi la mano verso la tessera dorata...[/yellow]")
            time.sleep(2)
            console.print("\n[red]Il Banchiere sorride mentre le tue dita toccano il metallo freddo.[/red]")
            time.sleep(2)
            console.print("\n[yellow]Una sensazione di potere ti attraversa, senti di appartenere a questo luogo...[/yellow]")
            time.sleep(2)
            console.print("\n[green]✨ SEI DIVENTATO UN MEMBRO ONORARIO DEL LEVEL 777 ✨[/green]")
            time.sleep(2)
            console.print("\n[red]'Benvenuto nell'eternità, nuovo... collega.'[/red]")
            state.chips *= 7  # Bonus speciale per l'accettazione
            banker.membership_response('accepted')
        else:
            # Finale 2: Rifiuto della tessera
            state.special_endings['membership_rejected'] = True
            console.print("\n[yellow]Fai un passo indietro, rifiutando l'offerta...[/yellow]")
            time.sleep(2)
            console.print("\n[red]'Interessante... la tua anima è più forte di quanto pensassi.'[/red]")
            time.sleep(2)
            console.print("\n[yellow]Una luce accecante riempie la stanza...[/yellow]")
            time.sleep(2)
            console.print("\n[green]✨ SEI RIUSCITO A SFUGGIRE AL RICHIAMO DEL LEVEL 777 ✨[/green]")
            time.sleep(2)
            console.print("\n[yellow]Ti ritrovi fuori dal casinò, ma le tue tasche sono piene di fiches trasformate in oro...[/yellow]")
            state.chips += 7777  # Bonus di libertà
            banker.membership_response('rejected')

    elif rounds_won >= 3:  # Pareggio
        console.print("\n[yellow]Una sfida memorabile... ma non abbastanza.[/yellow]")
        banker.challenge_taunt('during')
    else:  # Sconfitta
        console.print("\n[red]Il Banchiere ha prevalso![/red]")
        banker.challenge_taunt('defeat')

    state.save_game()
    time.sleep(2)


def get_rank_value(rank):
    if rank == 'A':
        return 14
    elif rank == 'K':
        return 13
    elif rank == 'Q':
        return 12
    elif rank == 'J':
        return 11
    else:
        return int(rank)


def final_challenge(state, banker):
    """
    La sfida finale contro il Banchiere: 30 mani di poker per la libertà
    """
    console.print("\n[red]╔═══════ LA SFIDA FINALE ═══════╗[/red]")
    console.print("\n[yellow]Il Banchiere si alza dal suo trono millenario...[/yellow]")
    time.sleep(2)
    console.print("\n[red]'In 777 anni, nessuno ha mai accumulato un tale potere...'[/red]")
    time.sleep(2)
    console.print("\n[yellow]L'aria si cristallizza, il tempo sembra fermarsi...[/yellow]")
    time.sleep(2)
    console.print("\n[red]'30 mani di poker. La tua libertà contro la mia eternità.'[/red]")

    if not Prompt.ask("\n[yellow]Accetti la sfida finale?[/yellow]", choices=["s", "n"]) == "s":
        console.print("\n[red]Il Banchiere sorride...[/red]")
        console.print("[red]'La paura è una scelta saggia...'[/red]")
        return

    player_wins = 0
    banker_wins = 0
    total_hands = 30
    current_hand = 0

    while current_hand < total_hands and player_wins < 16 and banker_wins < 16:
        current_hand += 1
        console.print(f"\n[red]╔════ Mano {current_hand} di {total_hands} ════╗[/red]")
        console.print(f"[yellow]Vittorie tue: {player_wins} - Vittorie del Banchiere: {banker_wins}[/yellow]")

        # Distribuzione carte
        deck = create_deck()
        random.shuffle(deck)

        player_hand = []
        banker_hand = []

        # 5 carte per ciascuno
        for _ in range(5):
            card = deck.pop()
            dramatic_card_reveal(card, 0.3)
            player_hand.append(card)

            card = deck.pop()
            banker_hand.append(card)

        # Mostra le mani
        console.print("\n[cyan]La tua mano:[/cyan]")
        console.print(display_hand(player_hand))

        # Possibilità di cambiare fino a 3 carte
        if Prompt.ask("\n[yellow]Vuoi cambiare delle carte?[/yellow]", choices=["s", "n"]) == "s":
            num_cards = int(Prompt.ask("Quante carte vuoi cambiare? (1-3)", choices=["1", "2", "3"]))
            for _ in range(num_cards):
                index = int(Prompt.ask("Quale carta vuoi cambiare? (1-5)")) - 1
                if 0 <= index < 5:
                    card = deck.pop()
                    dramatic_card_reveal(card, 0.3)
                    player_hand[index] = card

        console.print("\n[cyan]La tua mano finale:[/cyan]")
        console.print(display_hand(player_hand))

        # Il banchiere cambia le sue carte
        banker_score = hand_rank(banker_hand)
        if banker_score[0] < 2:  # Se ha meno di una coppia
            cards_to_change = random.randint(1, 3)
            for _ in range(cards_to_change):
                worst_card_index = banker_hand.index(min(banker_hand, key=lambda x: get_rank_value(x[0])))
                banker_hand[worst_card_index] = deck.pop()

        # Rivela la mano del banchiere
        console.print("\n[red]Il Banchiere rivela la sua mano...[/red]")
        time.sleep(1)
        console.print(display_hand(banker_hand))

        player_score = hand_rank(player_hand)
        banker_score = hand_rank(banker_hand)

        if player_score > banker_score:
            player_wins += 1
            console.print("\n[green]Hai vinto questa mano![/green]")
            if player_wins == 7:
                console.print("\n[yellow]Il Banchiere sussulta... il numero 7 risuona nel Level 777...[/yellow]")
            elif player_wins == 14:
                console.print("\n[yellow]Le ombre tremano... sei vicino alla libertà...[/yellow]")
        else:
            banker_wins += 1
            console.print("\n[red]Il Banchiere vince questa mano![/red]")

        time.sleep(1)

    # Risultato finale
    console.print("\n[red]═══════ VERDETTO FINALE ═══════[/red]")
    console.print(f"[yellow]Le tue vittorie: {player_wins}[/yellow]")
    console.print(f"[red]Vittorie del Banchiere: {banker_wins}[/red]")

    if player_wins >= 16:
        # Vittoria del giocatore
        console.print("\n[green]HAI SCONFITTO IL BANCHIERE![/green]")
        time.sleep(2)
        console.print("\n[red]Il Banchiere si alza lentamente...[/red]")
        time.sleep(2)
        console.print("\n[red]'777 anni... e finalmente qualcuno ha spezzato la maledizione.'[/red]")
        time.sleep(2)
        console.print("\n[yellow]Una luce accecante riempie la stanza...[/yellow]")
        time.sleep(2)
        console.print("\n[green]Le pareti del Level 777 iniziano a dissolversi...[/green]")
        time.sleep(2)
        console.print("\n[red]'Sei libero... e io sono finalmente in pace.'[/red]")
        time.sleep(2)
        console.print("\n[green]✨ HAI COMPLETATO IL LEVEL 777 ✨[/green]")
        state.special_endings['final_challenge_completed'] = True
        state.save_game()
        sys.exit()
    else:
        # Vittoria del banchiere
        console.print("\n[red]Il Banchiere ha prevalso![/red]")
        time.sleep(2)
        console.print("\n[red]'La tua anima si unirà alle altre... per l'eternità.'[/red]")
        time.sleep(2)
        console.print("\n[yellow]Le ombre del Level 777 ti avvolgono...[/yellow]")
        state.chips = 0
        state.save_game()
        sys.exit()