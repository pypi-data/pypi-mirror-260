import random

def generate_affirmation():
    affirmations = [
        "I believe in myself and my abilities.",
        "I create my own luck.",
        "Every day I am growing and evolving.",
        "I appreciate every moment of my life.",
        "I inspire and motivate myself and others.",
        "I am capable of more than I think.",
    ]
    return random.choice(affirmations)

def generate_motivational_quote():
    quotes = [
        "Success is the ability to go from one failure to another with no loss of enthusiasm. - Winston Churchill",
        "Only those who dare to fail greatly can ever achieve greatly. - Robert F. Kennedy",
        "Don't be afraid of lofty goals, they foster great achievements. - Pekka Himanen",
        "If you cannot do great things, do small things in a great way. - Napoleon Hill",
        "Beginning is always scary. Make the first step and you're already not in the same place. - Brandon Basten",
    ]
    return random.choice(quotes)

def save_quotes_to_file(quotes, filename):
    """
    Save the list of quotes to a file.

    :param quotes: List of quotes to save.
    :param filename: Name of the file to save the quotes to.
    """
    with open(filename, 'w') as file:
        for quote in quotes:
            file.write(quote + '\n')

if __name__ == "__main__":
    affirmation = generate_affirmation()
    quote = generate_motivational_quote()

    print("Random affirmation of the day:")
    print(affirmation)
    print("\nMotivational quote of the day:")
    print(quote)

    # Save quotes to a file
    quotes_to_save = [affirmation, quote]
    filename = 'quotes_of_the_day.txt'
    save_quotes_to_file(quotes_to_save, filename)
