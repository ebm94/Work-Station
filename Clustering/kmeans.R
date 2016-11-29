library(datasets)
head(iris)

library(ggplot2)
ggplot(iris, aes(Petal.Length, Petal.Width, color=Species))+geom_point()
# Petal.length and Petal.Width are similar among the same speciesbut variees between different species

set.seed(20)
irisCluster<-kmeans(iris[, 3:4], 3, nstart=20)
#Group into 3 clusters because we know that there are three species
# R will start with 20 different random starting assignments and then select the one with the lowest
#within sample variation.
irisCluster

# To compare cluster with the species
table(irisCluster$cluster, iris$Species)

irisCluster$cluster<-as.factor(irisCluster$cluster)
ggplot(iris, aes(Petal.Length, Petal.Width, color=irisCluster$cluster))+geom_point()
