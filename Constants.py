import numpy as np
board_rows = 20
board_columns = 10
bag_size = 5 


piece_offsets= {
#I piece, light blue
1:
np.array([
[-1.5,-0.5,0.5,1.5],
[-0.5,-0.5,-0.5,-0.5]
    ]),
#J piece, dark blue
2:
np.array([
[-1,-1,0,1],
[-1,0,0,0]
    ]),
#L piece, orange
3:
np.array([
[1,-1,0,1],
[-1,0,0,0]
    ]),
#O piece, yellow square
4:
np.array([
[-0.5,0.5,-0.5,0.5],
[-0.5,-0.5,0.5,0.5],
    ]),
#S piece, green
5:
np.array([
[0,1,-1,0],
[-1,-1,0,0]
    ]),
#T piece, purple
6:
np.array([
[0,-1,0,1],
[-1,0,0,0]
    ]),
#Z piece, red
7:
np.array([
[-1,0,0,1],
[-1,-1,0,0]
    ])
}

centerShifted = (int) (np.floor(board_columns/2))-(1-board_columns%2)

piece_origins={
#I piece, light blue
1:
np.array([[centerShifted+0.5],[1+0.5]]),
#J piece, dark blue
2:
np.array([[centerShifted],[1]]),
#L piece, orange
3:
np.array([[centerShifted],[1]]),
#O piece, yellow square
4:
np.array([[centerShifted+0.5],[0.5]]),
#S piece, green
5:
np.array([[centerShifted],[1]]),
#T piece, purple
6:
np.array([[centerShifted],[1]]),
#Z piece, red
7:
np.array([[centerShifted],[1]])
}

max_time_per_drop = 10/60
#Higher values mean that holding down drops pieces faster
drop_inertia = 0.5