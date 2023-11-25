from os import environ

SESSION_CONFIGS = [
    # dict(
    #     name='public_goods',
    #     app_sequence=['public_goods'],
    #     num_demo_participants=3,
    # ),
    dict(
        name='bots_shared',
        display_name='bots extension shared',
        app_sequence=['bots_shared'],
        num_demo_participants=8
    ),
    dict(
        name='bots_split',
        display_name='bots extension split',
        app_sequence=['bots_split'],
        num_demo_participants=8
    ),
    dict(
            name='bots_single',
            display_name='bots extension single',
            app_sequence=['bots_single'],
            num_demo_participants=8
        ),
    dict(
        name='bots_shared_flipped',
        display_name='bots extension shared topsy-turvy',
        app_sequence=['bots_shared_flipped'],
        num_demo_participants=8
    ),
    dict(
        name='bots_split_flipped',
        display_name='bots extension split topsy-turvy',
        app_sequence=['bots_split_flipped'],
        num_demo_participants=8
    ),
    dict(
        name='bots_shared_instrucs',
        display_name='bots shared instrucs',
        app_sequence=['bots_shared_instrucs'],
        num_demo_participants=1
    ),
    dict(
        name='bots_shared_instrucs_flipped',
        display_name='bots shared instrucs flipped',
        app_sequence=['bots_shared_flipped_instrucs'],
        num_demo_participants=1
    ),
    dict(
        name='survey',
        display_name='bots multi survey',
        app_sequence=['bots_multi_survey'],
        num_demo_participants=1
    ),
    dict(
        name='survey2',
        display_name='bots multi survey flipped',
        app_sequence=['bots_multi_flipped_survey'],
        num_demo_participants=1
    ),
    dict(
        name='bots_shared_full_experiment',
        display_name='bots shared full experiment',
        app_sequence=['bots_shared_instrucs', 'bots_shared', 'bots_multi_survey'],
        num_demo_participants=8
    ),
    dict(
        name='bots_shared_flipped_full_experiment',
        display_name='bots shared flipped full experiment',
        app_sequence=['bots_shared_flipped_instrucs', 'bots_shared_flipped', 'bots_multi_flipped_survey'],
        num_demo_participants=8
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.02, participation_fee=7.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = 'TestPassword'

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '2837266070105'

OTREE_PRODUCTION=1
