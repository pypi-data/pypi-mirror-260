def index():
    print(""" 

1) Design a simple machine learning model to train the training instances and test the same. 
          
2) Find-s algorithm for finding the most specific.
          
3a) Support Vector Machine Algorithm for Multiclass classification using Iris.CSV  dataset from sklearn.
3b) Support Vector Machine Algorithm for Multiclass classification using wine dataset from sklearn.
                         
4)	For a given set of training data examples stored in a .csv file, 
    implement and demonstrate the candidate-elimination algorithm 
    to output a description of the set of all hypotheses consistent with the training examples.     

5) Write a program to implement the Naïve Bayesian classifier 
    for a sample training data set stored as a .csv file. 
    Compute the accuracy of the classifier, considering few test data sets.
          
6) Decision Tree classifier & Random Forest Classifier. 
          
7) Data loading, feature scoring and ranking, feature selection 
    (Principal Component Analysis)
          
8a) Least Square Regression Algorithm. 
8b) Logistic Regression algorithm.
             
9a) Build an Artificial Neural Network by implementing the Backpropagation algorithm and 
    test the same using appropriate data sets. 
9b) Perform Text pre-processing, Text clustering, classification with Prediction, Test Score and Confusion Matrix  
          
10a) Implement the different Distance methods (Euclidean) with Prediction, Test Score and Confusion Matrix.
10b) Implement the classification model using K means clustering with Prediction, Test Score and Confusion Matrix.

""")
    

def prog(num):
    if num =="1":
        print(""" 
        --- Pract 1 ---
              
import numpy
import matplotlib.pyplot as plt #pip install matplotlib
numpy.random.seed(2)#pip install numpy
from sklearn.model_selection import train_test_split #pip install scikit-learn
from sklearn.metrics import r2_score

x = numpy.random.normal(3,1,100)
y = numpy.random.normal(156,40,100) /x
plt.scatter(x,y)
plt.xlabel("X")
plt.ylabel("Y")
plt.show()

train_x = x[:80]
train_y = y[:80]
test_x = x[:20]
test_y = y[:20]

plt.scatter(train_x,train_y)
plt.xlabel("train_x")
plt.ylabel("train_y")
plt.show()

train_x, test_x, train_y, test_y = train_test_split(x,y,test_size=0.3)
plt.scatter(test_x,test_y)
plt.xlabel("test_x")
plt.ylabel("test_y")
plt.show()

# Draw a Polynomial Regression line through the data points with training data
mymodel = numpy.poly1d(numpy.polyfit(train_x, train_y, 4))
myline = numpy.linspace(0,6,100)
plt.scatter(train_x, train_y)
plt.plot(myline, mymodel(myline))
plt.xlabel("train_x")
plt.ylabel("train_y")
plt.show()

# Draw a Polynomial Regression line through the data points with test data
mymodel = numpy.poly1d(numpy.polyfit(test_x, test_y, 4))
myline = numpy.linspace(0,6,100)
plt.scatter(test_x, test_y)
plt.plot(myline, mymodel(myline))
plt.xlabel("test_x")
plt.ylabel("test_y")
plt.show()

r2 = r2_score(train_y, mymodel(train_x))
print("\n\nr2 Score: ",r2)
print("\nPrediction: ",mymodel(5)) 

              

        """)

    elif num =="2":
        print(""" 
        --- Pract 2  ---

import csv
a = []
with open('data.csv', 'r') as csvfile:
    next(csvfile)
    for row in csv.reader(csvfile):
        a.append(row)
    print(a)

print("\nThe total number of training instances are : ",len(a))

num_attribute = len(a[0])-1

print("\nThe initial hypothesis is : ")
hypothesis = ['0']*num_attribute
print(hypothesis)

for i in range(0, len(a)):
    if a[i][num_attribute] == 'yes':
        print ("\nInstance ", i+1, "is", a[i], " and is Positive Instance")
        for j in range(0, num_attribute):
            if hypothesis[j] == '0' or hypothesis[j] == a[i][j]:
                hypothesis[j] = a[i][j]
            else:
                hypothesis[j] = '?'
        print("The hypothesis for the training instance", i+1, " is: " , hypothesis, "\n")

    if a[i][num_attribute] == 'no':
        print ("\nInstance ", i+1, "is", a[i], " and is Negative Instance Hence Ignored")
        print("The hypothesis for the training instance", i+1, " is: " , hypothesis, "\n")

print("\nThe Maximally specific hypothesis for the training instance is ", hypothesis) 

                            
        """)

    elif num =="3a":
        print(""" 
        --- Pract 3a  ---

from sklearn import svm, datasets
import sklearn.model_selection as model_selection
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns #pip install seaborn

iris = datasets.load_iris()
#iris = datasets.load_wine()

X = iris.data[:, :2]
y = iris.target
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, train_size=0.80, test_size=0.20, random_state=101)

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

# Calculate the confusion matrix for the Polynomial Kernel model
poly_confusion_matrix = confusion_matrix(y_test, poly_pred)
print('Confusion Matrix (Polynomial Kernel):\n', poly_confusion_matrix)

# Create a heatmap of the confusion matrix for Polynomial Kernel
plt.figure(figsize=(8, 6))
sns.heatmap(poly_confusion_matrix, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix (Polynomial Kernel)')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

# Calculate the confusion matrix for the RBF Kernel model
rbf_confusion_matrix = confusion_matrix(y_test, rbf_pred)
print('Confusion Matrix (RBF Kernel):\n', rbf_confusion_matrix)

# Create a heatmap of the confusion matrix for RBF Kernel
plt.figure(figsize=(8, 6))
sns.heatmap(rbf_confusion_matrix, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix (RBF Kernel)')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show() 


                            
        """)
    
    elif num =="3b":
        print(""" 
        --- Pract 3b  ---

from sklearn import svm, datasets
import sklearn.model_selection as model_selection
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns 

#iris = datasets.load_iris()
wine = datasets.load_wine()

X = wine.data[:, :2]
y = wine.target
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, train_size=0.80, test_size=0.20, random_state=101)

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


# Calculate the confusion matrix for the Polynomial Kernel model
poly_confusion_matrix = confusion_matrix(y_test, poly_pred)
print('Confusion Matrix (Polynomial Kernel):\n', poly_confusion_matrix)

# Create a heatmap of the confusion matrix for Polynomial Kernel
plt.figure(figsize=(8, 6))
sns.heatmap(poly_confusion_matrix, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix (Polynomial Kernel)')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

# Calculate the confusion matrix for the RBF Kernel model
rbf_confusion_matrix = confusion_matrix(y_test, rbf_pred)
print('Confusion Matrix (RBF Kernel):\n', rbf_confusion_matrix)

# Create a heatmap of the confusion matrix for RBF Kernel
plt.figure(figsize=(8, 6))
sns.heatmap(rbf_confusion_matrix, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix (RBF Kernel)')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show() 



                            
        """)    
    
    elif num =="4":
        print(""" 
        --- Pract 4  ---

import numpy as np
import pandas as pd

#Loading data from a csv file.
data = pd.DataFrame(data=pd.read_csv('data.csv'))
print(data)

print("############################################################")
#Separating concept features from Target
concepts = np.array(data.iloc[:,0:6])
print(concepts)

print("############################################################")
#Isolating target into a separate DataFrame
#Copying last column to target  array
target = np.array(data.iloc[:,6])
print(target) 

print("############################################################")

def learn(concepts, target): 
#Initialise S0 with the first instance from concepts.
#.copy()makes sure a new list is created instead of just pointing to the same memory location.
    specific_h = concepts[0].copy()
    print()          
    print("Initialization of specific_h and genearal_h") 
    print() 
    print("Specific Boundary: ", specific_h)             
    general_h = [["?" for i in range(len(specific_h))] for i in range(len(specific_h))]
    print() 
    print("Generic Boundary: ",general_h)                
# The learning iterations.
    for i, h in enumerate(concepts):
        print()       
        print("Instance", i+1 , "is ", h)                  
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
        print("")
# find indices where we have empty rows, meaning those that are unchanged.
    indices = [i for i, val in enumerate(general_h) if val == ['?', '?', '?', '?', '?', '?']]    
    for i in indices:   
# remove those rows from general_h
        general_h.remove(['?', '?', '?', '?', '?', '?']) 
# Return final values
    return specific_h, general_h 

s_final, g_final = learn(concepts, target)
print("Final Specific_h: ", s_final, sep="\ n") <-------------------
print("Final General_h: ", g_final, sep="\ n")  <------------------- 


                            
        """)

    elif num =="5":
        print(""" 
        --- Pract 5  ---
import numpy as np
import pandas as pd
from sklearn import datasets

#Load dataset
wine = datasets.load_wine()

#print (wine) #if you want to see the data you can print data
#print the name of the 13 features
#print("Features: ", wine.feature_names) 

#print the label type of wine
print("Labels: ", wine.target_names)
X=pd.DataFrame(wine['data'])
print(X.head())
print(wine.data.shape)

#print the wine labels (0:Class_0, 1:class_2, 2:class_2)
y= wine.target
print("y=",y)


#import train_test_split function
from sklearn.model_selection import train_test_split
#split dataset into training set and test set.
X_train, X_test, y_train, y_test = train_test_split(wine.data, wine.target, test_size=0.30,random_state=10)

#import gaussian naive bayes model.
from sklearn.naive_bayes import GaussianNB
#create a gaussian classifier
gnb = GaussianNB()
#train the model using the training sets
gnb.fit(X_train,y_train)
print("")
print("#############################################################")
print("")
#predict the response for test dataset
y_pred = gnb.predict(X_test)
print(y_pred) 

from sklearn import metrics
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

#confusion matrix
from sklearn.metrics import confusion_matrix
cm=np.array(confusion_matrix(y_test,y_pred))
print(cm) 

        """)

    elif num =="6":
        print(""" 
        --- Pract 6  ---
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#%matplotlib inline

df = pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.csv") 
#Keeping emp position unaffects.
print(df.head())

#Exploratory Data Analysis
sns.countplot(x='Attrition', data=df)
plt.show()

from pandas.core.arrays import categorical
df.drop(['EmployeeCount','EmployeeNumber', 'Over18', 'StandardHours'], axis="columns", inplace=True)
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

from sklearn.metrics import (accuracy_score, log_loss, classification_report, confusion_matrix)
def print_score(clf, X_train, y_train, X_test, y_test, train=True):
  if train:
    pred = clf.predict(X_train)
    clf_report = pd.DataFrame(classification_report(y_train, pred, output_dict=True))
    print("Train Result:\n=======================================")
    print(f"Accuracy Score: {accuracy_score(y_train, pred) * 100:.2f}%")
    print("____________________________________")
    print(f"CLASSIFICATION REPORT:\n{clf_report}")
    print("____________________________________")
    print(f"Confusion Matrix: \n{confusion_matrix(y_train, pred)}\n")

  elif train==False:
    pred = clf.predict(X_test)
    clf_report = pd.DataFrame(classification_report(y_test, pred, output_dict=True))
    print("Test Result:\n=======================================")
    print(f"Accuracy Score: {accuracy_score(y_test, pred) * 100:.2f}%")
    print("____________________________________")
    print(f"CLASSIFICATION REPORT:\n{clf_report}")
    print("____________________________________")
    print(f"Confusion Matrix: \n{confusion_matrix(y_test, pred)}\n") 

### Decision Tree Classifier ###
from sklearn.tree import DecisionTreeClassifier
from pickle import TRUE
from sklearn.tree import DecisionTreeClassifier

tree_clf = DecisionTreeClassifier(random_state=42)
tree_clf.fit(X_train, y_train)
print_score(tree_clf, X_train,y_train, X_test, y_test, train=True)
print_score(tree_clf, X_train,y_train, X_test, y_test, train=False) 


### Random Forest Classifier ###
from sklearn.ensemble import RandomForestClassifier

rf_clf = RandomForestClassifier(random_state=42)
rf_clf.fit(X_train, y_train)
print_score(rf_clf, X_train, y_train, X_test, y_test, train=True)
print_score(rf_clf, X_train, y_train, X_test, y_test, train=False)

        """)

    elif num =="7":
        print(""" 
        --- Pract 7  ---
import numpy as np 
import pandas as pd 
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data' 

names = ['sepal-length','sepal-width','petal-length','petal-width','Class'] 
dataset = pd.read_csv(url, names=names) 
print(dataset.head())

#store the features sets into X variables and  
# the series of corresponding variables in y 
x=dataset.drop('Class',axis=1) 
y=dataset['Class'] 

from sklearn.model_selection import train_test_split 
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2, random_state=0) 


from sklearn.preprocessing import StandardScaler 
sc = StandardScaler() 
x_train1 = sc.fit_transform(x_train) 
x_test1 = sc.transform(x_test) 
y_train1 = y_train 
y_test1 = y_test 
 
from sklearn.decomposition import PCA 
pca=PCA() 
x_train1=pca.fit_transform(x_train1) 
x_test1=pca.transform(x_test1) 
explained_variance = pca.explained_variance_ratio_ 
print(explained_variance) 

pca = PCA(n_components=1)  
x_train1 = pca.fit_transform(x_train1) 
x_test1 = pca.transform(x_test1) 

from sklearn.ensemble import RandomForestClassifier 
classifier = RandomForestClassifier(max_depth=2, random_state=0) 
classifier.fit(x_train1, y_train1) 
y_pred=classifier.predict(x_test1) 

from sklearn.metrics import confusion_matrix 
from sklearn.metrics import accuracy_score 
 
cm=confusion_matrix(y_test,y_pred) 
print(cm) 
print('Accuracy',accuracy_score(y_test,y_pred)) 


        """)

    elif num =="8a":
        print(""" 
        --- Pract 8a  ---
# Making imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (12.0,9.0)

np.random.seed(42)
X = np.linspace(0, 10, 100)
Y = 2.5 * X + 1.5 + np.random.normal(0, 2, 100)
data = pd.DataFrame({'X': X, 'Y': Y})

plt.scatter(X, Y)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Synthetic Data for Least Square Regression')
plt.show()

# Building the model
X_mean = np.mean(X)
Y_mean = np.mean(Y)

num = 0
den = 0
for i in range(len(X)):
  num += (X[i] - X_mean)*(Y[i] - Y_mean)
  den += (X[i] - X_mean)**2
m = num/den
c = Y_mean - m*X_mean
print (m,c)

# Making predictions
Y_pred = m*X + c
plt.scatter(X, Y)  # actual
plt.plot([min(X),max(X)],[min(Y_pred), max(Y_pred)], color='red') #prediction
plt.show() 


        """)

    elif num =="8b":
        print(""" 
        --- Pract 8b  ---

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('https://raw.githubusercontent.com/mk-gurucharan/Classification/master/DMVWrittenTests.csv')
X = dataset.iloc[:, [0,1]].values
Y = dataset.iloc[:,2].values
print(dataset.head(5))

# Splitting the dataset into the training set and test set.
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.25, random_state = 0)


from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


# Training the logistic regression model on the training set
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression()
classifier.fit(X_train, Y_train)
# Predicting the test set results.
y_pred = classifier.predict(X_test)
print(y_pred)

# Confusion Matrix and Accuracy.
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(Y_test,y_pred)
from sklearn.metrics import accuracy_score
print ("Accuracy:", accuracy_score(Y_test, y_pred))
print(cm)

              
        """)

    elif num =="9a":
        print(""" 
        --- Pract 9a  ---

import numpy as np
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
for i in range(2000):
  obj.train(X,Y)

print("input\ n"+str(X))                    <--------------
print("\ n \ n Actual output\ n"+str(Y))        <--------------
print("\ n \ n Predicted output\ n"+str(obj.forward(X)))  <--------------
print("\ n \ n loss"+str(np.mean(np.square(Y-obj.forward(X)))))  <--------------
              
        """)

    elif num =="9b":
        print(""" 
        --- Pract 9b  ---

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.read_csv('Restaurant_Reviews.tsv', delimiter = '\t', quoting = 3)

import re
import nltk #pip install nltk
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

              
        """)

    elif num =="10a":
        print(""" 
        --- Pract 10a  ---

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

#Load the dataset
df = pd.read_csv("Iris.csv")

#quick look into the data
print(df.head(5))
print("")

#Separate data and label
x = df.drop(['variety'], axis=1)
y = df['variety']

#Prepare data for classification process
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)

#Create a model , p = 2 => Euclidean Distance:
knn = KNeighborsClassifier(n_neighbors = 6, p = 2, metric='minkowski')

#Train the model
knn.fit(x_train, y_train)

# Calculate the accuracy of the model
print(knn.score(x_test, y_test))
y_pred = knn.predict(x_test)

#confusion matrix 
from sklearn.metrics import  confusion_matrix
cm=np.array(confusion_matrix(y_test,y_pred))
print(cm)
print("")

#Create a model , p = 1 => Manhattan Distance
knn = KNeighborsClassifier(n_neighbors = 6, p = 1, metric='minkowski')

#Train the model
knn.fit(x_train, y_train)

# Calculate the accuracy of the model
print(knn.score(x_test, y_test))
y_pred = knn.predict(x_test)

#confusion matrix 
from sklearn.metrics import  confusion_matrix
cm=np.array(confusion_matrix(y_test,y_pred))
print(cm)
print("")

#Create a model ,p = ∞, Chebychev Distance
#let ∞ = 10000
knn = KNeighborsClassifier(n_neighbors = 6, p = 10000, metric='minkowski')

#Train the model
knn.fit(x_train, y_train)

# Calculate the accuracy of the model
print(knn.score(x_test, y_test))
y_pred = knn.predict(x_test)

#confusion matrix 
from sklearn.metrics import  confusion_matrix
cm=np.array(confusion_matrix(y_test,y_pred))
print(cm)
print("") 
              
        """)

    elif num =="10b":
        print(""" 
        --- Pract 10b  ---

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sklearn

#Import the dataset and slice the important features
dataset = pd.read_csv('Mall_Customers.csv')
X = dataset.iloc[:, [3,4]].values

#Find the optimal k value for clustering the data.
from sklearn.cluster import KMeans
wcss = []
for i in range(1,11):
    kmeans = KMeans(n_clusters=i, init='k-means++',random_state=42)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)
    
plt.plot(range(1,11),wcss)
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show() 

#The point at which the elbow shape is created is 5.
kmeans = KMeans(n_clusters=5,init="k-means++",random_state=42)
y_kmeans = kmeans.fit_predict(X)

plt.scatter(X[y_kmeans == 0,0], X[y_kmeans == 0,1], s = 60, c = 'red', label = 'Cluster1')
plt.scatter(X[y_kmeans == 1,0], X[y_kmeans == 1,1], s = 60, c = 'blue', label = 'Cluster2')
plt.scatter(X[y_kmeans == 2,0], X[y_kmeans == 2,1], s = 60, c = 'green', label = 'Cluster3')
plt.scatter(X[y_kmeans == 3,0], X[y_kmeans == 3,1], s = 60, c = 'violet', label = 'Cluster4')
plt.scatter(X[y_kmeans == 4,0], X[y_kmeans == 4,1], s = 60, c = 'yellow', label = 'Cluster5')
plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1],s=100,c='black',label='Centroids')
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score (1-100')
plt.legend()
plt.show() 
              
        """)

    else:
        print("Invalid input")
        
        