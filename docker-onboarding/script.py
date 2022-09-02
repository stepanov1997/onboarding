import os
import sys
import numpy as np
from datetime import datetime

import time

if __name__ == "__main__":
    matrix_elements_string = os.environ["MATRIX_ELEMENTS"]
    matrix_elements = [int(num) for num in matrix_elements_string.split(",")]
    args = sys.argv[1:]
    width, height = tuple(args)
    array = np.array(matrix_elements)
    matrix = np.reshape(array, newshape=(int(width), int(height)))
    if width == height:
        det = np.linalg.det(matrix)
        print(det)
        try:
            with open(f"/results/report-{datetime.today().strftime('%y%m%d:%H%M%S')}.txt", "w") as f:
                f.write(f"""
                    Matrix: 
                    {matrix}
                    
                    Determinant: {det}
                """)
        except Exception as e:
            print(e)
    else:
        print("Width and height are not the same.")