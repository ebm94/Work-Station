### Author: Edwin Basil Mathew
### OLS, Ridge regression, Lasso Regression, GBM, decision trees implementation on NHTSA dataset

install.packages(c('glmnet', 'gbm', 'rpart'))
library("glmnet") # For Ridge Regression Fitting
library(gbm)
library(rpart) # For building decision trees

#Reading in data
temp<-tempfile()
download.file("ftp://ftp.nhtsa.dot.gov/GES/GES12/GES12_Flatfile.zip", temp, quiet=TRUE)
accident_data_set<-read.delim(unz(temp, "PERSON.TXT"))

print(sort(colnames(accident_data_set)))
table(accident_data_set$INJSEV_IM)
accident_data_set<-accident_data_set[accident_data_set$INJSEV_IM!=6, ]

for (i in 1:ncol(accident_data_set)) {
  if(sum(as.numeric(is.na(accident_data_set[, i])))>0){
    num_missing<-sum(as.numeric(is.na(accident_data_set[, i])))
    print(paste0(colnames(accident_data_set)[i], ": ", num_missing))
  }
}

rows_to_drop<-which(apply(accident_data_set, 1, FUN=function(X){
  return(sum(is.na(X))>0)
}))
data<-accident_data_set[-rows_to_drop,]
data$INJ_SEV<-NULL


data$INJSEV_IM<-as.numeric(data$INJSEV_IM==4)
target<-data$INJSEV_IM


# Data Splitting
train_rows<-sample(nrow(data), round(nrow(data)*0.5))
traindf<-data[train_rows, ]
testdf<-data[-train_rows, ]

# Time for OLS model
OLS_model<-lm(INJSEV_IM~., data=traindf)

# Now, for a GBM

# Training the GBM
# GBM is easier to process as a data matrix
response_column<-which(colnames(traindf)=="INJSEV_IM")
trainy<-traindf$INJSEV_IM
gbm_formula<-as.formula(paste0("INJSEV_IM~", paste(colnames(traindf[, -response_column]), collapse= " + ")))
gbm_model<-gbm(gbm_formula, traindf, distribution = "bernoulli", n.trees=500, bag.fraction = 0.75, cv.folds = 5, interaction.depth = 3)

# For glmnet we make a copy of our dataframe into a matrix
trainx_dm<-data.matrix(traindf[, -response_column])

# Start fitting Lasso
lasso_model<-cv.glmnet(x=trainx_dm, y=traindf$INJSEV_IM, alpha=1)

# Start fitting Ridge
ridge_model<-cv.glmnet(x=trainx_dm, y=traindf$INJSEV_IM, alpha=0)

# Finally, a decision tree
dtree_model<-rpart(INJSEV_IM~., traindf)

# A plot to see how GBM performs in the 500 iterations. The green line has to be minimized.
gbm_perf<-gbm.perf(gbm_model, method="cv")

# Making predictions using our trained models
predictions_ols<-predict(OLS_model, testdf[, -response_column])

predictions_gbm<-predict(gbm_model, newdata=testdf[, -response_column], n.trees=gbm_perf, type="response")

testx_dm<-data.matrix(testdf[, -response_column])
predictions_lasso<-predict(lasso_model, newx=testx_dm, type="response", s="lambda.min")[, 1]

predictions_ridge<-predict(ridge_model, newx=testx_dm, type="response", s="lambda.min")[, 1]

predictions_dtree<-predict(dtree_model, testdf[, -response_column])

# OLS: AUC
auc(testdf$INJSEV_IM, predictions_ols)
# Ridge AUC
auc(testdf$INJSEV_IM, predictions_ridge)
# Lasso AUC
auc(testdf$INJSEV_IM, predictions_lasso)
# GBM AUC
auc(testdf$INJSEV_IM, predictions_gbm)
# Decision Tree AUC
auc(testdf$INJSEV_IM, predictions_dtree)
