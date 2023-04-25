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
# Title: main
# Author: Jemima Eve Bradley
# CID: 01493163
# ###############################################################################################

import utils
import jem_code

def Tetris(T):
    
    a = jem_code.FlowyBoi()
    b = jem_code.SolvyBoi()
    c = jem_code.GreedyBoi()
    # three possible class methods can be used depending on the size and density of the target matrix
    
    height = len(T)
    width = len(T[0]) 
    
    if (height <= 20 and width <= 20):
        # if the matrix is small, a purely recursive algorithm can be used regardless of density
        M = b(T)
        return M
    
    count = 0
    
    for row in T:
            for col in row:
                if col == 1:
                    count += 1
    
    piece_count = count/4 # using a count, the densiy of the target matrix can be estiated so that more accurate solutions can be found for less dense targets
    density = count/(height*width)
    
    if density <= 0.5:
        if height <= 35 and width <= 35:
            # matrices of small size and density can again be solved purely using recursion
            M = b(T)
            return M
        
        else:
            # if the target is not dense but large, it can be solved with a flood fill algorithm as well as recursion
            M = a(T, piece_count)
            return M

    else:
        # for larger, dense targets, a greedy approach is used
        M = c(T)
        return M

