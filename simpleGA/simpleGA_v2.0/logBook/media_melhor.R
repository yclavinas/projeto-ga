###media
setwd("~/Documents/UnB/GA/projeto-ga/simpleGA/simpleGA_v2.0/logBook")
library("Hmisc", lib.loc="/Library/Frameworks/R.framework/Versions/3.1/Resources/library")
mediaGeracao <- function(file, n){
  raw_data = read.csv2(file, sep='', header=F)
  teste = apply(raw_data, 1, as.character)
  y2000 = apply(teste, 1, as.numeric)
  
  soma = rep(0, 100)
  for (i in 1:50){
    for(j in 1:100){
      soma[j]  = y2000[(n*5000)+((i-1)*100)+j,5] + soma[j]
    }  
  }
  soma = soma/50
  return(soma)
}

desvioPadrao <- function(file, n){
  
  raw_data = read.csv2(file, sep='', header=F)
  teste = apply(raw_data, 1, as.character)
  y2000 = apply(teste, 1, as.numeric)
  
  std = rep(0,100)
  for (i in 1:50){
    for(j in 1:100){
      std[j]  = y2000[(n*5000)+((i-1)*100)+j,6] + std[j]
    }  
  }
  std = std/50
  return(std)
}

graficos <- function(uniform, blend, simulatedBinary, simBinBounded,
                     stdUniform,stdBlend,stdSimBinary,stdSimBinBounded,
                     year){
  #   boxplot(uniform, blend,simulatedBinary, simBinBounded)
  #   titulo = paste("Media do Valor Media das geracoes-", year, sep = '')
  #   title(titulo,
  #         ylab='LogLikelihood', 
  #         xlab=c('Uniform, Blend, Binary, Binary Bounded')
  #   )
  #   arquivo = paste(year, "MediaGeracaoBoxPlot.png", sep = '')
  #   dev.copy(png, arquivo)
  #   dev.off()
  UN = data.frame(
    x  = c(1:100)
    , y  = uniform
    , sd = stdUniform
  )
  BL = data.frame(
    x  = c(1:100)
    , y  = blend
    , sd = stdBlend
  )
  SB = data.frame(
    x  = c(1:100)
    , y  = simulatedBinary
    , sd = stdSimBinary
  )
  SBB = data.frame(
    x  = c(1:100)
    , y  = simBinBounded
    , sd = stdSimBinBounded
  )
  
  arquivo = paste(year, "-MediaGeracaoCurvas.png", sep = '')
  png(arquivo, width = 800, height = 800)
  par(mfrow=c(2,2))
  plot(UN$x, UN$y, pch = 19, col = "blue", lwd=2.5,
       ylab='LogLikelihood', 
       xlab=c('Numero da geracao 0-99'),
       ylim=range(c(uniform, blend, simBinBounded, simulatedBinary)),
       las = 2
  ) 
  with (
    data = UN
    , expr = errbar(x, y, y+sd, y-sd, add=T, pch=1)
  ) 
  axis(2,at=seq(-3000,-2000,50), las = 2)
  axis(1,at=seq(0,100,10),las=2)
  titulo = paste("Media do Valor Media das geracoes-", year, sep = '')
  title(titulo)
  plot(BL$x, BL$y,pch=19,col="yellow",lwd=2.5,ylim=range(c(uniform, blend, simBinBounded, simulatedBinary)),las=2)
  with (
    data = BL
    , expr = errbar(x, y, y+sd, y-sd, add=T, pch=1)
  ) 
  axis(2,at=seq(-3000,-2000,50), las = 2)
  axis(1,at=seq(0,100,10),las=2)
  plot(SBB$x, SBB$y, pch = 19, col = "red", lwd=2.5,ylim=range(c(uniform,blend,simBinBounded,simulatedBinary)),las=2)
  with (
    data = SBB
    , expr = errbar(x, y, y+sd, y-sd, add=T, pch=1)
  )  
  axis(2,at=seq(-3000,-2000,50), las = 2)
  axis(1,at=seq(0,100,10),las=2)
  plot(SBB$x, SBB$y,pch = 19,col="green",lwd=2.5,ylim=range(c(uniform, blend, simBinBounded, simulatedBinary)),las=2)
  with (
    data = SB
    , expr = errbar(x, y, y+sd, y-sd, add=T, pch=1)
  ) 
  axis(2,at=seq(-3000,-2000,50), las = 2)
  axis(1,at=seq(0,100,10),las=2)
  legend('bottom',
         c('Uniform', 'Blend', 'Binary', 'Binary Bounded'),
         lwd=c(2.5,2.5),
         col=c("blue","yellow","red", "green")
  )
  dev.off()
}

uniform2000 = mediaGeracao("2000_Uniform.txt", 0)
stdUniform2000 = desvioPadrao("2000_Uniform.txt", 0)
uniform2001 = mediaGeracao("2001_Uniform.txt", 1)
stdUniform2001 = desvioPadrao("2001_Uniform.txt", 1)
uniform2002 = mediaGeracao("2002_Uniform.txt", 2)
stdUniform2002 = desvioPadrao("2002_Uniform.txt", 2)
uniform2003 = mediaGeracao("2003_Uniform.txt", 3)
stdUniform2003 = desvioPadrao("2003_Uniform.txt", 3)
uniform2004 = mediaGeracao("2004_Uniform.txt", 4)
stdUniform2004 = desvioPadrao("2004_Uniform.txt", 4)
uniform2005 = mediaGeracao("2005_Uniform.txt", 5)
stdUniform2005 = desvioPadrao("2005_Uniform.txt", 5)
uniform2006 = mediaGeracao("2006_Uniform.txt", 6)
stdUniform2006 = desvioPadrao("2006_Uniform.txt", 6)
uniform2007 = mediaGeracao("2007_Uniform.txt", 7)
stdUniform2007 = desvioPadrao("2007_Uniform.txt", 7)
uniform2008 = mediaGeracao("2008_Uniform.txt", 8)
stdUniform2008 = desvioPadrao("2008_Uniform.txt", 8)
uniform2009 = mediaGeracao("2009_Uniform.txt", 9)
stdUniform2009 = desvioPadrao("2009_Uniform.txt", 9)
uniform2010 = mediaGeracao("2010_Uniform.txt", 10)
stdUniform2010 = desvioPadrao("2010_Uniform.txt", 10)

blend2000 = mediaGeracao("2000_blend.txt", 0)
stdBlend2000 = desvioPadrao("2000_blend.txt", 0)
blend2001 = mediaGeracao("2001_blend.txt", 1)
stdBlend2001 = desvioPadrao("2001_blend.txt", 1)
blend2002 = mediaGeracao("2002_blend.txt", 2)
stdBlend2002 = desvioPadrao("2002_blend.txt", 2)
blend2003 = mediaGeracao("2003_blend.txt", 3)
stdBlend2003 = desvioPadrao("2003_blend.txt", 3)
blend2004 = mediaGeracao("2004_blend.txt", 4)
stdBlend2004 = desvioPadrao("2004_blend.txt", 4)
blend2005 = mediaGeracao("2005_blend.txt", 5)
stdBlend2005 = desvioPadrao("2005_blend.txt", 5)
blend2006 = mediaGeracao("2006_blend.txt", 6)
stdBlend2006 = desvioPadrao("2006_blend.txt", 6)
blend2007 = mediaGeracao("2007_blend.txt", 7)
stdBlend2007 = desvioPadrao("2007_blend.txt", 7)
blend2008 = mediaGeracao("2008_blend.txt", 8)
stdBlend2008 = desvioPadrao("2008_blend.txt", 8)
blend2009 = mediaGeracao("2009_blend.txt", 9)
stdBlend2009 = desvioPadrao("2009_blend.txt", 9)
blend2010 = mediaGeracao("2010_blend.txt", 10)
stdBlend2010 = desvioPadrao("2010_blend.txt", 10)

simulatedBinary2000 = mediaGeracao("2000_simulatedBinary.txt", 0)
stdsimulatedBinary2000 = desvioPadrao("2000_simulatedBinary.txt", 0)
simulatedBinary2001 = mediaGeracao("2001_simulatedBinary.txt", 1)
stdsimulatedBinary2001 = desvioPadrao("2001_simulatedBinary.txt", 1)
simulatedBinary2002 = mediaGeracao("2002_simulatedBinary.txt", 2)
stdsimulatedBinary2002 = desvioPadrao("2002_simulatedBinary.txt", 2)
simulatedBinary2003 = mediaGeracao("2003_simulatedBinary.txt", 3)
stdsimulatedBinary2003 = desvioPadrao("2003_simulatedBinary.txt", 3)
simulatedBinary2004 = mediaGeracao("2004_simulatedBinary.txt", 4)
stdsimulatedBinary2004 = desvioPadrao("2004_simulatedBinary.txt", 4)
simulatedBinary2005 = mediaGeracao("2005_simulatedBinary.txt", 5)
stdsimulatedBinary2005 = desvioPadrao("2005_simulatedBinary.txt", 5)
simulatedBinary2006 = mediaGeracao("2006_simulatedBinary.txt", 6)
stdsimulatedBinary2006 = desvioPadrao("2006_simulatedBinary.txt", 5)
simulatedBinary2007 = mediaGeracao("2007_simulatedBinary.txt", 7)
stdsimulatedBinary2007 = desvioPadrao("2007_simulatedBinary.txt", 7)
simulatedBinary2008 = mediaGeracao("2008_simulatedBinary.txt", 8)
stdsimulatedBinary2008 = desvioPadrao("2008_simulatedBinary.txt", 8)
simulatedBinary2009 = mediaGeracao("2009_simulatedBinary.txt", 9)
stdsimulatedBinary2009 = desvioPadrao("2009_simulatedBinary.txt", 9)
simulatedBinary2010 = mediaGeracao("2010_simulatedBinary.txt", 10)
stdsimulatedBinary2010 = desvioPadrao("2010_simulatedBinary.txt", 10)

simBinBounded2000 = mediaGeracao("2000_simBinBounded.txt", 0)
stdsimBinBounded2000 = desvioPadrao("2000_simBinBounded.txt", 0)
simBinBounded2001 = mediaGeracao("2001_simBinBounded.txt", 1)
stdsimBinBounded2001 = desvioPadrao("2001_simBinBounded.txt", 1)
simBinBounded2002 = mediaGeracao("2002_simBinBounded.txt", 2)
stdsimBinBounded2002 = desvioPadrao("2002_simBinBounded.txt", 2)
simBinBounded2003 = mediaGeracao("2003_simBinBounded.txt", 3)
stdsimBinBounded2003 = desvioPadrao("2003_simBinBounded.txt", 3)
simBinBounded2004 = mediaGeracao("2004_simBinBounded.txt", 4)
stdsimBinBounded2004 = desvioPadrao("2004_simBinBounded.txt", 4)
simBinBounded2005 = mediaGeracao("2005_simBinBounded.txt", 5)
stdsimBinBounded2005 = desvioPadrao("2005_simBinBounded.txt", 5)
simBinBounded2006 = mediaGeracao("2006_simBinBounded.txt", 6)
stdsimBinBounded2006 = desvioPadrao("2006_simBinBounded.txt", 6)
simBinBounded2007 = mediaGeracao("2007_simBinBounded.txt", 7)
stdsimBinBounded2007 = desvioPadrao("2007_simBinBounded.txt", 7)
simBinBounded2008 = mediaGeracao("2008_simBinBounded.txt", 8)
stdsimBinBounded2008 = desvioPadrao("2008_simBinBounded.txt", 8)
simBinBounded2009 = mediaGeracao("2009_simBinBounded.txt", 9)
stdsimBinBounded2009 = desvioPadrao("2009_simBinBounded.txt", 9)
simBinBounded2010 = mediaGeracao("2010_simBinBounded.txt", 10)
stdsimBinBounded2010 = desvioPadrao("2010_simBinBounded.txt", 10)

graficos(uniform2000, blend2000, simulatedBinary2000, simBinBounded2000,
         stdUniform2000, stdBlend2000, stdsimulatedBinary2000, stdsimBinBounded2000, "2000")
graficos(uniform2001, blend2001, simulatedBinary2001, simBinBounded2001,
         stdUniform2001, stdBlend2001, stdsimulatedBinary2001, stdsimBinBounded2001,"2001")
graficos(uniform2002, blend2002, simulatedBinary2002, simBinBounded2002,
         stdUniform2002, stdBlend2002, stdsimulatedBinary2002, stdsimBinBounded2002,"2002")
graficos(uniform2003, blend2003, simulatedBinary2003, simBinBounded2003,
         stdUniform2003, stdBlend2003, stdsimulatedBinary2003, stdsimBinBounded2003,"2003")
graficos(uniform2004, blend2004, simulatedBinary2004, simBinBounded2004,
         stdUniform2004, stdBlend2004, stdsimulatedBinary2004, stdsimBinBounded2004,"2004")
graficos(uniform2005, blend2005, simulatedBinary2005, simBinBounded2005,
         stdUniform2005, stdBlend2005, stdsimulatedBinary2005, stdsimBinBounded2005,"2005")
graficos(uniform2006, blend2006, simulatedBinary2006, simBinBounded2006,
         stdUniform2006, stdBlend2006, stdsimulatedBinary2006, stdsimBinBounded2006,"2006")
graficos(uniform2007, blend2007, simulatedBinary2007, simBinBounded2007,
         stdUniform2007, stdBlend2007, stdsimulatedBinary2007, stdsimBinBounded2007,"2007")
graficos(uniform2008, blend2008, simulatedBinary2008, simBinBounded2008,
         stdUniform2008, stdBlend2008, stdsimulatedBinary2008, stdsimBinBounded2008,"2008")
graficos(uniform2009, blend2009, simulatedBinary2009, simBinBounded2009,
         stdUniform2009, stdBlend2009, stdsimulatedBinary2009, stdsimBinBounded2009,"2009")
graficos(uniform2010, blend2010, simulatedBinary2010, simBinBounded2010,
         stdUniform2010, stdBlend2010, stdsimulatedBinary2010, stdsimBinBounded2010,"2010")

