from insults import Insults

def load_model(path):
    Insults.load_model()
    return "no model yet"

def predict(text):
    load_model()
    return Insults.rate_comment(text)
