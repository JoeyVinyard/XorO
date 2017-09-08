from PIL import Image
import math

def handleNum(value):
	return -(round(value/127.5,2)-1)

def getPointForConv(x,y,map):
	# print("Returning value at:",x,y)
	if x>=width:
		return 0
	elif x<0:
		return 0
	elif y>=height:
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

xC, yC = 0,0
convoluted = [[0]*height for n in range(width)]

convolute(0,0,fltr,numberMap)

for n in numberMap:
	xC=0
	for a in n:
		convoluted[yC][xC] = (convolute(xC,yC,fltr,numberMap))
		xC+=1
	yC+=1

for d in numberMap:
	print(d)
print("----------------------")
for c in convoluted:
	print(c)