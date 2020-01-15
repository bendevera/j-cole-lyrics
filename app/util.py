import keras
from keras.models import load_model
import numpy as np
import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(dir_path, 'lib/model2.h5')
model = load_model(path)

path = os.path.join(dir_path, 'lib/char.json')
chars = json.loads(open(path).read())
path = os.path.join(dir_path, 'lib/char_indices.json')
char_indices = json.loads(open(path).read())
maxlen = 60

def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype("float64")
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

# need to save chars and char_indices somehow
def generate_prediction(data):
    # need to add something to handle if it is shorter than maxlen
    temperature = data['temperature']
    data = data['data'].lower()
    generated_text = data[:maxlen]
    result = generated_text
    for i in range(400):
        sampled = np.zeros((1, maxlen, len(chars)))
        for t, char in enumerate(generated_text):
            sampled[0, t, char_indices[char]] = 1.
        preds = model.predict(sampled, verbose=0)[0]
        next_index = sample(preds,temperature)
        next_char = chars[next_index]
        generated_text += next_char 
        generated_text = generated_text[1:]
        result += next_char
    return result
