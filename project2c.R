setwd("C:\\Users\\Bryan\\Documents\\UT\\Digital Arch\\")
data<- read.table( 'pro2.txt', header = TRUE, sep = ';', stringsAsFactors = FALSE )

#Delta is proxy for commit
#Size is in bytes? check
head(data)
names(data)<-c("repository","Num_Watchers","Num_Forks","Num_Pulls","Num_Delta","Num_Authors","Num_Files","VCS",
               "Size","begin_date","end_date","User",
               "Num_Followers","Num_Followed")
hist(log(data$nW))
summary(data)

data$begin_date<-as.POSIXct(data$begin_date, origin="1970-01-01")
data$begin_date<-as.Date(as.POSIXct(data$begin_date, origin="1970-01-01"))

data$end_date<-as.POSIXct(data$end_date, origin="1970-01-01")
data$end_date<-as.Date(as.POSIXct(data$end_date, origin="1970-01-01"))

data$time_active<-data$end_date-data$begin_date
data$time_active<-as.numeric(data$time_active)+1

data$weighted_influence<-(data$Num_Forks+data$Num_Watchers)/data$time_active

str(data)
data_user<- aggregate(data[,c(2:7,9,13:16)], by = list(data$User), sum, na.rm = TRUE)
data_repo<-aggregate(data$User,by=list(data$User), length)

head(data_user)
head(data_repo)
data2<-merge(data_user,data_repo,by="Group.1")
str(data2)
head(data2)
rm(data,data_user,data_repo)

summary(data2)
write.csv(data2,"C:\\Users\\Bryan\\Documents\\UT\\Digital Arch\\BB_user_info.csv")
data2<-read.csv("C:\\Users\\Bryan\\Documents\\UT\\Digital Arch\\BB_user_info.csv")
str(data2)
summary(data2)


data2$Influential<-ifelse(data2$weighted_influence>0,1,0)

loggy<-function(x){
  return(log(x+1))}

log(5)==loggy(4)

data2_log<-apply(data2[,c(5:11)],1:2,loggy)

data2<-cbind(data2_log,data2$x,data2$Influential,data2$weighted_influence)
data2<-data.frame(data2)
rm(data2_log)

str(data2)

names(data2)<-c("Num_Pulls","Num_Delta","Num_Authors","Num_Files",
               "Size","Num_Followers","Num_Followed","Repos",
               "Influential","Weighted_Influence")

cor(data2, use="all.obs", method="spearman")[,9:10]

train_x<-data.frame(data2[,c(1:8)])
train_y<-as.factor(data2[,9])

if (!require("randomForest")) install.packages('randomForest'); library('randomForest')
require(AUC)


rFmodel <- randomForest(x=train_x,y=train_y,  ntree=100, importance=TRUE)

#look at the importance of the variables
importance(rFmodel)[,"MeanDecreaseAccuracy"]
varImpPlot(rFmodel)

data2<-read.csv("C:\\Users\\Bryan\\Documents\\UT\\Digital Arch\\BB_user_info.csv")

data3_red<-(data2[which(data2$weighted_influence>0),])
names(data3_red)
loggy<-function(x){
                   return(log(x+1))}

log(5)==loggy(4)

data3_red_log<-apply(data3_red[c(3:13)],1:2,loggy)

data3<-cbind(data3_red$x,data3_red_log)
data3<-data.frame(data3)
str(data3)
names(data3)<-c("repository","Num_Watchers","Num_Forks","Num_Pulls","Num_Delta","Num_Authors","Num_Files",
               "Size","Num_Followers","Num_Followed","time_active","weighted_influence")

rm(data2,data3_red,data3_red_log)


summary(data3)


train_x<-data.frame(data3[,c(1,4:10)])
train_y<-data3[,12]



if (!require("randomForest")) install.packages('randomForest'); library('randomForest')
require(AUC)


rFmodel <- randomForest(x=train_x,y=train_y,  ntree=25, importance=TRUE)

#look at the importance of the variables
importance(rFmodel)[,"MeanDecreaseAccuracy"]
varImpPlot(rFmodel)


if(require('rpart')==FALSE)  install.packages('rpart',repos="http://www.freestatistics.org/cran/") ; require('rpart')

tree<-rpart(train_y ~ ., control=rpart.control(cp = 0.007), train_x)

tree$variable.importance
printcp(tree) # display the results 
plotcp(tree) # visualize cross-validation results 
summary(tree) # detailed summary of splits

# plot tree 
plot(tree, uniform=TRUE
     ,      main="Classification Tree for Influence")
text(tree, use.n=TRUE, all=TRUE, cex=1)





