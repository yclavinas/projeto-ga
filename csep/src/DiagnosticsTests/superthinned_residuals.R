#AUTHOR: Robert Clements
#DATE: 11/06/2012

##SUPER-THINNED RESIDUALS

##INPUT: PATH TO CATALOG, PATH TO FORECAST, K-VALUE, PROPORTION OF FORECAST PERIOD BEING TESTED, PATH TO SAVE RESIDUALS (IF WANTED), SEED FOR RANDOM NUMBER GENERATOR 

##OUTPUT: LON, LAT, AND MAG COORDINATES OF ALL THINNED RESIDUALS
#		  

#CATALOG - EARTHQUAKE CATALOG
#FORECAST - CSEP FORECAST
#K - NUMBER OF THINNED RESIDUALS TO RETAIN; DEFAULT = 100
#SEED - ANY INTEGER; DEFAULT = 1
#PROPORTION - PROPORTION OF 5 YEARS BEING TESTED; DEFAULT = 1			

superthin.csep<-function(catalog.name, forecast.name, k=100, prop=1, path=NULL, seed=1)
{
  if(file.info(catalog.name)$size > 0) {
    catalog <- read.table(catalog.name, header=F, col.names=c("L","l","dy","m","d","mag","depth","h","min","s","he","de","me", "1","2","3"))
    catalog <- catalog[,c("L","l","mag")]
  } else {
    catalog <- NULL
  }
	forecast <- read.table(forecast.name, header=F)
	
	names(forecast) <- c("minlon", "maxlon", "minlat", "maxlat", "mindepth", "maxdepth", "minmag", "maxmag", "rate", "mask")
	
	#SCALE THE RATES BASED ON PROPORTION OF PERIOD BEING TESTED
	forecast$rate <- forecast$rate * prop
	
	#CONVERT RATES TO CONDITIONAL INTENSITIES
	volume <- (forecast$maxlon-forecast$minlon)*(forecast$maxlat-forecast$minlat)*(forecast$maxdepth-forecast$mindepth)*(forecast$maxmag-forecast$minmag)
	forecast$rate <- forecast$rate / volume
	
	#GET AREA OF THE SPACE FOR THRESHOLD VALUE
	temp <- forecast[which(forecast$mask==1), 1:4]
	temp <- unique(forecast[which(forecast$mask == 1), 1:4])
	area <- sum(abs((temp[ ,2] - temp[ ,1])*(temp[ ,4] - temp[ ,3])))
	
	#SET THRESHOLD VALUE FOR THINNING AND SUPERPOSITION
	threshold <- k/(area * (forecast$maxdepth[1] - forecast$mindepth[1]) * (max(forecast$maxmag) - min(forecast$minmag)))
	
	
	#EXTRACT THE RATE FOR EACH EARTHQUAKE IN THE CATALOG
	rates <- data.frame()
  if(!is.null(catalog)) {
	  for(i in 1:nrow(catalog)) {
		  rates <- rbind(rates, forecast[which((catalog[i,1] >= forecast[,1])&(catalog[i,1] < forecast[,2])&(catalog[i,2] >= forecast[,3])&(catalog[i,2] < forecast[,4])&(catalog[i,3] >= forecast[,7])&(catalog[i,3] < forecast[,8])) , c(9, 10)])
	  }
	  #COMBINE CATALOG WITH RATES
	  catalog.new <- data.frame(cbind(catalog, rates))
	  
	  #KEEP EXTRACTED EARTHQUAKE RATES THAT FALL IN UNMASKED CELLS
	  catalog.new <- catalog.new[which(catalog.new$mask == 1), ]
  } else {
    catalog.new <- NULL
  }
	  
	
	#PERFORM RANDOM THINNING ON ALL OBSERVATIONS SUCH THAT THE RATE >= THRESHOLD 
  #CONSTRUCT THE SEEDS SO THAT RESULTS CAN BE REPRODUCED
  set.seed(seed)
  if(!is.null(catalog.new)) {    	    
    #SET PROBABILITY OF KEEPING EACH OBSERVATION
    prob <- threshold/catalog.new$rate
    u <- runif(length(prob)) 
          
    #RANDOMLY KEEP OR REMOVE OBSERVATIONS  
    retain <- (u<=prob)
    thinres <- catalog.new[retain, ]
    thinres.pts <- thinres[ ,c(1,2,3)]
    tag.thin <- rep(1, nrow(thinres.pts))
    thinres.pts <- cbind(tag.thin, thinres.pts)
  } else {
    thinres.pts <- data.frame()
  }
	
	if(nrow(thinres.pts) > 0)
		names(thinres.pts) <- c("tag", "lon", "lat", "mag")
        
  #SET THE SEED FOR THE SUPERPOSITION 
  set.seed(seed*2)
          
  #PERFORM SUPERPOSITION IN ALL BINS WITH RATE < THRESHOLD
  sim.pts.xloc <- c(); sim.pts.yloc <- c(); sim.pts.mloc <- c()
    
  sim.rate <- rep(0, nrow(forecast))
  sim.rate[which(forecast$rate < threshold)] <- threshold - forecast[which(forecast$rate < threshold), 9]
    
  sim.points <- rpois(rep(1,nrow(forecast)), sim.rate*volume)
  forecast.new <- cbind(forecast, sim.points)
          
  #SIMULATE 0 EARTHQUAKES IN MASKED CELLS
  if(any(forecast.new$mask == 0)) {
	  forecast.new[which(forecast.new$mask == 0), 11] <- 0
	}
	
	#LOCATIONS OF SIMULATED POINTS
	set.seed(seed*3)
	num.pts <- sum(forecast.new$sim.points)
	jitter <- runif(num.pts*3, 0, .1)
	sim.cells <- forecast.new[which(forecast.new[,11] > 0), ]
	
	place <- seq(1:nrow(sim.cells))
	duplicate <- c()
	for(i in 1:length(place)) {
		duplicate <- c(duplicate, rep(place[i], sim.cells[i, 11]))
	}
	
	sim.data <- sim.cells[duplicate, ]
	
	sim.pts.xloc <- sim.data$minlon + jitter[1:num.pts]
	sim.pts.yloc <- sim.data$minlat + jitter[(num.pts+1):(num.pts*2)]
	sim.pts.mloc <- sim.data$minmag + jitter[(num.pts*2+1):(num.pts*3)]
	
	sim.tag <- rep(2, length(sim.pts.xloc))	
	sim.pts <- data.frame(cbind(sim.tag, sim.pts.xloc, sim.pts.yloc, sim.pts.mloc))
	if(nrow(sim.pts) > 0) {
		names(sim.pts)<-c("tag", "lon", "lat", "mag")
	}
		
	#COMBINE THINNED AND SUPERPOSED POINTS
	if((nrow(sim.pts) > 0) & (nrow(thinres.pts) > 0)) {
		y <- rbind(thinres.pts, sim.pts)
	}
	if((nrow(sim.pts) == 0) & (nrow(thinres.pts) > 0)) {
		y <- thinres.pts
	}
	if((nrow(thinres.pts) == 0) & (nrow(sim.pts) > 0)) {
		y <- sim.pts
	}
	if((nrow(thinres.pts) == 0) & (nrow(sim.pts) == 0)) {
		stop("Super-thinned residuals consist of 0 points")
	}
     
  #OUTPUT SUPER-THINNED RESIDUALS
  if(!is.null(path)) {
  	write.table(y, path, row.names=F, col.names=T)
  }
	y
}

superthin.csep(inputCatalog, inputForecast, kValue, forecastPeriodProportion, resultFile, seedValue)