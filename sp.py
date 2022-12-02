from keras.layers import Dense, Dropout
from keras.models import Sequential
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
import helper_funcs
import feature_builder



subset = {}
subset = helper_funcs.get_subset(helper_funcs.raw_data, subset)
team_season_data = helper_funcs.get_season_table(subset)

## Complete features/Targets
complete_features = feature_builder.get_features(team_season_data, subset, helper_funcs.raw_data)
complete_features_dropna = complete_features.dropna()
complete_targets_dropna = complete_features_dropna['Result']
complete_targets_OH_dropna = complete_features_dropna[(['Win', 'Loss', 'Draw'])]
complete_features_dropna = complete_features_dropna.drop((['Win', 'Loss', 'Draw', 'Result']), axis=1)

X_train, X_test, y_train, y_test = train_test_split(complete_features_dropna, complete_targets_OH_dropna,
                                                    random_state=42)

# Building the model
model_1 = Sequential()
model_1.add(Dense(64, activation='relu', input_shape=(X_train.shape[1],)))
model_1.add(Dropout(.3))
model_1.add(Dense(32, activation='tanh'))
model_1.add(Dropout(.2))
model_1.add(Dense(16, activation='tanh'))
model_1.add(Dropout(.2))
model_1.add(Dense(y_train.shape[1], activation='softmax'))

model_1.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
hist = model_1.fit(X_train, y_train, epochs=20, validation_data=(X_test, y_test))
score = model_1.evaluate(X_test, y_test, verbose=0)

print("Accuracy of the model is : ", score[1])
plt.show()
