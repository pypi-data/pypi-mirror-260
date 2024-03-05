from PIL import Image
from scipy.fftpack import fft2, ifft2
import numpy as np
import cv2
from skimage.morphology import binary_opening, binary_closing, disk

import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.color import rgb2gray
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from skimage import filters, img_as_float
from PIL import Image
import matplotlib.pylab as pylab

import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage.util import random_noise
from skimage import feature
import numpy as np

def allai():
    code=r"""
symptomCheckerES
AIBot
bayesTheorem
conditionalProb
familyTree
fuzzyOperations
simulateSupervised
simulateUnsupervised
clustering
svm
intelligentClothesAgent
simulateLanParser
feedforward"""
    print(code)
    
def symptomCheckerES():
    code=r"""
name = input("Enter your name: ")
fever = input("Do you have fever? (yes/no) ").lower()
cough = input("Do you have cough? (yes/no) ").lower()
sob = input("Do you have shortness of breath? (yes/no) ").lower()
st = input("Do you have sore throat? (yes/no) ").lower()
mp = input("Do you have muscle pain? (yes/no) ").lower()
hc = input("Do you have headache? (yes/no) ").lower()
diarrhea = input("Do you have diarrhea? (yes/no) ").lower()
conjuctivitis = input("Do you have conjuctivitis? (yes/no) ").lower()
lot = input("Do you have Loss of Taste? (yes/no) ").lower()
cp = input("Do you have Chest pain or Pressure? (yes/no) ").lower()
lsp = input("Do you have Loss of Speech or Movement? (yes/no) ").lower()

flu_symptoms = (fever=="yes" and cough=="yes" and sob=="yes" and st=="yes" and mp=="yes" and hc=="yes")
corona_symptoms = (diarrhea=="yes" and st=="yes" and fever=="yes" and cough=="yes" and conjuctivitis=="yes" and lot=="yes")
common_cold = (fever=="yes" and cough=="yes")

if flu_symptoms:
    print(name + " YOU HAVE FLU...")
    med = input("Aditi!, would you like to look at same medicine for the flu? (yes/no): ").lower()
    if med == "yes":
        print("Disclaimer: Contact a doctor for better guidance.")
        print("There are four FDA-approved antiviral drugs recommended by CDC to treat flu this season: ")
        print("1. Oseltamivir phosphate")
        print("2. Zanamivir")
        print("3. Peramivir")
        print("4. Baloxavir marboxil")
elif corona_symptoms:
    print(name + " YOU HAVE Corona")
    med = input("Aditi!, would you like to look at some remedies for Corona? (yes/no): ").lower()
    if med == "yes":
        print("TAKE VACCINE AND QUARANTINE")
elif common_cold:
    print(name + " YOU HAVE COMMON CODE")
    med = input("Aditi!, would you like to look at some remedies for Corona? (yes/no): ").lower()
    if med == "yes":
        print("Disclaimer: Contact a doctor for better guidance")
        print("Treatment consists of abti-inflammatories and decongestants. Most people d=recover on their own. ")
        print("1. Nonsteroidal abti-inflammatory drug")
        print("2. Analgesic")
        print("3. Antihistamine")
        print("4. Cough medicine")
        print("5. Decongestant")
else:
    print("Unable to identify")


Program: 2 Flu disease checker:
info=[]
name=input("Enter your name: ")
info.append(name)
age=int(input("Enter your age: "))
info.append(age)
print("----------------------------------------------")
a=["Fever", "Headache", "Tiredness", "Vomitting"]
b=["Urinate a lot", "Feels thirsty", "Weight loss", "Blurry vision", "Feels very hungry", "Feels very tired"]
print("----------------------------------------------")
print(a, b)
symp=input("Enter symptoms as above separated by comm ")
lst=symp.split(",")
print(info)
print("Symptoms: ")
for i in lst:
    print(i)
if i.strip() in a:
    print("You May Have Malaria\n...visit a Doctor")
elif i.strip() in b:
    print("You May Have Diabetes\n...Consume less Sugar")
else:
    print("Symptoms does not Match")


"""
    print(code)


def AIBot():
    code=r"""
Open cmd and install pip –
pip install aiml 
pip install python-aiml 

basic_chat.aiml
<aiml version="1.0.1" encoding="UTF-8">
<!-- basic_chat.aiml -->
 
    <category>
        <pattern>HELLO *</pattern>
        <template>
            Well, Hello PCS!
        </template>
    </category>
 
    <category>
        <pattern>WHAT ARE YOU</pattern>
        <template>
            I'm a bot, and I'm silly!
        </template>
    </category>
 
    <category>
        <pattern>WHAT DO YOU DO</pattern>
        <template>
            I'm here to motivate you!
        </template>
    </category>
 
    <category>
        <pattern>WHO AM I</pattern>
        <template>
            You are a Professional Footballer....
        </template>
    </category>
 
</aiml>
 
std-startup.xml
<aiml version="1.0.1" encoding="UTF-8">
<!--  std-startup.xml  -->
<!--  Category is an atomic AIML unit  -->
<category>
<!--  Pattern to match in user input  -->
<!--  If user enters "LOAD AIML B"  -->
<pattern>LOAD AIML B</pattern>
<!--  Template is the response to the pattern  -->
<!--  This learn an aiml file  -->
<template>
<learn>basic_chat.aiml</learn>
<!--  You can add more aiml files here  -->
<!-- <learn>more_aiml.aiml</learn> -->
</template>
</category>
</aiml>
 
AI_Prac2_Bot.py
import aiml
kernel=aiml.Kernel()
kernel.learn("std-startup.xml")
kernel.respond("load aiml b")
while True:
    input_text=input(">Human:")
    response=kernel.respond(input_text)
    print(">Bot: "+response)

"""
    print(code)


def bayesTheorem():
    code=r"""
Program: 1
def bayes_theorem(p_h, p_e_given_h, p_e_given_not_h):
    not_h= 1 - p_h
    p_e= p_e_given_h * p_h + p_e_given_not_h * not_h
    p_h_given_e= (p_e_given_h * p_h)/p_e
    return p_h_given_e
p_h=float(input("Enter probability of hk having cold P(H): "))
p_e_given_h=float(input("Enter probability of hk observed sneezing when he had cold P(E|H): "))
p_e_given_not_h=float(input("Enter probability of hk observed sneezing when he did not have cold P(E|~H): "))
result=bayes_theorem(p_h, p_e_given_h, p_e_given_not_h)
print("Hk probability of having cold given that he sneezes is P(H|E)= ", round(result, 2))

Program: 2
def bayes_theorem(p_h, p_e_given_h, p_e_given_not_h):
    not_h= 1 - p_h
    p_e= p_e_given_h * p_h + p_e_given_not_h * not_h
    p_h_given_e= (p_e_given_h * p_h)/p_e
    return p_h_given_e
p_h=float(input("Enter probability of hk having cold: "))
p_e_given_h=float(input("Enter probability of hk observed sneezing when he had cold: "))
p_e_given_not_h=float(input("Enter probability of hk observed sneezing when he did not have cold: "))
result=bayes_theorem(p_h, p_e_given_h, p_e_given_not_h)
print("Hk probability of having cold given that he sneezes is P(H|E)= ", round(result, 2))

Program: 3
def drug_user(prob_th=0.5, sensitivity=0.97, specificity=0.95, prevelance=0.005, verbose=True):
    p_user=prevelance
    p_non_user=1-prevelance
    p_pos_user=sensitivity
    p_neg_user=1-specificity
    p_pos_non_user=1-specificity
    num=p_pos_user*p_user
    den=p_pos_user*p_user+p_pos_non_user*p_non_user
    prob=num/den
    print("Probability of the test-taker being a drug user is ", round(prob, 1))
    if verbose:
        if prob > prob_th:
            print("The test-taker could be an user")
        else:
            print("The test-taker may not be an user")
        return prob
drug_user()
"""
    print(code)


def conditionalProb():
    code=r"""
def conditional_and_joint_probability(A, B, sample_space):
    prob_A_and_B = len(set(A) & set(B))/len(sample_space)
    prob_B = len(B)/len(sample_space)
    prob_A_given_B = prob_A_and_B/prob_B
    return prob_A_and_B, prob_A_given_B
sample_space = range(1, 11)
A = [2, 4, 6, 8, 10]
B = [1, 2, 3, 4, 5]
print("Set(A): ", A)
print("Set(B): ", B)
prob_A_and_B, prob_A_given_B = conditional_and_joint_probability(A, B, sample_space)
print("Joint probability P(A n B) = ", prob_A_and_B)
print("Conditional probability P(A | B) = ", prob_A_given_B)

"""
    print(code)


def familyTree():
    code=r"""
male(j1).    %brother
male(k).     %father
male(a).     %uncle
male(v).    %grandfather
male(s).		%greatgrandfather

female(a1).      %me
female(a2).     %sister
female(j2).     %cousin
female(sk).     %mother
female(aa).     %aunt
female(sv).     %grandmother 
female(ps).     %greatgrandmother 

parent(k,a1).
parent(sk,a1).
parent(k,a2).
parent(sk,a2).
parent(a,j1).
parent(aa,j1).

mother(X,Y):-parent(X,Y),female(X).
father(X,Y):-parent(X,Y), male(X).
sibling(X,Y):-parent(Z,X), parent(Z,Y), X \= Y.
grandparent(X,Y):-parent(X,Z),parent(Z,Y).
greatgrandparent(X,Y):-parent(X,Z),grandparent(Z,Y).
uncle(X,Y):- male(X), sibling(X,P), parent(P,Y).
aunt(X,Y):- female(X), sibling(X,P), parent(P,Y).
"""
    print(code)


def fuzzyOperations():
    code=r"""
Program: 1
A={"a":0.2, "b":0.3, "c":0.6, "d":0.6}
B={"a":0.9, "b":0.9, "c":0.4, "d":0.5}
print("The first fuzzy set: ", A)
print("The second fuzzy set: ", B)
#Union
result={}
for i in A:
    if(A[i]>B[i]):
        result[i]=A[i]
    else:
        result[i]=B[i]
print("\nUnion of sets A and B is(A U B): ", result)
#Intersection
result={}
for i in A:
    if(A[i]<B[i]):
        result[i]=A[i]
    else:
        result[i]=B[i]
print("\nIntersection of sets A and B is(A n B): ", result)
#Complement
result={}
for i in A:
    result[i]=round(1-A[i], 2)
print("\nComplement of set A is(A'): ", result)
for i in B:
    result[i]=round(1-B[i], 2)
print("Complement of set B is(B'): ", result)
#Difference
result={}
for i in A:
    result[i]=round(min(A[i], 1-B[i]), 2)
print("\nDifference of sets A and B is(A - B):", result)

Program: 2
#pip install fuzzywuzzy
 from fuzzywuzzy import fuzz
from fuzzywuzzy import process
 s1 = "I love GeeksforGeeks"
 s2 = "I am loving GeeksforGeeks"
 print("FuzzyWuzzy Ratio: ", fuzz.ratio(s1, s2))
print("FuzzyWuzzy PartialRatio: ", fuzz.partial_ratio(s1, s2))
print("FuzzyWuzzy TokenSortRatio: ", fuzz.token_sort_ratio(s1, s2))
print("FuzzyWuzzy TokenSetRatio: ", fuzz.token_set_ratio(s1, s2))
print("FuzzyWuzzy Weighted Ratio: ", fuzz.WRatio(s1, s2),'\n\n')
# for process library,
query = 'geeks for geeks'
choices = ['geek for geek', 'geek geek', 'g. for geeks']
print("List of ratios: ")
print(process.extract(query, choices), '\n')
print("Best among the above list: ",process.extractOne(query, choices))
"""
    print(code)


def simulateSupervised():
    code=r"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

#Generate random data
np.random.seed(0)
x=2*np.random.rand(100,1)
y=4+3*x+np.random.rand(100,1)

#split data into train and test data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

#Instantiate linear model
model = LinearRegression()

#Train the model
model.fit(x_train, y_train)

#Make predictions
predictions=model.predict(x_test)

#Plot training data
plt.scatter(x_train, y_train, color='blue', label='Training data')
plt.scatter(x_test, y_test, color='red', label='Testing data')
plt.plot(x_test, predictions, color='green', linewidth=3, label='Predictions')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Linear regression')
plt.legend()
plt.show()
"""
    print(code)


def simulateUnsupervised():
    code=r"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
np.random.seed(0)
x=np.random.randn(100, 2)
plt.scatter(x[:, 0], x[:, 1], s=50)
plt.title("Randomly generated data points")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.show()

#Applying k-means clustering
kmeans=KMeans(n_clusters=3)
kmeans.fit(x)

#Getting centroids
centroids=kmeans.cluster_centers_
labels=kmeans.labels_

#Visualizing clustered data points
plt.scatter(x[:,0], x[:,1], s=50, cmap='viridis')
plt.scatter(centroids[:,0], centroids[:,1], marker='*', c='red', s=200, label='Centroids')
plt.title("K-means clustering")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.legend()
plt.show()
"""
    print(code)

def clustering():
    code=r"""
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
import scipy.cluster.hierarchy as shc

# Load customer data
customer_data = pd.read_csv("Mall_Customers.csv")

# Extract relevant features
data = customer_data[['Annual Income (k$)', 'Spending Score (1-100)']].values

# Perform hierarchical clustering
cluster = AgglomerativeClustering(n_clusters=5)
cluster_labels = cluster.fit_predict(data)

# Plot dendrogram
plt.figure(figsize=(10, 7))
plt.title("Customer Dendrogram")
shc.dendrogram(shc.linkage(data, method='ward'))

# Plot clustered data
plt.figure(figsize=(10, 7))
plt.scatter(data[:, 0], data[:, 1], c=cluster_labels, cmap='rainbow')
plt.show()
"""
    print(code)

def svm():
    code=r"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC, SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load Titanic dataset
titanic = pd.read_csv('train.csv')

# Preprocessing
titanic.drop(['Name', 'Ticket'], axis=1, inplace=True)
titanic['Cabin'].fillna(titanic['Cabin'].value_counts().idxmax(), inplace=True)
titanic['Embarked'].fillna(titanic['Embarked'].value_counts().idxmax(), inplace=True)
titanic['Age'].fillna(titanic['Age'].mean(), inplace=True)
titanic_cat = titanic.select_dtypes(object).apply(LabelEncoder().fit_transform)
titanic_num = titanic.select_dtypes(np.number).drop('PassengerId', axis=1)
titanic_final = pd.concat([titanic_cat, titanic_num], axis=1)

# Train-test split
X = titanic_final.drop('Survived', axis=1)
Y = titanic_final['Survived']
split_idx = int(0.80 * len(X))
X_train, Y_train = X[:split_idx], Y[:split_idx]
X_test, Y_test = X[split_idx:], Y[split_idx:]

# Model training and evaluation
models = [LogisticRegression(), KNeighborsClassifier(), GaussianNB(), LinearSVC(), SVC(kernel='rbf'),
          DecisionTreeClassifier(), RandomForestClassifier()]
for model in models:
    model_fit = model.fit(X_train, Y_train)
    Y_pred = model_fit.predict(X_test)
    accuracy = accuracy_score(Y_pred, Y_test) * 100
    print(f"{model.__class__.__name__} is {accuracy:.2f}% accurate")
"""
    print(code)


def intelligentClothesAgent():
    code=r"""
class ClothesAgent:
    def __init__(self):
        self.weather = None
    
    def get_weather(self):
        self.weather = input("Enter the weather (Sunny, Rainy, Windy, Snowy): ").lower()
    
    def suggest_clothes(self):
        suggestions = {
            "sunny": "light clothes, sunglasses, and sunscreen",
            "rainy": "an umbrella, raincoat, and waterproof shoes",
            "windy": "layers and a jacket",
            "snowy": "a heavy coat, gloves, and boots"
        }
        if self.weather in suggestions:
            print(f"It is {self.weather} outside. You should wear {suggestions[self.weather]}.")
        else:
            print("Sorry, I don't understand the weather conditions. Please enter sunny, rainy, windy, or snowy.")

def main():
    agent = ClothesAgent()
    agent.get_weather()
    agent.suggest_clothes()

if __name__ == "__main__":
    main()
"""
    print(code)



def simulateLanParser():
    code=r"""
import string
def sentence_segment(text):
    return [sentence.strip() for sentence in text.split('.') + text.split('!') + text.split('?') if sentence.strip()]

def remove_punctuation(input_string):
    return ''.join(char for char in input_string if char not in string.punctuation)

def convert_to_lower(s):
    return s.lower()

def tokenize(s):
    return s.split()

text = "Hello, NLP world!! In this example, we are going to do the basics of Text processing which will be used later."

sentences = sentence_segment(text)
punc_removed_text = remove_punctuation(text)
lower_text = convert_to_lower(punc_removed_text)
tokenized_text = tokenize(lower_text)

print(sentences)
print("\n")
print(tokenized_text)
print("\n")

# Tokenization using str.split()
tokens_split = text.split()
print(tokens_split)
print("\n")

sentence = "We're going to John's house today."
tokens_sentence = sentence.split()
print(tokens_sentence)
"""
    print(code)


def feedforward():
    code=r"""
import numpy as np
def relu(n):
    if n<0:
        return 0
    else:
        return n
inp=np.array([[-1,2],[2,2],[3,3]])
weights=[np.array([3,3]),np.array([1,5]),np.array([3,3]),np.array([1,5]),np.array([2,-1])]
for x in inp :
    node0=relu((x*weights[0]).sum())
    node1=relu((x*weights[1]).sum())
    node2=relu(([node0,node1]*weights[2]).sum())
    node3=relu(([node0,node1]*weights[3]).sum())
    op=relu(([node2,node3]*weights[4]).sum())
    print(x,op)
"""
    print(code)

def allml():
    code=r"""
TrainingInstances
EnjoySportsOrNotFindSAlgo
MultiClassUsingIris
MultiClassUsingWine
CandidateElimination
NaiveAndGaussianClassifier
decision
random
pca
linearreg
logisticreg
euclidean
classificationusingk
backpropagate
textprocessing
"""
    print(code)

def TrainingInstances():
    code=r"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

np.random.seed(2)

x = np.random.normal(3, 1, 100)
y = np.random.normal(150, 40, 100) / x

plt.scatter(x, y)
plt.show()

train_x = x[:80]
train_y = y[:80]
test_x = x[80:]
test_y = y[80:]

plt.scatter(train_x, train_y)
plt.show()

train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.3)

# Draw polynomial Regression line through the data points with training data
degree = 4
mymodel_train = np.poly1d(np.polyfit(train_x, train_y, degree))
myline_train = np.linspace(0, 6, 100)

plt.scatter(train_x, train_y)
plt.plot(myline_train, mymodel_train(myline_train))
plt.show()

# Draw polynomial Regression line through the data points with test data
mymodel_test = np.poly1d(np.polyfit(test_x, test_y, degree))
myline_test = np.linspace(0, 6, 100)

plt.scatter(test_x, test_y)
plt.plot(myline_test, mymodel_test(myline_test))
plt.show()

# Measures the relationship between x and y axis for training data
r2_train = r2_score(train_y, mymodel_train(train_x))
print("R2 Score (Training Data):", r2_train)

# Measures the relationship between x and y axis for test data
r2_test = r2_score(test_y, mymodel_test(test_x))
print("R2 Score (Test Data):", r2_test)

# Predict the values
prediction = mymodel_test(5)
print("Prediction for x=5:", prediction)

"""
    print(code)


def EnjoySportsOrNotFindSAlgo():
    code=r"""
import csv
num_attributes=6
a=[]
print("\n Given dataset: \n")
with
open(r'C:\Users\admin\Downloads\EnjoySportOrNot\EnjoySportOrNot.csv', 'r')
as csvfile:
 reader=csv.reader(csvfile)
 count=0
 for row in reader:
 if count==0:
 print(row)
 count+=1
 else:
 a.append(row)
 print(row)
 count+=1
print("\n The initial value of hypothesis: ")
hyp=["0"]*num_attributes
print(hyp)
for j in range(0, num_attributes):
 hyp[j]=a[0][j]
 print(hyp)
print("\n Find S: finding a maximally specific hypothesis \n")
for i in range(0, len(a)):
 if a[i][num_attributes]=='Yes':
 for j in range(0, num_attributes):
 if a[i][j]!=hyp[j]:
 hyp[j]='?'
 else:
 hyp[j]=a[i][j]
 print(" For training example no: {0} the hypothesis is ".format(i), hyp)
print(hyp)

"""
    print(code)


def MultiClassUsingIris():
    code=r"""
from sklearn import svm, datasets
import sklearn.model_selection as model_selection
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
iris = datasets.load_iris()
X = iris.data[:, :2]
y = iris.target
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, train_size=0.80,
test_size=0.20, random_state=101)
rbf = svm.SVC(kernel='rbf', gamma=0.5, C=0.1).fit(X_train, y_train)
poly = svm.SVC(kernel='poly', degree=3, C=1).fit(X_train, y_train)
poly_pred = poly.predict(X_test)
rbf_pred = rbf.predict(X_test)
poly_accuracy = accuracy_score(y_test, poly_pred)
poly_f1 = f1_score(y_test, poly_pred, average='weighted')
print('Accuracy (Polynomial Kernel): ', "%.2f" % (poly_accuracy*100))
print('F1 (Polynomial Kernel): ', "%.2f" % (poly_f1*100))
rbf_accuracy = accuracy_score(y_test, rbf_pred)
rbf_f1 = f1_score(y_test, rbf_pred, average='weighted')
print('Accuracy (RBF Kernel): ', "%.2f" % (rbf_accuracy*100))
print('F1 (RBF Kernel): ', "%.2f" % (rbf_f1*100))

"""
    print(code)


def MultiClassUsingWine():
    code=r"""
from sklearn import svm, datasets
import sklearn.model_selection as model_selection
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
wine = datasets.load_wine()
X = wine.data[:, :2]
y = wine.target
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, train_size=0.80,
test_size=0.20, random_state=101)
rbf = svm.SVC(kernel='rbf', gamma=0.5, C=0.1).fit(X_train, y_train)
poly = svm.SVC(kernel='poly', degree=3, C=1).fit(X_train, y_train)
poly_pred = poly.predict(X_test)
rbf_pred = rbf.predict(X_test)
poly_accuracy = accuracy_score(y_test, poly_pred)
poly_f1 = f1_score(y_test, poly_pred, average='weighted')
print('Accuracy (Polynomial Kernel): ', "%.2f" % (poly_accuracy*100))
print('F1 (Polynomial Kernel): ', "%.2f" % (poly_f1*100))
rbf_accuracy = accuracy_score(y_test, rbf_pred)
rbf_f1 = f1_score(y_test, rbf_pred, average='weighted')
print('Accuracy (RBF Kernel): ', "%.2f" % (rbf_accuracy*100))
print('F1 (RBF Kernel): ', "%.2f" % (rbf_f1*100))

"""
    print(code)


def CandidateElimination():
    code=r"""
import numpy as np
import pandas as pd

#Loading data from a csv file.
data = pd.DataFrame(data=pd.read_csv('enjoysport.csv'))
print(data)
#Separating concept features from Target
concepts = np.array(data.iloc[:,0:6])
print(concepts)
#Isolating target into a separate DataFrame
#Copying last column to target  array
target = np.array(data.iloc[:,6])
print(target)
def learn(concepts, target): 
#Initialise S0 with the first instance from concepts.
#.copy()makes sure a new list is created instead of just pointing to the same memory location.
    specific_h = concepts[0].copy()
    print("\nInitialization of specific_h and genearal_h")
    print("\nSpecific Boundary: ", specific_h)
    general_h = [["?" for i in range(len(specific_h))] for i in range(len(specific_h))]
    print("\nGeneric Boundary: ",general_h)
# The learning iterations.
    for i, h in enumerate(concepts):
        print("\nInstance", i+1 , "is ", h)
# Checking if the hypothesis has a positive target.
        if target[i] == "yes":
            print("Instance is Positive ")
            for x in range(len(specific_h)): 
# Change values in S & G only if values change.
                if h[x]!= specific_h[x]:                    
                    specific_h[x] ='?'                     
                    general_h[x][x] ='?'
# Checking if the hypothesis has a positive target.                  
        if target[i] == "no":            
            print("Instance is Negative ")
            for x in range(len(specific_h)): 
# For negative hypothesis change values only in G.
                if h[x]!= specific_h[x]:                    
                    general_h[x][x] = specific_h[x]                
                else:                    
                    general_h[x][x] = '?'        
        print("Specific Bundary after ", i+1, "Instance is ", specific_h)         
        print("Generic Boundary after ", i+1, "Instance is ", general_h)
# find indices where we have empty rows, meaning those that are unchanged.
    indices = [i for i, val in enumerate(general_h) if val == ['?', '?', '?', '?', '?', '?']]    
    for i in indices:   
# remove those rows from general_h
        general_h.remove(['?', '?', '?', '?', '?', '?']) 
# Return final values
    return specific_h, general_h 
s_final, g_final = learn(concepts, target)
print("Final Specific_h: ", s_final, sep="\n")
print("Final General_h: ", g_final, sep="\n")

"""
    print(code)


def NaiveAndGaussianClassifier():
    code=r"""
import pandas as pd
from sklearn import tree
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

data = pd.read_csv('PlayTennis.csv')
print("The first 5 values of data are: \n", data.head())
x = data.iloc[:, :-1].copy()  # Make a copy of the DataFrame
print("\nThe First 5 values of train data are: \n", x.head())
y = data.iloc[:, -1]
print("\nThe first 5 values of Train output are: \n", y.head())

le_outlook = LabelEncoder()
x['Outlook'] = le_outlook.fit_transform(x['Outlook'])
le_Temperature = LabelEncoder()
x['Temperature'] = le_Temperature.fit_transform(x['Temperature'])
le_Humidity = LabelEncoder()
x['Humidity'] = le_Humidity.fit_transform(x['Humidity'])
le_Wind = LabelEncoder()
x['Wind'] = le_Wind.fit_transform(x['Wind'])

print("\nNow the Train data is : \n", x.head())

le_PlayTennis = LabelEncoder()
y = le_PlayTennis.fit_transform(y)
print("\nNow the Train output is: \n", y)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20)
classifier = GaussianNB()
classifier.fit(x_train, y_train)

print("Accuracy is: ", accuracy_score(classifier.predict(x_test), y_test))

"""
    print(code)

def decision():
    code=r"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
#%matplotlib inline
df = pd.read_csv(r"WA_Fn-UseC_-HR-Employee-Attrition.csv")
df.head()
# Exploratory Data Analysis
sns.countplot(x='Attrition', data=df)
plt.show()
from pandas.core.arrays import categorical
df.drop(['EmployeeCount','EmployeeNumber', 'Over18', 'StandardHours'], axis="columns",
inplace=True)
categorical_col = []
for column in df.columns:
 if df[column].dtype == object:
     categorical_col.append(column)
df['Attrition'] = df.Attrition.astype("category").cat.codes
from sklearn.preprocessing import LabelEncoder
for column in categorical_col:
 df[column] = LabelEncoder().fit_transform(df[column])
from sklearn.model_selection import train_test_split
X = df.drop('Attrition', axis=1)
y = df.Attrition
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
def print_score(clf, X_train, y_train, X_test, y_test, train=True):
 if train:
     pred = clf.predict(X_train)
     clf_report = pd.DataFrame(classification_report(y_train, pred, output_dict=True))
     print("Train Result:\n=======================================")
     print(f"Accuracy Score: {accuracy_score(y_train, pred) * 100:.2f}%")
     print(" ")
     print(f"CLASSIFICATION REPORT:\n{clf_report}")
     print(" ")
     print(f"Confusion Matrix: \n{confusion_matrix(y_train, pred)}\n")
 elif train==False:
     pred = clf.predict(X_test)
     clf_report = pd.DataFrame(classification_report(y_test, pred, output_dict=True))
     print("Test Result:\n=======================================")
     print(f"Accuracy Score: {accuracy_score(y_test, pred) * 100:.2f}%")
     print(" ")
     print(f"CLASSIFICATION REPORT:\n{clf_report}")
     print(" ")
     print(f"Confusion Matrix: \n{confusion_matrix(y_test, pred)}\n")
from sklearn.tree import DecisionTreeClassifier
from pickle import TRUE
from sklearn.tree import DecisionTreeClassifier
tree_clf = DecisionTreeClassifier(random_state=42)
tree_clf.fit(X_train, y_train)
print_score(tree_clf, X_train, y_train, X_test, y_test, train=True)
print_score(tree_clf, X_train, y_train, X_test, y_test, train=False)
from sklearn.ensemble import RandomForestClassifier
rf_clf = RandomForestClassifier(random_state=42)
rf_clf.fit(X_train, y_train)
print_score(rf_clf, X_train, y_train, X_test, y_test, train=True)
print_score(rf_clf, X_train, y_train, X_test, y_test, train=False)
"""
    print(code)

def random():
    code=r"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Define the print_score function
def print_score(clf, X_train, y_train, X_test, y_test, train=True):
    if train:
        pred = clf.predict(X_train)
        clf_report = pd.DataFrame(classification_report(y_train, pred, output_dict=True))
        print("Train Result:\n=======================================")
        print(f"Accuracy Score: {accuracy_score(y_train, pred) * 100:.2f}%")
        print(" ")
        print(f"CLASSIFICATION REPORT:\n{clf_report}")
        print(" ")
        print(f"Confusion Matrix: \n{confusion_matrix(y_train, pred)}\n")
    else:
        pred = clf.predict(X_test)
        clf_report = pd.DataFrame(classification_report(y_test, pred, output_dict=True))
        print("Test Result:\n=======================================")
        print(f"Accuracy Score: {accuracy_score(y_test, pred) * 100:.2f}%")
        print(" ")
        print(f"CLASSIFICATION REPORT:\n{clf_report}")
        print(" ")
        print(f"Confusion Matrix: \n{confusion_matrix(y_test, pred)}\n")

# Load the dataset
df = pd.read_csv(r"WA_Fn-UseC_-HR-Employee-Attrition.csv")

# EDA
sns.countplot(x='Attrition', data=df)
plt.show()

# Drop unnecessary columns
df.drop(['EmployeeCount', 'EmployeeNumber', 'Over18', 'StandardHours'], axis="columns", inplace=True)

# Convert categorical columns to numerical
categorical_col = [col for col in df.columns if df[col].dtype == object]
df['Attrition'] = df['Attrition'].astype("category").cat.codes

for column in categorical_col:
    df[column] = LabelEncoder().fit_transform(df[column])

# Split the data
X = df.drop('Attrition', axis=1)
y = df['Attrition']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Create a RandomForestClassifier
classifier = RandomForestClassifier()
classifier.fit(X_train, y_train)

# Call print_score function for both training and testing
print_score(classifier, X_train, y_train, X_test, y_test, train=True)
print_score(classifier, X_train, y_train, X_test, y_test, train=False)
"""
    print(code)

def pca():
    code=r"""
import numpy as np
import pandas as pd
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'Class']
dataset = pd.read_csv(url, names=names)
dataset.head()
x = dataset.drop('Class',1)
y = dataset['Class']
y.head()
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
x_train1 = sc.fit_transform(x_train)
x_test1 = sc.transform(x_test)
y_train1 = y_train
y_test1 = y_test
from sklearn.decomposition import PCA
pca = PCA()
x_train1 = pca.fit_transform(x_train1)
x_test1 = pca.transform(x_test1)
explained_variance = pca.explained_variance_ratio_
print ("Explained variance: ", explained_variance)
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(max_depth=2, random_state=0)
classifier.fit(x_train1,y_train1)
y_pred = classifier.predict(x_test1)
#Confusion matrix
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
cm = confusion_matrix(y_test, y_pred)
print(cm)
print('Accuracy', accuracy_score(y_test1, y_pred))
"""
    print(code)


def linearreg():
    code="""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (12.0, 9.0)
# Preprocessing Input data
data = pd.read_csv(r"C:\\Users\\Aditi\\OneDrive\\Documents\\Python Scripts\\data.csv")
X = data.iloc[:, 0]
Y = data.iloc[:, 1]
plt.scatter(X, Y)
plt.show()
# Building the model
X_mean = np.mean(X)
Y_mean = np.mean(Y)
num = 0
den = 0
for i in range(len(X)):
    num += (X[i] - X_mean)*(Y[i] - Y_mean)
    den += (X[i] - X_mean)**2
m = num / den
c = Y_mean - m*X_mean
# Making predictions
Y_pred = m*X + c
plt.scatter(X, Y) 
plt.plot([min(X), max(X)], [min(Y_pred), max(Y_pred)], color='red') # predicted
plt.show()
"""
    print(code)

def logisticreg():
    code=r"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
dataset = pd.read_csv(r"C:\Users\Aditi\OneDrive\Documents\Python Scripts\DMVWrittenTests.csv")
X = dataset.iloc[:, [0, 1]].values
y = dataset.iloc[:, 2].values
dataset.head(5)
# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)
# Feature Scaling is used to normalize the data within a particular range. It also aids in speeding up the calculations.
# As the data is widely varying, we use this function to limit the range of the data within a small limit ( -2,2).
#For example, the score 62.0730638 is normalized to -0.21231162 and the score 96.51142588 is normalized to 1.55187648. In this way, the scores of X_train and X_test are normalized to a smaller range.
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
# Training the Logistic Regression model on the Training Set
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression()
classifier.fit(X_train, y_train)
#predicting the test set results
y_pred = classifier.predict(X_test)
y_pred
#confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
from sklearn.metrics import accuracy_score
print("Accuracy Score of Logistic Regression: ", accuracy_score(y_test,y_pred),"\n")
print("Confusion Matrix: \n",cm)
"""
    print(code)

def euclidean():
    code=r"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
df = pd.read_csv(r"C:\Users\Aditi\OneDrive\Documents\Python Scripts\iris.csv")
df.head(5)
X = df.drop(['variety'], axis=1)
y = df['variety']
X_train, X_test, y_train , y_test = train_test_split(X, y, test_size=0.3, random_state=0)
knn = KNeighborsClassifier(n_neighbors= 6, p = 2, metric='minkowski')
knn.fit(X_train, y_train)
print(knn.score(X_test,y_test))
y_pred = knn.predict(X_test)
from sklearn.metrics import confusion_matrix
cm=np.array(confusion_matrix(y_test,y_pred))
print(cm)
knn = KNeighborsClassifier(n_neighbors= 6, p = 1, metric='minkowski')
knn.fit(X_train, y_train)
print(knn.score(X_test,y_test))
from sklearn.metrics import confusion_matrix
cm=np.array(confusion_matrix(y_test,y_pred))
print(cm)
"""
    print(code)

def classficationusingk():
    code="""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sklearn
dataset = pd.read_csv(r"C:\Users\Aditi\OneDrive\Documents\Python Scripts\Mall_Customers.csv")
X = dataset.iloc[:, [3,4]].values
from sklearn.cluster import KMeans
wcss=[]
for i in range(1,11):
 kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
 kmeans.fit(X)
 wcss.append(kmeans.inertia_)
plt.plot(range(1,11), wcss)
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()
kmeans = KMeans(n_clusters= 5, init= "k-means++", random_state=42)
y_kmeans = kmeans.fit_predict(X)
plt.scatter(X[y_kmeans == 0,0], X[y_kmeans == 0,1], s = 60, c='red', label = 'Cluster1')
plt.scatter(X[y_kmeans == 1,0], X[y_kmeans == 1,1], s = 60, c='blue', label = 'Cluster2')
plt.scatter(X[y_kmeans == 2,0], X[y_kmeans == 2,1], s = 60, c='green', label = 'Cluster3')
plt.scatter(X[y_kmeans == 3,0], X[y_kmeans == 3,1], s = 60, c='violet', label = 'Cluster4')
plt.scatter(X[y_kmeans == 4,0], X[y_kmeans == 4,1], s = 60, c='yellow', label = 'Cluster5')
plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], s=100, c='black', label = 'Centroids')
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score (1-100)')
plt.legend()
plt.show()
plt.scatter(X[y_kmeans == 0,0], X[y_kmeans== 0,1], s=100, c='red', label = 'Careful')
plt.scatter(X[y_kmeans == 1,0], X[y_kmeans== 1,1], s=100, c='blue', label = 'Standard')
plt.scatter(X[y_kmeans == 2,0], X[y_kmeans== 2,1], s=100, c='green', label = 'Target')
plt.scatter(X[y_kmeans == 3,0], X[y_kmeans== 3,1], s=100, c='violet', label = 'Careless')
plt.scatter(X[y_kmeans == 4,0], X[y_kmeans== 4,1], s=100, c='yellow', label = 'Sensible')
plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], s=100, c='black', label = 'Centroids')
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score (1-100)')
plt.title('Cluster of Customers')
plt.legend()
plt.show()
"""
    print(code)

def backpropagate():
    code=r"""import numpy as np
X=np.array(([2,9],[1,5],[3,6]),dtype=float)
Y=np.array(([92],[86],[89]),dtype=float)
X=X/np.amax(X,axis=0)
Y=Y/100;

class NN(object):
    def __init__(self):
        self.inputsize=2
        self.outputsize=1
        self.hiddensize=3
        self.W1=np.random.randn(self.inputsize,self.hiddensize)
        self.W2=np.random.randn(self.hiddensize,self.outputsize)
    def forward(self,X):
        self.z=np.dot(X,self.W1)
        self.z2=self.sigmoidal(self.z)
        self.z3=np.dot(self.z2,self.W2)
        op=self.sigmoidal(self.z3)
        return op;
    def sigmoidal(self,s):
        return 1/(1+np.exp(-s))
    def sigmoidalprime(self,s):
        return s* (1-s)
    def backward(self,X,Y,o):
        self.o_error=Y-o
        self.o_delta=self.o_error * self.sigmoidalprime(o)
        self.z2_error=self.o_delta.dot(self.W2.T)
        self.z2_delta=self.z2_error * self.sigmoidalprime(self.z2)
        self.W1 = self.W1 + X.T.dot(self.z2_delta)
        self.W2= self.W2+ self.z2.T.dot(self.o_delta)
    def train(self,X,Y):
        o=self.forward(X)
        self.backward(X,Y,o)
obj=NN()
for i in range(4):
    print("input"+str(X))
    print("Actual output"+str(Y))
    print("Predicted output"+str(obj.forward(X)))
    print("loss"+str(np.mean(np.square(Y-obj.forward(X)))))
    obj.train(X,Y)
"""
    print(code)

def textprocessing():
    code=r"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.read_csv('Restaurant_Reviews.tsv', delimiter = '\t', quoting = 3)

import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
corpus = []

for i in range(0,1000):
  review = re.sub('[^a-zA-Z]','',dataset['Review'][i])
  review = review.lower()
  review = review.split()
  ps = PorterStemmer()
  review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
  review = ''.join(review)
  corpus.append(review)


#Creating the bag of words model
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=1500)
X = cv.fit_transform(corpus).toarray()
Y = dataset.iloc[:,1].values

#Splitting the dataset into the training set and test set
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.25, random_state=100)


#Fitting naive bayes to the training set.
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, Y_train)


# Predicting the test set results.
Y_pred = classifier.predict(X_test)

#Model Accuracy
from sklearn import metrics
from sklearn.metrics import confusion_matrix
print("Accuracy:",metrics.accuracy_score(Y_test, Y_pred))


#Making the confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(Y_test, Y_pred)
print(cm)
"""
    print(code)
    
