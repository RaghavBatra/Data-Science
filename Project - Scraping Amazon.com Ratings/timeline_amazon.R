setwd("C:/Users/Raghav/Desktop/Data Analyst Nanodegree/Project - Scraping Amazon.com ratings")
library(ggplot2)
ratings = read.csv('ratings_amazon_3.csv')

str(ratings)

ratings$DaysSimple = ratings$Days - min(ratings$Days)

ratings$Year = floor(ratings$Days/365)

ratings$Vine.Voice = as.logical(ratings$Vine.Voice)
ratings$Verified = as.logical(ratings$Verified)

summary(ratings)

ggplot(data = ratings, aes(x = DaysSimple, y = Rating, group = 1)) +
  # geom_point() +
  geom_line()
  
View(ratings)

ggplot(data = ratings, aes(x = Year, y = Rating, group = 1)) +
  # geom_point() +
  geom_line(stat = "summary",  fun.y = mean)


ggplot(data = ratings_before2007, aes(x = DaysSimple/365, y = Rating, group = 1)) +
  # geom_point(aes(color = Year)) +
  geom_line(aes(color = factor(Year)))
  
ratings_before2007 = subset(ratings, ratings$Year < 2007)
ratings_after2007 = subset(ratings, ratings$Year >= 2007)

summary(ratings_before2007)
summary(ratings_after2007)

ratings_weird = subset(ratings_before2007, ratings_before2007$Vine.Voice == FALSE)

ggplot(data = ratings_weird, aes(x = DaysSimple/365, y = Rating, group = 1)) +
  geom_line()

write.csv(ratings_weird, 'ratings_weird.csv')
