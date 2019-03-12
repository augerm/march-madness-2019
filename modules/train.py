import tensorflow.keras as k
from modules.matchups import Matchups

matchups = Matchups()

completed_matchups = matchups.get_completed_matchups()

X = map(lambda completed_matchup: completed_matchup.get_features(), completed_matchups)
Y = map(lambda completed_matchup: completed_matchup.result, completed_matchups)

# Create neural network architecture
model = k.Sequential()
model.add(k.Dense(2, input_dim=1, activation='relu'))
model.add(k.Dense(8, activation='relu'))
model.add(k.Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X, Y, epochs=150, batch_size=10)
