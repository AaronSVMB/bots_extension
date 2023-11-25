from otree.api import *
import time

doc = """
Survey Questions for MULTI-group sessions of the BOTS extensions with FLIPPED screens
"""


class C(BaseConstants):
    NAME_IN_URL = 'bots_multi_flipped_survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def make_survey_question(label):
    return models.LongStringField(label=label)


class Player(BasePlayer):
    password_to_start = models.StringField()

    # General Qs

    gender = models.IntegerField(
        choices=[
            [1, 'Male'],
            [2, 'Female'],
            [3, "Other"]
        ],
        label="1. What is your gender?",
        widget=widgets.RadioSelect
    )

    age = models.IntegerField(label="2. What is your age?")

    grade = models.IntegerField(
        choices=[
            [1, 'Freshman'],
            [2, 'Sophomore'],
            [3, 'Junior'],
            [4, 'Senior'],
            [5, 'Graduate']
        ],
        label="3. What year are you in?",
        widget=widgets.RadioSelect
    )

    major = models.StringField(label="4. What is your major?")

    risk = models.IntegerField(
        choices=[
            [1, 'Strongly Disagree'],
            [2, 'Disagree'],
            [3, 'Slightly Disagree'],
            [4, 'Neutral'],
            [5, 'Slightly Agree'],
            [6, 'Agree'],
            [7, 'Strongly Agree']
        ],
        widget=widgets.RadioSelectHorizontal,
        label='5. You are a person who is fully prepared to take risks.'
    )

    # Larry Specific Qs

    # Short Response

    compare_groups = models.LongStringField(label="6. In a few sentences, please explain what led you to invest more or"
                                                  " less in one group's account versus the other group's account.")

    personal_versus_group = models.LongStringField(label="7. In a few sentences, please explain what led you to invest"
                                                         " more or less of your endowment in your personal account"
                                                         " versus the group accounts. Be as specific as possible.")

    change = models.LongStringField(label="8. In a few sentences, please explain what led you to change how much you"
                                          " invested in the group accounts over time. Be  as specific as possible.")

    # Bots Scale Qs

    bot_number_blue = models.IntegerField(
        choices=[[1, 'All three of the members were computerized subjects.'],
                 [2, 'Two of the other members were computerized subjects.'],
                 [3, 'One of the other members was a computerized subject.'],
                 [4, 'None of the other members were computerized subjects.'],
                 [5, "I'm not at all sure how many of the other members were computerized subjects."]
                 ],
        widget=widgets.RadioSelect,
        label='Regarding the NUMBER of computerized subjects'
    )

    bot_level_blue = models.IntegerField(
        choices=[[1, 'They tended to invest more in the group account than the human subject(s).'],
                 [2, 'They tended to invest less in the group account than the human subject(s).'],
                 [3, 'They tended to invest about as much in the group account as the human subject(s).'],
                 [4, "I really don't know their investments compared to those of the human subject(s)."]],
        widget=widgets.RadioSelect,
        label='Regarding the investment LEVELS of the computerized members'
    )

    bots_pattern_blue = models.IntegerField(
        choices=[
            [1,
             'They tended to invest more in the group account followinga period in which the human subject(s) invested more.'],
            [2,
             'They tended to invest less in the group account following a period in which the human subject(s) invested more.'],
            [3,
             "I don't think their investments were influenced by the investments of the human subject(s) in the previous period."]
        ],
        widget=widgets.RadioSelect,
        label='Regarding the investment PATTERNS of the computerized members'
    )

    bots_own_blue = models.IntegerField(
        choices=[
            [1, 'The presence of computerized subjects led me to invest more in the group account.'],
            [2, 'The presence of computerized subjects led me to invest less in the group account.'],
            [3, 'The presence of computerized subjects did not influence my level of investment in the group account.']
        ],
        widget=widgets.RadioSelect,
        label='Regarding MY OWN INVESTMENT'
    )

    bots_understand_blue = models.IntegerField(
        choices=[
            [1,
             "Trying to understand the computerized subject(s)' investment decisions helped me increase my own earnings."],
            [2,
             "Trying to understand the computerized subject(s)' investment decisions did not help me increase my own earnings."],
            [3,
             "I really don't know whether trying to understand the computerized subject(s) investment decisions helped me increase my own earnings."]
        ],
        widget=widgets.RadioSelect,
        label='Regarding MY OWN EARNINGS'
    )

    bot_number_green = models.IntegerField(
        choices=[[1, 'All three of the members were computerized subjects.'],
                 [2, 'Two of the other members were computerized subjects.'],
                 [3, 'One of the other members was a computerized subject.'],
                 [4, 'None of the other members were computerized subjects.'],
                 [5, "I'm not at all sure how many of the other members were computerized subjects."]
                 ],
        widget=widgets.RadioSelect,
        label='Regarding the NUMBER of computerized subjects'
    )

    bot_level_green = models.IntegerField(
        choices=[[1, 'They tended to invest more in the group account than the human subject(s).'],
                 [2, 'They tended to invest less in the group account than the human subject(s).'],
                 [3, 'They tended to invest about as much in the group account as the human subject(s).'],
                 [4, "I really don't know their investments compared to those of the human subject(s)."]],
        widget=widgets.RadioSelect,
        label='Regarding the investment LEVELS of the computerized members'
    )

    bots_pattern_green = models.IntegerField(
        choices=[
            [1,
             'They tended to invest more in the group account followinga period in which the human subject(s) invested more.'],
            [2,
             'They tended to invest less in the group account following a period in which the human subject(s) invested more.'],
            [3,
             "I don't think their investments were influenced by the investments of the human subject(s) in the previous period."]
        ],
        widget=widgets.RadioSelect,
        label='Regarding the investment PATTERNS of the computerized members'
    )

    bots_own_green = models.IntegerField(
        choices=[
            [1, 'The presence of computerized subjects led me to invest more in the group account.'],
            [2, 'The presence of computerized subjects led me to invest less in the group account.'],
            [3, 'The presence of computerized subjects did not influence my level of investment in the group account.']
        ],
        widget=widgets.RadioSelect,
        label='Regarding MY OWN INVESTMENT'
    )

    bots_understand_green = models.IntegerField(
        choices=[
            [1,
             "Trying to understand the computerized subject(s)' investment decisions helped me increase my own earnings."],
            [2,
             "Trying to understand the computerized subject(s)' investment decisions did not help me increase my own earnings."],
            [3,
             "I really don't know whether trying to understand the computerized subject(s) investment decisions helped me increase my own earnings."]
        ],
        widget=widgets.RadioSelect,
        label='Regarding MY OWN EARNINGS'
    )

    # Scale (9)

    reason_own = models.IntegerField(
        choices=[
            [1, 'Strongly Agree'],
            [2, 'Agree'],
            [3, 'Disagree'],
            [4, 'Strongly Disagree'],
            [5, 'Uncertain']
        ],
        widget=widgets.RadioSelectHorizontal,
        label="I mainly tried to make investments that would maximize my own overall earnings."
    )

    reason_group = models.IntegerField(
        choices=[
            [1, 'Strongly Agree'],
            [2, 'Agree'],
            [3, 'Disagree'],
            [4, 'Strongly Disagree'],
            [5, 'Uncertain']
        ],
        widget=widgets.RadioSelectHorizontal,
        label="I mainly tried to make investments that would maximize each group's overall earnings."
    )

    reason_conditional = models.IntegerField(
        choices=[
            [1, 'Strongly Agree'],
            [2, 'Agree'],
            [3, 'Disagree'],
            [4, 'Strongly Disagree'],
            [5, 'Uncertain']
        ],
        widget=widgets.RadioSelectHorizontal,
        label="I mainly tried to make investments that would encourage other members of each group to make large "
              "investments in the group account."
    )

    reason_experiment = models.IntegerField(
        choices=[
            [1, 'Strongly Agree'],
            [2, 'Agree'],
            [3, 'Disagree'],
            [4, 'Strongly Disagree'],
            [5, 'Uncertain']
        ],
        widget=widgets.RadioSelectHorizontal,
        label="I experimented with different levels of investment in each group account to see how it would affect what"
              " the other members invested."
    )

    reason_adjust = models.IntegerField(
        choices=[
            [1, 'Strongly Agree'],
            [2, 'Agree'],
            [3, 'Disagree'],
            [4, 'Strongly Disagree'],
            [5, 'Uncertain']
        ],
        widget=widgets.RadioSelectHorizontal,
        label="I adjusted my own investment to each group account based on what the other members were investing in the"
              " group account."
    )

    reason_future_rounds = models.IntegerField(
        choices=[
            [1, 'Strongly Agree'],
            [2, 'Agree'],
            [3, 'Disagree'],
            [4, 'Strongly Disagree'],
            [5, 'Uncertain']
        ],
        widget=widgets.RadioSelectHorizontal,
        label="The size of my investment in each group account influenced how much the other group members invested in"
              " the following period."
    )

    # Decision-making style (10)

    decision_style_facts = models.IntegerField(
        choices=[
            [1, 'Almost Always'],
            [2, 'Often'],
            [3, 'Rarely'],
            [4, 'Almost Never']
        ],
        widget=widgets.RadioSelectHorizontal,
        label="When making important decisions, I focus on facts and logic."
    )

    decision_style_feelings = models.IntegerField(
        choices=[
            [1, 'Almost Always'],
            [2, 'Often'],
            [3, 'Rarely'],
            [4, 'Almost Never']
        ],
        widget=widgets.RadioSelectHorizontal,
        label="When making important decisions, I trust my feelings and intuition."
    )

    decision_style_family = models.IntegerField(
        choices=[
            [1, 'Almost Always'],
            [2, 'Often'],
            [3, 'Rarely'],
            [4, 'Almost Never']
        ],
        widget=widgets.RadioSelectHorizontal,
        label="When making important decisions, I consult with one or more family members."
    )

    decision_style_friend = models.IntegerField(
        choices=[
            [1, 'Almost Always'],
            [2, 'Often'],
            [3, 'Rarely'],
            [4, 'Almost Never']
        ],
        widget=widgets.RadioSelectHorizontal,
        label="When making important decisions, I consult with one or more friends."
    )

    # Meta Questions

    clarity = models.IntegerField(
        choices=[
            [1, 'Strongly Disagree'],
            [2, 'Disagree'],
            [3, 'Agree'],
            [4, 'Strongly Agree'],
            [5, "Don't know"]
        ],
        widget=widgets.RadioSelectHorizontal,
        label='12. The instructions for the experiment were clear and easy to follow.'
    )

    suggestions = make_survey_question("13. We value your feedback, so please use the following text box for comments"
                                       " or suggestions.")

    # Track Time

    start_time = models.FloatField(initial=0)

    time_spent_survey_one = models.FloatField(initial=0)

    time_spent_survey_bots = models.FloatField(initial=0)

    time_spent_survey_two = models.FloatField(initial=0)

    time_spent_survey_three = models.FloatField(initial=0)

    time_spent_survey_four = models.FloatField(initial=0)


# PAGES


class ThankYou(Page):
    form_model = 'player'
    form_fields = ['password_to_start']

    def error_message(player: Player, values):
        if values['password_to_start'] != 'Questionnaire':
            return 'Check your spelling or ask the experimenter for help'


class SurveyOne(Page):
    form_model = 'player'
    form_fields = ['gender', 'age', 'grade', 'major',
                   'risk',
                   'compare_groups', 'personal_versus_group', 'change']

    @staticmethod
    def is_displayed(player: Player):
        player.start_time = time.time()
        return True

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.time_spent_survey_one = time.time() - player.start_time  # Save invest decision time spent


class SurveyBots(Page):
    form_model = 'player'
    form_fields = ['bot_number_blue', 'bot_level_blue', 'bots_pattern_blue', 'bots_own_blue', 'bots_understand_blue',
                   'bot_number_green', 'bot_level_green', 'bots_pattern_green', 'bots_own_green',
                   'bots_understand_green']

    @staticmethod
    def is_displayed(player: Player):
        player.start_time = time.time()
        return True

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.time_spent_survey_bots = time.time() - player.start_time  # Save invest decision time spent


class SurveyTwo(Page):
    form_model = 'player'
    form_fields = ['reason_own', 'reason_group', 'reason_conditional',
                   'reason_experiment', 'reason_adjust', 'reason_future_rounds']

    @staticmethod
    def is_displayed(player: Player):
        player.start_time = time.time()
        return True

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.time_spent_survey_two = time.time() - player.start_time  # Save invest decision time spent


class SurveyThree(Page):
    form_model = 'player'
    form_fields = ['decision_style_facts', 'decision_style_feelings',
                   'decision_style_family', 'decision_style_friend']

    @staticmethod
    def is_displayed(player: Player):
        player.start_time = time.time()
        return True

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.time_spent_survey_three = time.time() - player.start_time  # Save invest decision time spent


class SurveyFour(Page):
    form_model = 'player'
    form_fields = ['clarity', 'suggestions']

    @staticmethod
    def is_displayed(player: Player):
        player.start_time = time.time()
        return True

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.time_spent_survey_four = time.time() - player.start_time  # Save invest decision time spent


class EndPage(Page):
    pass


page_sequence = [ThankYou,
                 SurveyOne,
                 SurveyBots,
                 SurveyTwo,
                 SurveyThree,
                 SurveyFour,
                 EndPage]
