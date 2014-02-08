# 

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
if (!require(rjson)){
  install.packages("rjson")
}

# Loading installed libraries
require("ggplot2")
require("gridExtra") 
require("stargazer")
require("rjson")

# Loading data
coaches_data <- read.csv("/tmp/RtmpkVFCek/data55f13eae0c8")

# Selecting row at time t
t <- 2000
coaches_t <- coaches_data[coaches_data$"year" == t,]

# Feature set
feat <- c("season_win","season_loss","playoff_win","playoff_loss")
coach_feat <- coaches_t[,feat]



# Json data
