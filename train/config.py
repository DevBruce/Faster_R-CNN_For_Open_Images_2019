from tensorflow.keras.optimizers import Adam
import os
import math


__all__ = (
    'ROOT_DIR', 'CONFIG_DIR', 'SAVED_MODEL_DIR', 'PRETAINED_MODEL_DIR', 'DATA_DIR', 'RECORD_DIR',
    'SAVE_RECORD_PATH', 'SAVE_MODEL_PATH', 'SAVE_CONFIG_PATH',
    'PRETAINED_MODEL_FILE_PATH', 'TRAIN_ANNOTATION_FILE_PATH',
    'MASK_ANNOTATION_FILE_PATH',
    'optimizer', 'optimizer_classifier',
    'epsilon',
    'lambda_rpn_regr', 'lambda_rpn_class', 'lambda_cls_class', 'lambda_cls_regr',
    'Config',
)

# Path Config
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(ROOT_DIR, 'config')
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR, exist_ok=True)
SAVED_MODEL_DIR = os.path.join(ROOT_DIR, 'saved_model')
if not os.path.exists(SAVED_MODEL_DIR):
    os.makedirs(SAVED_MODEL_DIR, exist_ok=True)
RECORD_DIR = os.path.join(ROOT_DIR, 'record')
if not os.path.exists(RECORD_DIR):
    os.makedirs(RECORD_DIR, exist_ok=True)
PRETAINED_MODEL_DIR = os.path.join(ROOT_DIR, 'pretained_model')
DATA_DIR = os.path.join(ROOT_DIR, 'data')

SAVE_RECORD_PATH = os.path.join(RECORD_DIR, 'record.csv')  # Record data
SAVE_MODEL_PATH = os.path.join(SAVED_MODEL_DIR, 'saved_model.hdf5')
SAVE_CONFIG_PATH = os.path.join(CONFIG_DIR, 'config.pickle')
PRETAINED_MODEL_FILE_PATH = os.path.join(PRETAINED_MODEL_DIR, 'vgg16_weights_tf_dim_ordering_tf_kernels.h5')
TRAIN_ANNOTATION_FILE_PATH = os.path.join(DATA_DIR, 'train_annotation.txt')
MASK_ANNOTATION_FILE_PATH = os.path.join(DATA_DIR, 'train-segmentation-masks_light.csv')  # To Change If Train All Data

# Optimizer Function
optimizer = Adam(lr=1e-5)
optimizer_classifier = Adam(lr=1e-5)

# ETC
epsilon = 1e-4
lambda_rpn_regr = 1.0
lambda_rpn_class = 1.0
lambda_cls_regr = 1.0
lambda_cls_class = 1.0


# Config Class
class Config:
    def __init__(self):
        # Print the process or not
        self.verbose = True
        # Name of base network
        self.network = 'vgg'
        self.base_net_weights = PRETAINED_MODEL_FILE_PATH
        # Setting for data augmentation
        self.use_horizontal_flips = True
        self.use_vertical_flips = True
        self.rot_90 = True

        # Anchor box scales
        # Note that if im_size is smaller, anchor_box_scales should be scaled
        # Original anchor_box_scales in the paper is [128, 256, 512]
        self.anchor_box_scales = [64, 128, 256]

        # Anchor box ratios
        self.anchor_box_ratios = [
            [1, 1],
            [1. / math.sqrt(2), 2. / math.sqrt(2)],
            [2. / math.sqrt(2), 1. / math.sqrt(2)],
        ]

        # Size to resize the smallest side of the image
        # Original setting in paper is 600. Set to 300 in here to save training time
        self.im_size = 300

        # image channel-wise mean to subtract
        self.img_channel_mean = [103.939, 116.779, 123.68]
        self.img_scaling_factor = 1.0

        # number of ROIs at once
        self.num_rois = 4

        # stride at the RPN (this depends on the network configuration)
        self.rpn_stride = 16  # vgg --> MaxPooling x 4 --> 2 ** 4

        self.balanced_classes = False

        # scaling the stdev
        self.std_scaling = 4.0
        self.classifier_regr_std = [8.0, 8.0, 4.0, 4.0]

        # overlaps for RPN
        self.rpn_min_overlap = 0.3
        self.rpn_max_overlap = 0.7

        # overlaps for classifier ROIs
        self.classifier_min_overlap = 0.1
        self.classifier_max_overlap = 0.5

        # placeholder for the class mapping, automatically generated by the parser
        self.class_mapping = None
        self.model_path = SAVE_MODEL_PATH
