import os
import streamlit.components.v1 as components
from streamlit.components.v1.components import CustomComponent
from typing import List
import cv2
import time
import streamlit as st
import streamlit.elements.image as st_image
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from hashlib import md5
from streamlit_image_annotation_customize import IS_RELEASE

if IS_RELEASE:
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    build_path = os.path.join(absolute_path, "frontend/build")
    _component_func = components.declare_component("st-detection", path=build_path)
else:
    _component_func = components.declare_component("st-detection", url="http://localhost:3000")

def get_colormap(label_names, colormap_name='gist_rainbow'):
    colormap = {} 
    cmap = plt.get_cmap(colormap_name)
    for idx, l in enumerate(label_names):
        rgb = [int(d) for d in np.array(cmap(float(idx)/len(label_names)))*255][:3]
        colormap[l] = ('#%02x%02x%02x' % tuple(rgb))
    return colormap

#'''
#bboxes:
#[[x,y,w,h],[x,y,w,h]]
#labels:
#[0,3]
#'''
def detection(image_path, masked_image, label_list, bboxes=None, points=None, neg_points=None,labels=None, height=800, width=512, line_width=5.0, key=None, m_labels=None, is_processing=False, need_update_annotation=0, need_update_loading=0) -> CustomComponent:
    image = None
    if masked_image is not None:
        try:
            image = Image.fromarray(masked_image)
        except:
            image = masked_image
        
    else:
        image = Image.open(image_path)
    original_image_size = image.size
    image.thumbnail(size=(width, height))
    resized_image_size = image.size
    scale = original_image_size[0]/resized_image_size[0]
    
    image_url = st_image.image_to_url(image, image.size[0], True, "RGB", "PNG", f"detection-{md5(image.tobytes()).hexdigest()}-{key}")
    if image_url.startswith('/'):
        image_url = image_url[1:]
    m_labels = m_labels if m_labels else  get_colormap(label_list, colormap_name='gist_rainbow')
    bbox_info = [{'bbox':[b/scale for b in item[0]], 'label_id': item[1], 'label': item[1]} for item in zip(bboxes, labels["bboxes"]["labels"])]
    points_info = [{'point':[b/scale for b in item[0]], 'label_id': item[1], 'label': item[1]} for item in zip(points, labels["points"]["labels"])]
    neg_points_info = [{'neg_point':[b/scale for b in item[0]], 'label_id': item[1], 'label': item[1]} for item in zip(neg_points, labels["neg_points"]["labels"])]
    component_value = _component_func(image_url=image_url, image_size=image.size, label_list=label_list, bbox_info=bbox_info, points_info=points_info, neg_points_info=neg_points_info,m_labels=m_labels, line_width=line_width, is_processing=is_processing, need_update_annotation=need_update_annotation, need_update_loading=need_update_loading, key=key)
    #print("component_value...", component_value)
    ##print([list(x * scale for  in p["points"]) for p in component_value["points"]])
    if component_value is not None:
        component_value_bbox = {"bboxes":[[x * scale for x in bbox["bboxes"]] for bbox in component_value["bboxes"]], "labels":[bbox["label_id"] for bbox in component_value["bboxes"]]}
        component_value_point = {"points": [[x * scale for x in p["points"]] for p in component_value["points"]], "labels": [p["label_id"] for p in component_value["points"]]}  
        component_value_neg_point = {"neg_points": [[x * scale for x in p["neg_points"]] for p in component_value["neg_points"]], "labels": [p["label_id"] for p in component_value["neg_points"]]} 
        return {
        "bboxes": component_value_bbox,
        "points": component_value_point,
        "neg_points": component_value_neg_point
        }
    else:
        return None
        component_value_bbox = {"bboxes": [], "labels":[]}
        component_value_point = {"points": [], "labels":[]}
        component_value_neg_point = {"neg_points": [], "labels":[]}
   
# if not IS_RELEASE:
#     from glob import glob
#     import pandas as pd
#     label_list = ['deer', 'human', 'dog', 'penguin', 'framingo', 'teddy bear']
#     image_path_list = glob('/Users/hocnx/code/streamlit_image_annotation_customize/image/*.jpg')
#     if 'result_dict' not in st.session_state:
#         result_dict = {}
#         for img in image_path_list:
#             result_dict[img] = {'bboxes':{"bboxes": [],'labels':[]}, 'points': {"points":[], 'labels':[]},'neg_points':  {"neg_points":[],'labels':[]}}
#         st.session_state['result_dict'] = result_dict.copy()
#     #num_page = st.slider('page', 0, len(image_path_list)-1, 0, key='slider1')
#     #print("image_path_list", image_path_list)
#     target_image_path = image_path_list[0]
#     #print("aaaa",st.session_state['result_dict'][target_image_path])
#     if "image" not in st.session_state:
#         st.session_state["image"] = None
#     new_labels = detection(image_path=target_image_path, 
#                            masked_image=st.session_state["image"],
#                       bboxes=st.session_state['result_dict'][target_image_path]['bboxes']['bboxes'], 
#                       points=st.session_state['result_dict'][target_image_path]['points']['points'],
#                       neg_points=st.session_state['result_dict'][target_image_path]['neg_points']['neg_points'],
#                       labels=st.session_state['result_dict'][target_image_path], 
#                       label_list=label_list, line_width=5, key=target_image_path,color_map={"deer": "#66ff66"})
#     #print("new_labels", new_labels)
    
#     if new_labels["bbox"] is not None:
#         #time.sleep(10)
#         st.session_state['result_dict'][target_image_path]['bboxes']['bboxes'] = [
#             v['bbox'] for v in new_labels['bbox']]
#         st.session_state['result_dict'][target_image_path]['bboxes']['labels'] = [
#             v['label'] for v in new_labels['bbox']]
        

#         st.session_state['result_dict'][target_image_path]['points']['points'] = [
#             v['point'] for v in new_labels['point']]
#         st.session_state['result_dict'][target_image_path]['points']['labels'] = [
#             v['label'] for v in new_labels['point']]

#         st.session_state['result_dict'][target_image_path]['neg_points']['neg_points'] = [
#             v['neg_point'] for v in new_labels['neg_point']]
#         st.session_state['result_dict'][target_image_path]['neg_points']['labels'] = [
#             v['label'] for v in new_labels['neg_point']]
#         st.session_state["image"] = cv2.imread(target_image_path)
#         time.sleep(10)
#         #print("aa", st.session_state['result_dict'][target_image_path])
    #st.button("aaaa")
    #st.json(st.session_state['result_dict'])
    