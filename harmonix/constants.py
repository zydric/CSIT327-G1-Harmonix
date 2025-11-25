# Shared constants for the Harmonix project
# These choices should be used consistently across all apps

# Genre choices - standardized as per design requirements
# Sorted by popularity/commonness
GENRE_CHOICES = [
    ('rock', 'Rock'),
    ('pop', 'Pop'),
    ('indie', 'Indie'),
    ('hip-hop', 'Hip-Hop'),
    ('electronic', 'Electronic'),
    ('jazz', 'Jazz'),
    ('blues', 'Blues'),
    ('metal', 'Metal'),
    ('punk', 'Punk'),
    ('alternative', 'Alternative'),
    ('folk', 'Folk'),
    ('country', 'Country'),
    ('r&b', 'R&B'),
    ('classical', 'Classical'),
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