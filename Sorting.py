#use of these comment tags for better understanding 

#COMMON QUESTIONS
# 1) what is pygame?

#import differnet module(libraries in cpp)
from cgitb import grey
import math
from operator import truediv
from pickle import FALSE, TRUE
from re import T
import math
import pygame 
import random
pygame.init() #intializes all of the pygame modules

#a class with all the variables which will be used globally
class DrawInformation:
    BLACK = 0,0,0   # color constants module
    WHITE = 255,255,255
    GREEN = 0,255,0
    RED = 255,0,0
    BACKGROUND_COLOR = WHITE

    #gradients are color of rectangles
    GRADIENTS = [
        (128,128,128),
        (160,160,160),
        (192,192,192)
    ]
    
    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 30)
    SIDE_PAD =100
    TOP_PAD =150

    #constructor
    def __init__(self,width,height, lst):
        self.width = width    # self is used to to represent instance(object) of that class
        self.height = height

        #working in pygame -- a window to draw everything on
        self.window =pygame.display.set_mode((width,height))
        pygame.display.set_caption("Sorting Algorithm Visulaization")
        self.set_list(lst)

    #new method set_list
    def set_list(self,lst):
        #now for different list input width and height of numbers will change dynamically 
        self.lst=lst
        self.min_val=min(lst)
        self.max_val=max(lst)


        self.block_width=round((self.width-self.SIDE_PAD) / len(lst))
        self.block_height= math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x=self.SIDE_PAD // 2 #two tzypes of division in python / gives float value ans // gives round down whole val

def draw(draw_info, algo_name , ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR) #background color of window

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1 , draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending ", 1 , draw_info.BLACK )
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 45)) # to display on top x ,y cordinate x must calculated to make perfectly symmentrical

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort ", 1 , draw_info.BLACK )
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 75))

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info , color_positions={} ,clear_bg=FALSE):   #draw lists rectangles
    
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2 , draw_info.TOP_PAD , draw_info.width - draw_info.SIDE_PAD , draw_info.height - draw_info.TOP_PAD)

        pygame.draw.rect(draw_info.window , draw_info.BACKGROUND_COLOR ,clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color=color_positions[i]

        
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width , draw_info.height))

    if clear_bg:
        pygame.display.update()


def generate_starting_list(n,min_val,max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val , max_val)
        lst.append(val)

    return lst

#pygame event loop = in pygame we need a loop constantly running in background because if you don't have that then program will immediately end so need a loop 
# to handle all of the event like sorting or exit program or anything a loop to handle them

def bubble_sort(draw_info , ascending = True):
    lst = draw_info.lst
    
    for i in range(len(lst)-1):
        for j in range(len(lst)-1):
            num1 = lst[j]
            num2 = lst[j+1]

            if ( num1 > num2 and ascending ) or (num1 < num2 and not ascending):
                lst[j], lst[j+1] = lst[j+1] , lst[j]
                draw_list(draw_info , {j : draw_info.GREEN , j+1 : draw_info.RED}, True)
                yield True
    
    return lst

def insertion_sort(draw_info , ascending =True ):
    lst = draw_info.lst

    for i in range(1,len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i-1] > current and ascending
            descending_sort = i > 0 and lst[i-1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i-1]
            i = i-1 
            lst[i] = current
            draw_list(draw_info , {i : draw_info.GREEN , i - 1 : draw_info.RED} , True)
            yield True
        
    return lst


def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100


    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)

    sorting = False

    ascending = True 

    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(120) #60 is fps maximum number of time loop can run in 1 second

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = FALSE
        else:
            draw(draw_info , sorting_algorithm_name , ascending)
        
        pygame.display.update()

        for event in pygame.event.get():  #Pygame will register all events from the user into an event queue which can be received with the code pygame. event. get() this will return the list of all the events occured since the last loop
            if event.type == pygame.QUIT:
                run = False
            
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:  # K_r is okay uppercase not k_r
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algorithm_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algorithm_name = "Bubble Sort"
    
    pygame.quit()


if __name__ == "__main__":
    main()