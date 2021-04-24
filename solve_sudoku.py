def check_empty_cell(sudoku):
    
    for i in range(9):
        for j in range(9):
            if sudoku[i][j]==0:
                return (i,j)
    return None



def is_insertion_valid(sudoku,row,col,num):
    
    for j in range(9):
        if sudoku[row][j]==num and j!=col:
            return False
        
    for i in range(9):
        if sudoku[i][col]==num and i!=row:
            return False
    
    box_i=row//3
    box_j=col//3
    box_start_i=box_i*3
    box_start_j=box_j*3
    for i in range(box_start_i,box_start_i+3):
        for j in range(box_start_j,box_start_j+3):
            if sudoku[i][j]==num and (i,j)!=(row,col):
                return False
    
    return True




def solve(sudoku):
    
    check=check_empty_cell(sudoku)
    if check==None:
        return True
    
    row,col=check
    for num in range(1,10):
        if is_insertion_valid(sudoku,row,col,num):
            sudoku[row][col]=num
            if solve(sudoku)==True:
                return True
            sudoku[row][col]=0
    
    return False
    