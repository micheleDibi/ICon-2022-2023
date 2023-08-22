import pyswip
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import uniform, randint

from knowledge_base import KB

# Modelli
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

# Valutazione
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_validate
from sklearn.model_selection import GridSearchCV, StratifiedShuffleSplit, RandomizedSearchCV


import warnings
warnings.filterwarnings('ignore')


def cross_validation(model, _X, _y, _cv=5):
    _scoring = ['accuracy', 'precision', 'recall', 'f1']
    results = cross_validate(estimator=model
                             , X=_X
                             , y=_y
                             , cv=_cv
                             , scoring=_scoring
                             , return_train_score=True
                            )
    return {
        "Training Accuracy scores": results['train_accuracy'],
        "Mean Training Accuracy": results['train_accuracy'].mean()*100,
        "Training Precision scores": results['train_precision'],
        "Mean Training Precision": results['train_precision'].mean(),
        "Training Recall scores": results['train_recall'],
        "Mean Training Recall": results['train_recall'].mean(),
        "Training F1 scores": results['train_f1'],
        "Mean Training F1 Score": results['train_f1'].mean(),
        "Validation Accuracy scores": results['test_accuracy'],
        "Mean Validation Accuracy": results['test_accuracy'].mean()*100,
        "Validation Precision scores": results['test_precision'],
        "Mean Validation Precision": results['test_precision'].mean(),
        "Validation Recall scores": results['test_recall'],
        "Mean Validation Recall": results['test_recall'].mean(),
        "Validation F1 scores": results['test_f1'],
        "Mean Validation F1 Score": results['test_f1'].mean()
    }

def plot_results(x_label, y_label, plot_title, train_data, val_data):
    '''
        x_label: str
            Nome dell'algoritmo utilizzato nel training e.g 'Decision Tree'
            
        y_label: str
            Nome della metrica che deve essere visualzzata e.g 'Accuracy'
            
        plot_title: str
            Titolo del plot e.g 'Accuracy Plot'
            
        train_result: array
            Array che contiene la precisione di addestramento, l'accuratezza o l'f1
            
        test_result: array
            Array che contiene la precisione di valutazione, l'accuratezza o l'f1
    '''
    
    plt.figure(figsize=(12, 6))
    labels = ["1st Fold", "2nd Fold", "3rd Fold", "4th Fold", "5th Fold"]
    X_axis = np.arange(len(labels))
    ax = plt.gca()
    plt.ylim(0.40000, 1)
    plt.bar(X_axis-0.2, train_data, 0.4, color='blue', label='Training')
    plt.bar(X_axis+0.2, val_data, 0.4, color='red', label='Validation')
    plt.title(plot_title)
    plt.xticks(X_axis, labels)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.grid(True)
    plt.show()
     
def plot_range_results(x_label, y_label, plot_title, train_data, val_data, range):
    plt.figure(figsize=(12, 6))
    plt.plot(range, train_data, marker='o', linestyle='-', color='blue', label='training scores')
    plt.plot(range, val_data, marker='o', linestyle='-', color='red', label='test scores')
    plt.title(plot_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.grid(True)
    plt.show()

prolog = KB()

path_brani_preferiti = "./datasets/brani_preferiti_2023-08-11.csv"
path_brani_scaricati = "./datasets/brani_scaricati_2023-08-11.csv"

df_brani_preferiti = pd.read_csv(path_brani_preferiti)
df_brani_scaricati = pd.read_csv(path_brani_scaricati)

df_brani_preferiti['Liked'] = 1
df_brani_scaricati['Liked'] = 0

df_brani = pd.merge(df_brani_preferiti, df_brani_scaricati, how='outer')
df_brani.to_csv("brani.csv")

for index, row in df_brani.iterrows():
    if bool(list(prolog.query(f"brano_ascoltato_freq(\"{row['track_id']}\")"))):
        df_brani.at[index, 'brano_ascoltato_freq'] = 1
    else: 
        df_brani.at[index,'brano_ascoltato_freq'] = 0
        
    if bool(list(prolog.query(f"artista_ascoltato_freq(\"{row['main_artist_id']}\")"))):
        df_brani.at[index,'artista_ascoltato_freq'] = 1
    else: 
        df_brani.at[index,'artista_ascoltato_freq'] = 0

    if bool(list(prolog.query(f"artista_singolare_importante(\"{row['main_artist_id']}\")"))):
        df_brani.at[index, 'artista_singolare_importante'] = 1
    else:
        df_brani.at[index, 'artista_singolare_importante'] = 0
        
    if bool(list(prolog.query(f"collaboratore_canzone(\"{row['track_id']}\", IdArtista), artista_ascoltato_freq(IdArtista)"))):
        df_brani.at[index, 'coll_artista_asc_freq'] = 1
    else:
        df_brani.at[index, 'coll_artista_asc_freq'] = 0
    
    if bool(list(prolog.query(f"simile_struttura_musicale(\"{row['track_id']}\", Canzone), brano_ascoltato_freq(Canzone)"))):
        df_brani.at[index, 'sim_struttura_musicale_brano_asc_freq'] = 1
    else: 
        df_brani.at[index, 'sim_struttura_musicale_brano_asc_freq'] = 0

    if bool(list(prolog.query(f"simili_emozioni(\"{row['track_id']}\", Canzone), brano_ascoltato_freq(Canzone)"))):
        df_brani.at[index, 'sim_emozioni_brano_asc_freq'] = 1
    else: 
        df_brani.at[index, 'sim_emozioni_brano_asc_freq'] = 0

    if bool(list(prolog.query(f"macro_categoria_artista(\"{row['main_artist_id']}\", Categoria), macro_categoria_artista(Artista, Categoria), artista_ascoltato_freq(Artista)"))):
        df_brani.at[index, 'macro_categoria_artista_asc_freq'] = 1
    else: 
        df_brani.at[index, 'macro_categoria_artista_asc_freq'] = 0
        
    if bool(list(prolog.query(f"genere_artista(\"{row['main_artist_id']}\", Genere), genere_ascoltato_freq(Genere, _)"))):
        df_brani.at[index, 'genere_asc_freq'] = 1
    else:
        df_brani.at[index, 'genere_asc_freq'] = 0
        
df_brani.to_csv("brani.csv")
        
# Temp
from sklearn.datasets import load_iris

iris = load_iris()
X = iris.data
y = iris.target 

# X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=4)

# Classificazione dataset con k-NN e valutazione modello
k_range = range(1, 13) # intervallo di valori per k
k_scores = []

for k in k_range: # calcolo modello con valori di k 
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, X, y, cv=5, scoring='accuracy')
    k_scores.append(scores.mean())

plt.plot(k_range, k_scores)
plt.xlabel('Valore di K per K-NN')
plt.ylabel('Cross-Validated accuratezza')
plt.show()

mean_training_accuracy_scores = []
mean_validation_accuracy_scores = []
# Classificazione dataset con Decision Tree Classifier e valutazione
for n in range(1, 16):
    decision_tree_model = DecisionTreeClassifier(max_depth=n
                                                 , criterion='entropy'
                                                 , min_samples_split=5
                                                 , random_state=0
                                                )
    
    results = cross_validation(decision_tree_model, X, y, 5)
    mean_training_accuracy_scores.append(results["Mean Training Accuracy"])
    mean_validation_accuracy_scores.append(results["Mean Validation Accuracy"])
    
    """
    plot_results("Decision Tree"
                , "Accuracy"
                , "Accuracy scores in 5 folds"
                , results["Training Accuracy scores"]
                , results["Validation Accuracy scores"]
                )
    """
plot_range_results("Profondità alberi", "Scores", "Decision Tree Classifier", mean_training_accuracy_scores, mean_validation_accuracy_scores, range(1, 16))

# Classificazione dataset con Random Forest Classifier e valutazione
mean_training_accuracy_scores = []
mean_validation_accuracy_scores = []
for n in range(1, 16):
    random_forest_model = RandomForestClassifier(max_depth=n
                                                 , criterion= 'entropy'
                                                 , min_samples_split=5
                                                 , random_state=0
                                                )

    results = cross_validation(random_forest_model, X, y, 5)
    mean_training_accuracy_scores.append(results["Mean Training Accuracy"])
    mean_validation_accuracy_scores.append(results["Mean Validation Accuracy"])

plot_range_results("Profondità alberi", "Scores", "Random Forest Classifier", mean_training_accuracy_scores, mean_validation_accuracy_scores, range(1, 16))
    
# Classificazione dataset con Gradient Boosting Classifier
mean_training_accuracy_scores = []
mean_validation_accuracy_scores = []
for n in range(1, 21):
    gradient_boosting_model = GradientBoostingClassifier(n_estimators=n
                                                         , learning_rate=0.5
                                                         , random_state=0
                                                         , max_features="log2"
                                                        )
    
    results = cross_validation(gradient_boosting_model, X, y, 5)
    mean_training_accuracy_scores.append(results["Mean Training Accuracy"])
    mean_validation_accuracy_scores.append(results["Mean Validation Accuracy"])
    
plot_range_results("Numero alberi", "Scores", "Gradient Boosting Classifier", mean_training_accuracy_scores, mean_validation_accuracy_scores, range(1, 21))

# Classificazione dataset con Regressione logica e valutazione
mean_training_accuracy_scores = []
mean_validation_accuracy_scores = []
C_values = [0.001, 0.01, 0.1, 1, 10, 100]
for C in C_values:
    logistic_regression = LogisticRegression(C=C, random_state=0)
    results = cross_validation(logistic_regression, X, y, 5)
    mean_training_accuracy_scores.append(results["Mean Training Accuracy"])
    mean_validation_accuracy_scores.append(results["Mean Validation Accuracy"])
    
plot_range_results("C", "Scores", "Logistic Regression Classifier", mean_training_accuracy_scores, mean_validation_accuracy_scores, C_values)

# Classificazione dataset con SVM e valutazione
C_range = np.logspace(-2, 10, 13)
gamma_range = np.logspace(-9, 3, 13)
param_grid = dict(gamma=gamma_range, C=C_range)
cv = StratifiedShuffleSplit(n_splits=5, test_size=0.4, random_state=42)
grid = GridSearchCV(SVC(), param_grid=param_grid, cv=cv)
grid.fit(X, y)

print("I parametri migliori sono %s con lo score di %0.2f" %(grid.best_params_, grid.best_score_))

# Classificazione dataset con MLPClassifier e valutazione
param_grid = {
    'hidden_layer_sizes': [(50,), (100,), (50, 50)],
    'activation': ['logistic', 'tanh', 'relu'],
    'solver': ['adam', 'sgd'],
    'alpha': [0.0001, 0.001, 0.01]
}

param_dist = {
    'hidden_layer_sizes': [(50,), (100,), (50, 50)],
    'activation': ['logistic', 'tanh', 'relu'],
    'solver': ['adam', 'sgd'],
    'alpha': uniform(0.0001, 0.01)
}

# Creazione del classificatore MLP
clf = MLPClassifier(max_iter=10000, random_state=42)

# Ricerca a griglia con cross-validation
grid_search = GridSearchCV(clf, param_grid, cv=5, n_jobs=-1)
grid_search.fit(X, y)

# Ricerca casuale con cross-validation
random_search = RandomizedSearchCV(clf, param_distributions=param_dist, n_iter=10, cv=5, n_jobs=-1, random_state=42)
random_search.fit(X, y)

# Parametri ottimali e risultati
best_params = grid_search.best_params_
best_score = grid_search.best_score_
print("Ricerca a griglia - Best Parameters:", best_params)
print("Ricerca a griglia - Best Cross-Validation Score:", best_score)

best_params = random_search.best_params_
best_score = random_search.best_score_
print("Ricerca Casuale - Best Parameters:", best_params)
print("Ricerca Casuale - Best Cross-Validation Score:", best_score)