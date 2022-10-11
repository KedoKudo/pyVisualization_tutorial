#!/usr/bin/env python


import numba
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from matplotlib import cm

# MACRO
IMGSIZE = 512
CONSTC = complex(-0.8, 0.156)
ZABSMAX = 10
ITERMAX = 200

# Build the img
@numba.jit(nopython=True)
def juliaset(z, max_iter=ITERMAX, c=CONSTC):
    img = np.zeros(z.shape)
    for i in range(max_iter):
        z = z**2 + c
        img = np.where(np.abs(z) < ZABSMAX, i, img)
    return img/max_iter

def draw(max_iter=ITERMAX, scale=1.0, c=CONSTC, img_size=IMGSIZE, cmap='jet'):
    # build starting z
    r = np.linspace(-0.5*scale, 0.5*scale, img_size)
    i = np.linspace(-0.5*scale, 0.5*scale, img_size)
    i, r = np.meshgrid(i, r, sparse=False, indexing='xy')
    z = r + 1j*i
    # compute julia set
    img = juliaset(z, max_iter=max_iter, c=c)
    # plot
    fig, ax = plt.subplots()
    ims = ax.imshow(img, interpolation='nearest', cmap=cmap)
    plt.colorbar(ims)
    ax.set_xticks([])
    ax.set_yticks([])
    return fig

# Header
st.title("Julia Set Visualizer")
st.latex("Z = Z^2 + C")
# Control
scale = st.sidebar.slider(label="Zoom", min_value=1e-3, max_value=1.0, value=0.1)
creal = st.number_input(label="C.real", min_value=-2.0, max_value=2.0, value=CONSTC.real)
cimag = st.number_input(label="C.imag", min_value=-2.0, max_value=2.0, value=CONSTC.imag)
cmap = st.selectbox(
    label="Color Map",
    options=[cmap for cmap in cm.cmaps_listed.keys() if not cmap.endswith("_r")],
    index=0,
)
# Display
st.pyplot(draw(scale=scale, c=complex(creal, cimag), cmap=cmap))
