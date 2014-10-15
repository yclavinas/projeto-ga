#2000-media melhores
#2001-media pop
setwd("~/Documents/UnB/GA/projeto-ga/simpleGA/simpleGA_v2.0/14-10.mapas")
options(scipen=999)
library(grid)
library(latticeExtra)
library(png)

image <- readPNG("kantomap.png")

raw_data = read.csv2("2000-cxBlend(selRoulette, mutPolynomialBounded).txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2000 = apply(teste, 1, as.numeric)
raw_data = read.csv2("2001-modelo.txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2001 = apply(teste, 1, as.numeric)
raw_data = read.csv2("2002-modelo.txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2002 = apply(teste, 1, as.numeric)
raw_data = read.csv2("2003-modelo.txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2003 = apply(teste, 1, as.numeric)
raw_data = read.csv2("2004-modelo.txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2004 = apply(teste, 1, as.numeric)
raw_data = read.csv2("2005-modelo.txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2005 = apply(teste, 1, as.numeric)
raw_data = read.csv2("2006-modelo.txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2006 = apply(teste, 1, as.numeric)
raw_data = read.csv2("2007-modelo.txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2007 = apply(teste, 1, as.numeric)
raw_data = read.csv2("2008-modelo.txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2008 = apply(teste, 1, as.numeric)
raw_data = read.csv2("2009-modelo.txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2009 = apply(teste, 1, as.numeric)
raw_data = read.csv2("2010-modelo.txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2010 = apply(teste, 1, as.numeric)


media2000 = matrix(data = 0 ,nrow = 45, ncol = 45) 
k = 1
for(i in 1:45){
  for(j in 1:45){
    for(l in 1:10){
      media2000[i,j] = y2000[l,k] + media2000[i,j]
    }
    k = k + 1
  }
}
media2000 = media2000/10


media2001 = matrix(data = 0 ,nrow = 45, ncol = 45) 
k = 1
for(i in 1:45){
  for(j in 1:45){
    for(l in 1:10){
      media2001[i,j] = y2001[l,k] + media2001[i,j]
    }
    k = k + 1
  }
}
media2001 = media2001/10
media2002 = matrix(data = 0 ,nrow = 45, ncol = 45) 
k = 1
for(i in 1:45){
  for(j in 1:45){
    for(l in 1:10){
      media2002[i,j] = y2002[l,k] + media2002[i,j]
    }
    k = k + 1
  }
}
media2002 = media2002/10
media2003 = matrix(data = 0 ,nrow = 45, ncol = 45) 
k = 1
for(i in 1:45){
  for(j in 1:45){
    for(l in 1:10){
      media2003[i,j] = y2003[l,k] + media2003[i,j]
    }
    k = k + 1
  }
}
media2003 = media2003/10
media2004 = matrix(data = 0 ,nrow = 45, ncol = 45) 
k = 1
for(i in 1:45){
  for(j in 1:45){
    for(l in 1:10){
      media2004[i,j] = y2004[l,k] + media2004[i,j]
    }
    k = k + 1
  }
}
media2004 = media2004/10
media2005 = matrix(data = 0 ,nrow = 45, ncol = 45) 
k = 1
for(i in 1:45){
  for(j in 1:45){
    for(l in 1:10){
      media2005[i,j] = y2005[l,k] + media2005[i,j]
    }
    k = k + 1
  }
}
media2005 = media2005/10
media2006 = matrix(data = 0 ,nrow = 45, ncol = 45) 
k = 1
for(i in 1:45){
  for(j in 1:45){
    for(l in 1:10){
      media2006[i,j] = y2006[l,k] + media2006[i,j]
    }
    k = k + 1
  }
}
media2006 = media2006/10
media2007 = matrix(data = 0 ,nrow = 45, ncol = 45) 
k = 1
for(i in 1:45){
  for(j in 1:45){
    for(l in 1:10){
      media2007[i,j] = y2007[l,k] + media2007[i,j]
    }
    k = k + 1
  }
}
media2007 = media2007/10
media2008 = matrix(data = 0 ,nrow = 45, ncol = 45) 
k = 1
for(i in 1:45){
  for(j in 1:45){
    for(l in 1:10){
      media2008[i,j] = y2008[l,k] + media2008[i,j]
    }
    k = k + 1
  }
}
media2008 = media2008/10
media2009 = matrix(data = 0 ,nrow = 45, ncol = 45) 
k = 1
for(i in 1:45){
  for(j in 1:45){
    for(l in 1:10){
      media2009[i,j] = y2009[l,k] + media2009[i,j]
    }
    k = k + 1
  }
}
media2009 = media2009/10
media2010 = matrix(data = 0 ,nrow = 45, ncol = 45) 
k = 1
for(i in 1:45){
  for(j in 1:45){
    for(l in 1:10){
      media2010[i,j] = y2010[l,k] + media2010[i,j]
    }
    k = k + 1
  }
}
media2010 = media2010/10

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
###DADOS REAIS###
raw_data = read.csv2("2000-reais.txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2000_real = apply(teste, 1, as.numeric)
raw_data = read.csv2("2001-reais.txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2001_real = apply(teste, 1, as.numeric)
raw_data = read.csv2("2002-reais.txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2002_real = apply(teste, 1, as.numeric)
raw_data = read.csv2("2003-reais.txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2003_real = apply(teste, 1, as.numeric)
raw_data = read.csv2("2004-reais.txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2004_real = apply(teste, 1, as.numeric)
raw_data = read.csv2("2005-reais.txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2005_real = apply(teste, 1, as.numeric)
raw_data = read.csv2("2006-reais.txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2006_real = apply(teste, 1, as.numeric)
raw_data = read.csv2("2007-reais.txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2007_real = apply(teste, 1, as.numeric)
raw_data = read.csv2("2008-reais.txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2008_real = apply(teste, 1, as.numeric)
raw_data = read.csv2("2009-reais.txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2009_real = apply(teste, 1, as.numeric)
raw_data = read.csv2("2010-reais.txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2010_real = apply(teste, 1, as.numeric)

matriz2000_real = matrix(nrow = 45, ncol = 45) 
k = 1
for (i in 1:45){
  for (j in 1:45){
    matriz2000_real[i,j] = y2000_real[k] + 1
    k = k + 1
  }
}
matriz2001_real = matrix(nrow = 45, ncol = 45) 
k = 1
for (i in 1:45){
  for (j in 1:45){
    matriz2001_real[i,j] = y2001_real[k] +1
    k = k + 1
  }
}
matriz2002_real = matrix(nrow = 45, ncol = 45) 
k = 1
for (i in 1:45){
  for (j in 1:45){
    matriz2002_real[i,j] = y2002_real[k] +1
    k = k + 1
  }
}
matriz2003_real = matrix(nrow = 45, ncol = 45) 
k = 1
for (i in 1:45){
  for (j in 1:45){
    matriz2003_real[i,j] = y2003_real[k] +1
    k = k + 1
  }
}
matriz2004_real = matrix(nrow = 45, ncol = 45) 
k = 1
for (i in 1:45){
  for (j in 1:45){
    matriz2004_real[i,j] = y2004_real[k] +1
    k = k + 1
  }
}
matriz2005_real = matrix(nrow = 45, ncol = 45) 
k = 1
for (i in 1:45){
  for (j in 1:45){
    matriz2005_real[i,j] = y2005_real[k] + 1
    k = k + 1
  }
}
matriz2006_real = matrix(nrow = 45, ncol = 45) 
k = 1
for (i in 1:45){
  for (j in 1:45){
    matriz2006_real[i,j] = y2006_real[k] +1
    k = k + 1
  }
}
matriz2007_real = matrix(nrow = 45, ncol = 45) 
k = 1
for (i in 1:45){
  for (j in 1:45){
    matriz2007_real[i,j] = y2007_real[k] +1
    k = k + 1
  }
}
matriz2008_real = matrix(nrow = 45, ncol = 45) 
k = 1
for (i in 1:45){
  for (j in 1:45){
    matriz2008_real[i,j] = y2008_real[k] +1
    k = k + 1
  }
}

matriz2009_real = matrix(nrow = 45, ncol = 45) 
k = 1
for (i in 1:45){
  for (j in 1:45){
    matriz2009_real[i,j] = y2009_real[k] +1
    k = k + 1
  }
}
matriz2010_real = matrix(nrow = 45, ncol = 45) 
k = 1
for (i in 1:45){
  for (j in 1:45){
    matriz2010_real[i,j] = y2010_real[k] + 1
    k = k + 1
  }
}

p = levelplot(log(matriz2000_real), col.regions = terrain.colors,
              alpha.regions = 0.5, contour = 1)
p + layer(grid.raster(as.raster(image)), under=TRUE)
dev.copy(png,'matriz2000_real.png')
dev.off()
p = levelplot(log(matriz2001_real), col.regions = terrain.colors,
              alpha.regions = 0.5, contour = 1)
p + layer(grid.raster(as.raster(image)), under=TRUE)
dev.copy(png,'matriz2001_real.png')
dev.off()
p = levelplot(log(matriz2002_real), col.regions = terrain.colors,
              alpha.regions = 0.5, contour = 1)
p + layer(grid.raster(as.raster(image)), under=TRUE)
dev.copy(png,'matriz2002_real.png')
dev.off()
p = levelplot(log(matriz2003_real), col.regions = terrain.colors,
              alpha.regions = 0.5, contour = 1)
p + layer(grid.raster(as.raster(image)), under=TRUE)
dev.copy(png,'matriz2003_real.png')
dev.off()
p = levelplot(log(matriz2004_real), col.regions = terrain.colors,
              alpha.regions = 0.5, contour = 1)
p + layer(grid.raster(as.raster(image)), under=TRUE)
dev.copy(png,'matriz2004_real.png')
dev.off()
p = levelplot(log(matriz2005_real), col.regions = terrain.colors,
              alpha.regions = 0.5, contour = 1)
p + layer(grid.raster(as.raster(image)), under=TRUE)
dev.copy(png,'matriz2005_real.png')
dev.off()
p = levelplot(log(matriz2006_real), col.regions = terrain.colors,
              alpha.regions = 0.5, contour = 1)
p + layer(grid.raster(as.raster(image)), under=TRUE)
dev.copy(png,'matriz2006_real.png')
dev.off()
p = levelplot(log(matriz2007_real), col.regions = terrain.colors,
              alpha.regions = 0.5, contour = 1)
p + layer(grid.raster(as.raster(image)), under=TRUE)
dev.copy(png,'matriz2007_real.png')
dev.off()
p = levelplot(log(matriz2008_real), col.regions = terrain.colors,
              alpha.regions = 0.5, contour = 1)
p + layer(grid.raster(as.raster(image)), under=TRUE)
dev.copy(png,'matriz2008_real.png')
dev.off()
p = levelplot(log(matriz2009_real), col.regions = terrain.colors,
              alpha.regions = 0.5, contour = 1)
p + layer(grid.raster(as.raster(image)), under=TRUE)
dev.copy(png,'matriz2009_real.png')
dev.off()
p = levelplot(log(matriz2010_real), col.regions = terrain.colors,
              alpha.regions = 0.5, contour = 1)
p + layer(grid.raster(as.raster(image)), under=TRUE)
dev.copy(png,'matriz2010_real.png')
dev.off()