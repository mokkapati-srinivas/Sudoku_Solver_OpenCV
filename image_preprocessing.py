import cv2
import numpy as np

def preprocess(input_image_copy):
    
    #gaussian blur is applied on the copy of the input image
    gaussian=cv2.GaussianBlur(input_image_copy,(11,11),0)
    #cv2.imshow("Gaussian Blurred Image", gaussian)
    #cv2.waitKey(0)
    
    
    #thresholding is done to binarise the image
    thresholded=cv2.adaptiveThreshold(gaussian,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,11,2)
    #cv2.imshow("Thresholded Image",thresholded)
    #cv2.waitKey(0)
    
    
    #Dilation
    #kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]], np.uint8)
    #dilated = cv2.dilate(thresholded, kernel)
    #cv2.imshow("Dilated Image",dilated)
    #cv2.waitKey(0)
    
    return thresholded
    

def find_corners(thresholded,input_image):
    
    #We find the contours of the given image
    contours, hierarchy=cv2.findContours(thresholded,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #sort the contours as per the area
    contours=sorted(contours,key=cv2.contourArea,reverse=True)
    #print(contours)
    
    
    
    #Now for the contours we have to approzimate four corner points
    sudoku_contours=[]
    for c in contours:
        perimeter=cv2.arcLength(c,True)
        sudoku_contours=cv2.approxPolyDP(c,0.010*perimeter,True)
        if len(sudoku_contours)==4:
            #print(sudoku_contours)
            break

        
    #cv2.drawContours(input_image,sudoku_contours,-1,(0,255,0),10)
    #cv2.imshow("Contours Corners",input_image)
    #cv2.waitKey(0)
    
    
    #sudoku_contours are 3D so we reduce to 2D
    sudoku_contours_2d=[con[0] for con in sudoku_contours]
    
    #Now sort the corners based on top-left, bottom-left, top-right, bottom-right
    sudoku_corners_sorted=sorted(sudoku_contours_2d,key=lambda x:(x[0]+x[1],x[0]))
    #print(sudoku_corners_sorted)
    
    #corners_for_printing=[[con] for con in sudoku_corners_sorted]
    #cv2.drawContours(input_image,np.asarray(corners_for_printing,dtype=np.int32),-1,(0,255,0),10)
    #cv2.imshow("Contours Corners Sorted",input_image)
    #cv2.waitKey(0)
    
    return sudoku_corners_sorted
        


def transform_perspective(input_image,corners):
    
    #Extract the corners from the list
    top_left=corners[0]
    bottom_left=corners[1]
    top_right=corners[2]
    bottom_right=corners[3]
    
    
    #get height and width of the sudoku puzzle
    height_left=np.sqrt((top_left[0]-bottom_left[0])**2+(top_left[1]-bottom_left[1])**2)
    height_right=np.sqrt((top_right[0]-bottom_right[0])**2+(top_right[1]-bottom_right[1])**2)
    width_top=np.sqrt((top_left[0]-top_right[0])**2+(top_left[1]-top_right[1])**2)
    width_bottom=np.sqrt((bottom_left[0]-bottom_right[0])**2+(bottom_left[1]-bottom_right[1])**2)
    
    #Extract max width and max height
    width=int(max(width_top,width_bottom))
    height=int(max(height_left,height_right))
    
    
    #Construct a sample 2D view with above width and height
    two_dimensional_sample=np.array([[0,0],[width-1,0],[width-1,height-1],[0,height-1]],dtype="float32")
    
    #Reorder the corners for transformation
    corners_reordered=[top_left,top_right,bottom_right,bottom_left]
    #Convert them to numpy array
    corners_reordered=np.array(corners_reordered,dtype="float32")
    
    
    #Calculate the perspective transform matrix
    perspective_matrix=cv2.getPerspectiveTransform(corners_reordered,two_dimensional_sample)
    #print(perspective_matrix)
    
    #Warp the image to the given perspective
    warped_image=cv2.warpPerspective(input_image,perspective_matrix,(width,height))
    
    #Show the warped image
    #cv2.imshow("Warped Image",warped_image)
    #cv2.waitKey(0)

    
    return warped_image

    
def split_images_store(warped_image):
    
    #Again repeat the operations performed on the input image
    warped_processed=cv2.cvtColor(warped_image.copy(),cv2.COLOR_BGR2GRAY)
    warped_processed=cv2.GaussianBlur(warped_processed,(13,13),0)
    warped_processed=cv2.adaptiveThreshold(warped_processed,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,11,2)
    
    #Show the warped image processed
    #cv2.imshow("Warped Image Processed",warped_processed)
    #cv2.waitKey(0)
    
    
    #Find the height and width of image
    height=np.shape(warped_image)[0]
    width=np.shape(warped_image)[1]
    cell_height=height//9
    cell_width=width//9
    #print(height,width)
    
    #Split the images and store in a temporary grid
    temp_grid=[]
    
    #row=warped_processed[0:cell_height]
    #print([row[k][0:cell_width] for k in range(len(row))])
    for i in range(0,height-cell_height+1,cell_height):
        rows=warped_processed[i:i+cell_height]
        for j in range(0,width-cell_width+1,cell_width):
            temp_grid.append([rows[k][j:j+cell_width] for k in range(len(rows))])
    
    
    #Storing images in 9*9 grid
    cells=[]
    for i in range(0,len(temp_grid)-8,9):
        cells.append(temp_grid[i:i+9])
    
    
    #Converting each cell to numpy array to display and store
    for i in range(9):
        for j in range(9):
            cells[i][j]=np.array(cells[i][j])
     
    #Verify whether image is being displayed or not
    #cv2.imshow("Cell 0",cells[0][0])
    #cv2.waitKey(0)
    
    
    #Now store these images on the disk. Before storing see if there are any images any remove them
    try:
        for i in range(9):
            for j in range(9):
                np.os.remove("Extracted_Cells/cell"+str(i*9+j)+".jpg")
    except:
        pass
    
    #Now store them
    for i in range(9):
        for j in range(9):
            cv2.imwrite(("Extracted_Cells/cell"+str(i*9+j)+".jpg"),cells[i][j])
    
    
    return cells


