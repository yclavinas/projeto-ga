###media
setwd("~/Documents/UnB/GA/projeto-ga/simpleGA/simpleGA_v2.0/logBook")
mediaGeracao <- function(file, n){
  raw_data = read.csv2(file, sep='', header=F)
  teste = apply(raw_data, 1, as.character)
  y2000 = apply(teste, 1, as.numeric)
  
  soma = rep(0, 50)
  for (i in 1:50){
    #for(j in 1:100){
      soma[i]  = y2000[(n*5000)+100*i,5] + soma[i]
    #}  
  }
  #soma = soma/50
  return(soma)
}

graficos <- function(uniform, blend, simulatedBinary, simBinBounded, year){
  boxplot(uniform, blend,simulatedBinary, simBinBounded)
  titulo = paste("Melhor individuo da ultima geracao-", year, sep = '')
  title(titulo,
        ylab='Log-likelihood', 
        xlab=c('Uniform, Blend, Binary, Binary Bounded')
  )
  arquivo = paste(year, "MelhorUltimaBoxPlot.png", sep = '')
  dev.copy(png, arquivo)
  dev.off()
#   plot(uniform, pch = 19, col = "blue", lwd=2.5,
#        ylab='Tempo', 
#        xlab=c('Numero da geracao 0-99') 
#   )
#   lines(blend, pch = 19, col = "yellow", lwd=2.5)
#   lines(simBinBounded, pch = 19, col = "red", lwd=2.5)
#   lines(simulatedBinary, pch = 19, col = "green", lwd=2.5)
#   titulo = paste("Media do Tempo Media das geracoes-", year, sep = '')
#   title(titulo)
#   legend('bottom',
#          c('Uniform', 'Blend', 'Binary', 'Binary Bounded'),
#          lwd=c(2.5,2.5),
#          col=c("blue","yellow","red", "green")
#   )
#   arquivo = paste(year, "MediaTempoGeracaoCurvas.png", sep = '')
#   dev.copy(png, arquivo)
#   dev.off()
}

uniform2000 = mediaGeracao("2000_Uniform.txt", 0)
uniform2001 = mediaGeracao("2001_Uniform.txt", 1)
uniform2002 = mediaGeracao("2002_Uniform.txt", 2)
uniform2003 = mediaGeracao("2003_Uniform.txt", 3)
uniform2004 = mediaGeracao("2004_Uniform.txt", 4)
uniform2005 = mediaGeracao("2005_Uniform.txt", 5)
uniform2006 = mediaGeracao("2006_Uniform.txt", 6)
uniform2007 = mediaGeracao("2007_Uniform.txt", 7)
uniform2008 = mediaGeracao("2008_Uniform.txt", 8)
uniform2009 = mediaGeracao("2009_Uniform.txt", 9)
uniform2010 = mediaGeracao("2010_Uniform.txt", 10)

blend2000 = mediaGeracao("2000_blend.txt", 0)
blend2001 = mediaGeracao("2001_blend.txt", 1)
blend2002 = mediaGeracao("2002_blend.txt", 2)
blend2003 = mediaGeracao("2003_blend.txt", 3)
blend2004 = mediaGeracao("2004_blend.txt", 4)
blend2005 = mediaGeracao("2005_blend.txt", 5)
blend2006 = mediaGeracao("2006_blend.txt", 6)
blend2007 = mediaGeracao("2007_blend.txt", 7)
blend2008 = mediaGeracao("2008_blend.txt", 8)
blend2009 = mediaGeracao("2009_blend.txt", 9)
blend2010 = mediaGeracao("2010_blend.txt", 10)

simulatedBinary2000 = mediaGeracao("2000_simulatedBinary.txt", 0)
simulatedBinary2001 = mediaGeracao("2001_simulatedBinary.txt", 1)
simulatedBinary2002 = mediaGeracao("2002_simulatedBinary.txt", 2)
simulatedBinary2003 = mediaGeracao("2003_simulatedBinary.txt", 3)
simulatedBinary2004 = mediaGeracao("2004_simulatedBinary.txt", 4)
simulatedBinary2005 = mediaGeracao("2005_simulatedBinary.txt", 5)
simulatedBinary2006 = mediaGeracao("2006_simulatedBinary.txt", 6)
simulatedBinary2007 = mediaGeracao("2007_simulatedBinary.txt", 7)
simulatedBinary2008 = mediaGeracao("2008_simulatedBinary.txt", 8)
simulatedBinary2009 = mediaGeracao("2009_simulatedBinary.txt", 9)
simulatedBinary2010 = mediaGeracao("2010_simulatedBinary.txt", 10)

simBinBounded2000 = mediaGeracao("2000_simBinBounded.txt", 0)
simBinBounded2001 = mediaGeracao("2001_simBinBounded.txt", 1)
simBinBounded2002 = mediaGeracao("2002_simBinBounded.txt", 2)
simBinBounded2003 = mediaGeracao("2003_simBinBounded.txt", 3)
simBinBounded2004 = mediaGeracao("2004_simBinBounded.txt", 4)
simBinBounded2005 = mediaGeracao("2005_simBinBounded.txt", 5)
simBinBounded2006 = mediaGeracao("2006_simBinBounded.txt", 6)
simBinBounded2007 = mediaGeracao("2007_simBinBounded.txt", 7)
simBinBounded2008 = mediaGeracao("2008_simBinBounded.txt", 8)
simBinBounded2009 = mediaGeracao("2009_simBinBounded.txt", 9)
simBinBounded2010 = mediaGeracao("2010_simBinBounded.txt", 10)


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


