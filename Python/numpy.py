# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 12:01:14 2016

@author: ebm94
"""

import numpy as np

a = np.array(range(9))

#change the dimensions of an array into desired ones
a_square = a.reshape((3,3))
a
a_square

b_square = np.array(range(10,19)).reshape((3,3))

#add both matrices
c = a_square + b_square

#subtract one from another
c = a_square - b_square

# add a column vector and a row vector together
row_vector = np.array(range(3)).reshape((1,3))
column_vector = np.array(range(3)).reshape((3,1))

row_vector + column_vector

#multiply both
result = row_vector*column_vector

#define a function that calculates a the inverse of a square matrix
def calculate_inverse(square_matrix):
    inverted_matrix = 1 / square_matrix
    return inverted_matrix

input_matrix = np.array([[1,2,3],[4,5,6],[7,8,8]])
result = calculate_inverse(input_matrix)
result2=np.linalg.inv(input_matrix)

#create a matrix of zeros
matrix_zeros = np.zeros((10,10))
#create an identity matrix
identity = np.eye(10)
identity

#accessing rows and columns of a matrix
c = np.array([[1,2,3],[4,5,6],[7,8,9]])
c[0]
c.shape[0]

c[:,2]

#write a function to print out the row and column sums
def calculate_sums(input_matrix):
    for i in range(input_matrix.shape[0]):
        print 'sum of row ',i+1,' = ',input_matrix[i].sum()
    for i in range(input_matrix.shape[1]):
        print 'sum of column ',i+1, ' = ',input_matrix[:,i].sum()
        # Removed curly brackets from print


calculate_sums(c)



