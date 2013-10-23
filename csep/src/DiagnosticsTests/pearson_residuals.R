#AUTHOR: Robert Clements
#DATE: 11/06/2012

##PEARSON OR RAW RESIDUALS

##INPUT: PATH TO CATALOG, PATH TO FORECAST, PROPORTION OF FORECAST PERIOD BEING TESTED, MAGNITUDE RANGE TO TEST, PATH TO SAVE OUTPUT (IF WANTED)

##OUPUT: EACH BIN AND EACH BINS RESIDUAL VALUE

#NOTE: FOR DAILY FORECAST MODELS, THIS FUNCTION CAN BE USED ON EACH DAY AND THEN THE RESIDUALS MAY BE SUMMED UP OVER TIME. 
#      FOR 3-MONTH MODELS, THIS FUNCTION CAN BE USED ON EACH 3-MONTH PERIOD AND THEN THE RESIDUALS MAY BE SUMMED UP OVER TIME.

#CATALOG - EARTHQUAKE CATALOG (NOTE: UNLESS ONLY ONE DAY IS BEING TESTED, DAILY CATALOGS NEED TO BE COMBINED BEFORE USING THIS FUNCTION)
#FORECAST - CSEP FORECAST (NOTE: UNLESS ONLY ONE DAY IS BEING TESTED, DAILY FORECASTS NEED TO BE COMBINED BEFORE USING THIS FUNCTION)
#PROPORTION - PROPORTION OF 5 YEARS BEING TESTED; DEFAULT = 1
#MAG - VECTOR OF MAGNITUDE RANGES TO EXTRACT AND TEST; DEFAULT = ALL MAGNITUDES. EXAMPLE: MAG = c(4.95, 5.05) 

pearson.csep <- function(catalog.name, forecast.name, prop=1, mag=1, path=NULL)
{
	if(file.info(catalog.name)$size > 0) {
	  catalog <- read.table(catalog.name, header=F, col.names=c("L","l","dy","m","d","mag","depth","h","min","s","he","de","me", "1","2","3"))
	  catalog <- catalog[,c("L","l","mag")]
	} else {
    catalog <- NULL
	}
  
  forecast <- read.table(forecast.name, header=F)
	
	
  names(forecast) <- c("minlon", "maxlon", "minlat", "maxlat", "mindepth", "maxdepth", "minmag", "maxmag", "rate", "mask")
    
  #SCALE THE RATES BASED ON PROPORTION BEING TESTED
  forecast$rate <- forecast$rate * prop
    
  #GET THE CONDITIONAL INTENSITY AND INTEGRATE OVER MAGNITUDES AND DEPTH
  volume <- abs((forecast$maxlon-forecast$minlon)*(forecast$maxlat-forecast$minlat))
  intensity <- forecast$rate/volume
  forecast$rate <- intensity
  if(mag == 1)
	  cat("mag = all magnitude ranges\n")
  else
	  cat("mag = ", mag, "\n")
    
  if(length(mag) == 2) {
    forecast <- forecast[which((forecast$minmag >= mag[1]) & (forecast$maxmag <= mag[2])),]
    if(!is.null(catalog)) {
      catalog <- catalog[which((catalog$mag >= mag[1]) & (catalog$mag < mag[2])),]
    }
  }
    
  tag <- paste(forecast$minlon,forecast$maxlon,forecast$minlat,forecast$maxlat,forecast$mindepth,forecast$maxdepth,forecast$mask)    
  forecast <- cbind(forecast, tag)
  agg <- aggregate(forecast$rate, list(forecast$tag), sum)
  forecast.new <- unique(forecast[ ,c(1:6, 10, 11)])
    
  positions <- match(agg[ ,1], forecast.new$tag)
  rate <- rep(0, nrow(forecast.new))
  forecast.new <- cbind(forecast.new, rate)
  forecast.new[positions, 9] <- agg[ ,2]
    
  count <- rep(0, nrow(forecast.new))
    
  #MATCH EARTHQUAKES FROM THE CATALOG TO THEIR PIXELS
  if(!is.null(catalog)) {
	  for(i in 1:nrow(catalog)) {
	  	place <- which((catalog[i,1] >= forecast.new[,1])&(catalog[i,1] < forecast.new[,2])&(catalog[i,2] >= forecast.new[,3])&(catalog[i,2] < forecast.new[,4]))
		  count[place] <- count[place]+1
	  }
  }
    
  forecast.new <- cbind(forecast.new, count) 
	
	#COMPUTE RAW RESIDUALS IF LAMBDA=0 FOR ANY UNMASKED CELL
	if(any((forecast.new$mask == 1) & (forecast.new$rate == 0))) {
		integral <- forecast.new$rate * abs((forecast.new[ ,2] - forecast.new[ ,1])*(forecast.new[ ,4]-forecast.new[ ,3]))
		raw.residual <- forecast.new$count - integral
		raw.residual[which(forecast.new$mask == 0)] <- 0
		y <- data.frame(cbind(forecast.new[, c(1:4, 7, 9, 10)], raw.residual))
	}
		
	#COMPUTE PEARSON RESIDULAS
	if(!any((forecast.new$mask == 1) & (forecast.new$rate == 0))) {
		sqrt.lambda <- sqrt(forecast.new$rate)
		inv.sqrt.lambda <- sqrt.lambda^-1
		sum <- inv.sqrt.lambda * forecast.new$count
		integral <- sqrt.lambda * abs((forecast.new[,2]-forecast.new[,1])*(forecast.new[,4]-forecast.new[,3]))
		
		P.residual <- sum - integral
		P.residual[which(forecast.new$mask == 0)] <- 0
		y <- data.frame(cbind(forecast.new[, c(1:4, 7, 9, 10)], P.residual))
	}
	if(!is.null(path)) {	
    write.table(y, file = path, row.names = F)
	}
	return(y)
}

pearson.csep(inputCatalog, inputForecast, forecastPeriodProportion, magnitudeRange, resultFile)