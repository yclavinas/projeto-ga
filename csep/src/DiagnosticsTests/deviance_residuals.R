#AUTHOR: Robert Clements
#DATE: 11/06/2012

##DEVIANCE RESIDUALS

##INPUT: PATH TO CATALOG1, PATH TO FORECAST1, PATH TO CATALOG2, PATH TO FORECAST2, PROPORTION OF FORECAST PERIOD BEING TESTED, MAGNITUDE RANGE TO TEST, PATH TO SAVE OUTPUT

##OUPUT: EACH BIN AND EACH BINS DEVIANCE RESIDUAL VALUE FOR FORECAST 1 VS. FORECAST 2

#NOTE: FOR DAILY FORECAST MODELS, THIS FUNCTION CAN BE USED ON EACH DAY AND THEN THE RESIDUALS MAY BE SUMMED UP OVER TIME. 
#      FOR 3-MONTH MODELS, THIS FUNCTION CAN BE USED ON EACH 3-MONTH PERIOD AND THEN THE RESIDUALS MAY BE SUMMED UP OVER TIME.

#CATALOG1 - EARTHQUAKE CATALOG FOR FORECAST 1
#FORECAST1 - CSEP FORECAST
#CATALOG2 - EARTHQUAKE CATALOG FOR FORECAST 2
#FORECAST2 - CSEP FORECAST
#PROPORTION - PROPORTION OF 5 YEARS BEING TESTED; DEFAULT = 1
#MAG - VECTOR OF MAGNITUDE RANGES TO EXTRACT AND TEST; DEFAULT = ALL MAGNITUDES. EXAMPLE: MAG = c(4.95, 5.05) 

deviance.csep <- function(catalog1.name, forecast1.name, catalog2.name, forecast2.name, prop=1, mag=1, path=NULL)
{
  if(file.info(catalog1.name)$size > 0) {
	  catalog1 <- read.table(catalog1.name, header=F, col.names=c("L","l","dy","m","d","mag","depth","h","min","s","he","de","me", "1","2","3"))
	  catalog1 <- catalog1[,c("L","l","mag")]
  } else {
    catalog1 <- data.frame()
  }
  forecast1 <- read.table(forecast1.name, header=F)
  if(file.info(catalog2.name)$size > 0) {
	  catalog2 <- read.table(catalog2.name, header=F, col.names=c("L","l","dy","m","d","mag","depth","h","min","s","he","de","me","1","2","3"))
	  catalog2 <- catalog2[,c("L","l","mag")]
  } else {
    catalog2 <- data.frame()
  }
  forecast2 <- read.table(forecast2.name, header=F)	
	
  
	catalog3 <- rbind(catalog1, catalog2)
  if(nrow(catalog3) > 0) {
	  catalog.ult <- catalog3[duplicated(catalog3), ]
  } else {
    catalog.ult <- catalog3
  }
    
  if(mag == 1)
	  cat("mag = all magnitude ranges\n")
  else
		cat("mag = ", mag, "\n")
    
  f.new1 <- data.frame(); forecast.new <- data.frame()
  forecast <- forecast1; catalog <- catalog.ult
  for(i in 1:2) {
    f.new1 <- forecast.new    
    names(forecast) <- c("minlon", "maxlon", "minlat", "maxlat", "mindepth", "maxdepth", "minmag", "maxmag", "rate", "mask")
    
  	#SCALE THE RATES BASED ON PROPORTION BEING TESTED
  	forecast$rate <- forecast$rate * prop
    
  	#GET THE CONDITIONAL INTENSITY AND INTEGRATE OVER MAGNITUDES AND DEPTH
  	volume <- abs((forecast$maxlon-forecast$minlon)*(forecast$maxlat-forecast$minlat))
  	intensity <- forecast$rate/volume
  	forecast$rate <- intensity
    
  	if(length(mag) == 2) {
  		forecast <- forecast[which((forecast$minmag >= mag[1]) & (forecast$maxmag <= mag[2])),]
      if(nrow(catalog) > 0) {
  		  catalog <- catalog[which((catalog[,3] >= mag[1]) & (catalog[,3] < mag[2])),]
      }
  	}
    		
  	tag <- paste(forecast[,1],forecast[,2],forecast[,3],forecast[,4],forecast[,5],forecast[,6],forecast[,10])    
  	forecast <- cbind(forecast, tag)
  	agg <- aggregate(forecast$rate, list(forecast$tag), sum)
  	forecast.new <- unique(forecast[ ,c(1:6, 10, 11)])
    
  	positions <- match(agg[ ,1], forecast.new$tag)
  	rate <- rep(0, nrow(forecast.new))
  	forecast.new <- cbind(forecast.new, rate)
  	forecast.new[positions, 9] <- agg[ ,2]
    
  	count <- rep(0, nrow(forecast.new))
    
  	#MATCH EARTHQUAKES FROM THE CATALOG TO THEIR PIXELS
    if(nrow(catalog) > 0) {
		  for(i in 1:nrow(catalog)) {
			  place <- which((catalog[i,1] >= forecast.new[,1])&(catalog[i,1] < forecast.new[,2])&(catalog[i,2] >= forecast.new[,3])&(catalog[i,2] < forecast.new[,4]))
			  count[place] <- count[place]+1
		  }
    }
  	forecast.new <- cbind(forecast.new, count)
    forecast <- forecast2; catalog <- catalog.ult
  } 
	
	f.new2 <- forecast.new
	
	#REPLACE ANY RATES OF 0 WITH SOMETHING VERY SMALL
	log.lambda1 <- rep(0, nrow(f.new1))
	log.lambda2 <- rep(0, nrow(f.new2))
	logic1 <- f.new1$rate == 0
	logic2 <- f.new2$rate == 0
	f.new1[logic1, 9] <- min(f.new1[which(f.new1$rate > 0), 9])*.01
	f.new2[logic2, 9] <- min(f.new2[which(f.new2$rate > 0), 9])*.01
	log.lambda1 <- log(f.new1$rate)
	log.lambda2 <- log(f.new2$rate)
		
	#AREA OF CELLS
	area1 <- abs((f.new1$maxlon-f.new1$minlon)*(f.new1$maxlat-f.new1$minlat))
	area2 <- abs((f.new2$maxlon-f.new2$minlon)*(f.new2$maxlat-f.new2$minlat))
	
	#SUM OF THE LOG LAMBDAS IN EACH CELL
	sum1 <- log.lambda1*f.new1$count
	sum2 <- log.lambda2*f.new2$count
	
	#INTEGRAL IN EACH CELL
	avoid1 <- f.new1$rate*area1
	avoid2 <- f.new2$rate*area2
	
	#DEVIANCE IN EACH CELL
	deviance <- sum1-avoid1-(sum2-avoid2)
	
	#SET DEVIANCE IN MASKED CELLS TO 0
	masked1<-f.new1$mask == 0
	masked2<-f.new2$mask == 0
	deviance[masked1] <- 0
	deviance[masked2] <- 0

	y <- data.frame(cbind(f.new1[, c(1:4,7)], f.new2[,7], deviance))
	names(y) <- c("minlon", "maxlon", "minlat", "maxlat", "mask1", "mask2", "deviance")
	
	if(!is.null(path)) {
	  write.table(y, file = path, row.names = F)
	}
	return(y)
}

deviance.csep(inputCatalog1, inputForecast1, inputCatalog2, inputForecast2, forecastPeriodProportion, magnitudeRange, resultFile)