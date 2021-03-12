import numpy as np
import matplotlib.pyplot as plt

up = 1.1
down = 1/up
p_up = (1-down)/(up-down)
p_down = 1 - p_up

underlying_call = np.zeros((53, 53))
underlying_call[0,0] = 50
for i in range(53):
    for j in range(53):
        if i != j:
            underlying_call[i,j] = underlying_call[i,j-1] * 1.1
        else:
            if i != 0:
                underlying_call[i,j]=underlying_call[i-1,j-1] / 1.1

underlying_put = np.zeros((53, 53))
underlying_put[0,0] = 50000
for i in range(53):
    for j in range(53):
        if i != j:
            underlying_put[i,j] = underlying_put[i,j-1] * 1.1
        else:
            if i != 0:
                underlying_put[i,j]=underlying_put[i-1,j-1] / 1.1

def swing_up(underlying_call, previous=None):
    if previous is None:
        previous = np.zeros_like(underlying_call)
    swing = np.zeros_like(underlying_call)
    exercise_nodes = np.zeros_like(underlying_call)
    for j in range(52, -1, -1):
        for i in range(j+1):
            if j != 52:
                val_not_exe = p_up*swing[i,j+1] + p_down*swing[i+1, j+1]
                val_exe = underlying_call[i, j]-50 + p_up*previous[i,j+1]+p_down*previous[i+1,j+1]
            else:
                val_not_exe = 0
                val_exe = underlying_call[i, j]-50            
            if val_exe > val_not_exe * 1.0001:
                exercise_nodes[i, j] = 4
                swing[i, j] = val_exe
            elif val_exe  < val_not_exe:
                exercise_nodes[i, j] = 1
                swing[i, j] = val_not_exe
            else:
                exercise_nodes[i, j] = 2
                swing[i, j] = val_not_exe
    return swing, exercise_nodes

def swing_down(underlying_put, previous=None):
    if previous is None:
        previous = np.zeros_like(underlying_put)
    swing = np.zeros_like(underlying_put)
    exercise_nodes = np.zeros_like(underlying_put)
    for j in range(52, -1, -1):
        for i in range(j+1):
            if j != 52:
                val_not_exe = p_up*swing[i,j+1] + p_down*swing[i+1, j+1]
                val_exe = 50000-underlying_put[i, j] + p_up*previous[i,j+1]+p_down*previous[i+1,j+1]
            else:
                val_not_exe = 0
                val_exe = 50000 - underlying_put[i, j]           
            if val_exe > val_not_exe * 1.0001:
                exercise_nodes[i, j] = 4
                swing[i, j] = val_exe
            elif val_exe  < val_not_exe:
                exercise_nodes[i, j] = 1
                swing[i, j] = val_not_exe
            else:
                exercise_nodes[i, j] = 2
                swing[i, j] = val_not_exe
    return swing, exercise_nodes

up1, exercise_nodes = swing_up(underlying_call, None)
up2, exercise_nodes = swing_up(underlying_call, up1)
up3, exercise_nodes = swing_up(underlying_call, up2)
up4, exercise_nodes = swing_up(underlying_call, up3)
print(up4[0,0])
plt.imshow(exercise_nodes, cmap="Greys")


down1, exercise_nodes = swing_down(underlying_put, None)
down2, exercise_nodes = swing_down(underlying_put, down1)
down3, exercise_nodes = swing_down(underlying_put, down2)
down4, exercise_nodes = swing_down(underlying_put, down3)
print(down4[0,0])
#plt.imshow(exercise_nodes, cmap="Greys")

