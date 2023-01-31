import cv2
import xml.etree.ElementTree as ET

FILE_NAME_ANOT = 'My_test2_1.png.xml'
FILE_NAME_PRED = 'My_test2_1_pred.png.xml'

def draw_box(frame, bbox, color=(255,0,0)):
	x1, y1, x2, y2 = bbox
	cv2.rectangle(frame, pt1=(x1, y1), pt2=(x2, y2), color=color, thickness=2)
	return frame

def IOU(box1, box2):
	""" We assume that the box follows the format:
		box1 = [x1,y1,x2,y2], and box2 = [x3,y3,x4,y4],
		where (x1,y1) and (x3,y3) represent the top left coordinate,
		and (x2,y2) and (x4,y4) represent the bottom right coordinate """
	x1, y1, x2, y2 = box1	
	x3, y3, x4, y4 = box2
	x_inter1 = max(x1, x3)
	y_inter1 = max(y1, y3)
	x_inter2 = min(x2, x4)
	y_inter2 = min(y2, y4)
	width_inter = abs(x_inter2 - x_inter1)
	height_inter = abs(y_inter2 - y_inter1)
	area_inter = width_inter * height_inter
	width_box1 = abs(x2 - x1)
	height_box1 = abs(y2 - y1)
	width_box2 = abs(x4 - x3)
	height_box2 = abs(y4 - y3)
	area_box1 = width_box1 * height_box1
	area_box2 = width_box2 * height_box2
	area_union = area_box1 + area_box2 - area_inter
	iou = area_inter / area_union
	return iou

def read_content_pred(xml_file: str):

    tree = ET.parse(xml_file)
    root = tree.getroot()

    list_with_all_boxes = []
    filename = root.find('filename').text
    ymin, xmin, ymax, xmax = None, None, None, None
    
    object = root.find('object')
    if object is not None:
        for boxes in root.iter('object'):    
	
            ymin = int(boxes.find("boundingbox/y1").text)
            xmin = int(boxes.find("boundingbox/x1").text)
            ymax = int(boxes.find("boundingbox/y2").text)
            xmax = int(boxes.find("boundingbox/x2").text)

            list_with_single_boxes = [xmin, ymin, xmax, ymax]
            list_with_all_boxes.append(list_with_single_boxes)

    return filename, list_with_all_boxes
    #return filename, list_with_single_boxes

def read_content_anotation(xml_file: str):

    tree = ET.parse(xml_file)
    root = tree.getroot()

    list_with_all_boxes = []
    #filename = root.find('filename').text
    ymin, xmin, ymax, xmax = None, None, None, None
    
    object = root.find('project')
    if object is not None:
	    for clases in root.iter('class'):

		    for boxes in clases.iter('boundingbox'):
                     ymin = int(boxes.find("y1").text)
                     xmin = int(boxes.find("x1").text)
                     ymax = int(boxes.find("y2").text)
                     xmax = int(boxes.find("x2").text)

                     list_with_single_boxes = [xmin, ymin, xmax, ymax]
                     list_with_all_boxes.append(list_with_single_boxes)

    return list_with_all_boxes
    #return filename, list_with_single_boxes

def main():
	#bbox_cat1 = [130, 32, 450, 452]	# Defining the coordinates of the first bounding box (x1,y1,x2,y2)
	#bbox_cat2 = [140, 42, 350, 447]	# Defining the coordinates of the second bounding box (x3,y3,x4,y4)
	bbox_array_anot = []
	bbox_array_pred = []
	bbox_array_anot = read_content_anotation("Images/Tester6_robicart/Tester6_robicart_24.png.xml")
	img_name, bbox_array_pred = read_content_pred("Images/Tester6_robicart/Tester6_robicart_24.png_pred.xml")
	#img = cv2.imread("Images/Cat.jpg")	# Read the image 
	img = cv2.imread(img_name)	# Read the image 
	img = cv2.resize(img, (640, 480))	# Resize the image to be displayed on the screen
	for x in bbox_array_anot:

		img = draw_box(img,x,color=(0,255,0))

	for x in bbox_array_pred:

		img = draw_box(img,x,color=(255,0,0))

	for x in bbox_array_anot:
		for y in bbox_array_pred:
			iou = IOU(x, y)	# Calling the function to return the IOU
			img = cv2.putText(img, 'IOU: {}'.format(iou), (x[0], x[1]), cv2.FONT_HERSHEY_SIMPLEX , 1, 
						(255,0,0), 2, cv2.LINE_AA) 	# Draw the IOU on the image
			print("IOU OF THE BOXES IS: ", iou)	# Print the iou

	#img = draw_box(img,bbox_cat1,color=(0,255,0)) # Call the function to draw the first box	
	#img = draw_box(img,bbox_cat2,color=(255,0,0)) # Call the function to draw the second box	
	#iou = IOU(bbox_cat1, bbox_cat2)	# Calling the function to return the IOU
	#img = cv2.putText(img, 'IOU: {}'.format(iou), (bbox_cat1[0], bbox_cat1[1]), cv2.FONT_HERSHEY_SIMPLEX , 1, 
	#					(255,0,0), 2, cv2.LINE_AA) 	# Draw the IOU on the image
	#print("IOU OF THE BOXES IS: ", iou)	# Print the iou
	cv2.imshow("IMG", img)	# Show the image
	cv2.waitKey()	# Wait for any key to be pressed to exit

if __name__ == "__main__":
	main()
