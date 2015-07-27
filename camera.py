# USAGE
# python drone.py --video FlightDemo.mp4

# import the necessary packages
import sys
import argparse
import cv2
import math
import numpy as np
import time

debug = True
debug = False

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
args = vars(ap.parse_args())

white = 0.5
atl = 0
L = 40
OL = 4
OR = 10
BST = 0.8

#axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)

#objp = np.float32( [ [ 0,0,0 ], [100,0,0], [100,100,0], [0,100,0] ] )

# (x,y,z) (right,down,into)
objp = np.float32([ [ [ 0,0,0 ], [100,0,0], [100,100,0], [0,100,0] ],   #0, not used
                    [ [ 0,0,0 ], [100,0,0], [100,100,0], [0,100,0] ],   #1
                    [ [ 0,0,0 ], [100,0,0], [100,100,0], [0,100,0] ],   #2
                    [ [ 0,0,0 ], [100,0,0], [100,100,0], [0,100,0] ],   #3
                    [ [ 0,0,0 ], [100,0,0], [100,100,0], [0,100,0] ],   #4
                    [ [ 0,0,0 ], [100,0,0], [100,100,0], [0,100,0] ],   #5
                    [ [ 0,0,0 ], [100,0,0], [100,100,0], [0,100,0] ],   #6
                    [ [ 0,0,0 ], [100,0,0], [100,100,0], [0,100,0] ],   #7
                    [ [ 0,0,0 ], [100,0,0], [100,100,0], [0,100,0] ],   #8
                    [ [ 0,0,0 ], [100,0,0], [100,100,0], [0,100,0] ],   #9
                    [ [ 0,0,0 ], [100,0,0], [100,100,0], [0,100,0] ],   #10
                    [ [ 0,0,0 ], [100,0,0], [100,100,0], [0,100,0] ],   #11
                    [ [ 0,0,0 ], [100,0,0], [100,100,0], [0,100,0] ],   #12
                    [ [ 0,0,0 ], [100,0,0], [100,100,0], [0,100,0] ],   #13
                    [ [ 0,0,0 ], [100,0,0], [100,100,0], [0,100,0] ],   #14
                    [ [ 0,0,0 ], [100,0,0], [100,100,0], [0,100,0] ],   #15
                    [ [ 0,0,0 ], [100,0,0], [100,100,0], [0,100,0] ],   #16
                    [ [ 200,0,0 ], [300,0,0], [300,100,0], [200,100,0] ],   #17
                    [ [ 0,0,0 ], [100,0,0], [100,100,0], [0,100,0] ],   #18
                    [ [ 0,0,0 ], [100,0,0], [100,100,0], [0,100,0] ],   #19
                    [ [ 0,0,0 ], [100,0,0], [100,100,0], [0,100,0] ] ]  #20
                    )



data = [[1,0,1,1,1,1,1,0,0,1,1,1,1,1,0,1],
        [0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1],
        [1,1,1,1,1,0,0,1,1,0,0,1,1,0,0,1],
        [1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1],
        [0,1,0,0,1,1,1,0,0,1,1,1,0,0,1,1],
        [1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0],
        [1,1,1,0,0,0,0,0,0,1,0,0,0,1,0,0],
        [0,0,1,1,1,1,1,1,0,1,1,0,0,0,1,0],
        [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,0,1,0,1,0,1,0,1,0,1,0,0,0,0,0],
        [0,0,0,1,1,1,1,1,0,1,0,0,0,1,1,1],
        [0,1,1,0,0,0,0,0,1,0,0,1,1,0,0,1],
        [0,0,1,1,0,0,0,1,1,0,1,1,1,1,1,0],
        [1,1,1,0,1,0,0,0,1,0,0,0,1,1,1,0],
        [1,1,0,0,0,1,0,0,0,1,0,0,1,1,1,0],
        [1,1,0,0,0,1,0,0,1,0,0,0,1,1,0,0],
        [1,0,1,0,1,0,1,0,1,1,1,0,0,0,1,0],
        [0,1,1,0,0,1,0,0,0,0,1,0,0,1,1,0],
        [1,1,1,0,0,0,1,0,0,0,1,0,0,0,1,0],
        [0,1,0,1,1,1,0,1,1,1,0,1,0,1,0,1]]

dataL =[[1,0,1,1,1,1,1,0,0,1,1,1,1,1,0,1],
        [1,0,0,1,1,0,0,1,1,0,0,1,0,0,0,0],
        [1,1,1,1,1,0,0,0,1,0,0,0,1,1,1,1],
        [0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0],
        [0,0,1,1,0,1,1,1,1,1,1,0,0,1,0,0],
        [0,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,1,1,1,0,0,0],
        [1,1,0,0,1,1,1,1,0,1,1,0,0,1,0,0],
        [0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0],
        [0,0,0,0,1,1,1,0,0,0,0,0,1,1,1,0],
        [1,1,0,1,0,1,0,1,0,1,1,1,0,1,0,0],
        [0,0,1,1,1,0,0,0,1,0,0,0,0,0,1,1],
        [1,1,1,0,1,0,1,1,0,0,0,1,0,0,1,1],
        [0,0,0,0,1,0,0,1,1,0,0,1,1,1,1,1],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,1],
        [0,0,0,0,0,0,0,0,1,1,0,1,1,0,1,1],
        [0,0,0,0,1,1,1,1,0,0,1,0,1,1,1,0],
        [0,0,0,0,1,0,1,1,1,1,0,1,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,0,0,0,1,0,0,0],
        [1,1,1,1,0,0,0,0,1,1,1,1,0,1,1,0]]

dataR =[[1,0,1,1,1,1,1,0,0,1,1,1,1,1,0,1],
        [0,0,0,0,1,0,0,1,1,0,0,1,1,0,0,1],
        [1,1,1,1,0,0,0,1,0,0,0,1,1,1,1,1],
        [0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0],
        [0,0,1,0,0,1,1,1,1,1,1,0,1,1,0,0],
        [0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,0],
        [0,0,0,1,1,1,0,1,0,0,0,1,0,0,0,0],
        [0,0,1,0,0,1,1,0,1,1,1,1,0,0,1,1],
        [0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0],
        [0,1,1,1,0,0,0,0,0,1,1,1,0,0,0,0],
        [0,0,1,0,1,1,1,0,1,0,1,0,1,0,1,1],
        [1,1,0,0,0,0,0,1,0,0,0,1,1,1,0,0],
        [1,1,0,0,1,0,0,0,1,1,0,1,0,1,1,1],
        [1,1,1,1,1,0,0,1,1,0,0,1,0,0,0,0],
        [1,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0],
        [1,1,0,1,1,0,1,1,0,0,0,0,0,0,0,0],
        [0,1,1,1,0,1,0,0,1,1,1,1,0,0,0,0],
        [0,0,0,0,1,0,1,1,1,1,0,1,0,0,0,0],
        [0,0,0,1,0,0,0,1,1,1,1,1,0,0,0,0],
        [0,1,1,0,1,1,1,1,0,0,0,0,1,1,1,1]]

dataD =[[1,0,1,1,1,1,1,0,0,1,1,1,1,1,0,1],
        [1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0],
        [1,0,0,1,1,0,0,1,1,0,0,1,1,1,1,1],
        [1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1],
        [1,1,0,0,1,1,1,0,0,1,1,1,0,0,1,0],
        [0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1],
        [0,0,1,0,0,0,1,0,0,0,0,0,0,1,1,1],
        [0,1,0,0,0,1,1,0,1,1,1,1,1,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
        [0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,1],
        [1,1,1,0,0,0,1,0,1,1,1,1,1,0,0,0],
        [1,0,0,1,1,0,0,1,0,0,0,0,0,1,1,0],
        [0,1,1,1,1,1,0,1,1,0,0,0,1,1,0,0],
        [0,1,1,1,0,0,0,1,0,0,0,1,0,1,1,1],
        [0,1,1,1,0,0,1,0,0,0,1,0,0,0,1,1],
        [0,0,1,1,0,0,0,1,0,0,1,0,0,0,1,1],
        [0,1,0,0,0,1,1,1,0,1,0,1,0,1,0,1],
        [0,1,1,0,0,1,0,0,0,0,1,0,0,1,1,0],
        [0,1,0,0,0,1,0,0,0,1,0,0,0,1,1,1],
        [1,0,1,0,1,0,1,1,1,0,1,1,1,0,1,0]]

Discriminable = [ False, False, True, True, False, True,
                        True, True, True, True, True,
                        True, True, True, True, True,
                        True, True, False, True, True ]

No = { 48765 : 1 , 57358 : 2 , 39327 : 3 , 50115 : 4 , 52850 : 5 ,
        3591 : 6 , 8711 : 7 , 18172 : 8 , 3 : 9 , 1365 : 10 ,
        58104 : 11 , 39174 : 12 , 32140 : 13 , 28951 : 14 , 29219 : 15 ,
        12579 : 16 , 18261 : 17 , 25638 : 18 , 17479 : 19 , 43962 : 20 }

LNo = { 48765 : 1, 2457 : 2, 61727 : 3, 21930 : 4, 10220 : 5,
        5460 : 6, 7440 : 7, 9971 : 8, 4352 : 9, 28784 : 10,
        11947 : 11, 49436 : 12, 51415 : 13, 63888 : 14, 40832 : 15,
        56064 : 16, 29936 : 17, 3024 : 18, 4592 : 19, 28431 : 20 }

RNo = { 48765 : 1, 39312 : 2, 63631 : 3, 21930 : 4, 14308 : 5,
        10920 : 6, 2232 : 7, 53092 : 8, 136 : 9, 3598 : 10,
        54644 : 11, 14467 : 12, 60179 : 13, 2463 : 14, 505 : 15,
        219 : 16, 3886 : 17, 3024 : 18, 3976 : 19, 61686 : 20 }

DNo = { 48765 : 1, 28679 : 2, 63897 : 3, 50115 : 4, 20083 : 5,
        57456 : 6, 57412 : 7, 16226 : 8, 49152 : 9, 43680 : 10,
        8007 : 11, 24729 : 12, 12734 : 13, 59534 : 14, 50254 : 15,
        50316 : 16, 43746 : 17, 25638 : 18, 57890 : 19, 24021 : 20 }
# 
Xpos = { 1 : 0 , 2 : 0 , 3 : 0 , 4 : 0 , 5 : 0 ,
        6 : 0 , 7 : 0 , 8 : 0 , 9 : 0 , 10 : 0 ,
        11 : 0 , 12 : 0 , 13 : 0 , 14 : 0 , 15 : 0 ,
        16 : 0 , 17 : 0 , 18 : 0 , 19 : 0 , 20 : 0 }

Ypos = { 1 : 0 , 2 : 0 , 3 : 0 , 4 : 0 , 5 : 0 ,
        6 : 0 , 7 : 0 , 8 : 0 , 9 : 0 , 10 : 0 ,
        11 : 0 , 12 : 0 , 13 : 0 , 14 : 0 , 15 : 0 ,
        16 : 0 , 17 : 0 , 18 : 0 , 19 : 0 , 20 : 0 }

Zpos = { 1 : 0 , 2 : 0 , 3 : 0 , 4 : 0 , 5 : 0 ,
        6 : 0 , 7 : 0 , 8 : 0 , 9 : 0 , 10 : 0 ,
        11 : 0 , 12 : 0 , 13 : 0 , 14 : 0 , 15 : 0 ,
        16 : 0 , 17 : 0 , 18 : 0 , 19 : 0 , 20 : 0 }

Area = { 1 : 10 , 2 : 10 , 3 : 10 , 4 : 10 , 5 : 10 ,
        6 : 10 , 7 : 10 , 8 : 10 , 9 : 10 , 10 : 10 ,
        11 : 10 , 12 : 10 , 13 : 10 , 14 : 10 , 15 : 10 ,
        16 : 10 , 17 : 10 , 18 : 10 , 19 : 10 , 20 : 10 }


argN = 6
argM = 6

#roi = (9, 14, 619, 456)
roi = (9, 14, 640, 480)
newcameramtx = np.array( [ [ 281.12072754, 0., 301.53388122 ],
                            [ 0., 278.01669312, 226.06360354 ],
                            [ 0., 0., 1. ] ] , dtype = "float32" )
mtx = np.array( [ [ 347.10459884, 0., 300.70799417 ],
                    [ 0., 342.94810439, 227.0917187 ],
                    [ 0., 0., 1. ] ] , dtype = "float32" )
dist = np.array( [ [-0.24673248,  0.00181109, -0.00032335,  0.00127357,  0.06125373] ] , dtype = "float32" )

def get_pos( targetNo , kd , dx1 , dy1 , area , theta ):
#    print( theta )
    po = area / Area.get( targetNo )
    if po < 0.001 : po = 1
    nZpos = 10 / ( po * po )
    tdltx, tdlty = 0, 0
    if kd == 0: tdltx, tdlty = -dx1, dy1
    elif kd == 1: tdltx, tdlty = dy1, dx1
    elif kd == 2: tdltx, tdlty = -dy1, -dx1
    elif kd == 3: tdltx, tdlty = dx1, -dy1
    dltx = tdltx * math.cos( theta ) - tdlty * math.sin( theta )
    dlty = tdltx * math.sin( theta ) + tdlty * math.cos( theta )
    return ( dltx + Xpos.get( targetNo ),
            dlty + Ypos.get( targetNo ),
            nZpos + Zpos.get( targetNo ) )

def get_pos2( targetNo , kd , dx1 , dy1 , area1 , targetNo2 , kd2 , dx2 , dy2 , area2 ):
    nXpos1, nYpos1, nZpos1 = get_pos( targetNo , kd , dx1 , dy1 , area1 )    
    nXpos2, nYpos2, nZpos2 = get_pos( targetNo2 , kd2 , dx2 , dy2 , area2 )    
    dx1 -= Xpos.get( targetNo )
    dy1 -= Ypos.get( targetNo )
    dx2 -= Xpos.get( targetNo2 )
    dy2 -= Ypos.get( targetNo2 )

    poX = ( Xpos.get( targetNo2 ) - Xpos.get( targetNo1 ) ) / ( dx2 - dx1 )
    poY = ( Ypos.get( targetNo2 ) - Ypos.get( targetNo1 ) ) / ( dy2 - dy1 )
    nXpos = Xpos.get( targetNo1 ) + poX * dx1
    nYpos = Ypos.get( targetNo1 ) + poY * dy1
    nZpos = ( nZpos1 * nZpos2 ) ** 0.5
    npos = ( nXpos, nYpos, Zpos.get( targetNo1 ) + nZpos)
    return npos

# return the order points (LU,RU,RD,LD)
def order_points(pts):
    rect = np.zeros((4, 2), dtype = "float32")

    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
     
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
     
    return rect
#
def getTarget( image , x , y , lx , ly , n , m ):
    px , py = ( lx + n - 1 ) / n , ( ly + m - 1 ) / m
    Sum = []
    for i in range( n ):
        Sum.append( [] )
        for j in range( m ):
            si, ti = x + px * i, min( x + px * ( i + 1 ) , x + lx )
            sj, tj = y + py * j, min( y + py * ( j + 1 ) , y + ly )
            Sum[ i ].append( np.mean( image[si:ti,sj:tj] ) )
    return Sum

def good( T ):
    avo, avi = 0, 0
    for i in range( 6 ):
        for j in range( 6 ):
            if i == 0 or j == 0 or i == 5 or j == 5:
                avo += T[ i ][ j ]
            else: avi += T[ i ][ j ]
    avo /= 20.0
    avi /= 16.0
    return avo < avi

def find_pwd( T ):
    if not good( T ): return -1
# find by corelation
    T2 = []
    for i in range(1,5):
        for j in range(1,5):
            T2.append( T[ i ][ j ] )

    c = []
    for i in range( 20 ):
        M = np.corrcoef( T2 , data[ i ] )
        c.append( M[ 0 ][ 1 ] )
    bst, bsti = -1, -1
    for i in range( 20 ):
        if c[ i ] != c[ i ]: pass
        elif c[ i ] > bst:
            bst, bsti = c[ i ], i + 1
    if bst > BST:
        if debug: print( bsti, bst )
        for i in No:
            if No[ i ] == bsti:
                return i
    c = []
    for i in range( 20 ):
        M = np.corrcoef( T2 , dataL[ i ] )
        c.append( M[ 0 ][ 1 ] )
    bst, bsti = -1, -1
    for i in range( 20 ):
        if c[ i ] != c[ i ]: pass
        elif c[ i ] > bst:
            bst, bsti = c[ i ], i + 1
    if bst > BST:
        if debug: print( bsti, bst )
        for i in LNo:
            if LNo[ i ] == bsti:
                return i
    c = []
    for i in range( 20 ):
        M = np.corrcoef( T2 , dataR[ i ] )
        c.append( M[ 0 ][ 1 ] )
    bst, bsti = -1, -1
    for i in range( 20 ):
        if c[ i ] != c[ i ]: pass
        elif c[ i ] > bst:
            bst, bsti = c[ i ], i + 1
    if bst > BST:
        if debug: print( bsti, bst )
        for i in RNo:
            if RNo[ i ] == bsti:
                return i
    c = []
    for i in range( 20 ):
        M = np.corrcoef( T2 , dataD[ i ] )
        c.append( M[ 0 ][ 1 ] )
    bst, bsti = -1, -1
    for i in range( 20 ):
        if c[ i ] != c[ i ]: pass
        elif c[ i ] > bst:
            bst, bsti = c[ i ], i + 1
    if bst > BST:
        if debug: print( bsti, bst )
        for i in DNo:
            if DNo[ i ] == bsti:
                return i
    return -1

# find by dist
    pwd = 0
    for i in range( argN - 2 , 0 , -1 ):
        for j in range( argM - 2 , 0 , -1 ):
            pwd = pwd * 2
            if T[ i ][ j ] > white + atl:
                pwd = pwd + 1
            elif T[ i ][ j ] > white - atl:
                return -1
    return pwd

#trans the image by the pts
def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
     
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
     
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
     
    tLength = max( maxWidth, maxHeight )
    maxWidth = tLength
    maxHeight = tLength

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
     
    M = cv2.getPerspectiveTransform(rect, dst)

    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
#    warped = cv2.warpPerspective(image, M, (width, height))
#    warped = myTrans( image , M )

    co = M[ 1 ][ 1 ] / ( ( M[ 1 ][ 0 ] ** 2 + M[ 1 ][ 1 ] ** 2 ) ** 0.5 )
    
    if co >= -1 and co <= 1:
        return (warped, maxWidth, maxHeight, math.acos( co ) )
    return (warped, maxWidth, maxHeight, 0 )

# load the video
#camera = cv2.VideoCapture(args["video"])
camera = cv2.VideoCapture( 0 );

preTime = int(round(time.time() * 1000))

while True:

    nowTime = int(round(time.time() * 1000))
    if debug: print( nowTime - preTime )
    preTime = nowTime

	# grab the current frame and initialize the status text
    (grabbed, frame) = camera.read()
    frame = cv2.undistort( frame, mtx, dist, None, newcameramtx )
    #frame = cv2.fisheye.undistortImage( frame, mtx, dist, None, newcameramtx )
    
    xx, yy, ww, hh = roi
    frame = frame[ yy:yy+hh, xx:xx+ww ]
    height, width, channels = frame.shape
    status = "No Targets"

	# check to see if we have reached the end of the video
    if not grabbed:
        break

	# convert the frame to grayscale, blur it, and detect edges
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    edged = cv2.Canny(blurred, 50, 150)

	# find contours in the edge map
    #(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
    #    cv2.CHAIN_APPROX_SIMPLE)
    (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE)

    #framet = cv2.drawContours(edged, cnts, -1, (255,0,0), 3)

    #if framet != None and len( framet ) > 0:
    #    cv2.imshow( "Con" , framet )
    #cv2.imshow( "Edge" , edged )

	# loop over the contours
    centerh = height // 2
    centerw = width // 2

    posi = np.ones( ( height , width ) ) * 255
    #posi = gray.copy()
    #for i in range( height ):
    #    for j in range( width ):
    #        posi[ i ][ j ] = 255
    cv2.line(posi, (centerw, 0), (centerw, height-1), (0, 0, 255), 3)
    cv2.line(posi, (0, centerh), (width-1, centerh), (0, 0, 255), 3)

    Npos = [ centerh , centerw , 0 ]
    
    allobjp = []
    allch = []

    for c in cnts:
		# approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)
        convexhull = cv2.convexHull( approx )

		# ensure that the approximated contour is "roughly" rectangular
        #cv2.drawContours(frame, [approx], -1, (0, 255, 0), 4)
        if ( len(approx) >= OL and len(approx) <= OR ) or ( len(convexhull) >= OL and len(convexhull) <= OR ):
                        
                    # compute the bounding box of the approximated contour and
                    # use the bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            aspectRatio = w / float(h)
            ch = np.array( [ approx[ 0 ][ 0 ], approx[ 1 ][ 0 ], approx[ 2 ][ 0 ], approx[ 3 ][ 0 ] ], dtype = "float32" )   		

                    # compute the solidity of the original contour
            area = cv2.contourArea(c)
            hullArea = cv2.contourArea(cv2.convexHull(c))
            solidity = area / float(hullArea)

                    # compute whether or not the width and height, solidity, and
                    # aspect ratio of the contour falls within appropriate bounds
            keepSolidity = solidity > 0.9
            keepAspectRatio = aspectRatio >= 0.9 and aspectRatio <= 1.1

            if w < L or h < L: continue

            if keepSolidity:
                cX, cY = 0, 0
                for i in range(4):
                    cX = cX + ch[ i ][ 0 ]
                    cY = cY + ch[ i ][ 1 ]
                cX = cX / 4
                cY = cY / 4
			    
                (frame2, tw, th, theta ) = four_point_transform( gray , ch )
                if debug: cv2.imshow( "Frame3" , frame2 )
                if th < L : continue
                T = getTarget( frame2 , 0 , 0 , th , tw , argN , argM )
                pwd = find_pwd( T )
                cv2.drawContours(frame, [approx], -1, (0, 0, 255), 4)
                
                way = -1
                Num = 0

                if pwd in No:
                    #Npos = get_pos( No.get( pwd ) , 0 , cX - ( width // 2 ) , cY - ( height // 2 ) , area , theta )
                    way = 0
                    Num = No.get( pwd )
                elif pwd in LNo:
                    #Npos = get_pos( LNo.get( pwd ) , 1 , cX - ( width // 2 ) , cY - ( height // 2 ) , area , theta )
                    way = 1
                    Num = LNo.get( pwd )
                elif pwd in RNo:
                    #Npos = get_pos( RNo.get( pwd ) , 2 , cX - ( width // 2 ) , cY - ( height // 2 ) , area , theta )
                    way = 2
                    Num = RNo.get( pwd )
                elif pwd in DNo:
                    #Npos = get_pos( DNo.get( pwd ) , 3 , cX - ( width // 2 ) , cY - ( height // 2 ) , area , theta )
                    way = 3
                    Num = DNo.get( pwd )
                else: continue

                rvecs, tvecs, inliers = None, None, None
                if len( convexhull ) == 4:
                    tmp = np.array( [ convexhull[ 0 ][ 0 ] ,
                                convexhull[ 1 ][ 0 ] ,
                                convexhull[ 2 ][ 0 ] ,
                                convexhull[ 3 ][ 0 ] ] )
                    convexhull = order_points( tmp )
                    if way == 1: convexhull = [ convexhull[ 3 ] , convexhull[ 0 ] , convexhull[ 1 ] , convexhull[ 2 ] ]
                    if way == 2: convexhull = [ convexhull[ 1 ] , convexhull[ 2 ] , convexhull[ 3 ] , convexhull[ 0 ] ]
                    if way == 3: convexhull = [ convexhull[ 2 ] , convexhull[ 3 ] , convexhull[ 0 ] , convexhull[ 1 ] ]
                # take all
                    for i in range(4):
                        allobjp.append( objp[ Num ][ i ] )
                        allch.append( convexhull[ i ] )
                # /take all
                    retval, rvecs, tvecs = cv2.solvePnP(objp[ Num ], np.float32( convexhull ), mtx, None)
                    rmtx, jacob = cv2.Rodrigues( rvecs )


                    #Npos = -np.dot( ( rmtx ).T , tvecs )
                    #Npos[ 2 ] = -Npos[ 2 ]
                    #status = "Target(s) Acquired " + str( pwd ) + " X:" + str( Npos[ 0 ] ) + " Y:" + str( Npos[ 1 ] ) + " Z:" + str( Npos[ 2 ] )
                    #status = " ".join(map(lambda x: str(x[0]), Npos))
                    #if debug: print(status)
                    #sys.stdout.flush()
                if debug: cv2.imshow( "Frame2" , frame2 )
                #status = "Target(s) Acquired modified " + str( pwd ) + " " + str( area )

# take all
    if len( allobjp ) > 0:
        retval, rvecs, tvecs = cv2.solvePnP( np.float32( allobjp ) , np.float32( allch ), mtx, None)
        rmtx, jacob = cv2.Rodrigues( rvecs )

        Npos = np.dot( ( rmtx ).T , tvecs )
        Npos[ 0 ] = -Npos[ 0 ]
        status = str( pwd ) + " X:" + str( Npos[ 0 ] ) + " Y:" + str( Npos[ 1 ] ) + " Z:" + str( Npos[ 2 ] )
        status = " ".join(map(lambda x: str(x[0]), Npos))
        if debug: print( "                       " + str( len( allobjp ) ) )
        print( status )
        sys.stdout.flush()
# /take all

	# draw the status text on the frame
    cv2.putText(frame, status, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    #cv2.circle(posi , ( int(centerw + Npos[ 0 ]) , int( centerh - Npos[ 1 ] ) ) , 10 , (0,0,255) , -1 )
    cv2.circle(posi , ( int(centerw + Npos[ 0 ]) , int( centerh - Npos[ 1 ] ) ) , 10 , (0,0,255) , -1 )
    cv2.putText(posi, status, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    if debug: cv2.imshow( "POS" , posi )

	# show the frame and record if a key is pressed
    if debug: cv2.imshow( "Frame" , frame )
    key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
