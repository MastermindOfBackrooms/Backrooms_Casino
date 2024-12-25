from rich.console import Console
import random
import time

console = Console()

class Banker:
    def __init__(self):
        self.greetings = [
            "Benvenuto nel mio eterno stabilimento...",
            "Ah, un nuovo giocatore... Che... fortuna.",
            "La casa vince sempre, ma prego... tenta la sorte.",
            "Il tempo qui non ha significato... solo le fiches contano.",
            "Finalmente... carne fresca.",
            "777... un numero così perfetto, non trovi?",
            "Le tue fiches brillano... come anime intrappolate.",
            "Ogni gioco è un passo verso... l'eternità."
        ]

        self.loan_responses = {  # Nuove risposte per il sistema di prestito
            'offer': [
                "Un prestito... interessante proposta.",
                "Le mie condizioni sono... ragionevoli.",
                "Il prezzo è alto... ma ne vale la pena?",
                "La disperazione ha un... sapore delizioso.",
                "Un prestito può essere... un cappio al collo."
            ],
            'accepted': [
                "Eccellente... ora mi appartieni un po' di più.",
                "Le fiches sono tue... per ora.",
                "Il contratto è sigillato... con la tua essenza.",
                "Saggio... o folle? Lo scopriremo presto.",
                "Il tempo del debito... è iniziato."
            ],
            'rejected': [
                "Forse più saggio... di quanto pensassi.",
                "La prudenza ti salva... per ora.",
                "Un'occasione sprecata... o forse no?",
                "La paura ti rende... cauto.",
                "Tornerai... quando la disperazione crescerà."
            ],
            'repaid': [
                "Il debito è saldato... ma il marchio rimane.",
                "Libero dal prestito... non da me.",
                "Hai mantenuto la parola... impressionante.",
                "Il contratto è concluso... per ora.",
                "La libertà ha un sapore... dolce, vero?"
            ]
        }

        self.membership_responses = {  # Nuove risposte per la tessera del casinò
            'offer': [
                "Hai dimostrato il tuo valore... vuoi unirti a noi?",
                "La tessera del Level 777... ti chiama.",
                "Potresti diventare... parte di qualcosa di più grande.",
                "Il casinò ti vuole... come membro permanente.",
                "La scelta è tua... ma scegli saggiamente."
            ],
            'accepted': [
                "Benvenuto... nella famiglia.",
                "Il Level 777 ha un nuovo... guardiano.",
                "La tua anima ora appartiene... al casinò.",
                "Uno di noi... per l'eternità.",
                "Il cerchio si chiude... inizia il tuo regno."
            ],
            'rejected': [
                "La libertà... ha un prezzo alto.",
                "Rifiuti il potere... interessante.",
                "Forse più saggio... di quanto credessi.",
                "La tua scelta... ti condanna alla libertà.",
                "Il casinò ricorderà... questo momento."
            ]
        }

        self.secret_ending_responses = {  # Nuove risposte per i finali segreti
            'first_secret': [
                "777777... il numero della perfezione assoluta.",
                "Hai scoperto... ciò che era nascosto.",
                "Il Level 777 trema... al tuo potere.",
                "L'impossibile... diventa realtà.",
                "Il velo si squarcia... rivelandoti la verità."
            ],
            'second_secret': [
                "666666... il numero del caos primordiale.",
                "Hai visto... ciò che non dovevi vedere.",
                "Le ombre sussurrano... il tuo nome.",
                "Il Level 777 si piega... alla tua volontà oscura.",
                "Il confine tra realtà e incubo... svanisce."
            ]
        }

        self.game_specific_taunts = {
            'craps': [
                "I dadi raccontano storie... di destini spezzati.",
                "Sette... un numero potente in questo regno.",
                "I dadi danzano... come spiriti inquieti.",
                "Ogni lancio è un sussurro... del fato.",
                "Il Seventh Sign attende... il prescelto.",
                "La profezia del sette... si sta avverando?",
                "I numeri mistici... risuonano nell'aria.",
                "Le ombre danzano... al ritmo dei dadi.",
                "Il destino si svela... ad ogni lancio.",
                "Sento il potere del 7... crescere."
            ],
            'sic_bo': [
                "Tre dadi... tre destini intrecciati.",
                "Il caos dei dadi... riflette la tua anima.",
                "I numeri si combinano... come una danza macabra.",
                "Antichi segreti... nei simboli dei dadi.",
                "La sequenza mistica... chiama il tuo nome.",
                "Il settimo sigillo... attende di essere spezzato.",
                "Tre è il numero del caos... sette della perfezione.",
                "I dadi sussurrano... antiche verità.",
                "Le combinazioni... nascondono segreti.",
                "Il Level 777... benedice i coraggiosi."
            ],
            'poker': [
                "I tuoi tell sono... affascinanti.",
                "Le tue fiches tremano... come la tua anima.",
                "Bluffare con me è... pericoloso.",
                "Vedo la paura nei tuoi occhi... deliziosa.",
                "Le tue carte nascondono... segreti oscuri."
            ],
            'blackjack': [
                "Il 21 è un numero interessante... come la vita e la morte.",
                "Le carte non mentono mai... ma io sì.",
                "Ogni carta è un passo verso... il tuo destino.",
                "Vuoi un'altra carta? O hai... paura?",
                "Il mazzo sussurra... ascolta attentamente."
            ],
            'roulette': [
                "La ruota gira eternamente... come il tuo destino.",
                "Rosso o nero... vita o morte... scegli.",
                "I numeri sussurrano... li senti?",
                "La pallina danza... come un'anima perduta.",
                "Ogni giro è un nuovo... tormento."
            ],
            'baccarat': [
                "Punto o Banco... due facce dello stesso destino.",
                "Le carte scorrono... come il tempo in questo luogo.",
                "Un gioco elegante... per anime raffinate.",
                "La semplicità nasconde... profonda oscurità."
            ]
        }

        self.win_responses = {
            'seven_related': [
                "Il potere del 7 scorre... attraverso di te.",
                "Tre 7... un segno del destino.",
                "Il numero sacro ti ha benedetto... oggi.",
                "777... la chiave di questo regno.",
                "I sette sigilli si incrinano... interessante.",
                "Le stelle si allineano... nel segno del 7.",
                "Il Level 777 riconosce... il tuo potere.",
                "Questa vittoria ha un sapore... particolare.",
                "Il numero perfetto ti sorride...",
                "Sento i numeri cantare... per te."
            ],
            'devils_defeated': [
                "I demoni si inchinano... davanti a te.",
                "Sette prove superate... impossibile.",
                "Le ombre si ritirano... per ora.",
                "Mai visto nulla di simile... in 777 anni.",
                "Il Level 777 ha un nuovo... campione.",
                "La tua anima brucia... di potere oscuro.",
                "I demoni ricorderanno... questo giorno.",
                "Le carte tremano... al tuo tocco.",
                "Questa vittoria echeggerà... nell'eternità.",
                "Forse... sei più di un semplice giocatore."
            ],
            'normal': [
                "Che... inaspettato. Congratulazioni.",
                "Goditi la vittoria. Finché dura.",
                "Forse sei più interessante di quanto pensassi...",
                "Una vittoria... ma a quale prezzo?",
                "Il Level 777 ti sorride... per ora."
            ],
            'big_win': [
                "Impressionante... molto impressionante.",
                "Le tue abilità sono... notevoli.",
                "Questa vittoria ti è costata... più di quanto pensi.",
                "Il 777 risuona con la tua fortuna...",
                "Una vittoria degna... del mio regno."
            ],
            'streak': [
                "La fortuna ti sorride... per ora.",
                "Il pendolo oscilla... presto cambierà direzione.",
                "La tua fortuna sta attirando... attenzione indesiderata.",
                "Vedo il 777 nei tuoi occhi...",
                "Le tue vittorie alimentano... qualcosa di più grande."
            ],
            'mystic_sequence': [
                "La sequenza si completa... perfetta.",
                "I numeri danzano... in armonia.",
                "Il ritmo del caos... si rivela.",
                "La danza dei dadi... è completa.",
                "Una combinazione... predestinata."
            ],
            'seventh_seal': [
                "Il sigillo si spezza... finalmente.",
                "Il potere del 7... scorre attraverso te.",
                "I segreti del Level 777... si svelano.",
                "Le barriere... cadono.",
                "L'impossibile... diventa realtà."
            ]
        }

        self.lose_responses = {
            'devils_defeat': [
                "I demoni reclamano... il loro premio.",
                "Sette prove... sette fallimenti.",
                "Le ombre ti consumano... delizioso.",
                "Un'altra anima per la collezione...",
                "I Seven Devils rimangono... imbattuti.",
                "Il buio ti avvolge... per sempre.",
                "La tua audacia... ti è costata cara.",
                "I demoni si nutrono... della tua sconfitta.",
                "Nessuno sfugge... ai Seven Devils.",
                "Il Level 777 reclama... la sua preda."
            ],
            'normal': [
                "Come previsto. La casa vince sempre.",
                "La tua fortuna è finita. Come sempre qui.",
                "Un'altra anima reclamata dal casinò...",
                "Le tue fiches mi appartengono... come la tua anima.",
                "Il Level 777 reclama... il suo tributo."
            ],
            'big_loss': [
                "Le tue fiches... ora sono mie.",
                "La disperazione... ti dona.",
                "Sento l'odore della tua paura...",
                "Il prezzo della sfida... è alto.",
                "La tua sconfitta alimenta... questo luogo."
            ],
            'bankruptcy': [
                "Game over... letteralmente.",
                "La tua anima ora mi appartiene...",
                "Un'altra collezione alla mia... raccolta.",
                "777 anime... e la tua fa 778.",
                "Il Level 777 ha... un nuovo residente."
            ]
        }

        self.challenge_taunts = {
            'start': [
                "Osi sfidarmi... nel mio dominio?",
                "777 anime hanno tentato... tutte hanno fallito.",
                "La posta in gioco è... la tua essenza.",
                "Questa sfida sarà... memorabile.",
                "Il Level 777 osserva... con interesse."
            ],
            'during': [
                "Senti il peso... della tua scelta?",
                "Le carte danzano... tra vita e morte.",
                "Ogni mossa potrebbe essere... l'ultima.",
                "Il tempo si contorce... in questo momento.",
                "777 battiti... nel silenzio della sfida."
            ],
            'victory': [
                "Impossibile... dopo 777 vittorie...",
                "Il Level 777 ha un nuovo... campione.",
                "La tua vittoria risuonerà... eternamente.",
                "Hai vinto... ma sei ancora qui.",
                "Forse... non sei un semplice giocatore."
            ],
            'defeat': [
                "Come tutti gli altri... prima di te.",
                "La tua anima arricchirà... la mia collezione.",
                "777 vittorie... e counting.",
                "Il Level 777 reclamava... il tuo destino.",
                "Un'altra storia... per la mia eternità."
            ]
        }

        self.special_message = {
            "777": [
                "Il numero sacro... si manifesta.",
                "777... il codice dell'eternità.",
                "Senti il potere... del Level 777?",
                "Le barriere tra i mondi... si assottigliano.",
                "Il casinò risuona... con questo numero.",
                "Gli ingranaggi del destino... si allineano.",
                "Le ombre danzano... al ritmo del 7.",
                "Il tempo si piega... intorno a questo numero.",
                "I segreti del Level 777... si svelano.",
                "L'aria vibra... con energia antica."
            ]
        }

    def welcome_message(self):
        message = random.choice(self.greetings)
        console.print(f"\n[red]Il Banchiere:[/red] [italic]{message}[/italic]")
        time.sleep(2)

    def game_taunt(self, game_type):
        messages = self.game_specific_taunts.get(game_type, self.game_specific_taunts['poker'])
        message = random.choice(messages)
        console.print(f"\n[red]Il Banchiere:[/red] [italic]{message}[/italic]")
        time.sleep(1)

    def win_response(self, type='normal'):
        responses = self.win_responses.get(type, self.win_responses['normal'])
        message = random.choice(responses)
        console.print(f"\n[red]Il Banchiere:[/red] [italic]{message}[/italic]")
        time.sleep(1)

    def lose_response(self, type='normal'):
        responses = self.lose_responses.get(type, self.lose_responses['normal'])
        message = random.choice(responses)
        console.print(f"\n[red]Il Banchiere:[/red] [italic]{message}[/italic]")
        time.sleep(1)

    def challenge_taunt(self, phase='start'):
        taunts = self.challenge_taunts.get(phase, self.challenge_taunts['start'])
        message = random.choice(taunts)
        console.print(f"\n[red]Il Banchiere:[/red] [italic]{message}[/italic]")
        time.sleep(1.5)

    def special_message(self, trigger):
        messages = self.special_message.get(trigger, [])
        if messages:
            message = random.choice(messages)
            console.print(f"\n[red]Il Banchiere:[/red] [italic]{message}[/italic]")
            time.sleep(1)

    def loan_response(self, type='offer'):
        responses = self.loan_responses.get(type, self.loan_responses['offer'])
        message = random.choice(responses)
        console.print(f"\n[red]Il Banchiere:[/red] [italic]{message}[/italic]")
        time.sleep(1.5)

    def membership_response(self, type='offer'):
        responses = self.membership_responses.get(type, self.membership_responses['offer'])
        message = random.choice(responses)
        console.print(f"\n[red]Il Banchiere:[/red] [italic]{message}[/italic]")
        time.sleep(1.5)

    def secret_ending_response(self, type='first_secret'):
        responses = self.secret_ending_responses.get(type, self.secret_ending_responses['first_secret'])
        message = random.choice(responses)
        console.print(f"\n[red]Il Banchiere:[/red] [italic]{message}[/italic]")
        time.sleep(2)