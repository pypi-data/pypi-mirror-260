import random

def shuffle_questions(description_widgets, dropdowns, seed, **kwargs):
    # Set the seed for reproducibility
    random.seed(seed)

    # Combine the widgets into pairs
    widget_pairs = list(zip(description_widgets, dropdowns))

    # Shuffle the list of pairs
    random.shuffle(widget_pairs)

    return widget_pairs

def shuffle_options(options, seed, **kwargs):
    # Set the seed for reproducibility
    random.seed(seed)

    # Shuffle the list of pairs
    random.shuffle(options)

    return options