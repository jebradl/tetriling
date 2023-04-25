# ###############################################################################################
#
#         ,----,                                                                               
#       ,/   .`|                                                                               
#     ,`   .'  :            ___                        ,--,                                    
#   ;    ;     /          ,--.'|_             ,--,   ,--.'|     ,--,                           
# .'___,/    ,'           |  | :,'   __  ,-.,--.'|   |  | :   ,--.'|         ,---,             
# |    :     |            :  : ' : ,' ,'/ /||  |,    :  : '   |  |,      ,-+-. /  |  ,----._,. 
# ;    |.';  ;   ,---.  .;__,'  /  '  | |' |`--'_    |  ' |   `--'_     ,--.'|'   | /   /  ' / 
# `----'  |  |  /     \ |  |   |   |  |   ,',' ,'|   '  | |   ,' ,'|   |   |  ,"' ||   :     | 
#     '   :  ; /    /  |:__,'| :   '  :  /  '  | |   |  | :   '  | |   |   | /  | ||   | .\  . 
#     |   |  '.    ' / |  '  : |__ |  | '   |  | :   '  : |__ |  | :   |   | |  | |.   ; ';  | 
#     '   :  |'   ;   /|  |  | '.'|;  : |   '  : |__ |  | '.'|'  : |__ |   | |  |/ '   .   . | 
#     ;   |.' '   |  / |  ;  :    ;|  , ;   |  | '.'|;  :    ;|  | '.'||   | |--'   `---`-'| | 
#     '---'   |   :    |  |  ,   /  ---'    ;  :    ;|  ,   / ;  :    ;|   |/       .'__/\_: | 
#              \   \  /    ---`-'           |  ,   /  ---`-'  |  ,   / '---'        |   :    : 
#               `----'                       ---`-'            ---`-'                \   \  /  
#                                                                                     `--`-'
# 
# ###############################################################################################
# DE2-COM2 Computing 2: Individual project
#
# Title: jem_code
# Author: Jemima Eve Bradley
# CID: 01493163
# ###############################################################################################


# key:
# 1 = functions used by method 1 - SolvyBoi
# 2 = functions used by method 2 - FlowyBoi
# 3 = functions used by method 3 - GreedyBoi 


import utils

shapey_bois = {
    4: [(1,0), (2,0), (2,1)],
    5: [(1,-2), (1,-1), (1,0)],
    6: [(0,1), (1,1), (2,1)],
    7: [(0,1), (0,2), (1,0)],
    8: [(1,0), (2,-1), (2,0)],
    9: [(0,1), (0,2), (1,2)],
    10: [(0,1), (1,0), (2,0)],
    11: [(1,0), (1,1), (1,2)],
    12: [(1,0), (1,1), (2,0)],
    13: [(1,-1), (1,0), (1,1)],
    14: [(1,-1), (1,0), (2,0)],
    15: [(0,1), (0,2), (1,1)],
    16: [(0,1), (1,-1), (1,0)],
    17: [(1,0), (1,1), (2,1)],
    18: [(0,1), (1,1), (1,2)],
    19: [(1,-1), (1,0), (2,-1)]
    }
# here, the tetriling pieces are refereced to the leftmost piece on the top row
# as the algorithms run top left to bottom right, this is the most effective way of placing pieces, assuming everything above and directly to the left is filled

coordy_bois = {
    (1,0): {4, 5, 7, 8, 10, 11, 12, 13, 14, 16, 17, 19},
    (0,1): {6, 7, 9, 10, 15, 16, 18},
    (1,1): {6, 11, 12, 13, 15, 17, 18},
    (1,-1): {5, 13, 14, 16, 19},
    (2,0): {4, 8, 10, 12, 14},
    (2,1): {4, 6, 17},
    (1,2): {9, 11, 18},
    (0,2): {7, 9, 15},
    (2,-1): {8, 19},
    (1,-2): {5}
    }
# each coordinate possible has a set of all the shapes that use said coordinate, this is used in the FlowyBoi class

class FlowyBoi:
    
    def __init__(self): #2
        self.lay_me_down = []
        self.bois_yet_to_be = []
        self.suspects = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        self.chosen_ones = []
        self.flood_coords = []
        # initialising lists to be used in the FlowyBoi class


    def __call__(self, target, piece_count): #2
        self.target = target
        self.piece_count = piece_count
        self.caution_tape = []
        self.solution = [] 
        self.crime_scene()
        self.looky_boi_mark_2()
        self.flowy_boi() 
        return self.make_dat_solution()
        # setting the call order for the inclass functions
                    
    
    def crime_scene(self): #1, 2
        
        # this function creates a buffer around the target matrix - like, say, putting caution tape around a crime scene
        # it acts against any shapes with -ve column calls that would otherwise append to the other end of the row
            
        self.caution_tape = [[0 for _ in range(len(self.target[0])+4)] for __ in range(2)]
    
        for j in self.target:
            self.caution_tape.append([0] + [0] + j + [0] + [0])
            
        self.caution_tape.append([0 for _ in range(len(self.target[0])+4)])
        self.caution_tape.append([0 for _ in range(len(self.target[0])+4)])
        
    
    def looky_boi_mark_2(self): #2
        
        # this function initialises the flood fill algorithm every time an area has been completely filled
        # it reduces the memory and time required to run the main recusive function so can operate on larger targets
         
        for i, row_man in enumerate(self.caution_tape): 
            for j, ignore_this_boi in enumerate(row_man): 
                if self.caution_tape[i][j] == 1:
                    if self.chosen_ones != []:
                        self.flowy_boi()
                        self.flood_coords.clear()
                    self.flood_that(i, j)
    
    
    def flood_that(self, y, x): #2
        
        # this is the flood fill algorith, which changes the areas to be filled from 1s to 5s
        # it also uses recursion, calling itself on it's neighbours until it finds an enclosed area
     
        if (y < 0 or y >= len(self.caution_tape) or x < 0 or 
            x >= len(self.caution_tape[0]) or self.caution_tape[y][x] == 0 or 
            self.caution_tape[y][x] == 5):
            return False
        
        self.caution_tape[y][x] = 5
        self.flood_coords.append((y,x))
        
        if self.flood_that(y + 1, x) == False:
            pass
        if self.flood_that(y - 1, x) == False:
            pass
        if self.flood_that(y, x + 1) == False:
            pass
        if self.flood_that(y, x - 1) == False:
            pass
        
        # the returned list of coordinates must be sorted so that the next function can run them starting at the top left
        self.chosen_ones = sorted(self.flood_coords, key=lambda k: [k[0], k[1]])
        
    
    def flowy_boi(self): #2
        
        # this is the core function for the FlowyBoi class
        
        self.chosen_ones.sort()
        
        if len(self.chosen_ones) == 0: # the flood fill generated area is complete
            if len(self.lay_me_down) == self.piece_count: # the list of all pieces is full ie. prevents a solution from being generated prematurely
                self.make_dat_solution()
        
        for coord in self.chosen_ones:
            i, j = coord
            
            if self.caution_tape[i][j] == 5: # values in area to be filled were changed to 5s
                weapons = self.give_me_shapes_that_fit(i, j) # generates a set of possible shapes
                
                for accused in weapons:
                    self.place_that_shape(i, j, accused) # try placing the first possible shape
                            
                    if self.flowy_boi(): # if the function run again is successful ie. returns True
                        m = i-2
                        n = j-2 # recalibrating the coordinates given that there are two extra rows/columns of border 
                        self.lay_me_down.append([accused, (m,n)]) # add the shape ID and the coordinates of it's (0,0) square to a list of confirmed shapes
                        return True
                    
                    else:
                        self.unplace_that_shape_he_aint_no_good(i, j, accused) # remove the shape and try the next one

            return False # no shapes fit, the recursion function backtracks

        return True # there are no empty spaces left to fill in this section
        
    
    
    def give_me_shapes_that_fit(self, i, j): #2
        
        trial = set(self.suspects) # initialises a set of the shape IDs
        
        for coord in coordy_bois: # for every coordinate that it is possible to reach from the (0,0) square
            row_aim = i + coord[0]
            col_aim = j + coord[1] # finds coordinate with reference to (0,0) in matrix
            
            if self.caution_tape[row_aim][col_aim] != 5: # if said coordinate is unavailable
                trial -= coordy_bois[(coord[0], coord[1])] # use said coordinate as a coordy_bois dictionary key and subtract a set of all pieces
                                                           # requiring that square from the list of possible pieces
                
                if len(trial) == 0: # if no pieces can start at the location (i,j)
                    return trial # return an empty set
        
        return trial # else return the set of possible shape IDs
        
        
    
    def place_that_shape(self, i, j, shape): #3
        
        self.bois_yet_to_be.append((shape, 1)) # provisionally appends to a list before recursion

        self.caution_tape[i][j] = 8 # marks the starting square with 8 to show it's been filled
        self.chosen_ones.remove((i, j)) # removes the coordinate from the list of open spaces
        
        for coord in shapey_bois[shape]: # does the above for all coordinates in the dictionary list for that shape ID
            y, x = coord
            row_aim = i + y
            col_aim = j + x
            self.caution_tape[row_aim][col_aim] = 8
            self.chosen_ones.remove((row_aim, col_aim)) 
    
    
    def unplace_that_shape_he_aint_no_good(self, i, j, shape): #2
        
        self.bois_yet_to_be.pop(-1) # removes shape ID from provisional list
        self.caution_tape[i][j] = 5 # changes the square back to being an available 5
        self.chosen_ones.insert(0, (i, j)) # reinserts the coordinate back into the list of those available
            
        for z, coord in enumerate(shapey_bois[shape]): # does the above for all coordinates in the dictionary list for that shape ID
            y, x = coord
            row_aim = i + y
            col_aim = j + x
            self.caution_tape[row_aim][col_aim] = 5
            self.chosen_ones.insert(z, (row_aim, col_aim)) 
        
    
    def make_dat_solution(self): #1, 2, 3
        
        self.solution = self.target # generates a solution the same dimensions as the original target matrix
        
        for i, row in enumerate(self.solution):
            for j, col in enumerate(row):
                self.solution[i][j] = (0,0) # changes every element to (0,0)
        
        for q, k in enumerate(self.lay_me_down): # for every shape/starting coordinate pair in the list
            r0, c0 = k[1] # fetches starting coordinates
            self.solution[r0][c0] = (k[0], q+1) # changes the element in the solution to the (shapeID, pieceID)
            
            for coord in shapey_bois[k[0]]: # does the above for all coordinates in the dictionary list for that shape ID
                y, x = coord
                row_aim = r0 + y
                col_aim = c0 + x
                self.solution[row_aim][col_aim] = (k[0], q+1) 
                
        return self.solution # returns the solution matrix



class SolvyBoi(FlowyBoi):
    
    # this class is a child class of FlowyBoi, inheriting the crime_scene and make_dat_solution functions
    
    def __init__(self): #1
        self.lay_me_down = []
        self.bois_yet_to_be = []
        self.chosen_ones = []
        # initialising lists to be used in the SolvyBoi class

    def __call__(self, target): #1
        self.target = target
        self.caution_tape = []
        self.solution = [] 
        self.crime_scene()
        self.looky_boi() 
        return self.make_dat_solution()
        # setting the call order for the inclass functions


    def looky_boi(self): #1
        
        # this is the core function for the SolvyBoi class
        
        for i, row_man in enumerate(self.caution_tape): 
            for j, ignore_this_boi in enumerate(row_man):
                if self.caution_tape[i][j] != 1:
                    continue # if the element is not available, move on
                
                for k in range(4, 20): # for each shape in the dictionary of pieces
                    
                    accused = self.give_me_shape_that_fits(i, j, k) # tests whether the shape with ID 'k' is possible for (i,j)
                    
                    if accused == False: # if not, try the next 'k'
                        continue
                    
                    self.place_that_shape_easy_mode(i, j, k) # if possible, place provisionally
                    
                    if self.looky_boi(): # if the function run again is successful ie. returns True
                        m = i-2
                        n = j-2 # recalibrating the coordinates given that there are two extra rows/columns of border 
                        self.lay_me_down.append([k, (m,n)]) # add the shape ID and the coordinates of it's (0,0) square to a list of confirmed shapes
                        return True
                    
                    else:
                        self.unplace_that_shape_he_aint_no_good_easy_mode(i, j, k) # remove the shape and try the next one

                return False # no shapes fit, the recursion function backtracks

        return True # there are no empty spaces left to fill
        
    
    
    def give_me_shape_that_fits(self, i, j, k): #1, 3
        
        for coord in shapey_bois[k]: # sets the (0,0) coordinate for the shape
            row_aim = i + coord[0]
            col_aim = j + coord[1]
                
            if row_aim >= len(self.caution_tape) or col_aim >= len(self.caution_tape[0]) or self.caution_tape[row_aim][col_aim] != 1:
                return False # if any of the coordinates in that dictionary are out of bounds or the square is occupied, return false for that shape
        
        return True # if the shape fits
        
    
    def place_that_shape_easy_mode(self, i, j, shape): #1, 3
        
        self.bois_yet_to_be.append((shape, 1)) # provisionally appends to a list before recursion

        self.caution_tape[i][j] = 3 # changes element to a 3 to show it's been filled
        
        for coord in shapey_bois[shape]: # does the above for all coordinates in the dictionary list for that shape ID
            y, x = coord
            row_aim = i + y
            col_aim = j + x
            self.caution_tape[row_aim][col_aim] = 3
        
    
    
    def unplace_that_shape_he_aint_no_good_easy_mode(self, i, j, shape): #1, 3
        
        self.bois_yet_to_be.pop(-1) # removes shape ID from provisional list
        
        self.caution_tape[i][j] = 1 # changes the square back to being an available
            
        for coord in shapey_bois[shape]: # does the above for all coordinates in the dictionary list for that shape ID
            y, x = coord
            row_aim = i + y
            col_aim = j + x
            self.caution_tape[row_aim][col_aim] = 1
    
    

class GreedyBoi(SolvyBoi):
    
    # this class is a child class of SolvyBoi, inheriting the give_me_shape_that_fits, place_that_shape_easy_mode, and unplace_that_shape_he_aint_no_good_easy_mode functions
    # it also inherits the make_dat_solution function from FlowyBoi
    
    def __init__(self):
        self.lay_me_down = []
        self.bois_yet_to_be = []
        self.suspects = [5, 16, 13, 15, 7, 9, 18, 10, 6, 19, 8, 14, 4, 12, 17, 11]
        self.chosen_ones = []
        self.witnesses = []
        self.lets_try = []
        # initialising lists to be used in the GreedyBoi class

    def __call__(self, target):
        self.target = target
        self.caution_tape = []
        self.solution = [] 
        self.brooklyn()
        self.greedy_looky_boi()
        self.three_or_nothing()
        return self.make_dat_solution()
        # setting the call order for the inclass functions
    
    def brooklyn(self): #3
        
        # instead of making a border of 0s, makes a border of 99s is created so that they can be differentiated from genuine 0s when placing shapes with excess pieces 
            
        self.caution_tape = [[99 for _ in range(len(self.target[0])+4)] for __ in range(2)]
    
        for j in self.target:
            self.caution_tape.append([99] + [99] + j + [99] + [99])
            
        self.caution_tape.append([99 for _ in range(len(self.target[0])+4)])
        self.caution_tape.append([99 for _ in range(len(self.target[0])+4)])


    def greedy_looky_boi(self): #3
        
        # this is the core function for the GreedyBoi class
        
        for i, row_man in enumerate(self.caution_tape): 
            for j, ignore_this_boi in enumerate(row_man):
                if self.caution_tape[i][j] != 1:
                    continue # if the element is not available, move on
                 
                for k in self.suspects: # for each shape in the dictionary of pieces, ordered to be tested in the most effective way
                    
                    if not self.give_me_shape_that_fits(i, j, k): # if not possible, move on
                        continue
                    
                    self.place_that_shape_easy_mode(i, j, k) # if possible, place
                    
                    m = i-2
                    n = j-2 # recalibrating the coordinates given that there are two extra rows/columns of border 
                    self.lay_me_down.append([k, (m,n)]) # add the shape ID and the coordinates of it's (0,0) square to a list of confirmed shapes
                     
                    break # move onto the next element

        return True # entire matrix has been traversed
            
    
    def three_or_nothing(self): #3
        
        # this function runs after the first traversal of the target and finds sections that would gain from having a piece added in
        # ie. one excess to three availible spaces is a gain of two
        
        for i, row_man in enumerate(self.caution_tape): 
            for j, ignore_this_boi in enumerate(row_man):
                if self.caution_tape[i][j] == 1: 
                    self.witnesses.append((i, j)) # add all available coordinates to a list
                    
        for start in self.witnesses:
            y, x = start
            self.lets_try.append((y, x)) # add the proposed (0,0) to a list
            
            for k in range(4, 20):
                for coord in shapey_bois[k]:
                    w, z = coord
                    row_try = y + w
                    col_try = x + z # finds the coordinates for a shape
                    
                    if self.caution_tape[row_try][col_try] == 3 or self.caution_tape[row_try][col_try] == 99:
                        self.lets_try = [(y, x)]
                        break # if already filled, move on to the next shape
                    
                    elif row_try not in range(2, len(self.caution_tape)-2) or col_try not in range(2, len(self.caution_tape[0])-2):
                        self.lets_try = [(y, x)]
                        break # if out of bounds, move on to the next shape
                    
                    elif self.caution_tape[row_try][col_try] == 1:
                        self.lets_try.append((row_try, col_try)) # if actually available, add to list
                
                if len(self.lets_try) != 3: # if less than 3 squares were available, no gain, move on
                    self.lets_try.clear()
                    
                elif len(self.lets_try) == 3: # if three squares were available
                    self.caution_tape[y][x] = 3 # change (0,0) square so now unavailable
                    
                    for p in shapey_bois[k]:
                        l, f = p
                        u = y + l
                        v = x + f
                        self.caution_tape[u][v] = 3 # do the same for all coordinates needed for shape
                        
                    for q in self.lets_try:
                        self.witnesses.remove(q) # remove available coordinates from list
                        
                    self.lets_try.clear()
                    m = y-2
                    n = x-2 # recalibrating the coordinates given that there are two extra rows/columns of border
                    self.lay_me_down.append([k, (m,n)]) # add the shape ID and the coordinates of it's (0,0) square to the list of confirmed shapes
                    break # move on in the list of availible spaces