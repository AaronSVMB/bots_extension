from otree.api import *
from bots_utils.common_functions import make_comprehension_question
import time

doc = """
Instrucs and Comp Qs for for Shared Endowment Treatment FLIPPED screens
"""


class C(BaseConstants):
    NAME_IN_URL = 'bots_shared_flipped_instrucs'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    NUM_PERIODS = 20
    ENDOWMENT = cu(20)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Comprehension Questions
    comprehension_question_one = make_comprehension_question("")
    comprehension_question_two = models.IntegerField(
        choices=[
            [1, 'True'],
            [2, 'False'],
        ], label="True or False",
        widget=widgets.RadioSelect
    )
    comprehension_question_two_point_five = models.IntegerField(
        choices=[
            [1, 'True'],
            [2, 'False'],
        ], label="True or False",
        widget=widgets.RadioSelect
    )
    comprehension_question_three_a = models.IntegerField(label="What is the minimum amount you can invest in a group's"
                                                               " joint account?")
    comprehension_question_three_b = models.IntegerField(label="What is the maximum amount you can invest in a group's"
                                                               " joint account?")

    # Qs Regarding Earnings
    comprehension_question_four_a = make_comprehension_question("")
    comprehension_question_four_b = make_comprehension_question("")
    comprehension_question_four_c = make_comprehension_question("")
    comprehension_question_four_d = make_comprehension_question("")

    # Time to answer questions
    time_to_answer = models.IntegerField(initial=360)  # 6 minutes

    # Time Tracking
    start_time = models.FloatField(initial=0)

    time_spent_instrucs = models.FloatField(initial=0)

    time_spent_q_one = models.FloatField(initial=0)

    time_spent_q_two = models.FloatField(initial=0)

    time_spent_q_two_point_five = models.FloatField(initial=0)

    time_spent_q_three = models.FloatField(initial=0)

    time_spent_q_four = models.FloatField(initial=0)

    # Error Tracking
    num_errors_q_one = models.IntegerField(initial=0)

    num_errors_q_two = models.IntegerField(initial=0)

    num_errors_q_two_point_five = models.IntegerField(initial=0)

    num_errors_q_three_a = models.IntegerField(initial=0)
    num_errors_q_three_b = models.IntegerField(initial=0)

    num_errors_q_four_a = models.IntegerField(initial=0)
    num_errors_q_four_b = models.IntegerField(initial=0)
    num_errors_q_four_c = models.IntegerField(initial=0)
    num_errors_q_four_d = models.IntegerField(initial=0)


# PAGES
class Instructions(Page):

    @staticmethod
    def is_displayed(player: Player):
        player.start_time = time.time()
        return True

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.time_to_answer += int(time.time())
        # Save instructions time
        player.time_spent_instrucs = time.time() - player.start_time
        # reset start_time to time next page
        player.start_time = time.time()
        if player.time_spent_q_one is None:
            player.time_spent_q_one = 0


class QuestionOne(Page):
    form_model = 'player'
    form_fields = ['comprehension_question_one']
    timer_text = 'Time left to complete the quiz:'

    @staticmethod
    def get_timeout_seconds(player: Player):
        return player.time_to_answer - time.time()

    @staticmethod
    def error_message(player: Player, values):
        if values['comprehension_question_one'] != 20:
            end_time = time.time()
            elapsed_time = end_time - player.start_time
            player.time_spent_q_one += elapsed_time  # Increment total time spent on this page
            player.start_time = time.time()  # Reset the start time for the next iteration
            player.num_errors_q_one += 1
            return 'In each period you will receive 20 points that you can choose to invest to your two groups or ' \
                   'your personal account.'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        end_time = time.time()
        elapsed_time = end_time - player.start_time
        player.time_spent_q_one += elapsed_time  # Increment total time spent on this page
        # Reset timers for Q_2
        player.start_time = time.time()
        if player.time_spent_q_two is None:
            player.time_spent_q_two = 0


class QuestionTwo(Page):
    form_model = 'player'
    form_fields = ['comprehension_question_two']
    timer_text = 'Time left to complete the quiz:'

    @staticmethod
    def get_timeout_seconds(player: Player):
        return player.time_to_answer - time.time()

    @staticmethod
    def error_message(player: Player, values):
        if values['comprehension_question_two'] != 1:
            end_time = time.time()
            elapsed_time = end_time - player.start_time
            player.time_spent_q_two += elapsed_time  # Increment total time spent on this page
            player.start_time = time.time()  # Reset the start time for the next iteration
            player.num_errors_q_two += 1
            return 'If a participant is in your Blue Group, that same participant cannot be in your Green Group.'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        end_time = time.time()
        elapsed_time = end_time - player.start_time
        player.time_spent_q_two += elapsed_time  # Increment total time spent on this page
        # Reset Timers for Q3
        player.start_time = time.time()
        if player.time_spent_q_two_point_five is None:
            player.time_spent_q_two_point_five = 0


class QuestionTwoPointFive(Page):
    form_model = 'player'
    form_fields = ['comprehension_question_two_point_five']
    timer_text = 'Time left to complete the quiz:'

    @staticmethod
    def get_timeout_seconds(player: Player):
        return player.time_to_answer - time.time()

    @staticmethod
    def error_message(player: Player, values):
        if values['comprehension_question_two_point_five'] != 1:
            end_time = time.time()
            elapsed_time = end_time - player.start_time
            player.time_spent_q_two_point_five += elapsed_time  # Increment total time spent on this page
            player.start_time = time.time()  # Reset the start time for the next iteration
            player.num_errors_q_two_point_five += 1
            return 'Each AI participant is in two groups, receives 20 points each period to decide how to invest, and ' \
                   'faces the same investment decision as human subjects.'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        end_time = time.time()
        elapsed_time = end_time - player.start_time
        player.time_spent_q_two_point_five += elapsed_time  # Increment total time spent on this page
        # Reset Timers for Q3
        player.start_time = time.time()
        if player.time_spent_q_three is None:
            player.time_spent_q_three = 0


class QuestionThree(Page):
    form_model = 'player'
    form_fields = ['comprehension_question_three_a', 'comprehension_question_three_b']
    timer_text = 'Time left to complete the quiz:'

    @staticmethod
    def get_timeout_seconds(player: Player):
        return player.time_to_answer - time.time()

    @staticmethod
    def error_message(player: Player, values):
        if values['comprehension_question_three_a'] != 0:
            end_time = time.time()
            elapsed_time = end_time - player.start_time
            player.time_spent_q_three += elapsed_time  # Increment total time spent on this page
            player.start_time = time.time()  # Reset the start time for the next iteration
            player.num_errors_q_three_a += 1
            return 'Your minimum investment to a group account would be investing nothing – 0 points – in a period.'
        if values['comprehension_question_three_b'] != 20:
            end_time = time.time()
            elapsed_time = end_time - player.start_time
            player.time_spent_q_three += elapsed_time  # Increment total time spent on this page
            player.start_time = time.time()  # Reset the start time for the next iteration
            player.num_errors_q_three_b += 1
            return 'Each period you receive 20 points that you choose how to invest between your Personal Account, and' \
                   ' your two groups. At most you could invest all 20 points to one account.'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        end_time = time.time()
        elapsed_time = end_time - player.start_time
        player.time_spent_q_three += elapsed_time  # Increment total time spent on this page
        # Reset Timers for Q4
        player.start_time = time.time()
        if player.time_spent_q_four is None:
            player.time_spent_q_four = 0


class QuestionFour(Page):
    form_model = 'player'
    form_fields = ['comprehension_question_four_a',
                   'comprehension_question_four_b',
                   'comprehension_question_four_c',
                   'comprehension_question_four_d']
    timer_text = 'Time left to complete the quiz:'

    @staticmethod
    def get_timeout_seconds(player: Player):
        return player.time_to_answer - time.time()

    @staticmethod
    def error_message(player: Player, values):
        if values['comprehension_question_four_a'] != 12:
            end_time = time.time()
            elapsed_time = end_time - player.start_time
            player.time_spent_q_four += elapsed_time  # Increment total time spent on this page
            player.start_time = time.time()  # Reset the start time for the next iteration
            player.num_errors_q_four_a += 1
            return 'Reconsider your answer to question four B: You invested 6 points to the Blue Group, ' \
                   ' and Your other Blue Group members invested 18 points. Add these two together, then multiply by ' \
                   'the 0.5 to get your Blue Individual Share.'
        if values['comprehension_question_four_b'] != 21:
            end_time = time.time()
            elapsed_time = end_time - player.start_time
            player.time_spent_q_four += elapsed_time  # Increment total time spent on this page
            player.start_time = time.time()  # Reset the start time for the next iteration
            player.num_errors_q_four_b += 1
            return 'Reconsider your answer to question four A: You invested 11 points to your Green Group, ' \
                   'and Your other Green Group members invested 31 points. Add these two together, then multiply by' \
                   ' the 0.5 to get your Green Individual Share.'
        if values['comprehension_question_four_c'] != 3:
            end_time = time.time()
            elapsed_time = end_time - player.start_time
            player.time_spent_q_four += elapsed_time  # Increment total time spent on this page
            player.start_time = time.time()  # Reset the start time for the next iteration
            player.num_errors_q_four_c += 1
            return 'Reconsider your answer to question four C: Your Personal Account is the points you receive each ' \
                   'round (20 points) minus your investment to your Blue Group (6 points) and minus your investment ' \
                   'to your Green Group (11 points).'
        if values['comprehension_question_four_d'] != 36:
            end_time = time.time()
            elapsed_time = end_time - player.start_time
            player.time_spent_q_four += elapsed_time  # Increment total time spent on this page
            player.start_time = time.time()  # Reset the start time for the next iteration
            player.num_errors_q_four_d += 1
            return 'Reconsider your answer to question four D: Your Period Earnings are the sum of your Green and Blue' \
                   'Individual Shares, and your Personal Account (If your response to four A, B, and C are correct, sum' \
                   ' those together.'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        end_time = time.time()
        elapsed_time = end_time - player.start_time
        player.time_spent_q_four += elapsed_time  # Increment total time spent on this page


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Instructions,
                 QuestionOne,
                 QuestionTwo,
                 QuestionTwoPointFive,
                 QuestionThree,
                 QuestionFour,
                 Results,
                 ResultsWaitPage]
