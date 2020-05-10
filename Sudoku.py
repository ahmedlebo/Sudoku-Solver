import tkinter as tk '''importing the library needed to make the GUI'''
MARGIN = 10
SIDE = 60
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9
class Sudoku(tk.Tk):
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------'

    def __init__(self,master=None): 
        super().__init__(master)
        self.row, self.col = -1, -1
        
        self.title('Sudoku game')
        #self.pack(fill=tk.BOTH, expand=1)
        self.canvas = tk.Canvas(master, width=WIDTH, height=WIDTH, borderwidth=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, side=tk.TOP)
        self.initialize_board()
        self.puzzle=[[0 for x in range(9)]for y in range(9)]
        self.board=[[0 for x in range(9)]for y in range(9)]
        # Input from user in form of clicks
        self.bind('<Button-1>', self.click)
        self.canvas.bind("<Key>", self.key_pressed)
        solve_button = tk.Button(self,
                              text="Solve Sudoku",command=self.solve_sudoku)
        show_solution=tk.Button(self,
                              text="Show Solution",command=self.show_solution)
        reset_button=tk.Button(self,
                              text="Reset",command=self.reset_shape)
        solve_button.pack(fill=tk.BOTH, side=tk.BOTTOM)
        show_solution.pack(fill=tk.BOTH, side=tk.BOTTOM)
        reset_button.pack(fill=tk.BOTH, side=tk.BOTTOM)
                          
    def initialize_board(self):
        '''Function to create the grid to enter the sudoku to solve '''
        for i in range(10):
            color = "blue" if i % 3 == 0  else "gray"
            width = 2 if i % 3 == 0  else 1
            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color,width=width)
                
            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color,width=width) 
       
    def click(self,event):
        '''Function to determine the x and y of the click and dtermine the row and the column of the cell chosen'''
        x, y = event.x, event.y
        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.canvas.focus_set()

            # get row and col numbers from x,y coordinates
            self.row, self.col =int( (y - MARGIN) / SIDE), int((x - MARGIN) / SIDE)        
        else:
            self.row, self.col = -1,-1

        self.draw_cursor()
    def draw_cursor(self):
        '''Function to draw a rectangle around the cell chosen'''
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline="red", tags="cursor"
            )
    def key_pressed(self, event):
        
        if self.row >= 0 and self.col >= 0 and event.char in "1234567890" and not event.char in ' ':
            self.puzzle[self.row][self.col] = int(event.char)
            self.board[self.row][self.col] = int(event.char)
            self.col, self.row = -1, -1
            self.draw_puzzle()
            self.draw_cursor()
    
    def draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                Entry = self.puzzle[i][j]
                if Entry != 0:
                    x = MARGIN + j * SIDE + SIDE/2  
                    y = MARGIN + i * SIDE + SIDE/2  
                    self.canvas.create_text(
                        x, y, text=Entry, tags="numbers", fill='black') 
    
 # ------------------------------------------------------------------
    # Solving Functions:
    # ------------------------------------------------------------------'   
    def is_empty(self,board):
        for i in range(9):
            for j in range(9):
                if(board[i][j]==0):
                    a=[True,i,j]
                    return a         
        a=[False,-1,-1]
        return a 
    def no_conflicts(self,board,row_num,col_num,value):
        return ((not self.used_in_row(board,row_num,value))
                  and (not self.used_in_col(board,col_num,value)) 
                    and (not self.used_in_box(board,row_num,col_num, value)))
    def used_in_row(self,board,row_num,value):
        for i in range(9):
            if(board[row_num][i]==value):
                return True
        return False

    def used_in_col(self,board,col_num,value):
        for i in range(9):
            if(board[i][col_num]==value):
                return True
        return False

    def used_in_box(self,board,row_num,col_num, value):
        i=row_num-(row_num%3)
        j=col_num-(col_num%3)
        for x in range(i,i+3):
            for y in range(j,j+3):
                if(board[x][y]==value):
                    return True
        return False
    
    def solve_sudoku(self):
        
        data=self.is_empty(self.board)
        cond=data[0]
        if  cond==False:
            return True
        row_num=data[1]
        col_num=data[2]
        for sol in range(1,10):
            if(self.no_conflicts(self.board,row_num=row_num,col_num=col_num,value=sol)):
                self.board[row_num][col_num]=sol
                if(self.solve_sudoku()):
                    return True
                self.board[row_num][col_num]=0
        return False
    
    def show_solution(self):
        self.draw_solution(self.board)
        
    
    def reset_shape(self):
        self.puzzle=[[0 for x in range(9)]for y in range(9)]
        self.board=[[0 for x in range(9)]for y in range(9)]
        self.canvas.delete("numbers")
        self.canvas.delete("solution")
        self.initialize_board()
        
   
    def draw_solution(self,board):
        self.canvas.delete("solution")
        for i in range(9):
            for j in range(9):
                x = MARGIN + j * SIDE + SIDE/2  
                y = MARGIN + i * SIDE + SIDE/2
                value=board[i][j]
                if value ==0:
                    self.reset_shape()
                else:
                    fill='black' if(board[i][j]==self.puzzle[i][j]) else 'blue'
                    self.canvas.create_text(
                        x, y, text=value, tags="solution", fill=fill) 
if __name__ == '__main__':
    sudoku=Sudoku()
    
    tk.mainloop()