###media
raw_data = read.csv2("teste.txt", sep='', header=F)
teste = apply(raw_data, 1, as.character)
y2000 = apply(teste, 1, as.numeric)

soma = rep(0, 100)
for (i in 1:50){
  for(j in 1:100){
    soma[j]  = y2000[((i-1)*100)+j,4] + soma[j]
    
  }  
}
soma = soma/50


boxplot(soma, soma2)
plot(soma, type = "l")
lines(soma2)
###