# Sudoku Solver Using OpenCV

## Steps involved in making the app:

1. Loading the image.
2. Preprocessing the image.
3. Sudoku cells extraction.
4. Model building and training using MNIST dataset.
5. Predicting digits and storing them as a matrix.
6. Finding and displaying the solution.

## 1. Loading the Image:

Load the image from the user machine.

## 2. Preprocessing the Image:

### 2.1 Blurring:
I used Gaussian Blurring which blurs the pixel based on weights given to the other pixels.

### 2.2 Thresholding:
I used Adaptive thresholding because lighting condition might be unpredictable. This converts gray scale image to black and white.

### 2.3 Finding Contours:
1. I used RETR_EXTERNAL retrieval method for contours as we don't need any hierarchies.
2. I used CHAIN_APPROX_SIMPLE because there will be less space used to store the points.
  
After finding the contours I retrieved the largest contour that looks like a curve with 4 corners since the sudoku is the largest area in the image. We approximate the corners for this curve and get those corners.  
![alt text](https://github.com/mokkapati-srinivas/Sudoku_Solver_OpenCV/blob/main/Contours.PNG)

### 2.4 Perspective Transformation and Warping:
Using the corners obtained in the image we get the perspective matrix. Using this perspective matrix I warped the image into a 2D plane. This warped image is again blurred and thresholded.  
![alt text](https://github.com/mokkapati-srinivas/Sudoku_Solver_OpenCV/blob/main/Warped_Image_Processed.PNG)

## 3. Sudoku cells extraction:
1. I resized the warped image to 450x450 since there are 9 rows and 9 columns.
2. Now, I split the image into 81 parts (9 row wise and 9 column wise) and store them in "Extracted_Cells" folder for further inspection.
3. But, after splitting I observed there are a lot of white edges that interfere in the recognition process.  
![alt text](https://github.com/mokkapati-srinivas/Sudoku_Solver_OpenCV/blob/main/Extracted_Cells/cell12.jpg)
4. So, I dumped a cell which has a digit into "out.json" and upon seeing that I realized that the top 3 rows, bottom 3 rows, first 3 columns and last 2 columns are those edges.
5. So, I removed the edges by copping the image without the first 3 rows, last 3 rows, first 3 columns and last 3 columns.  
![alt text](https://github.com/mokkapati-srinivas/Sudoku_Solver_OpenCV/blob/main/Extracted_Cells_After_Removing_Borders/cell12.jpg) 
6. Now, our images are ready for prediction.

## 4. Model building and training using MNIST dataset:
![alt text](https://github.com/mokkapati-srinivas/Sudoku_Solver_OpenCV/blob/main/Model_Summary.PNG)  
The validation accuracy of this model is 99.04%. So, I saved the model as "model_digit_recognition.h5" for further use.

## 5. Predicting digits and storing them as a matrix:
1. Before I send the processed cells to predict, I noticed there are some empty images which can't be detected by the model.
2. I inspected the black space (the amount of pixels that are black in the image) for a sudoku and found out that for every empty cell there is more than 95% black space.
3. So, I filtered them using this metric and passed to the model to predict the cells which have a number in it.
4. I stored them as a matrix.
5. I measured the accuracy and it turned out to be 97.22%.

## 6. Finding and displaying the solution:
1. Now there might be some digits that are wrongly detected.
2. So, I gave the user freedom to change the values which are wrong (Since the accuracy is around 97%, there might be 2-3 errors that happen).  
![alt text](https://github.com/mokkapati-srinivas/Sudoku_Solver_OpenCV/blob/main/Extracted_Sudoku.PNG)  
![alt text](https://github.com/mokkapati-srinivas/Sudoku_Solver_OpenCV/blob/main/Change_In_The_Values.PNG)

3. Once the values are finalized, it is a classic backtracking solution to find the solved sudoku.
4. If I found a solution I displayd it, else I printed "No solution found".  
![alt text](https://github.com/mokkapati-srinivas/Sudoku_Solver_OpenCV/blob/main/Solved_Sudoku.PNG)
