import cv2
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

@st.cache
def image_thresh(img, ksize=100):
    imageGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imageGray, ksize, 255, cv2.THRESH_BINARY_INV)
    return thresh