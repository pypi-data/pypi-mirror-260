from flask import Flask, render_template
import random

app = Flask(__name__)

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

@app.route('/')
def index():
    affirmation = generate_affirmation()
    quote = generate_motivational_quote()
    return render_template('index.html', affirmation=affirmation, quote=quote)

if __name__ == '__main__':
    app.run(debug=True)
