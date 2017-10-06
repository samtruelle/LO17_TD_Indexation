fichier2 <- read.csv("fichier2.csv", header=TRUE)
head(fichier2)
hist(fichier2$idf_i)
summary(fichier2$idf_i)

tfidf__mean <- read.csv("tfidf__mean.csv", header=TRUE)
tfidf__mean[1000:1005,]
hist(tfidf__mean$tf_idf_i_j)
