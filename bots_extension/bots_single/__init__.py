from otree.api import *
from bots_utils.common_functions import setting_groups_single, setting_bot_decisions_single
import time

doc = """
Code for the Single Group public goods game for the BOTS extension
"""


class C(BaseConstants):
    NAME_IN_URL = 'bots_single'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 20
    ENDOWMENT = cu(20)
    MULTIPLIER = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Store ID of human partner
    human_partner = models.IntegerField()

    # For their group, store total investment and their individual share from the account
    group_total_investment = models.CurrencyField()
    group_individual_share = models.CurrencyField()

    personal_account = models.CurrencyField()

    # Investment Decision

    investment = models.CurrencyField(
        min=0, max=C.ENDOWMENT, label="How much will you invest to your Group's Joint Account?"
    )

    # Bot Investment Decisions
    bot_one_investment = models.CurrencyField()
    bot_two_investment = models.CurrencyField()

    # Track decision time
    start_time = models.FloatField(initial=0)
    time_spent_invest = models.FloatField(initial=0)
    time_spent_results = models.FloatField(initial=0)
    time_spent_cumulative_results = models.FloatField(initial=0)


# Functions

def set_payoffs_single_group(subsession: Subsession):
    """

    :param subsession:
    :return:
    """
    players = subsession.get_players()
    setting_groups_single(players)
    setting_bot_decisions_single(players)
    for p in players:
        p.group_total_investment = p.investment + \
                                   players[(p.human_partner - 1)].investment + \
                                   p.bot_one_investment + \
                                   p.bot_two_investment
        p.group_individual_share = (p.group_total_investment * C.MULTIPLIER) / 4
        p.personal_account = C.ENDOWMENT - p.investment
        p.payoff = p.personal_account + p.group_individual_share


# PAGES
class Invest(Page):
    form_model = 'player'
    form_fields = ['investment']

    @staticmethod
    def is_displayed(player: Player):
        player.start_time = time.time()
        return True

    @staticmethod
    def vars_for_template(player: Player):
        # Get the player's history up to the current round
        previous_rounds = player.in_previous_rounds()

        # extract investment and payoff for each round
        history = [
            {
                'round_number': p.round_number,
                'investment': p.investment,
                'tot_invest': p.group_total_investment,
                'individual_share': p.group_individual_share,
                'personal_account': p.personal_account,
                'payoff': p.payoff
            }
            for p in previous_rounds
        ]

        return {'history': history}

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.time_spent_invest = time.time() - player.start_time  # Save invest decision time spent


class ResultsWaitPage(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = set_payoffs_single_group


class Results(Page):

    @staticmethod
    def is_displayed(player: Player):
        player.start_time = time.time()
        return True

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.time_spent_results = time.time() - player.start_time  # Save results time spent


class CumulativeResults(Page):

    @staticmethod
    def is_displayed(player: Player):
        player.start_time = time.time()
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        cumulative_payoff = sum([p.payoff for p in player.in_all_rounds() if p.payoff])

        return {'cumulative_payoff': cumulative_payoff}

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.time_spent_cumulative_results = time.time() - player.start_time  # Save cumulative results time spent


page_sequence = [Invest,
                 ResultsWaitPage,
                 Results,
                 CumulativeResults]
