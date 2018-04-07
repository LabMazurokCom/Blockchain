##########  Рассчет дохода Арбитража  ############

# Очистка переменных
rm(list=ls())

# Цена, по которой мы  можем купить BTC
BID.price <- c(10.1,10.3,10.4,10.7,10.9,11.2,11.3)
# Комиссия на BID и курс с учетом комиссии
a <- 0.02
BID.price <- (1+a)*BID.price
# Объем (кумулятивный) BTC в доллах, который мы можем купить
BID.volume <- c(200,500,600,800,100,1100,1300)
# Цена, по которой мы  можем продать BTC
ASK.price <- c(10.8,10.6,10.4,10.3,10.2,9.9,9.7)
# Комиссия на ASK и курс с учетом комиссии
b <- 0.01
ASK.price <- (1-b)*ASK.price
# Объем (кумулятивный) BTC в долларах, который мы можем продать
ASK.volume <- c(100,300,400,700,1000,1200,1500)
# Формируем пары цена-объем
BID <- data.frame(BID.price,BID.volume)
BID
ASK <- data.frame(ASK.price,ASK.volume)
ASK

# Определяем - будет ли сделка
BID.price.min <- min(BID$BID.price)
ASK.price.max <- max(ASK$ASK.price)
if (BID.price.min > ASK.price.max) print("NO DEAL!") else print("WE'll DEAL!")
# Цена BID, до которой мы пожем покупать, если будет соответствующий объем 
BID.price.max <- max(BID$BID.price)
BID.price.limit <- min(BID.price.max,ASK.price.max)
print("Limit good BID price")
BID.price.limit

# Оставляем только хорошие ордера
BID.GOOD <- BID[BID$BID.price < BID.price.limit,]
BID.GOOD
ASK.GOOD <- ASK[ASK$ASK.price > BID.price.min,]
ASK.GOOD

# Определяем максимальный объем сделки
print("The maximum recommended volume")
VOLUME.BEST <- min(max(BID.GOOD$BID.volume),max(ASK.GOOD$ASK.volume))
VOLUME.BEST
# Объем в долларах, на который мы будем совершать сделку
VOLUME.CURR <- VOLUME.BEST

# Находим среднюю BID цену с учетом объемов ордеров
i <- 1
MINUS <- BID.GOOD$BID.volume[i]*BID.GOOD$BID.price[i]
while (BID.GOOD$BID.volume[i] < VOLUME.CURR) {
  i <- i+1
  MINUS <- MINUS+(BID.GOOD$BID.volume[i]-BID.GOOD$BID.volume[i-1])*BID.GOOD$BID.price[i]
  }
if (BID.GOOD$BID.volume[i]>VOLUME.CURR) MINUS <- MINUS-(BID.GOOD$BID.volume[i]-VOLUME.CURR)*BID.GOOD$BID.price[i]
Prise.weight.BID <- MINUS/VOLUME.CURR
# Средняя BID цена
Prise.weight.BID

# Находим среднюю ASK цену объемов ордеров
j <- 1
PLUS <- ASK.GOOD$ASK.volume[j]*ASK.GOOD$ASK.price[j]
while (ASK.GOOD$ASK.volume[j] < VOLUME.CURR) {
  j <- j+1
  PLUS <- PLUS+(ASK.GOOD$ASK.volume[j]-ASK.GOOD$ASK.volume[j-1])*ASK.GOOD$ASK.price[j]
}
ASK.GOOD$ASK.volume[j]-VOLUME.CURR
if (ASK.GOOD$ASK.volume[j]>VOLUME.CURR) MINUS <- MINUS-(ASK.GOOD$ASK.volume[j]-VOLUME.CURR)*ASK.GOOD$ASK.price[j]
Prise.weight.ASK <- PLUS/VOLUME.CURR
# Средняя ASK цена
Prise.weight.ASK

# Доход
PERCENT <- (Prise.weight.ASK-Prise.weight.BID)/Prise.weight.BID
print("PERCENT")
round(PERCENT*100,2)
PROFIT <- PERCENT*VOLUME.CURR
print("WE CAN GET PROFIT")
round(PROFIT,2)

######## THE END  ##############

