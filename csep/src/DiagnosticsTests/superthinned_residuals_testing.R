#AUTHOR: Robert Clements
#DATE: 11/06/2012

#SUPER-THINNED RESIDUALS TESTING


##ONE PACKAGE NEEDS TO BE INSTALLED: SPATSTAT

##INPUT: PATH TO FORECAST, PATH TO SUPER-THINNED RESIDUALS, K, ALPHA, PATH TO SAVE RESULTS (IF WANTED)

##OUTPUT: R, CENTERED WEIGHTED L-FUNCTION, UPPER BOUND, LOWER BOUND

#FORECAST - CSEP FORECAST USED TO PERFORM SUPERTHINNING
#SUPER-THINNED RESIDUALS - 
#K - THE K-VALUE USED DURING SUPER-THINNING; DEFAULT = 100
#ALPHA - 95*(100-ALPHA)% CONFIDENCE BOUNDS; DEFAULT = .05


superthin.test <- function(forecast.name, residuals.name, k=100, alpha=.05, path=NULL)
{
	#LOAD LIBRARIES
	library(spatstat)

	forecast <- read.table(forecast.name, header=F)
	residuals <- read.table(residuals.name, header=T)	

	names(forecast) <- c("minlon", "maxlon", "minlat", "maxlat", "mindepth", "maxdepth", "minmag", "maxmag", "rate", "mask")
	
	#CREATE THE OBSERVATION REGION
	temp <- forecast[which(forecast$mask == 1), 1:4]
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
	
	#CREATE A PPP OBJECT FOR USE WITH THE W L-FCTN
	locations <- cbind(residuals$lon, residuals$lat)
	points <- as.ppp(locations, W=window)
	
	#GET AREA OF THE SPACE FOR LAMBDAS
	temp <- forecast[which(forecast$mask==1), 1:4]
	temp <- unique(forecast[which(forecast$mask == 1), 1:4])
	area <- sum(abs((temp[ ,2] - temp[ ,1])*(temp[ ,4] - temp[ ,3])))
	
	#VECTOR OF LAMBDAS
	lambdas <- rep(k/area, points$n)
	
	#EXECUTE WEIGHTED L-FUNCTION
	l.fctn <- Linhom(points, lambdas, correction="Ripley", nlarge = 2*length(lambdas))
	r <- l.fctn$r
	w.c.l <- l.fctn$iso - r
	
	#CONFIDENCE BOUNDS
	
	z1 <- qnorm(alpha/2)
	z2 <- abs(z1)
	
	upper.bound <- z2 * sqrt(2 * pi * area) * r / k
	lower.bound <- z1 * sqrt(2 * pi * area) * r / k
	
	y <- data.frame(cbind(r, w.c.l, upper.bound, lower.bound))
	
	if(!is.null(path)) {
		write.table(y, path, row.names=F, col.names=T)
	}
	return(y)
}

superthin.test(inputForecast, inputResiduals, kValue, alpha, resultFile)