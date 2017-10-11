from PIL import Image
import random
import math

class cnn:
	def __init__(self, numChannels, image):
		self.numChannels = numChannels
		self.getImageData(image)
		self.buildChannels()
		self.main()
	def getImageData(self, image):
		data = img.getdata()
		width, height = img.size
		self.n = width

		# Number map for pixels in image
		self.numberMap = [[0]*width for n in range(height)]

		xC, yC = 0,0

		for v in data:
			self.numberMap[yC][xC] = self.normalizeNum(v)
			xC+=1
			if xC == width:
				xC=0
				yC+=1
	def buildChannels(self):
		self.channels = []
		for c in range(self.numChannels):
			self.channels.append([])
		for channel in self.channels:
			for layer in range(0,math.ceil(self.n/2)):
				channel.append(self.genFilter(3))
	def genFilter(self, n):
		f = []
		for i in range(n*n):
			f.append(round(random.uniform(-1,1),2))
		return f
	def normalizeNum(self, value):
		return -(round(value/127.5,2)-1)
	def normalizeFinal(self, value):
		return (value+1)/2
	def getPointForConv(self,x,y,map):
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
	def convolutePoint(self,x,y,filter, map):
		fltrRowLength = math.sqrt(len(filter))
		offset=math.floor(fltrRowLength/2)/-1
		total = 0
		for i, value in enumerate(filter):
			xC = int(x+offset+(i%fltrRowLength))
			yC = int(y+offset+(math.floor(i/fltrRowLength)))
			total += self.getPointForConv(xC,yC,map)*filter[i]
		total/=len(filter)
		return round(total,2)
	def convoluteMap(self, map, channel):
		xC, yC = 0,0
		fltr = channel.pop(0)
		convoluted = [[0]*len(map) for n in range(len(map[0]))]
		for n in map:
			xC=0
			for a in n:
				convoluted[yC][xC] = (self.convolutePoint(xC,yC,fltr,map))
				xC+=1
			yC+=1
		# print("Convoluted Map")
		# for a in convoluted:
		# 	print(a)
		# print("Filter")
		# print(fltr)
		
		return self.poolMap(convoluted, channel)
	def poolPoint(self,x,y,map):
		return max([self.getPointForConv(x,y,map),self.getPointForConv(x,y+1,map),self.getPointForConv(x+1,y,map),self.getPointForConv(x+1,y+1,map)])
	def poolMap(self,map,channel):
		pooledMap = [[0]*math.ceil(len(map)/2) for n in range(math.ceil(len(map)/2))]
		for y, row in enumerate(pooledMap):
			for x, value in enumerate(row):
				pooledMap[y][x] = self.poolPoint(2*x,2*y,map)
		# print("Pooled Map:")
		# for a in pooledMap:
		# 	print(a)
		if len(pooledMap) > 1:
			return self.convoluteMap(pooledMap, channel)
		return self.normalizeFinal(pooledMap[0][0])
	def main(self):
		for channel in self.channels:
			# print("Start Map")
			# for a in self.numberMap:
			# 	print(a)
			test = self.convoluteMap(self.numberMap,channel)
			print("Final convolution")
			print(test)

img = Image.open("x.png").convert("L")
cnn(3,img)
# data = img.getdata()
# width, height = img.size

# # Number map for pixels in image
# numberMap = [[0]*height for n in range(width)]

# xC, yC = 0,0

# for v in data:
# 	numberMap[yC][xC] = handleNum(v)
# 	xC+=1
# 	if xC == width:
# 		xC=0
# 		yC+=1

# fltr = 	[1,-1,-1,
# 		-1,1,-1,
# 		-1,-1,1] #3x3 grid

# while len(numberMap)>1:
# 	xC, yC = 0,0
# 	convoluted = [[0]*len(numberMap) for n in range(len(numberMap[0]))]
# 	for n in numberMap:
# 		xC=0
# 		for a in n:
# 			convoluted[yC][xC] = (convolute(xC,yC,fltr,numberMap))
# 			xC+=1
# 		yC+=1

# 	print("Convoluted")
# 	for d in convoluted:
# 		print(d)

# 	numberMap = poolMap(convoluted)
# 	print("Pooled:")
# 	for d in numberMap:
# 			print(d)

# 	print("-------------------------")

# for d in numberMap:
# 		print(d)

# print(genFilter(5))