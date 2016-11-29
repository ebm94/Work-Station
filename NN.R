### Author: Edwin Basil Mathew
### Testing of Neural Networks on College dataset in ISLR package in R

install.packages("ISLR")
library(ISLR)
head(College, 2)
print(head(College, 2))

# Find the max and min values in columns 2 to 18
maxs<-apply(College[, 2:18], 2, max)
mins<-apply(College[, 2:18], 2, min)

# Scale/normalize the dataset
scaled.data<-as.data.frame(scale(College[, 2:18], center=mins, scale=maxs-mins))
print(head(scaled.data, 2))

# Convert column from Yes/No to 1/0
Private<-as.numeric(College$Private)-1
data=cbind(Private, scaled.data)

# Random splitting of data
library(caTools)
set.seed(101)
split=sample.split(data$Private, SplitRatio = 0.7)
train<-subset(data, split==TRUE)
test<-subset(data, split==FALSE)

# Create formula for neural network function
feats<-names(scaled.data)
f<-paste(feats, collapse=' + ')
f<-paste('Private~', f)
f<-as.formula(f)

install.packages("neuralnet")
library(neuralnet)
nn<-neuralnet(f, data, hidden=c(10, 10, 10), linear.output=FALSE)

predicted.nn.values<-compute(nn, test[2:18])
head(predicted.nn.values$net.result)

predicted.nn.values$net.result<-sapply(predicted.nn.values$net.result, round, digits=0)

# A confusion matrix
table(test$Private, predicted.nn.values$net.result)
  
plot(nn)

#You can try varying number of hidden layers and neurons


