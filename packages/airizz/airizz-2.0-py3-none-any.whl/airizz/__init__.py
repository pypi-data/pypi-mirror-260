def index():
    print(""" 

1a)Design an Expert system using AIML (Malaria, Diabetes)
1b) An expert system for responding the patient query for identifying the flu.
          
2) Design a bot using AIML.
          
3a) Implement Bayes Theorem using Python.
    ((P(H|E) probability of Mike having a cold given that he sneezes )
3b) Implement Bayes Theorem using Python.
    (Drug user sensitivity specificity prevelance )
                
4a)	Write an application to implement BFS algorithm.
4a)	Write an application to implement DFS algorithm.
          
5) Write a program to implement Rule Based System
          
6a) Design Fuzzy based operations using Python / R. 
    (Union intersection complement difference) 
6b) Design Fuzzy based operations using Python / R. 
    (fuzzywuzzy Ratio PartialRatio TokenSortRatio TokenSetRatio WRatio)
          
7a) Implement  Conditional Probability using Python.
7b) Implement  Joint probability using Python.
          
8) Write an application to implement clustering algorithm. 
          
9a) Write an application to simulate supervised learning model.
9b) Write an application to simulate un-supervised learning model.
          
10) Design an Artificial Intelligence application to implement intelligent agents. 
          
11) Design an application to simulate language parser.

""")
    

def prog(num):
    if num =="1a":
        print(""" 
pract 1a


Info = []
Name = input("Enter Your Name: ")
Info.append(Name)
Age = int(input("Enter Your Age: "))
Info.append(Age)
A = ["Fever", "Headache", "Tiredness", "Vomitting"]
B = ["Urinate A Lot", "Feels Thirsty", "Weight Loss", "Blurry Vision", "Feels Very Hungry", "Feels Very Tired"]
print(A,B)
Symp = input("Enter Symptoms As Above Separated By Comma ")
Lst = Symp.split(",")
print(Info)
print("Symptoms:")
for i in Lst:
    print(i) 
 
if i.strip() in A:
    print("You May Have Malaria")
    print("Visit A Doctor")
elif i.strip() in B:
    print("You May Have Diabetes")
    print("Consume Less Sugar")
else:
    print("Symptoms Does Not Match")


""")
    
    elif num =="1b":
        print(""" 
pract 1b

name =input("Enter your name: ")
fever =input("DO YOU HAVE fever (Y/N)").lower()
cough =input("DO YOU HAVE cough (Y/N)").lower()
sob =input("DO YOU HAVE shortness of breath (Y/N)").lower()
st =input("DO YOU HAVE sore throat (Y/N)").lower()
mp =input("DO YOU HAVE mucle pain (Y/N)").lower()
hc =input("DO YOU HAVE headach(Y/N)").lower()
 
#CORONA
diarrhoea=input("DO YOU HAVE diarrhoea (Y/N)").lower()
conjunctivitis=input("DO YOU HAVE conjunctivitis (Y/N)").lower()
lot=input("DO YOU HAVE Loss OF taste (Y/N)").lower()
cp=input("DO YOU HAVE chest pain or pressure (Y/N)").lower()
lsp =input("DO YOU HAVE Loss Of Speech or movement (Y/N)").lower()

if fever=="y" and cough=="y" and sob=="y" and st=="y" and mp=="y" and hc=="y":
    print(name+" "+" YOU HAVE FLU")
    med=input("Sir/Ma'am would you like to took at some medicine for flu(Y/N)").lower()
    if med=="y":
        print("disclainer contact doctor for better guidance")
        print("There are four FDA-approved antiviral drugs recommended by CDC to treat flu this season")
        print("1.Oseltasivir phosphate")
        print("2.zonasivir ")
        print("3.perasivir ")
        print("4.balaxavir morboxil ")
elif diarrhoea=="y" and st=="y" and fever =="y" and cough=="y" and conjunctivitis=="y" and lot=="y":
    print(name+" "+" YOU HAVE Corona")
    med=input("Sir/Ma'am would you like to took at some remedi for Corona(Y/N)").lower()
    if med=="y":
        print("TAKE VACCINE AND QUARANTINE")       
elif fever=="y" and cough=="y":
    print(name+" "+" YOU HAVE Common Cold")
    med= input("Sir/Ma'am would you like to look at some remedi for common cold(Y/N)").lower()
    if med=="y":
        print("--------------------------------------------------------------------")
        print("disclainer contact doctor for better guidance")
        print("--------------------------------------------------------------------")
        print("Treatment consists of anti-inflammatories and decongestants\n Most prople recover on their own")
        print("1.Nonsteroidal anti-inflammatory drug, Analgesic, Antibistamine, Cough medicine and Deconges")
     
else:
    print("Unable to identify")

""")
    
    elif num =="2":
        print(""" 
pract 2

----- Open cmd and install pip –----
pip install aiml 
pip install python-aiml 
 
--------- main.py ---------
import aiml

kernel = aiml.Kernel()
kernel.learn("std-startup.xml")
kernel.respond("load aiml b")

while True:
    input_text = input(">Human: ")
    response = kernel.respond(input_text)
    print(">Bot: "+response)



--------- std-startup.xml ------------
<aiml version="1.0.1" encoding="UTF-8">
    <!-- std-startup.xml -->

    <!-- Category is an atomic AIML unit -->
    <category>

        <!-- Pattern to match in user input -->
        <!-- If user enters "LOAD AIML B" -->
        <pattern>LOAD AIML B</pattern>

        <!-- Template is the response to the pattern -->
        <!-- This learn an aiml file -->
        <template>
            <learn>basic_chat.aiml</learn>
            <!-- You can add more aiml files here -->
            <!--<learn>more_aiml.aiml</learn>-->
        </template>
        
    </category>

</aiml>




---------- basic_chat.aiml -------------
<aiml version="1.0.1" encoding="UTF-8">
<!-- basic_chat.aiml -->

    <category>
        <pattern>HELLO *</pattern>
        <template>
            Well, Hello ABC!
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


""")
    
    elif num =="3a":
        print(""" 
              
def bayes_theorem(p_h, p_e_given_h, p_e_given_not_h):
    # Calculate P(not H)
    p_not_h = 1 - p_h

    # Calculate P(E)
    p_e = (p_e_given_h * p_h) + (p_e_given_not_h * p_not_h)

    # Calculate P(H|E)
    p_h_given_e = (p_e_given_h * p_h) / p_e

    return p_h_given_e

# Input probabilities
# Enter value in float, e.g.: 0.2, 0.8
print("Enter probabilities in float value")
p_h = float(input("Enter the probability of Mike having a cold: "))
p_e_given_h = float(input("Enter the probability of observing sneezing when Mike has a cold: "))
p_e_given_not_h = float(input("Enter the probability of observing sneezing when Mike does not have a cold: "))

# Calculate P(H|E)
result = bayes_theorem(p_h, p_e_given_h, p_e_given_not_h)

# Print the result
print("Mike's probability of having a cold given that he sneezes (P(H|E)) is:", round(result, 2))

""")
        
    elif num =="3b":
        print(""" 
pract 3b
def drug_user(prob_th=0.5,sensitivity=0.97,specificity=0.95,prevelance=0.005,verbose=True): 

 #FORMULA  
    p_user = prevelance  
    p_non_user = 1-prevelance  
    p_pos_user = sensitivity  
    p_neg_non_user = specificity  
    p_pos_non_user = 1-specificity  

    #Probability of being a drug user = (Sensitivity * Prevalence) / [(Sensitivity * Prevalence) + ((1 - Specificity) * (1 - Prevalence))]

    num = p_pos_user*p_user  
    den = p_pos_user*p_user+p_pos_non_user*p_non_user
  
    prob = num/den  
    print("Probability of the Mike being a drug user is", round(prob,3)) 

    if verbose:  
        if prob > prob_th:  
            print("The Mike could be an user")  
        else:  
            print("The Mike may not be an user")  

    return prob  
drug_user() 


""")
        
    elif num =="4a":
        print(""" 
pract 4a
              
graph = {"5": ["3", "7"], "3": ["2", "4"], "7": ["8"], "2": [], "4": ["8"], "8": []}
visited = []  # List for visited nodes.
queue = []  # Initialize a queue

def bfs(visited, graph, node):  # function for BFS
    visited.append(node)
    queue.append(node)

    while queue:  # Creating loop to visit each node
        m = queue.pop(0)
        print(m, end=" ")
        for neighbour in graph[m]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)

# Driver Code
print("Following is the Breadth-First Search")
bfs(visited, graph, "5")  # function calling 

""")
    
    elif num =="4b":
        print(""" 
pract 4b
              
# Using a Python dictionary to act as an adjacency list
graph = {"5": ["3", "7"], "3": ["2", "4"], "7": ["8"], "2": [], "4": ["8"], "8": []}
visited = set()  # Set to keep track of visited nodes of graph.

def dfs(visited, graph, node):  # function for dfs
    if node not in visited:
        print(node)
        visited.add(node)
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)

# Driver Code
print("Following is the Depth-First Search")
dfs(visited, graph, "5")

""")
    
    elif num =="5":
        print(""" 
pract 5

male(drew). 
male(aaron). 
male(danny). 
male(john). 
male(matt). 
male(teddy). 
male(reese). 

female(isabel). 
female(claudia). 
female(marzia). 
female(kyrie). 

parent(drew,reese). 
parent(isabel,reese). 
parent(drew,danny). 
parent(isabel,danny). 
parent(drew,teddy). 
parent(isabel,teddy). 
parent(aaron,drew). 
parent(claudia,drew). 

mother(X,Y):-parent(X,Y),female(X). 
father(X,Y):- parent(X,Y), male(X). 

grandmother(GM,X):- mother(GM,Y) ,parent(Y,X). 
grandfather(GF,X):- father(GF,Y) ,parent(Y,X). 

greatgrandmother(GGM,X):- mother(GGM,GM) ,parent(GM,F),parent(F,Y),parent(Y,X). greatgrandfather(GGF,X):- father(GGF,GF) ,parent(GF,F),parent(F,Y),parent(Y,X). 

sibling(X,Y):-mother(M,X), mother(M,Y),X\=Y, father(F,X), father(F,Y). 
brother(X,Y):-sibling(X,Y), male(X). 
sister(X,Y):-sibling(X,Y), female(X). 

uncle(U,X):- parent(Y,X), brother(U,Y). 
aunt(A,X):- parent(Y,X), sister(A,Y). 
nephew(N,X):- sibling(S,X),parent(S,N),male(N). 
niece(N,X):-sibling(S,X), parent(S,N), female(N). 
cousin(X,Y):-parent(P,Y),sibling(S,P),parent(S,X). 

""")
    
    elif num =="6a":
        print(""" 
pract 6a
              
A = dict()
B = dict()
Y = dict()
A = {"a": 0.2, "b": 0.3, "c": 0.6, "d": 0.6}
B = {"a": 0.9, "b": 0.9, "c": 0.4, "d": 0.5}
print('The First Fuzzy Set is :', A)
print('The Second Fuzzy Set is :', B)

#Fuzzy Set Union.
result={}
for i in A:
    if(A[i]>B[i]):
        result[i]=A[i]
    else:
        result[i]=B[i]
print("Union of two sets is",result)
    
#Fuzzy Set Intersection
result={}
for i in A:
    if(A[i]<B[i]):
        result[i]=A[i]
    else:
        result[i]=B[i]
print("Intersection of two sets is",result)
    
#Fuzzt Set Complement
result={}
for i in A:
    result[i]=round(1-A[i],2)
print("Complement of First set is",result)

#Fuzzy Set Difference
result={}
for i in A:
    result[i]=round(min(A[i],1-B[i]),2)
print("Difference of two sets is",result)

""")
    
    elif num =="6b":
        print(""" 
pract 6b

#### pip install fuzzywuzzy 
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

s1 = "I love GeeksforGeeks"
s2 = "I am loving GeeksforGeeks"
print ("FuzzyWuzzy Ratio: ", fuzz.ratio(s1, s2))
print ("FuzzyWuzzy PartialRatio: ", fuzz.partial_ratio(s1, s2))
print ("FuzzyWuzzy TokenSortRatio: ", fuzz.token_sort_ratio(s1, s2))
print ("FuzzyWuzzy TokenSetRatio: ", fuzz.token_set_ratio(s1, s2))
print ("FuzzyWuzzy WRatio: ", fuzz.WRatio(s1, s2),'\n\n')
  
# for process library,
query = 'geeks for geeks'
choices = ['geek for geek', 'geek geek', 'g. for geeks'] 
print ("List of ratios: ")
print (process.extract(query, choices), '\n')
print ("Best among the above list: ",process.extractOne(query, choices)) 

""")
    
    elif num =="7a":
        print(""" 
pract 7a
              
#pip install seaborn
              
import seaborn as sns 
import pandas as pd 
import matplotlib.pyplot as plt 
# Create a dataframe
df = pd.DataFrame({'x': [10, 38, 5, 7, 300, 11, 113, 165, 17, 19],
                   'y': [28, 4, 6, 8, 10, 122, 14, 16, 158, 200]})


# Create a joint plot with a kernel density estimate (KDE) and a scatter plot
sns.jointplot(x='x', y='y', data=df, kind='kde').plot_joint(sns.scatterplot)
plt.show() 

""")
        
    elif num =="7b":
        print(""" 
pract 7b

import pandas as pd  
import numpy as np 

df = pd.read_csv('student-mat.csv')  
print("Head:")
print(df.head(3) )
print()
print("Length: ")
print(len(df))

df['grade_A'] = np.where(df['G3']*5 >= 80, 1, 0) 
df['high_absenses'] = np.where(df['absences'] >= 10, 1, 0) 
df['count'] = 1 
df = df[['grade_A','high_absenses','count']]  
print(df.head() )
print()
              
print()
print("Pivot Table:")
print(pd.pivot_table(  
    df,   
    values='count',   
    index=['grade_A'],   
    columns=['high_absenses'],   
    aggfunc=np.size,   
    fill_value=0  ))

""")
        
    elif num =="8":
        print(""" 
pract 8

#pip install scikit-learn

#Synthetic classification dataset
from numpy import where
from sklearn.datasets import make_classification
from matplotlib import pyplot
# Define datasets
X,y = make_classification(n_samples=1000, n_features=2, n_informative=2, n_redundant=0, n_clusters_per_class=1, random_state=4)
# Create scatter plot for samples from each class
for class_value in range(2):
  # Get row indexes for samples with this class
  row_ix = where(y == class_value)
  # Create scatter of these samples
  pyplot.scatter(X[row_ix, 0], X[row_ix, 1])
# Show the plot
pyplot.show() 

""")
    
    elif num =="9a":
        print(""" 
pract 9a

import pandas as pd
import numpy as np
titanic= pd.read_csv("titanic.csv")
titanic.head()

titanic_cat = titanic.select_dtypes(object)
titanic_num = titanic.select_dtypes(np.number)

titanic_cat.head()

titanic_num.head()

titanic_cat.drop(['Name','Ticket'], axis=1, inplace=True)
titanic_cat.head()

titanic_cat.isnull().sum()
titanic_cat.Cabin.fillna(titanic_cat.Cabin.value_counts().idxmax(), inplace=True)
titanic_cat.Embarked.fillna(titanic_cat.Embarked.value_counts().idxmax(), inplace=True)

titanic_cat.head(20)

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
titanic_cat = titanic_cat.apply(le.fit_transform)

titanic_cat.head()

titanic_num.isna().sum()

titanic_num.Age.fillna(titanic_num.Age.mean(), inplace=True)
titanic_num.isna().sum()

titanic_num.drop(['PassengerId'], axis=1, inplace=True)
titanic_num.head()

titanic_final = pd.concat([titanic_cat,titanic_num],axis=1)
titanic_final.head()

X=titanic_final.drop(['Survived'],axis=1)
Y= titanic_final['Survived']

X_train = np.array(X[0:int(0.80*len(X))])
Y_train = np.array(Y[0:int(0.80*len(Y))])
X_test = np.array(X[int(0.80*len(X)):])
Y_test = np.array(Y[int(0.80*len(Y)):])
len(X_train), len(Y_train), len(X_test), len(Y_test)

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

LR = LogisticRegression()
KNN = KNeighborsClassifier()
NB = GaussianNB()
LSVM = LinearSVC()
NLSVM = SVC(kernel='rbf')
DT = DecisionTreeClassifier()
RF = RandomForestClassifier()

LR_fit = LR.fit(X_train, Y_train)
KNN_fit = KNN.fit(X_train, Y_train)
NB_fit = NB.fit(X_train, Y_train)
LSVM_fit = LSVM.fit(X_train, Y_train)
NLSVM_fit = NLSVM.fit(X_train, Y_train)
DT_fit = DT.fit(X_train, Y_train)
RF_fit = RF.fit(X_train, Y_train)

LR_pred = LR_fit.predict(X_test)
KNN_pred = KNN_fit.predict(X_test)
NB_pred = NB_fit.predict(X_test)
LSVM_pred = LSVM_fit.predict(X_test)
NLSVM_pred = NLSVM_fit.predict(X_test)
DT_pred = DT_fit.predict(X_test)
RF_pred = RF_fit.predict(X_test)

from sklearn.metrics import accuracy_score
print("Logistic Regression is %f percent accurate" % (accuracy_score(LR_pred, Y_test)*100))
print("KNN is %f percent accurate" % (accuracy_score(KNN_pred, Y_test)*100))
print("Naive Bayes is %f percent accurate" % (accuracy_score(NB_pred, Y_test)*100))
print("Linear SVMs is %f percent accurate" % (accuracy_score(LSVM_pred, Y_test)*100))
print("Non Linear SVMs is %f percent accurate" % (accuracy_score(NLSVM_pred, Y_test)*100))
print("Decision Trees is %f percent accurate" % (accuracy_score(DT_pred, Y_test)*100))
print("Random Forests is %f percent accurate" % (accuracy_score(RF_pred, Y_test)*100)) 



""")
        
    elif num =="9b":
        print(""" 
pract 9b
              
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
customer_data = pd.read_csv('Mall_Customers.csv')
customer_data.shape
customer_data.head()
data = customer_data.iloc[:, 3:5].values
import scipy.cluster.hierarchy as shc
plt.figure(figsize=(10, 7))
plt.title("Customer Dendograms")
dend = shc.dendrogram(shc.linkage(data, method='ward'))
from sklearn.cluster import AgglomerativeClustering
cluster = AgglomerativeClustering(n_clusters=5, metric='euclidean', linkage='ward')
cluster.fit_predict(data)
plt.figure(figsize=(10,7))
plt.scatter(data[:,0], data[:,1], c=cluster.labels_, cmap='rainbow')
plt.show() 


""")
        
    elif num =="10":
        print(""" 
pract 10
              
class ClothesAgent:
    def __init__(self):
        self.weather = None

    def get_weather(self):
        print("Enter the weather (sunny, rainy, windy, snowy)")
        self.weather = input().lower()

    def suggest_clothes(self):
        if self.weather == 'sunny':
            print("You should wear light clothes.")
        elif self.weather == 'rainy':
            print("Don't forget an umbrella.")
        elif self.weather == 'windy':
            print("Wear layers and jacket.")
        elif self.weather == 'snowy':
            print("Dress warmly with heavy coat, gloves and boots.")
        else:
            print("Invlaid input")

def main():
    agent = ClothesAgent()
    agent.get_weather()
    agent.suggest_clothes()

if __name__ == '__main__':
    main() 

""")
    
    elif num =="11":
        print(""" 
pract 11

#pip install nltk              
              
def sentenceSegment(text):
    sentences = []
    start = 0

    for i in range(len(text)):
        if text[i] == '.' or text[i] == '!' or text[i] == '?':
            sentences.append(text[start:i+1].strip())
            start = i + 1

    return sentences

text = "Hello, NLP world!! In this example, we are going to do the basics of Text processing which will be used later."

print(sentenceSegment(text))

##############################################################

import nltk
nltk.download('punkt')

text = "Hello, NLP world!! In this example, we are going to do the basics of Text processing which will be used later."

sentences = nltk.sent_tokenize(text)

print(sentences)


##############################################################


import string

def remove_punctuation(input_string):
    # Define a string of punctuation marks and symbols
    punctuations = string.punctuation

    # Remove the punctuation marks and symbols from the input string
    output_string = "".join(char for char in input_string if char not in punctuations)

    return output_string


text = "Hello, NLP world!! In this example, we are going to do the basics of Text processing which will be used later."
sentences = sentenceSegment(text)
puncRemovedText = remove_punctuation(text)
print(puncRemovedText)


##############################################################


def convertToLower(s):
  return s.lower()

text = "Hello, NLP world!! In this example, we are going to do the basics of Text processing which will be used later."
puncRemovedText = remove_punctuation(text)

lowerText = convertToLower(puncRemovedText)
print(lowerText)



##############################################################


#in this code, we are not using any libraries
#tokenize without using any function from string or any other function.
#only using loops and if/else

def tokenize(s):
  words = [] #token words should be stored here
  i = 0
  word = ""
  while(i <len(s)):
    if (s[i] != " "):
      word = word+s[i]
    else:
        words.append(word)
        word = ""

    i = i + 1
  words.append(word)
  return words


text = "Hello, NLP world!! In this example, we are going to do the basics of Text processing which will be used later."
puncRemovedText = remove_punctuation(text)
lowerText = convertToLower(puncRemovedText)

tokenizedText = tokenize(lowerText)
print(tokenizedText)



##############################################################

import nltk

# Define input text
text = "Hello, NLP world!! In this example, we are going to do the basics of Text processing which will be used later."

#sentence segmentation - removal of punctuations and converting to lowercase
sentences = nltk.sent_tokenize(text)
puncRemovedText = remove_punctuation(text)
lowerText = convertToLower(puncRemovedText)

# Tokenize the text
tokens = nltk.word_tokenize(lowerText)

# Print the tokens
print(tokens)



##############################################################

import nltk

sentence = "We're going to John's house today."
tokens = nltk.word_tokenize(sentence)

print(tokens)



""")
    
    else:
        print("Invalid input")
        
        