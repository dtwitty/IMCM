# Installing required packages
if (!require(ggplot2)){
  install.packages("ggplot2")
}
if (!require(gridExtra)){
  install.packages("gridExtra")
} 
if (!require(stargazer)){
  install.packages("stargazer")
} 
if (!require(matrixStats)){
  install.packages("matrixStats")
}


# Loading installed libraries
require("ggplot2")
require("gridExtra")
require("stargazer")
require("matrixStats")

# Loading basketball data set
bask_stat <- read.csv("bb_wl .csv")
c <- c("school_1","school_2","school_3","school_4","school_5")
only <- bask_stat[rowSums(bask_stat[,c]) != -5,]
only <- only[,c("school_0") != -1]
only <- only[,c("school_0",c)]
size <- length(only[,1])

final <- rep(-1,size)
scale <- 50

# Removing all non-zero elements
for(i in 1:size){
  ds <- scale*unlist(only[i,only[i,] > 0])
  if (length(ds) == 1){
    next
  }
  final[i] <- chi2IsUniform(ds)
}

tot <- final[final != -1]
mean(tot)

# Plotting statistics of coaches
sonly <- bask_stat[,c("school_0") != -1]
only <- sonly[rowSums(sonly[,c]) == -5,]


# Histogram overlaid with kernel density curve
ggplot(only,aes(x=school_0)) + 
  #geom_histogram(aes(y=..density..),      
  #               binwidth=.5,
  #               colour="white", fill="greenyellow") +
  geom_density(alpha=.2, fill="chartreuse") + 
  opts(panel.background = theme_rect(fill='#d6ffb3', colour='white')) +
  ggtitle("Distribution of win/loss ratio for single team coaches") +
  xlim(0,1)

summary(only$"school_0")

ggplot(only,aes(x=school_0)) + 
  #geom_histogram(aes(y=..density..),      
  #               binwidth=.5,
  #               colour="white", fill="greenyellow") +
  geom_density(alpha=.2, fill="chartreuse") + 
  opts(panel.background = theme_rect(fill='#d6ffb3', colour='white')) +
  ggtitle("Distribution of win/loss ratio for single team coaches") +
  xlim(0,1)




