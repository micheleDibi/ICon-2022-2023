import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Modelli
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

# Valutazione
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_validate

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


