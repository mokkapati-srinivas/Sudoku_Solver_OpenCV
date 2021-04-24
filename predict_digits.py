import cv2
import numpy as np
from tensorflow.python.keras.models import load_model
import json
from matplotlib import image


def extract_digit_from_each_image(cells):
    
    sudoku_unfilled=[[0 for i in range(9)] for j in range(9)]
    
    f = open("out.json", "w")
    c = image.imread("C:/Users/VENU/Desktop/Sudoku_Project/Extracted_Cells/cell0.jpg")
    f.write(json.dumps(c.tolist(), indent=4))
    f.close()
    
    for i in range(9):
        for j in range(9):
            
            #print(cells[i][j])
            cell=cells[i][j]
            cell=cv2.resize(cell,(28,28))
            
            cell=cell[3:25,3:26]
            
            #Threshold the image
            thresholded=cv2.threshold(cell,128,255,cv2.THRESH_BINARY)[1]
            
            #Find the contours for the thresholded image
            #contours,hierarchy=cv2.findContours(thresholded,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            
            #Draw the contours
            #cell=cv2.cvtColor(cell,cv2.COLOR_GRAY2BGR)
            #cv2.drawContours(cell,contours,-1,(0,255,0),1)
            #cv2.imshow("Contours",cell)
            #cv2.waitKey(0)

            zeroPixels=506-cv2.countNonZero(thresholded)
            #print(zeroPixels)
            
            zeroPixelsForEmpty=int(0.95*506)
            
            if(zeroPixels>zeroPixelsForEmpty):
                cv2.imwrite(("Extracted_Cells_After_Removing_Borders/cell"+str(i*9+j)+".jpg"),cell)
                continue
            
            try:
                np.os.remove("Extracted_Cells_After_Removing_Borders/cell"+str(i*9+j)+".jpg")
            except:
                pass
            
            cv2.imwrite(("Extracted_Cells_After_Removing_Borders/cell"+str(i*9+j)+".jpg"),cell)
                
            sudoku_unfilled[i][j]=predict_number(thresholded)
                
    #print(sudoku_unfilled)
    
    return sudoku_unfilled


def predict_number(extracted_image):
    
    #Resize the image
    extracted_image=cv2.resize(extracted_image,(28,28))
    
    #Convert to float32 and reshape in accordance to mnist
    extracted_image=extracted_image.astype("float32")
    extracted_image=extracted_image.reshape(1,28,28,1)
    
    #Now normalize the image
    extracted_image=extracted_image/255
    
    model=load_model("model_digit_recognition.h5")
    pred=model.predict(extracted_image,batch_size=1)
    
    #Predicted number is the index
    predicted_number=pred.argmax()
    
    return predicted_number
