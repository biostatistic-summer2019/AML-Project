#Create a .png file of heat maps for all patients and genes
#Right corner labels from top to bottom
#shows from low-risk patients to high-risk patients
#Scripts modified from Sebastian Raschka
#"A short tutorial for decent heat maps in R"
#########################################################
### A) Installing and loading required packages
#########################################################

if (!require("gplots")) {
  install.packages("gplots", dependencies = TRUE)
  library(gplots)
}
if (!require("RColorBrewer")) {
  install.packages("RColorBrewer", dependencies = TRUE)
  library(RColorBrewer)
}


#########################################################
### B) Reading in data and transform it into matrix format
#########################################################
data <- read.table ("clinical_9A_standard_low_risk_sd3.txt", sep="\t", header=TRUE)
p.vec <- apply (data, 2, function (x){ t.test(x[1:44], x[45:72])$p.value})
ind <- which(p.vec < 0.000000005)
aml.sub <-aml.dat[, ind]
dim (aml.sub)

#data <- read.csv("../datasets/heatmaps_in_r.csv", comment.char="#")
rnames <- data[,1]                            # assign labels in column 1 to "rnames"
mat_data <- data.matrix(data[,2:ncol(data)])  # transform column 2-5 into a matrix
rownames(mat_data) <- rnames                  # assign row names


#########################################################
### C) Customizing and plotting the heat map
#########################################################

# creates a own color palette from red to green
my_palette <- colorRampPalette(c("red", "yellow", "green"))(n = 299)

# (optional) defines the color breaks manually for a "skewed" color transition
col_breaks = c(seq(-1,0,length=100),  # for red
               seq(0.01,0.8,length=100),           # for yellow
               seq(0.81,1,length=100))             # for green

# creates a 5 x 5 inch image
png("heatmaps_all_genes_in_r.png",    # create PNG for the heat map        
    width = 15*300,        # 5 x 300 pixels
    height = 15*300,
    res = 300,            # 300 pixels per inch
    pointsize = 4)        # smaller font size
#heatmap.2(mat_data,
#  cellnote = mat_data,  # same data set for cell labels
#  main = "Correlation", # heat map title
#  notecol="black",      # change font color of cell labels to black
#  density.info="none",  # turns off density plot inside color legend
#  trace="none",         # turns off trace lines inside the heat map
#  margins =c(12,9),     # widens margins around plot
#  col=my_palette,       # use on color palette defined earlier
#  breaks=col_breaks,    # enable color transition at specified limits
#  dendrogram="row",     # only draw a row dendrogram
#  Colv="NA")            # turn off column clustering
heatmap(as.matrix(data)
        ,scale = "column"
        ,col = heat.colors(256)
        ,margins =c(12,9)
        ,main = "Characteristic of All Gene models"
        ,Rowv = NA
        ,Colv = NA)

dev.off()               # close the PNG device


