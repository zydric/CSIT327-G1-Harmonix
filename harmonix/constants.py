# Shared constants for the Harmonix project
# These choices should be used consistently across all apps

# Genre choices - standardized as per design requirements
GENRE_CHOICES = [
    ('rock', 'Rock'),
    ('jazz', 'Jazz'),
    ('indie', 'Indie'),
    ('folk', 'Folk'),
    ('electronic', 'Electronic'),
    ('blues', 'Blues'),
    ('country', 'Country'),
    ('opm', 'OPM'),
]

# Common instrument choices
INSTRUMENT_CHOICES = [
    ('guitar', 'Guitar'),
    ('bass', 'Bass'),
    ('drums', 'Drums'),
    ('piano', 'Piano'),
    ('vocals', 'Vocals'),
    ('keyboard', 'Keyboard'),
    ('violin', 'Violin'),
    ('saxophone', 'Saxophone'),
    ('trumpet', 'Trumpet'),
    ('percussion', 'Percussion'),
]

# Export choices as dictionaries for easy lookup
GENRE_DICT = dict(GENRE_CHOICES)
INSTRUMENT_DICT = dict(INSTRUMENT_CHOICES)