import cv2
import image_preprocessing as imp
import predict_digits as pdi
import get_accuracy as ga
import solve_sudoku as ss

def readImage():
    
    #Image path is taken as an input from the user and converted to Black and White
    input_image_path=input("Please enter the image path: ")
    input_image=cv2.imread(input_image_path)
    input_image_bw=cv2.cvtColor(input_image.copy(),cv2.COLOR_BGR2GRAY)
    
    
    #Image resizing using numpy
    input_image_resized=cv2.resize(input_image,(1000,1000))
    input_image_resized_bw=cv2.resize(input_image_bw,(1000,1000))
    
    
    #Show the image that is read    
    #cv2.imshow("Input Image read in Gray Scale",input_image_resized)
    #cv2.waitKey(0)
    
    return (input_image_resized,input_image_resized_bw)

def print_sudoku(sudoku):
    
    print()
    print()
    for i in range(9):
        print("- - - - - - - - - - - - - - - - - - -")
        for j in range(9):
            if j==0:
                print("| ",end="")
            else:
                print(" | ",end="")
            if(sudoku_unsolved[i][j]==0):
                print('.',end="")
            else:
                print(sudoku_unsolved[i][j],end="")
        print(" |")
    
    print("- - - - - - - - - - - - - - - - - - -")
    print()

#Read the input image
input_image,input_image_bw=readImage()

#Get the thresholded image as output
thresholded=imp.preprocess(input_image_bw)

#Get the corners of sudoku
sudoku_corners=imp.find_corners(thresholded,input_image)

#Get the warped image
warped_image=imp.transform_perspective(input_image,sudoku_corners)

#Resize the warped image to 450*450
warped_image=cv2.resize(warped_image,(450,450))

#Get the cell images of sudoku
cells=imp.split_images_store(warped_image)

#Predict the sudoku numbers
sudoku_unsolved=pdi.extract_digit_from_each_image(cells)

#Get the accuracy for the 4 sudoku image in the img folder
accuracy=ga.get_accuracy()


#Now we will print the sudoku which we had predicted and ask
#the user whether to make any changes or it is fine
print_sudoku(sudoku_unsolved)


print("Is there anything that is detected incorrectly?")
print("If yes, type 'yes' else type 'no'.")
print("If yes, then enter the row index, column index (indexed from 0) and its new value seperated by commas continously.")
print("After entering the indices and their values type 'completed'.")

yes_or_no=input()

if(yes_or_no=="yes"):
    while True:
        change=input()
        if change=="completed":
            break
        
        #Else extract row index, column index, and value
        row_index,column_index,value=map(int,change.split(","))
        sudoku_unsolved[row_index][column_index]=value
    

solvable=ss.solve(sudoku_unsolved)
if solvable==True:
    sudoku_solved=sudoku_unsolved
    print_sudoku(sudoku_solved)
    
else:
    print("This sudoku has no solution")