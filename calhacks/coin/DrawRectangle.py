import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np

class DrawRectangle():
	def __init__(self, img, rectangles):
		self.img = img
		self.rectangles = rectangles

	def produceImg(self, path = '/Users/ryancheng/Desktop/calhacks/coin/media/plot.png'):
		print("URL: " + self.img)
		im = np.array(Image.open(self.img), dtype=np.uint8)

		# Create figure and axes
		fig,ax = plt.subplots(1)

		# Display the image
		ax.imshow(im)

		# Create a Rectangle patch
		rectangles = self.rectangles
		for rect in rectangles:
			print (rect)
			left = rect[1]["left"]
			top = rect[1]["top"]
			width = rect[1]["width"]
			height = rect[1]["height"]
			name = rect[0]
			rect = patches.Rectangle((left, top), width, height,linewidth=1,edgecolor='r',facecolor='none')

			# Add the patch to the Axes
			ax.add_patch(rect)

			#Add text
			font = {'family': 'serif',
	        	'color':  'white',
    	    	'weight': 'normal',
        		'size': 16,
        		'backgroundcolor': 'grey'
        	}

			ax.text(left,top - height / 8,name, fontdict = font)

		ax.xaxis.set_visible(False)
		ax.yaxis.set_visible(False)

		fig.savefig(path, bbox_inches = 'tight', pad_inches = 0)

#draw = DrawRectangle("/Users/ryancheng/Desktop/calhacks/coin/media/../media/studygroups/temp_vx4N0oW.png", [])
#draw.produceImg()