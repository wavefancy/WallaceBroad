# Dump KEGG pathways.
#
# --------------------------------
# Dependent packages.
# source("https://bioconductor.org/biocLite.R")
# biocLite("org.Hs.eg.db")
# source("https://bioconductor.org/biocLite.R")
# biocLite("clusterProfiler")
#
# download human KEGG pathways.
args <- commandArgs(TRUE)
if(length(args) != 1){
    print(args)
    print("Please set arguments: arg1 output_prefix")
    quit()
}

library(clusterProfiler)
library(org.Hs.eg.db)
out=args[1]
hm = download_KEGG('hsa', keggType = "KEGG", keyType = "kegg")
#write out kegg pathway id and readable name.
write.table(hm$KEGGPATHID2NAME, file=paste(out,'_kegg_path_name.txt',sep=""), quote=F, row.names=F, col.names=T,sep='\t')
names(hm$KEGGPATHID2EXTID) = c("pathwayid",'kegg')
write.table(hm$KEGGPATHID2EXTID, file=paste(out,'_kegg_pathways.txt',sep=""), quote=F, row.names=F, col.names=T,sep='\t')

# map from kegg id to uniprot id.
k2u <- bitr_kegg(hm$KEGGPATHID2EXTID$kegg, fromType='kegg', toType='uniprot', organism='hsa')

# map from uniprot id to ensembl id, gene symble, entriz id.
ids <- bitr(k2u$uniprot, fromType="UNIPROT", toType=c("SYMBOL", "ENSEMBL","ENTREZID","GENENAME"), OrgDb="org.Hs.eg.db")
t = merge(k2u,ids,by.x="uniprot",by.y="UNIPROT")
write.table(t, file=paste(out,'_geneid_maps.txt',sep=""), quote=F, row.names=F, col.names=T,sep='\t')
