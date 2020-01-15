import numpy as np 
import keras 
from keras import layers 
import random 
import sys 
import json


path = "./compiled.txt"
text = open(path).read().lower()
print("text length:", len(text))

maxlen = 60

step = 3

sentences = []

next_chars = []

for i in range(0, len(text)-maxlen, step):
    sentences.append(text[i: i+maxlen])
    next_chars.append(text[i+maxlen])

print("Number of sequences:", len(sentences))

# put all chars in "text" in a list
chars = sorted(list(set(text)))
print("Unique characters:", len(chars))

# make a dictionary that has each char mapped to a index in chars
char_indices = dict((char, chars.index(char)) for char in chars)

print("Saving char and char_indices")
with open('app/lib/char.json', 'w') as f:
    json.dump(chars, f)
with open('app/lib/char_indices.json', 'w') as f:
    json.dump(char_indices, f)


print("Vectorization...")
# vectorization of features and targets
X = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)

for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        X[i, t, char_indices[char]] = 1.
    y[i, char_indices[next_chars[i]]] = 1.


# building the model
'''
Model Alteration Ideas:
- add some additional dense layers
- look in to 1D CNN vs RNN
- can you stack LSTM layers?
- add dropout?
- try making a GAN

- Previous model did much better than below
'''
print("Building model...")
model = keras.models.Sequential()
model.add(layers.LSTM(
                        64, 
                        dropout=0.1,
                        recurrent_dropout=0.4,
                        return_sequences=True,
                        input_shape=(maxlen, len(chars))
                        ))
model.add(layers.LSTM(
                        128, 
                        dropout=0.1,
                        recurrent_dropout=0.4,
                        activation="relu"
                        ))
model.add(layers.Dense(len(chars), activation="softmax"))

optimizer = keras.optimizers.RMSprop(lr=.01)
model.compile(
    optimizer=optimizer,
    loss=['categorical_crossentropy']
)

print("Model summary:")
print(model.summary())

def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype("float64")
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

'''
Training Improvements:
- add more to analyze accuracy of the models being built
'''

''' 
Potential reasons for NAN issue: 
occured when both layers had 128 as units (aka output_shape[-1])
- model size isn't compatible with task
'''
for epoch in range(1, 3):
    print("epoch: ", epoch)
    model.fit(X, y, batch_size=128, epochs=epoch)
    # saves model
    model.save("app/lib/model"+str(epoch)+".h5")

    start_index = random.randint(0, len(text)-maxlen-1)
    generated_text = text[start_index: start_index+maxlen]
    print('---- Generating text with: ' + generated_text + ' ----------')

    for temperature in [.2, .5, .8]:
        print("--------- temperature: ", temperature)
        sys.stdout.write(generated_text)
        for i in range(400):
            sampled = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(generated_text):
                sampled[0, t, char_indices[char]] = 1.
            preds = model.predict(sampled, verbose=0)[0]
            next_index = sample(preds, temperature)
            next_char = chars[next_index]
            generated_text += next_char 
            generated_text = generated_text[1:]

            sys.stdout.write(next_char)