def filtro_terremoto():
	f = open('catalog_fnet_1997_20130429_f3.txt', 'r')
	g = open('filtro_terremotos.txt', 'w')

	i = 0

	for line in f:
		if( i != 12):
			i += 1
		if( i == 12):
			data = str.split(line)
			if(float(data[8]) < 20.00):
				g.write(line)			
				# raw_input("continue")

	f.close()
	g.close()

def mar_terra():
	# http://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&sensor=true_or_false
	# http://maps.googleapis.com/maps/api/elevation/json?locations=39.7391536,-104.9847034&sensor=true
	import urllib2
	# string = 'http://maps.googleapis.com/maps/api/geocode/xml?latlng='+'34.9000,139.1000'+'&sensor=false'
	# response = urllib2.urlopen(string)
	# html = response.read()

	f = open('filtro_terremotos.txt', 'r')
	# g = open('filtro_terremoto_terra.txt', 'r')
	# count_lines = len(g.readlines())
	# print count_lines
	# g.close()

	g = open('filtro_terremoto_terra.txt', 'a')

	i = 0
	for line in f:
		if( i != 12):
			i += 1
		if( i == 12):
			data = str.split(line)
			print data
			string = 'http://maps.googleapis.com/maps/api/elevation/json?locations='+data[6]+','+data[7]+'&sensor=false'
			response = urllib2.urlopen(string)
			html = response.readlines()
			data = str.split(html[3])
			if(data[2] == '"OVER_QUERY_LIMIT"'):
				print "So mais tarde.... :("
				f.close()
				g.close()
				exit(0)
			newfloat = float(data[2].replace(",", ""))
			if ( newfloat >= 0.0):
				g.write(line)

	f.close()
	g.close()


def main():
	mar_terra()



if __name__ == "__main__":
    main()