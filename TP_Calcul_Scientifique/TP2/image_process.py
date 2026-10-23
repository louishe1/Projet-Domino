#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Fonctions de traitement d'images.
Version non optimisée.

.. codeauthor:: R. Moitié
"""

import numpy as np


def copy(img):
    """Copie la couleur (3 valeurs) de chaque pixel.

    Parameters
    ----------
    img : numpy.array
        Image source.

    Returns
    -------
    res : numpy.array
        Image résultat
    """
    res = np.zeros(img.shape, dtype=np.uint8)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3):
                res[i, j, k] = img[i, j, k]
    return res

def negative(img) :

    for i in range(img.shape[0]) :
        for j in range(img.shape[1]) :
            img[i,j] = [255 - img[i,j, 0] , 255 - img[i, j, 1], 255 - img[i, j, 2] , img[i, j, 3] ]
    return(img)

def h_flip(img) :

    img2 = img.copy()                    # on peut utiliser np.zeros(img.shape, dtype=np.uint8)
    for i in range(img.shape[0]) :
        for j in range(img.shape[1]) :
            img2[i, j] = img[i,img.shape[1]-1-j]
    return(img2)

def v_flip(img) :

    img2 = img.copy()
    for i in range(img.shape[0]) :
        for j in range(img.shape[1]) :
            img2[i, j] = img[img.shape[0]-1-i,j]
    return(img2)

def blue(img) :
    for i in range(img.shape[0]) :
        for j in range(img.shape[1]) :
            img[i,j] = [img[i,j][0],0,0,img[i,j][3]]
    return(img)


def green(img):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i, j] = [ 0,img[i, j][1], 0, img[i, j][3]]
    return (img)

def red(img):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i, j] = [ 0, 0,img[i, j][2], img[i, j][3]]
    return (img)

def rotate_colors(img) :
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i, j] = [ img[i, j][2], img[i, j][0], img[i, j][1], img[i, j][3]]
    return(img)

def blur(img) :

    res = img.copy()
    for i in range(1,img.shape[0]-1):
        for j in range(1,img.shape[1]-1):
            res[i, j] = [int((float(img[i, j - 1, 0]) + float(img[i, j, 0]) + float(img[i, j + 1, 0]) + float(img[i - 1, j - 1, 0]) + float(img[i - 1, j, 0]) + float(img[i-1, j+1, 0]) + float(img[i+1, j-1, 0]) + float(img[i+1, j, 0]) + float(img[i+1, j+1, 0])))/9,
                         int((float(img[i, j - 1, 1]) + float(img[i, j, 1]) + float(img[i, j + 1, 1]) + float(img[i - 1, j - 1, 1]) + float(img[i - 1, j, 1]) + float(img[i - 1, j + 1, 1]) + float(img[i + 1, j - 1, 1]) + float(img[i + 1, j, 1]) + float(img[i + 1, j + 1, 1]))) / 9,
                         int((float(img[i, j - 1, 2]) + float(img[i, j, 2]) + float(img[i, j + 1, 2]) + float(img[i - 1, j - 1, 2]) + float(img[i - 1, j, 2]) + float(img[i - 1, j + 1, 2]) + float(img[i + 1, j - 1, 2]) + float(img[i + 1, j, 2]) + float(img[i + 1, j + 1, 2]))) / 9,
                          img[i, j, 3]]
    return(res)

def zoom(img) :
    N , M = (img.shape[0]//2)*2 , (img.shape[1]//2)*2   # force la taille paire
    res = np.zeros((N, M, 4), dtype=np.uint8)
    coupe = np.zeros((N//2, M//2, 4), dtype=np.uint8)
    for i in range(N//4, (N//4) + (N//2)) :
        for j in range(M // 4, (M // 4) + (M//2)):
            coupe[i - (N//4), j - (M//4)] = img[i,j]
    for i in range(N//2) :
        for j in range(M//2) :
            res[2*i,2*j],res[2*i,2*j+1],res[2*i+1,2*j],res[2*i+1,2*j+1] = coupe[i,j],coupe[i,j],coupe[i,j],coupe[i,j]
    return(res)










