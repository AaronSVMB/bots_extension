from otree.api import *
import numpy as np

doc = """
Code that is used in all bot sessions and multi-group sessions.
"""


def make_comprehension_question(label):
    """
    Reduces code repetition for creation of comprehension questions
    :param label: the message to be displayed to participants for a given question
    :return: an input field that can be displayed on a page that participants can interact with
    """
    return models.IntegerField(label=label)


# =====================================================================================================================
# Torus, lattice, implementation with bots involved | Group Formation
# =====================================================================================================================


def find_blue_human_partner(player_index: int):
    """
    Assigns the groups for the blue group. Groups are now 2-player groups with two bots
    :param player_index: the player of interests ID assigned by oTree
    :return: the ID of their blue group, human, partner
    """
    if player_index in (1, 3, 5, 7):
        blue_human_partner = player_index + 1
    else:  # player_index (2, 4, 6, 8)
        blue_human_partner = player_index - 1
    return blue_human_partner


def find_green_human_partner(player_index: int):
    """
        Assigns the groups for the blue group. Groups are now 2-player groups with two bots
        :param player_index: the player of interests ID assigned by oTree
        :return: the ID of their green group, human, partner
        """
    if player_index in (1, 2, 5, 6):
        green_human_partner = player_index + 2
    else:  # player_index in (3, 4, 7, 8)
        green_human_partner = player_index - 2
    return green_human_partner


def setting_groups(players):
    """
    Calls find_human_partner functions and sets that for each player as the subject they that interact with in the first
    and in all subsequent rounds
    :param players:  One subject we are attempting to group
    :return: saves player IDs to that player to be accessed later
    """
    for index, player in enumerate(players):
        player.blue_group_human_partner = find_blue_human_partner(index + 1)
        player.green_group_human_partner = find_green_human_partner(index + 1)


# =====================================================================================================================
# Bot Behavior and Adding to Groups | Multi-Group
# =====================================================================================================================


def gen_bot_freerider_behavior(lam, bound, shared):
    prob = np.random.rand()
    if prob < bound:
        amount_give = np.random.poisson(lam)
        if shared:
            amount_give = min(amount_give, 6)  # Endowment = 20 // 30% is 6.
            give_blue = int(np.round(amount_give / 2))
            give_green = int(np.round(amount_give / 2))
            return [give_blue, give_green]
        else:  # Split
            amount_give = min(amount_give, 3)  # Endowment = 10 // 30% is 3.
            int_values = int(np.round(amount_give))
            return [int_values, int_values]
    else:
        return [0, 0]


def gen_bot_altruist_behavior(lam, shared):
    amount_keep = np.random.poisson(lam)
    amount_keep = int(np.round(amount_keep))
    if shared:
        amount_give = 20 - amount_keep
        amount_give = max(amount_give, 14)  # Endowment = 20 // 70% is 14.
        give_blue = int(amount_give / 2)
        give_green = int(amount_give / 2)
        return [give_blue, give_green]
    else:  # Split
        amount_give = 10 - amount_keep
        amount_give = max(amount_give, 7)  # Endowment = 10 // 70% is 7.
        int_values = int(np.round(amount_give))
        return [int_values, int_values]


def gen_bot_behavior_list(lam, bound, shared):
    bot_behavior_list = []
    for i in range(1, 9):
        if i in (1, 2, 3, 4):
            bot_behavior = gen_bot_freerider_behavior(lam, bound, shared)
        else:  # i in (5, 6, 7, 8)
            bot_behavior = gen_bot_altruist_behavior(lam, shared)
        bot_behavior_list.append(bot_behavior)
    return bot_behavior_list


def setting_bot_decisions(players, shared):
    """
    Calls bot behavior functions and sets that for each player's bot variables for both groups
    :param players: One subject we are attempting to group
    :param shared: bool for if the treatment is shared or not
    :return: saves investment decisions in the current round of the bots a player interacts with in their groups
    """
    bot_behavior_list = gen_bot_behavior_list(2, 1/2, shared)
    for index, player in enumerate(players):
        if index in (0, 1):
            player.blue_bot_one_investment = bot_behavior_list[0][0]
            player.blue_bot_two_investment = bot_behavior_list[1][0]
            if index == 0:
                player.green_bot_one_investment = bot_behavior_list[4][1]
                player.green_bot_two_investment = bot_behavior_list[6][1]
            else:
                player.green_bot_one_investment = bot_behavior_list[5][1]
                player.green_bot_two_investment = bot_behavior_list[7][1]
        elif index in (2, 3):
            player.blue_bot_one_investment = bot_behavior_list[2][0]
            player.blue_bot_two_investment = bot_behavior_list[3][0]
            if index == 2:
                player.green_bot_one_investment = bot_behavior_list[4][1]
                player.green_bot_two_investment = bot_behavior_list[6][1]
            else:
                player.green_bot_one_investment = bot_behavior_list[5][1]
                player.green_bot_two_investment = bot_behavior_list[7][1]
        elif index in (4, 5):
            player.blue_bot_one_investment = bot_behavior_list[4][0]
            player.blue_bot_two_investment = bot_behavior_list[5][0]
            if index == 4:
                player.green_bot_one_investment = bot_behavior_list[0][1]
                player.green_bot_two_investment = bot_behavior_list[2][1]
            else:
                player.green_bot_one_investment = bot_behavior_list[1][1]
                player.green_bot_two_investment = bot_behavior_list[3][1]
        else:  # index in (6, 7)
            player.blue_bot_one_investment = bot_behavior_list[6][0]
            player.blue_bot_two_investment = bot_behavior_list[7][0]
            if index == 6:
                player.green_bot_one_investment = bot_behavior_list[0][1]
                player.green_bot_two_investment = bot_behavior_list[2][1]
            else:
                player.green_bot_one_investment = bot_behavior_list[1][1]
                player.green_bot_two_investment = bot_behavior_list[3][1]


# =====================================================================================================================
# Bot Behavior and Adding to Groups | Single-Group
# =====================================================================================================================


def find_human_partner(player_index: int):
    if player_index in (1, 3, 5, 7):
        human_partner = player_index + 1
    else:  # player_index in (2, 4, 6, 8)
        human_partner = player_index - 1
    return human_partner


def setting_groups_single(players):
    """
    Calls find_human_partner functions and sets that for each player as the subject they that interact with in the first
    and in all subsequent rounds
    :param players:  One subject we are attempting to group
    :return: saves player IDs to that player to be accessed later
    """
    for index, player in enumerate(players):
        player.human_partner = find_human_partner(index + 1)


def gen_bot_altruist_behavior_single(lam):
    amount_keep = np.random.poisson(lam)
    amount_keep = int(np.round(amount_keep))
    amount_give = 20 - amount_keep
    amount_give = max(amount_give, 14)  # Endowment = 20 // 70% is 14.
    int_value = int(np.round(amount_give))
    return int_value


def gen_bot_freerider_behavior_single(lam, bound):
    prob = np.random.rand()
    if prob < bound:
        amount_give = np.random.poisson(lam)
        amount_give = min(amount_give, 6)
        int_value = int(np.round(amount_give))
        return int_value
    else:
        return 0


def gen_bot_behavior_list_single(lam, bound):
    bot_behavior_list = []
    for i in range(1, 9):
        if i in (1, 2, 3, 4):
            bot_behavior = gen_bot_freerider_behavior_single(lam, bound)
        else:  # i in (5, 6, 7, 8)
            bot_behavior = gen_bot_altruist_behavior_single(lam)
        bot_behavior_list.append(bot_behavior)
    return bot_behavior_list


def setting_bot_decisions_single(players):
    bot_behavior_list = gen_bot_behavior_list_single(2, 1/2)
    for index, player in enumerate(players):
        if index in (0, 1):
            player.bot_one_investment = cu(bot_behavior_list[0])
            player.bot_two_investment = cu(bot_behavior_list[1])
        elif index in (2, 3):
            player.bot_one_investment = cu(bot_behavior_list[2])
            player.bot_two_investment = cu(bot_behavior_list[3])
        elif index in (4, 5):
            player.bot_one_investment = cu(bot_behavior_list[4])
            player.bot_two_investment = cu(bot_behavior_list[5])
        else:  # index in (6, 7)
            player.bot_one_investment = cu(bot_behavior_list[6])
            player.bot_two_investment = cu(bot_behavior_list[7])
