import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-sorter', help="which sorting algorithm to use (quick, bubble, heap)", required=True)
args = parser.parse_args()

#scikit package used
from skimage import color
#import needed for images
import imageio


#numpy package used
import numpy as np
import os


#function to split array
def partition(array, begin, end):
    pivot = begin
    swaps = []
    for i in range(begin + 1, end + 1):
        if array[i] <= array[begin]:
            pivot += 1
            array[i], array[pivot] = array[pivot], array[i]
            swaps.append([i, pivot])
    array[pivot], array[begin] = array[begin], array[pivot]
    swaps.append([pivot, begin])
    return pivot, swaps

#function for quick sort
def quicksort(array, begin=0, end=None):
   
    global swaps
    swaps = []
    if end is None:
        end = len(array) - 1

    def _quicksort(array, begin, end):
        global swaps
        if begin >= end:
            return
        pivot, newSwaps = partition(array, begin, end)
        swaps += newSwaps
        _quicksort(array, begin, pivot - 1)
        _quicksort(array, pivot + 1, end)
    return _quicksort(array, begin, end), swaps

#function for bubble sort
def bubblesort(A):

    swaps = []
    for i in range(len(A)):
        for k in range(len(A) - 1, i, -1):
            if (A[k] < A[k - 1]):
                swaps.append([k, k - 1])
                tmp = A[k]
                A[k] = A[k - 1]
                A[k - 1] = tmp
    return A, swaps
# function for heap sort
def heapsort( aList ):
   
    global swaps
    swaps = []
  
    length = len( aList ) - 1
    leastParent = length // 2
    for i in range ( leastParent, -1, -1 ):
        moveDown( aList, i, length )

   
    for i in range ( length, 0, -1 ):
        if aList[0] > aList[i]:
            swaps.append([0, i])
            swap( aList, 0, i )
            moveDown( aList, 0, i - 1 )
    return aList, swaps

#function to iterate through list
def moveDown( aList, first, last ):
    global swaps
    largest = 2 * first + 1
    while largest <= last:
       
        if ( largest < last ) and ( aList[largest] < aList[largest + 1] ):
            largest += 1

        if aList[largest] > aList[first]:
            swaps.append([largest, first])
            swap( aList, largest, first )
           
            first = largest;
            largest = 2 * first + 1
        else:
            return 
#function to swap arrays
def swap( A, x, y ):
    tmp = A[x]
    A[x] = A[y]
    A[y] = tmp

# producing image
img = np.zeros((200, 200, 3), dtype='float32') 

for i in range(img.shape[1]):
    img[:,i,:] = i / img.shape[0], .9, .9

in_rgb = color.convert_colorspace(img, 'HSV', 'RGB')

# allows for the image to be saved as .png
imageio.imsave('initial.png', in_rgb)

for i in range(img.shape[0]):
    np.random.shuffle(img[i,:,:])

in_rgb = color.convert_colorspace(img, 'HSV', 'RGB')
imageio.imsave('initial_shuffled.png', in_rgb)



maxMoves = 0
moves = []
#sorting according to which sort is being used
for i in range(img.shape[0]):
    newMoves = []
    if args.sorter == 'bubble':
        _, newMoves = bubblesort(list(img[i,:,0]))
    elif args.sorter == 'quick':
        _, newMoves = quicksort(list(img[i,:,0]))
    elif args.sorter == 'heap':
       
        integer_version = img[i,:,0] * 10000
        integer_version = integer_version.astype(int)
        _, newMoves = heapsort(list(integer_version))

    if len(newMoves) > maxMoves:
        maxMoves = len(newMoves)
    moves.append(newMoves)

currentMove = 0

def swap_pixels(row, places):
    tmp = img[row,places[0],:].copy()
    img[row,places[0],:] = img[row,places[1],:]
    img[row,places[1],:] = tmp


movie_image_step = maxMoves // 120
movie_image_frame = 0

os.makedirs(args.sorter, exist_ok=True)

#for each iteration saving the image
while currentMove < maxMoves:
    for i in range(img.shape[0]):
        if currentMove < len(moves[i]) - 1:
            swap_pixels(i, moves[i][currentMove])

    if currentMove % movie_image_step == 0:
        imageio.imsave('%s/%05d.png' % (args.sorter, movie_image_frame), color.convert_colorspace(img, 'HSV', 'RGB'))
        movie_image_frame += 1
    currentMove += 1

