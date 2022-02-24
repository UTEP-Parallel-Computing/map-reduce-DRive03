# Daniel Alejandro Rivera Estrada ID 80699287
import pymp, random, time
import numpy as np


# This function will make the array and will populate it with random numbers from 0 to max value
def populateArray(size):
    matrix = [[0] * size for i in range(size)]
    print("Generating 2d matrices..")
    for r in range(0, size):  # With these for loops we populate the array
        for c in range(0, size):
            matrix[r][c] = 1  # random.randint(0, maxValue)
    return matrix


# this function will only print a fraction of the original matrix
def printFractionMatrix(matrix, size):
    rang = 10
    if size <= 10:
        rang = size
    print()
    for row in range(1, rang):
        for col in range(1, rang):
            print(f'{matrix[row][col]}', end='')
        print('')
    print()


# Now this will be the parallel version for the matrix multiply function
def parallelMultiply(m1, m2, nT):
    startTime = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)  # start the timer for the execution
    product = pymp.shared.array((size, size),
                                dtype=np.intc)  # this will be the matrix where the result of the multiplication will be stored

    with pymp.Parallel(nT) as p:  # make the whole process parallel

        for i in p.range(0, size):  # same size for both because its a square matrix
            for j in range(0, size):
                for k in range(0, size):
                    product[i][j] += m1[i][k] * m2[k][j]

    endTime = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)  # get the time the matrix multiply ended
    totalTime = endTime - startTime
    printFractionMatrix(product, size)
    print("Time to multiply: %s", totalTime)


# Asking for the size and the maximum possible value of the matrices
print()
size = int(input("Enter the size of the square matrices:\n"))
# maxVal = int(input("Enter the max possible value that can be generated for the matrices:\n"))
nThreads = int(input("Enter the number of threads :\n"))

# Calling the function to generate the arrays
matrixA = populateArray(size)
matrixB = populateArray(size)

print("These are the matrices randomly generated..")
printFractionMatrix(matrixA, size)

print("Multiplies..\n")
printFractionMatrix(matrixB, size)

parallelMultiply(matrixA, matrixB, nThreads)