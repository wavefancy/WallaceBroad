# Check did the SPA test rescale the predictor.

ped = read.table('./iris.data.tsv',header = T)
score = read.table('./iris.score.txt',header = T)

myhead = colnames(score)
idname="ID"
common_id_index = match(ped[[idname]],myhead)

ped = ped[is.na(common_id_index)==F,]
common_id_index = common_id_index[is.na(common_id_index)==F]

genos = score[1,][common_id_index]
genos = t(genos)
colnames(genos) = c('score')
ped[['score']] = genos

b = glm(pheno~score,data = ped, family = 'binomial')
summary(b)

bs = glm(pheno~scale(score),data = ped, family = 'binomial')
summary(bs)