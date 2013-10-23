#AUTHOR: Robert Clements
#DATE: 11/06/2012

##WEIGHTED (INHOMOGENEOUS) L-FUNCTION


##ONE PACKAGE NEEDS TO BE INSTALLED: SPATSTAT

##INPUT: PATH TO CATALOG, PATH TO FORECAST, PROPORTION OF FORECAST PERIOD BEING TESTED, ALPHA LEVEL TO CREATE 100(1-ALPHA)% CONFIDENCE BOUNDS, PATH TO SAVE OUTPUT

##OUPUT: R, L(R), LOWER CONFIDENCE BOUND, UPPER CONFIDENCE BOUND

#CATALOG - EARTHQUAKE CATALOG (NOTE: UNLESS ONLY ONE DAY IS BEING TESTED, DAILY FORECAST CATALOGS NEED TO BE COMBINED BEFORE USING THIS FUNCTION)
#FORECAST - CSEP FORECAST (NOTE:  UNLESS ONLY ONE DAY IS BEING TESTED, DAILY FORECASTS WILL NEED TO BE COMBINED BEFORE USING THIS FUNCTION)
#PROPORTION - PROPORTION OF TIME BEING TESTED; DEFAULT = 1
#ALPHA - DEFAULT  =  .05 FOR 95% CONFIDENCE BOUNDS

wl.csep <- function(catalog.name, forecast.name, prop=1, alpha=.05, path=NULL)
{
	#LOAD LIBRARY
	library(spatstat)
	
	catalog <- read.table(catalog.name, header=F, col.names=c("L","l","dy","m","d","mag","depth","h","min","s","he","de","me", "1","2","3"))
	forecast <- read.table(forecast.name, header=F)
	
	if(nrow(catalog) == 0)
	{
		y <- c()
		write.table(y, file = path, row.names = F)
		return(y)
	}
		
	
	catalog <- catalog[,1:2]

	#CREATE THE OBSERVATION REGION
	temp <- forecast[which(forecast[, 10] == 1), 1:4]
	rows <- length(unique(temp[, 4]))

	x.left <- c(); x.right <- c(); y.left <- c(); y.right <- c()
	for(i in 1:rows) {
		mtop <- max(temp[,4])
		row <- temp[which(temp[ ,4] == mtop), ]
		xl <- min(row[,1])
		xr <- max(row[,2])
		x.left <- c(x.left, rep(xl, 2))
		x.right <- c(x.right, rep(xr, 2))
		y.left <- c(y.left, row[1,4], row[1,3])
		y.right <- y.left
		temp <- temp[which(temp[ ,4] != mtop), ]
	}
	
	x.right <- rev(x.right)
	y.right <- rev(y.right)

	top <- cbind(x.left, y.left)
	bottom <- cbind(x.right, y.right)

	space <- rbind(top, bottom)  
	space <- unique(space)  
  window<-owin(poly=list(x=space[,1], y=space[,2]))
    
  names(forecast) <- c("minlon", "maxlon", "minlat", "maxlat", "mindepth", "maxdepth", "minmag", "maxmag", "rate", "mask")
    
  #SCALE THE RATES BASED ON PROPORTION BEING TESTED
  forecast$rate <- forecast$rate * prop
    
  #FOR CONFIDENCE BOUNDS, GET TOTAL NUMBER OF EXPECTED EARTHQUAKES AND AREA OF THE SPACE. 
  temp <- forecast[which(forecast$mask == 1), ]
  total <- sum(temp$rate)
  temp <- unique(forecast[which(forecast$mask == 1), 1:4])
	area <- sum(abs((temp$maxlon - temp$minlon)*(temp$maxlat - temp$minlat)))
	l.mult <- qnorm(alpha/2)
	u.mult <- -l.mult
    
  #GET THE CONDITIONAL INTENSITY AND INTEGRATE OVER MAGNITUDES AND DEPTH
  volume <- abs((forecast$maxlon-forecast$minlon)*(forecast$maxlat-forecast$minlat))
  intensity <- forecast$rate/volume
  forecast$rate <- intensity
    
  tag <- paste(forecast[,1],forecast[,2],forecast[,3],forecast[,4],forecast[,5],forecast[,6],forecast[,10])    
  forecast <- cbind(forecast, tag)
  agg <- aggregate(forecast$rate, list(forecast$tag), sum)
  forecast.new <- unique(forecast[ ,c(1:6, 10, 11)])
  names(agg) <- c("x", "rate")
  positions <- match(agg$x, forecast.new$tag)
    
  forecast.new[positions, 9] <- agg$rate
    
  #MATCH EARTHQUAKES FROM THE CATALOG TO THEIR PIXELS
  rates <- data.frame()
	for(i in 1:nrow(catalog)) {
		rates <- rbind(rates, forecast.new[which((catalog[i,1] >= forecast.new[,1])&(catalog[i,1] < forecast.new[,2])&(catalog[i,2] >= forecast.new[,3])&(catalog[i,2] < forecast.new[,4])) , ])
	}
    
  catalog.new <- cbind(catalog, rates[ ,c(9, 7)])
  catalog.new <- catalog.new[which(catalog.new$mask==1), ] 
	
	#PERFORM THE WEIGHTED (INHOMOGENEOUS) L-FUNCTION
	lambda <- catalog.new[ , 3]
	pp <- catalog.new[ ,1:2]
	pp <- as.ppp(pp, window)
	l.fctn <- Linhom(pp, lambda, correction="Ripley")
	r <- l.fctn$r
	l.function <- l.fctn$iso - r
	l.bound <- l.mult * sqrt(2 * pi * area) * r / total
	u.bound <- u.mult * sqrt(2 * pi * area) * r / total
	y <- data.frame(cbind(r, l.function, l.bound, u.bound))
	
	if(!is.null(path)) {
	  write.table(y, file = path, row.names = F)
	}
	return(y)
}

wl.csep(inputCatalog, inputForecast, forecastPeriodProportion, alpha, resultFile)