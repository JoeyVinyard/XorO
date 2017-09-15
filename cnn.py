from PIL import Image
import random
import math

def genFilter(n):
	f = []
	for i in range(n*n):
		f.append(round(random.uniform(-1,1),2))
	return f

def handleNum(value):
	return -(round(value/127.5,2)-1)

def getPointForConv(x,y,map):
	if x>=len(map[0]):
		return 0
	elif x<0:
		return 0
	elif y>=len(map):
		return 0
	elif y<0:
		return 0
	else:
		return map[y][x]

def convolute(x,y,filter, map):
	fltrRowLength = math.sqrt(len(filter))
	offset=math.floor(fltrRowLength/2)/-1
	total = 0
	for i, value in enumerate(filter):
		xC = int(x+offset+(i%fltrRowLength))
		yC = int(y+offset+(math.floor(i/fltrRowLength)))
		total += getPointForConv(xC,yC,map)*filter[i]
	total/=len(filter)
	return round(total,2)

def poolPoint(x,y,map):
	return max([getPointForConv(x,y,map),getPointForConv(x,y+1,map),getPointForConv(x+1,y,map),getPointForConv(x+1,y+1,map)])

def poolMap(map):
	pooledMap = [[0]*math.ceil(len(map)/2) for n in range(math.ceil(len(map)/2))]
	for y, row in enumerate(pooledMap):
		for x, value in enumerate(row):
			pooledMap[y][x] = poolPoint(2*x,2*y,map)
	return pooledMap

img = Image.open("x.png").convert("L")

data = img.getdata()
width, height = img.size

# Number map for pixels in image
numberMap = [[0]*height for n in range(width)]

xC, yC = 0,0

for v in data:
	numberMap[yC][xC] = handleNum(v)
	xC+=1
	if xC == width:
		xC=0
		yC+=1

fltr = 	[1,-1,-1,
		-1,1,-1,
		-1,-1,1] #3x3 grid

while len(numberMap)>1:
	xC, yC = 0,0
	convoluted = [[0]*len(numberMap) for n in range(len(numberMap[0]))]
	for n in numberMap:
		xC=0
		for a in n:
			convoluted[yC][xC] = (convolute(xC,yC,fltr,numberMap))
			xC+=1
		yC+=1

	print("Convoluted")
	for d in convoluted:
		print(d)

	numberMap = poolMap(convoluted)
	print("Pooled:")
	for d in numberMap:
			print(d)

	print("-------------------------")

for d in numberMap:
		print(d)

print(genFilter(5))