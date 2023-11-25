from otree.api import *
from bots_utils.common_functions import setting_groups, setting_bot_decisions
import time


doc = """
Ceteris paribus the code for bots extension split, but with Green | Blue instead of Blue | Green
"""


class C(BaseConstants):
    NAME_IN_URL = 'bots_split_flipped'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 20
    ENDOWMENT = cu(10)
    MULTIPLIER = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    #  Store ID of human partner
    blue_group_human_partner = models.IntegerField()

    green_group_human_partner = models.IntegerField()
    #  For Each group, store total_investment and their individual share from this account
    blue_group_total_investment = models.CurrencyField()
    blue_group_individual_share = models.CurrencyField()

    green_group_total_investment = models.CurrencyField()
    green_group_individual_share = models.CurrencyField()
    #  For a period, a participants payoff is the sum of their earnings from their BLUE and GREEN groups
    blue_group_payoff = models.CurrencyField()
    green_group_payoff = models.CurrencyField()

    personal_account = models.CurrencyField()

    #  Each round, each subject makes a decision to each group of how much of their endowment to contribute
    blue_group_investment = models.CurrencyField(
        min=0, max=C.ENDOWMENT
    )
    green_group_investment = models.CurrencyField(
        min=0, max=C.ENDOWMENT
    )

    #  Bot investment decisions
    blue_bot_one_investment = models.CurrencyField()
    blue_bot_two_investment = models.CurrencyField()

    green_bot_one_investment = models.CurrencyField()
    green_bot_two_investment = models.CurrencyField()

    # Track decision time
    start_time = models.FloatField(initial=0)
    time_spent_invest = models.FloatField(initial=0)
    time_spent_results = models.FloatField(initial=0)
    time_spent_cumulative_results = models.FloatField(initial=0)


def set_payoffs_split_endowment(subsession: Subsession):
    """

    :param subsession:
    :return:
    """
    players = subsession.get_players()
    setting_groups(players)
    setting_bot_decisions(players, 0)
    for p in players:
        # Calculate Blue Group information
        p.blue_group_total_investment = p.blue_group_investment + \
                                        players[(p.blue_group_human_partner - 1)].blue_group_investment + \
                                        p.blue_bot_one_investment + \
                                        p.blue_bot_two_investment
        p.blue_group_individual_share = (p.blue_group_total_investment * C.MULTIPLIER) / 4
        p.blue_group_payoff = C.ENDOWMENT - p.blue_group_investment + p.blue_group_individual_share
        # Calculate Green Group Information
        p.green_group_total_investment = p.green_group_investment + \
                                         players[(p.green_group_human_partner - 1)].green_group_investment + \
                                         p.green_bot_one_investment + \
                                         p.green_bot_two_investment
        p.green_group_individual_share = (p.green_group_total_investment * C.MULTIPLIER) / 4
        p.green_group_payoff = C.ENDOWMENT - p.green_group_investment + p.green_group_individual_share
        # For Split Endowment I need 2 of the C.ENDOWMENTS for the TOTAL Personal Account
        p.personal_account = C.ENDOWMENT + C.ENDOWMENT - p.green_group_investment - p.blue_group_investment
        p.payoff = p.blue_group_payoff + p.green_group_payoff


# PAGES
class Invest(Page):
    form_model = 'player'
    form_fields = ['blue_group_investment', 'green_group_investment']

    @staticmethod
    def is_displayed(player: Player):
        player.start_time = time.time()
        return True

    @staticmethod
    def vars_for_template(player: Player):
        # Get the player's history up to the current round
        previous_rounds = player.in_previous_rounds()

        # Extract investment and payoff for each round
        history = [
            {
                'round_number': p.round_number,
                'blue_group_investment': p.blue_group_investment,
                'green_group_investment': p.green_group_investment,
                'blue_group_total_investment': p.blue_group_total_investment,
                'green_group_total_investment': p.green_group_total_investment,
                'blue_group_individual_share': p.blue_group_individual_share,
                'green_group_individual_share': p.green_group_individual_share,
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
    after_all_players_arrive = set_payoffs_split_endowment


class Results(Page):

    @staticmethod
    def is_displayed(player: Player):
        player.start_time = time.time()
        return True

    @staticmethod
    def vars_for_template(player: Player):
        blue_personal_account = C.ENDOWMENT - player.blue_group_investment
        green_personal_account = C.ENDOWMENT - player.green_group_investment
        personal_account = blue_personal_account + green_personal_account
        personal_account_dictionary = {
            'blue_personal_account': blue_personal_account,
            'green_personal_account': green_personal_account
        }
        return {'personal_account_dictionary': personal_account_dictionary}

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