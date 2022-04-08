import tf as tensorflow
import faulthandler

faulthandler.enable()

model = tf.saved_model.load('tmp-dir/ssd_mobilenet_v1_coco_2017_11_17/saved_model')