from keras.layers import Dense, Dropout
from keras.models import Sequential
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import numpy as np
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

scaler = MinMaxScaler(feature_range=[0, 1])
data_rescaled = scaler.fit_transform(complete_features_dropna)
# Fitting the PCA algorithm with our Data
pca = PCA().fit(data_rescaled)
n_components = list(np.cumsum(pca.explained_variance_ratio_)).index(
    np.cumsum(pca.explained_variance_ratio_)[(np.cumsum(pca.explained_variance_ratio_) >= 0.98)][0])
print("Best n_components is " + str(n_components))
X_train, X_test, y_train, y_test = train_test_split(complete_features_dropna, complete_targets_OH_dropna, test_size=0.2,
                                                    random_state=1)
pca = PCA(n_components=n_components, whiten=True, svd_solver='randomized')
pca.fit(X_train)
X_train_pca = pca.transform(X_train)
X_test_pca = pca.transform(X_test)

# Building the model
model_3 = Sequential()
model_3.add(Dense(64, activation='relu', input_shape=(X_train_pca.shape[1],)))
model_3.add(Dropout(.3))
model_3.add(Dense(32, activation='tanh'))
model_3.add(Dropout(.2))
model_3.add(Dense(16, activation='tanh'))
model_3.add(Dropout(.2))
model_3.add(Dense(y_train.shape[1], activation='softmax'))

# Com_3piling the model
model_3.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
model_3.summary()

hist = model_3.fit(X_train_pca, y_train, epochs=500, batch_size=15, verbose=0, validation_data=(X_test_pca, y_test))
score = model_3.evaluate(X_test_pca, y_test, verbose=0)
print("Accuracy: ", score[1])
