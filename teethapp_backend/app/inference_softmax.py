import tensorflow as tf
import os
import time
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import matplotlib as mpl#pang_add_20190703
from keras.preprocessing.image import load_img, img_to_array

from flask import current_app

class DeepLabModel(object):
    """Class to load deeplab model and run inference."""

    INPUT_TENSOR_NAME = 'ImageTensor:0'
    OUTPUT_TENSOR_NAME = 'SemanticPredictions:0'
    FROZEN_GRAPH_NAME = 'frozen_inference_graph.pb'
    #FROZEN_GRAPH_NAME = 'frozen_inference_graph_0705_700_700_726.pb'

    def __init__(self, model_path):
        """Creates and loads pretrained deeplab model."""
        self.graph = tf.Graph()

        graph_def = None
        graph_path = os.path.join(model_path, self.FROZEN_GRAPH_NAME)
        with tf.gfile.FastGFile(graph_path,'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())

        if graph_def is None:
            raise RuntimeError('Cannot find inference graph in tar archive.')

        with self.graph.as_default():
            tf.import_graph_def(graph_def, name='')

        self.sess = tf.Session(graph=self.graph)

    def run(self, image):
        """
        Runs inference on a single image.
        Args:
            image: A uint8 Image object, raw input image.
        Returns:
            result[0]: Segmentation map of `image`.
        """

        result = self.sess.run(
            self.OUTPUT_TENSOR_NAME,
            feed_dict={self.INPUT_TENSOR_NAME: image})

        return result

def create_model():
    sstime=time.time()
    opt={}
    #opt['model_dir']="models/deeplabv3/" #pang_comment_20190619
    #opt['model_dir']="/data/pzn/teethapp/app/model" #pang_add_20190619
    opt['model_dir']="/data2/pzn/teethapp/app/model" #apng_add_20190703

    print('loading DeepLab model...')
    MODEL = DeepLabModel(opt['model_dir'])
    print('model loaded successfully!')

    etime=time.time()
    print(etime-sstime)
    return MODEL

def batch_inference(MODEL, path):
    try:
        
        orignal_im = load_img(path)
        orignal_im = img_to_array(orignal_im)
        orignal_im = np.expand_dims(orignal_im, axis=0).astype(np.uint8)

    except IOError:
        print('Cannot retrieve image. Please check url: ' + path)
        return

    print('running deeplab on image %s...' % path)
    result = MODEL.run(orignal_im)

    
    
    print(type(result))
    print(result[0].shape)  # (1, height, width)

    num1 = 0
    num2 = 0
    for i in result[0]:
        for j in i:
            if j == 1:
                num1 = num1 + 1
            elif j == 2:
                num2 = num2 + 1
    ratio = round(num2 / (num1 + num2) * 100, 2)
    
    #pang_add_20190619
    #plt.imshow(result[0])#pang_comment_20190703
    

    #pang_add_20190703
    #print(np.sum(result[0]==2))
    plaque_num = np.sum(result[0]==2)
    if(plaque_num > 0):
        #my_color = ['black','white','red'] #pang_add_20190628  For Control Colormap
        my_color = ['black','white','yellow'] #pang_add_20190705  For Control Colormap  
        my_cmap = mpl.colors.ListedColormap(my_color)
        plt.imshow(result[0], cmap = my_cmap)

        cbar = plt.colorbar(shrink=0.5)
        cbar.set_ticks(np.linspace(0,10,11,endpoint=True))
        cbar.set_ticklabels(('background','teeth','plaque'))
        #cbar.set_ticklabels((u'背景',u'牙齿',u'菌斑'))
        
    else:
        #my_color = ['black','white'] #pang_add_20190628  For Control Colormap
        my_color = ['black','white'] #pang_add_20190705  For Control Colormap 
        my_cmap = mpl.colors.ListedColormap(my_color)
        plt.imshow(result[0], cmap = my_cmap)
        #plt.imshow(result[0])
        cbar = plt.colorbar(shrink=0.5)
        cbar.set_ticks(np.linspace(0,10,11,endpoint=True))
        cbar.set_ticklabels(('background','teeth'))
        #cbar.set_ticklabels((u'背景',u'牙齿'))

    resultpath = path.split('.')[0] + '.' + path.split('.')[1] + '.' + path.split('.')[
        2] + '_result' + '.jpg'
    print(resultpath)
    plt.savefig(resultpath)#get the recent image and save
    plt.clf() #pang_add_20190703
    return resultpath, ratio
