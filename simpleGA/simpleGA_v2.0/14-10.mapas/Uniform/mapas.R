#!/usr/bin/env Rscript
setwd("~/Documents/UnB/GA/projeto-ga/simpleGA/simpleGA_v2.0/14-10.mapas/Uniform")
options(scipen=999)
library(grid)
library(latticeExtra)
library(png)

image <- readPNG("../kantomap.png")

raw_data = read.csv2("2000-cxUniform(selRoulette, mutPolynomialBounded).txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2000 = apply(teste, 1, as.numeric)
raw_data = read.csv2("2001-cxUniform(selRoulette, mutPolynomialBounded).txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2001 = apply(teste, 1, as.numeric)
raw_data = read.csv2("2002-cxUniform(selRoulette, mutPolynomialBounded).txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2002 = apply(teste, 1, as.numeric)
raw_data = read.csv2("2003-cxUniform(selRoulette, mutPolynomialBounded).txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2003 = apply(teste, 1, as.numeric)
raw_data = read.csv2("2004-cxUniform(selRoulette, mutPolynomialBounded).txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2004 = apply(teste, 1, as.numeric)
raw_data = read.csv2("2005-cxUniform(selRoulette, mutPolynomialBounded).txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2005 = apply(teste, 1, as.numeric)
raw_data = read.csv2("2006-cxUniform(selRoulette, mutPolynomialBounded).txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2006 = apply(teste, 1, as.numeric)
raw_data = read.csv2("2007-cxUniform(selRoulette, mutPolynomialBounded).txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2007 = apply(teste, 1, as.numeric)
raw_data = read.csv2("2008-cxUniform(selRoulette, mutPolynomialBounded).txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2008 = apply(teste, 1, as.numeric)
raw_data = read.csv2("2009-cxUniform(selRoulette, mutPolynomialBounded).txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2009 = apply(teste, 1, as.numeric)
raw_data = read.csv2("2010-cxUniform(selRoulette, mutPolynomialBounded).txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2010 = apply(teste, 1, as.numeric)


media2000 = matrix(data = 0 ,nrow = 45, ncol = 45) 
k = 1
for(i in 1:45){
  for(j in 1:45){
    for(l in 1:50){
      media2000[i,j] = y2000[l,k] + media2000[i,j]
    }
    k = k + 1
  }
}
media2000 = media2000/50


media2001 = matrix(data = 0 ,nrow = 45, ncol = 45) 
k = 1
for(i in 1:45){
  for(j in 1:45){
    for(l in 1:50){
      media2001[i,j] = y2001[l,k] + media2001[i,j]
    }
    k = k + 1
  }
}
media2001 = media2001/50
media2002 = matrix(data = 0 ,nrow = 45, ncol = 45) 
k = 1
for(i in 1:45){
  for(j in 1:45){
    for(l in 1:50){
      media2002[i,j] = y2002[l,k] + media2002[i,j]
    }
    k = k + 1
  }
}
media2002 = media2002/50
media2003 = matrix(data = 0 ,nrow = 45, ncol = 45) 
k = 1
for(i in 1:45){
  for(j in 1:45){
    for(l in 1:50){
      media2003[i,j] = y2003[l,k] + media2003[i,j]
    }
    k = k + 1
  }
}
media2003 = media2003/50
media2004 = matrix(data = 0 ,nrow = 45, ncol = 45) 
k = 1
for(i in 1:45){
  for(j in 1:45){
    for(l in 1:50){
      media2004[i,j] = y2004[l,k] + media2004[i,j]
    }
    k = k + 1
  }
}
media2004 = media2004/50
media2005 = matrix(data = 0 ,nrow = 45, ncol = 45) 
k = 1
for(i in 1:45){
  for(j in 1:45){
    for(l in 1:50){
      media2005[i,j] = y2005[l,k] + media2005[i,j]
    }
    k = k + 1
  }
}
media2005 = media2005/50
media2006 = matrix(data = 0 ,nrow = 45, ncol = 45) 
k = 1
for(i in 1:45){
  for(j in 1:45){
    for(l in 1:50){
      media2006[i,j] = y2006[l,k] + media2006[i,j]
    }
    k = k + 1
  }
}
media2006 = media2006/50
media2007 = matrix(data = 0 ,nrow = 45, ncol = 45) 
k = 1
for(i in 1:45){
  for(j in 1:45){
    for(l in 1:50){
      media2007[i,j] = y2007[l,k] + media2007[i,j]
    }
    k = k + 1
  }
}
media2007 = media2007/50
media2008 = matrix(data = 0 ,nrow = 45, ncol = 45) 
k = 1
for(i in 1:45){
  for(j in 1:45){
    for(l in 1:50){
      media2008[i,j] = y2008[l,k] + media2008[i,j]
    }
    k = k + 1
  }
}
media2008 = media2008/50
media2009 = matrix(data = 0 ,nrow = 45, ncol = 45) 
k = 1
for(i in 1:45){
  for(j in 1:45){
    for(l in 1:50){
      media2009[i,j] = y2009[l,k] + media2009[i,j]
    }
    k = k + 1
  }
}
media2009 = media2009/50
media2010 = matrix(data = 0 ,nrow = 45, ncol = 45) 
k = 1
for(i in 1:45){
  for(j in 1:45){
    for(l in 1:50){
      media2010[i,j] = y2010[l,k] + media2010[i,j]
    }
    k = k + 1
  }
}
media2010 = media2010/50

p = levelplot(log(media2000), col.regions = terrain.colors,
              alpha.regions = 0.5, contour = 1)
p + layer(grid.raster(as.raster(image)), under=TRUE)
dev.copy(png,'media2000.png')
dev.off()
p = levelplot(log(media2001), col.regions = terrain.colors,
              alpha.regions = 0.5, contour = 1)
p + layer(grid.raster(as.raster(image)), under=TRUE)
dev.copy(png,'media2001.png')
dev.off()
p = levelplot(log(media2002), col.regions = terrain.colors,
              alpha.regions = 0.5, contour = 1)
p + layer(grid.raster(as.raster(image)), under=TRUE)
dev.copy(png,'media2002.png')
dev.off()
p = levelplot(log(media2003), col.regions = terrain.colors,
              alpha.regions = 0.5, contour = 1)
p + layer(grid.raster(as.raster(image)), under=TRUE)
dev.copy(png,'media2003.png')
dev.off()
p = levelplot(log(media2004), col.regions = terrain.colors,
              alpha.regions = 0.5, contour = 1)
p + layer(grid.raster(as.raster(image)), under=TRUE)
dev.copy(png,'media2004.png')
dev.off()
p = levelplot(log(media2005), col.regions = terrain.colors,
              alpha.regions = 0.5, contour = 1)
p + layer(grid.raster(as.raster(image)), under=TRUE)
dev.copy(png,'media2005.png')
dev.off()
p = levelplot(log(media2006), col.regions = terrain.colors,
              alpha.regions = 0.5, contour = 1)
p + layer(grid.raster(as.raster(image)), under=TRUE)
dev.copy(png,'media2006.png')
dev.off()
p = levelplot(log(media2007), col.regions = terrain.colors,
              alpha.regions = 0.5, contour = 1)
p + layer(grid.raster(as.raster(image)), under=TRUE)
dev.copy(png,'media2007.png')
dev.off()
p = levelplot(log(media2008), col.regions = terrain.colors,
              alpha.regions = 0.5, contour = 1)
p + layer(grid.raster(as.raster(image)), under=TRUE)
dev.copy(png,'media2008.png')
dev.off()
p = levelplot(log(media2009), col.regions = terrain.colors,
              alpha.regions = 0.5, contour = 1)
p + layer(grid.raster(as.raster(image)), under=TRUE)
dev.copy(png,'media2009.png')
dev.off()
p = levelplot(log(media2010), col.regions = terrain.colors,
              alpha.regions = 0.5, contour = 1)
p + layer(grid.raster(as.raster(image)), under=TRUE)
dev.copy(png,'media2010.png')
dev.off()
