###media
setwd("~/Documents/UnB/GA/projeto-ga/simpleGA/simpleGA_v2.0/logBook")
mediaGeracao <- function(file){
  raw_data = read.csv2(file, sep='', header=F)
  teste = apply(raw_data, 1, as.character)
  y2000 = apply(teste, 1, as.numeric)
  
  soma = rep(0, 100)
  for (i in 1:50){
    for(j in 1:100){
      soma[j]  = y2000[((i-1)*100)+j,2] + soma[j]
      
    }  
  }
  soma = soma/50
  return(soma)
}

graficos <- function(uniform, blend, simulatedBinary, simBinBounded, year){
#   boxplot(uniform, blend,simulatedBinary, simBinBounded)
#   titulo = paste("Media do Tempo Media das geracoes-", year, sep = '')
#   title(titulo,
#         ylab='Tempo', 
#         xlab=c('Uniform, Blend, Binary, Binary Bounded')
#   )
#   arquivo = paste(year, "MediaTempoGeracaoBoxPlot.png", sep = '')
#   dev.copy(png, arquivo)
#   dev.off()
  
  arquivo = paste(year, "MediaTempoGeracaoBoxPlot.png", sep = '')
  png(arquivo, width = 800, height = 600)
  par(mfrow=c(2,2))
  plot(uniform, pch = 19, col = "blue", lwd=2.5,
       ylab='Tempo', 
       xlab=c('Numero da geracao 0-99') 
  )
  plot(blend, pch = 19, col = "yellow", lwd=2.5)
  plot(simBinBounded, pch = 19, col = "red", lwd=2.5)
  plot(simulatedBinary, pch = 19, col = "green", lwd=2.5)
  titulo = paste("Media do Tempo Media das geracoes-", year, sep = '')
  title(titulo)
  legend('bottom',
         c('Uniform', 'Blend', 'Binary', 'Binary Bounded'),
         lwd=c(2.5,2.5),
         col=c("blue","yellow","red", "green")
  )
#   arquivo = paste(year, "MediaTempoGeracaoCurvas.png", sep = '')
#   dev.copy(png, arquivo)
  dev.off()
}

uniform2000 = mediaGeracao("2000_Uniform.txt")
uniform2001 = mediaGeracao("2001_Uniform.txt")
uniform2002 = mediaGeracao("2002_Uniform.txt")
uniform2003 = mediaGeracao("2003_Uniform.txt")
uniform2004 = mediaGeracao("2004_Uniform.txt")
uniform2005 = mediaGeracao("2005_Uniform.txt")
uniform2006 = mediaGeracao("2006_Uniform.txt")
uniform2007 = mediaGeracao("2007_Uniform.txt")
uniform2008 = mediaGeracao("2008_Uniform.txt")
uniform2009 = mediaGeracao("2009_Uniform.txt")
uniform2010 = mediaGeracao("2010_Uniform.txt")

blend2000 = mediaGeracao("2000_blend.txt")
blend2001 = mediaGeracao("2001_blend.txt")
blend2002 = mediaGeracao("2002_blend.txt")
blend2003 = mediaGeracao("2003_blend.txt")
blend2004 = mediaGeracao("2004_blend.txt")
blend2005 = mediaGeracao("2005_blend.txt")
blend2006 = mediaGeracao("2006_blend.txt")
blend2007 = mediaGeracao("2007_blend.txt")
blend2008 = mediaGeracao("2008_blend.txt")
blend2009 = mediaGeracao("2009_blend.txt")
blend2010 = mediaGeracao("2010_blend.txt")

simulatedBinary2000 = mediaGeracao("2000_simulatedBinary.txt")
simulatedBinary2001 = mediaGeracao("2001_simulatedBinary.txt")
simulatedBinary2002 = mediaGeracao("2002_simulatedBinary.txt")
simulatedBinary2003 = mediaGeracao("2003_simulatedBinary.txt")
simulatedBinary2004 = mediaGeracao("2004_simulatedBinary.txt")
simulatedBinary2005 = mediaGeracao("2005_simulatedBinary.txt")
simulatedBinary2006 = mediaGeracao("2006_simulatedBinary.txt")
simulatedBinary2007 = mediaGeracao("2007_simulatedBinary.txt")
simulatedBinary2008 = mediaGeracao("2008_simulatedBinary.txt")
simulatedBinary2009 = mediaGeracao("2009_simulatedBinary.txt")
simulatedBinary2010 = mediaGeracao("2010_simulatedBinary.txt")

simBinBounded2000 = mediaGeracao("2000_simBinBounded.txt")
simBinBounded2001 = mediaGeracao("2001_simBinBounded.txt")
simBinBounded2002 = mediaGeracao("2002_simBinBounded.txt")
simBinBounded2003 = mediaGeracao("2003_simBinBounded.txt")
simBinBounded2004 = mediaGeracao("2004_simBinBounded.txt")
simBinBounded2005 = mediaGeracao("2005_simBinBounded.txt")
simBinBounded2006 = mediaGeracao("2006_simBinBounded.txt")
simBinBounded2007 = mediaGeracao("2007_simBinBounded.txt")
simBinBounded2008 = mediaGeracao("2008_simBinBounded.txt")
simBinBounded2009 = mediaGeracao("2009_simBinBounded.txt")
simBinBounded2010 = mediaGeracao("2010_simBinBounded.txt")


graficos(uniform2000, blend2000, simulatedBinary2000, simBinBounded2000, "2000")
graficos(uniform2001, blend2001, simulatedBinary2001, simBinBounded2001, "2001")
graficos(uniform2002, blend2002, simulatedBinary2002, simBinBounded2002, "2002")
graficos(uniform2003, blend2003, simulatedBinary2003, simBinBounded2003, "2003")
graficos(uniform2004, blend2004, simulatedBinary2004, simBinBounded2004, "2004")
graficos(uniform2005, blend2005, simulatedBinary2005, simBinBounded2005, "2005")
graficos(uniform2006, blend2006, simulatedBinary2006, simBinBounded2006, "2006")
graficos(uniform2007, blend2007, simulatedBinary2007, simBinBounded2007, "2007")
graficos(uniform2008, blend2008, simulatedBinary2008, simBinBounded2008, "2008")
graficos(uniform2009, blend2009, simulatedBinary2009, simBinBounded2009, "2009")
graficos(uniform2010, blend2010, simulatedBinary2010, simBinBounded2010, "2010")

