
import numpy as np
num=np.matmul(np.array([
                [1,2,3,4],
                [5,6,7,8],
                [9,10,11,12],
                [13,14,15,16]], dtype = np.float32).T,
                np.array([
                [1,2,3,4],
                [5,6,7,8],
                [9,10,11,12],
                [13,14,15,16]], dtype = np.float32).T)
print(num)
