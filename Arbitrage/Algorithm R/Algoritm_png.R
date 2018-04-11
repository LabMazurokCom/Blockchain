# Для отображения записей на русс. - вкл. русс. клавиатуру!
setwd("C:/Users/Евгений Леончик/Dropbox/Crypto meetings/Arbitrage_in_R") # Указываем СВОЮ рабочую папку
getwd()

##########  Расчет дохода Арбитража  ############

# Очистка переменных
rm(list=ls())

# Чтение параметров
control <- read.table("control.csv", sep=",", h=T)
control

# Доступные нам средства
#print("OUR volume in $")
VOLUME.limit.our <- control$Amount_USD

# Комиссия на BUY
a <- control$Buy_percent/100
# Комиссия на SELL
b <- control$Sell_percent/100

# Кол-во точек для анализа
k.max <- control$k_max
k.max

# Загрузка файлов с ордерами, сортировка и расчет цены в долларах
BUY.RAW <- read.table("ask.csv", sep=",")
names(BUY.RAW) <- c("BUY.price","BUY.btc")
BUY.RAW$BUY.volume.USD <- BUY.RAW$BUY.price*BUY.RAW$BUY.btc
#BUY
BUY.SORT <- BUY.RAW[order(BUY.RAW$BUY.price),]
#BUY.SORT
SELL.RAW <- read.table("bid.csv", sep=",")
names(SELL.RAW) <- c("SELL.price","SELL.btc")
SELL.RAW$SELL.volume.USD <- SELL.RAW$SELL.price*SELL.RAW$SELL.btc
#SELL
SELL.SORT <- SELL.RAW[rev(order(SELL.RAW$SELL.price)),]
#SELL.SORT

# Цена, по которой мы  можем купить BTC
BUY.price <- BUY.SORT$BUY.price
# Объем BTC в долларах, который мы можем купить
BUY.volume.simple <- BUY.SORT$BUY.volume.USD
# Цена, по которой мы  можем продать BTC
SELL.price <- SELL.SORT$SELL.price
# Объем BTC в долларах, который мы можем продать
SELL.volume.simple <- SELL.SORT$SELL.volume.USD

# Курс с учетом комиссии
BUY.price <- (1+a)*BUY.price
SELL.price <- (1-b)*SELL.price

# Вычисляем кумуляту BUY и SELL
BUY.volume <- BUY.volume.simple[1]
for (h in 2:length(BUY.volume.simple)) BUY.volume[h] <- BUY.volume[h-1]+BUY.volume.simple[h]
SELL.volume <- SELL.volume.simple[1]
for (s in 2:length(SELL.volume.simple)) SELL.volume[s] <- SELL.volume[s-1]+SELL.volume.simple[s]

# Формируем пары цена-объем (кумулятивный)
BUY <- data.frame(BUY.price,BUY.volume)
#BUY
SELL <- data.frame(SELL.price,SELL.volume)
#SELL

# Кумуляты BUY и SELL по объему в USD
png(file="Cumulative curves.png", bg="transparent") # Запись в файл
plot(BUY.price,BUY.volume, type="l", xlab="Price in USD", ylab="Volume in USD", xlim=c(min(BUY.price,SELL.price),max(BUY.price,SELL.price)), ylim=c(min(BUY.volume,SELL.volume),max(BUY.volume,SELL.volume)), col="red", main="Cumulative curves")
lines(SELL.price,SELL.volume, col="green")
dev.off() # Закрытие окна графика

# Определяем - будет ли сделка
BUY.price.min <- min(BUY$BUY.price)
SELL.price.max <- max(SELL$SELL.price)
if (BUY.price.min >= SELL.price.max) stop("NO DEAL!") else print("WE'll DEAL!")
# Цена BUY, до которой мы можем покупать, если будет соответствующий объем 
BUY.price.limit <- SELL.price.max
#print("Limit good BUY price")
#BUY.price.limit

# Оставляем только "хорошие" ордера
BUY.GOOD <- BUY[BUY$BUY.price < BUY.price.limit,]
BUY.GOOD
#BUY.GOOD
SELL.GOOD <- SELL[SELL$SELL.price > BUY.price.min,]
SELL.GOOD

# Определяем максимальный объем сделки
# Объем, который не принесет убытки
VOLUME.limit.max <- min(max(BUY.GOOD$BUY.volume),max(SELL.GOOD$SELL.volume))
VOLUME.limit <- min(VOLUME.limit.max,VOLUME.limit.our)
#VOLUME.limit <- VOLUME.limit.max
VOLUME.limit

# Переменные для анализа
VOLUME.CURR <- 0
Profit.USD <-0
Amount.USD <-0
Function.Prise.weight.BUY <-0
Function.Prise.weight.SELL <-0

for (k in 1:k.max) {
  VOLUME.CURR <- VOLUME.CURR+1/k.max*VOLUME.limit
  # Находим текущую среднюю BUY цену с учетом объемов ордеров
  i <- 1
  MINUS <- BUY.GOOD$BUY.volume[i]*BUY.GOOD$BUY.price[i]
  while (BUY.GOOD$BUY.volume[i]<VOLUME.CURR-1) {
    i <- i+1
    MINUS <- MINUS+(BUY.GOOD$BUY.volume[i]-BUY.GOOD$BUY.volume[i-1])*BUY.GOOD$BUY.price[i]
  }
  #if (BUY.GOOD$BUY.volume[j]>VOLUME.CURR) MINUS <- MINUS-(BUY.GOOD$BUY.volume[i]-VOLUME.CURR)*BUY.GOOD$BUY.price[i]
  MINUS <- MINUS-(BUY.GOOD$BUY.volume[i]-VOLUME.CURR)*BUY.GOOD$BUY.price[i]
  # Средняя текущая BUY цена
  Prise.weight.BUY <- MINUS/VOLUME.CURR
  Function.Prise.weight.BUY[k] <- Prise.weight.BUY
  # Находим текущую среднюю SELL цену с учетом объемов ордеров
  j <- 1
  PLUS <- SELL.GOOD$SELL.volume[j]*SELL.GOOD$SELL.price[j]
  while (SELL.GOOD$SELL.volume[j]<VOLUME.CURR-1) {
    j <- j+1
    PLUS <- PLUS+(SELL.GOOD$SELL.volume[j]-SELL.GOOD$SELL.volume[j-1])*SELL.GOOD$SELL.price[j]
  }
  #if (SELL.GOOD$SELL.volume[j]>VOLUME.CURR) PLUS <- PLUS-(SELL.GOOD$SELL.volume[j]-VOLUME.CURR)*SELL.GOOD$SELL.price[j]
  PLUS <- PLUS-(SELL.GOOD$SELL.volume[j]-VOLUME.CURR)*SELL.GOOD$SELL.price[j]  
  # Средняя текущая SELL цена
  Prise.weight.SELL <- PLUS/VOLUME.CURR
  Function.Prise.weight.SELL[k] <- Prise.weight.SELL
  # Доход
  PERCENT <- (Prise.weight.SELL-Prise.weight.BUY)/Prise.weight.BUY
  PROFIT <- PERCENT*VOLUME.CURR
  Profit.USD[k] <- PROFIT
  Amount.USD[k] <- VOLUME.CURR
}

# Средневзвешенные по объему цены
#Function.Prise.weight.BUY
#Function.Prise.weight.SELL
png(file="Price-Amount relation.png", bg="transparent") # Запись в файл
plot(Amount.USD, Function.Prise.weight.BUY, ylab="Prise.USD", ylim=c(min(Function.Prise.weight.BUY),max(Function.Prise.weight.SELL)), type="l", col="red",  main="Price-Amount relation")
lines(Amount.USD, Function.Prise.weight.SELL, col="green")
dev.off() # Закрытие окна графика

# Вывод результатов
ALL.plot.data <- data.frame(Amount.USD,Profit.USD)
#ALL.plot.data
png(file="Profit-Amount relation.png", bg="transparent") # Запись в файл
plot(ALL.plot.data, type="l", main="Profit-Amount relation")
dev.off() # Закрытие окна графика
print("THE MAXIMAL PROFIT AND OPTIMAL AMOUNT")
BEST.plot.data <- ALL.plot.data[ALL.plot.data$Profit.USD == max(Profit.USD),]
round(BEST.plot.data,0)
# Запись результата в файл
write.table(file="maxprofit.csv", round(BEST.plot.data,0), row.names=F, sep=",", quote=F)

# Подсчет процента доходности
TOBEST.plot.data <- ALL.plot.data[ALL.plot.data$Amount.USD <= BEST.plot.data[[1]],]
TOBEST.plot.data$PERCENT.per.Amount <- TOBEST.plot.data$Profit.USD*100/TOBEST.plot.data$Amount.USD
png(file="Profit Percent-Amount relation.png", bg="transparent") # Запись в файл
plot(TOBEST.plot.data$PERCENT.per.Amount~TOBEST.plot.data$Amount.USD, xlab="Amount.USD", ylab="Percent", type="l", main="Amount-Profit Percent relation")
dev.off() # Закрытие окна графика

################### The END #######################################

