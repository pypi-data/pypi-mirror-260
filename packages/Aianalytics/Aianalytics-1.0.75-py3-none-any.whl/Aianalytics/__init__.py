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
