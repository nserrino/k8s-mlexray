import os
import tensorflow as tf
import numpy as np
import json

from flask import Flask
app = Flask(__name__)

mobilenet = tf.keras.applications.MobileNet()
file = tf.keras.utils.get_file(
    "grace_hopper.jpg",
    "https://storage.googleapis.com/download.tensorflow.org/example_images/grace_hopper.jpg")
grace_hopper_img = tf.keras.utils.load_img(file, target_size=[224, 224])
x = tf.keras.utils.img_to_array(grace_hopper_img)
x = tf.keras.applications.mobilenet.preprocess_input(
    x[tf.newaxis,...])

labels_path = tf.keras.utils.get_file(
    'ImageNetLabels.txt',
    'https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
imagenet_labels = np.array(open(labels_path).read().splitlines())


resnet50 = tf.keras.applications.resnet50.ResNet50(weights="imagenet")
img_path = "elephant.jpg"
file = tf.keras.utils.get_file(
    img_path,
    "https://upload.wikimedia.org/wikipedia/commons/f/f9/Zoorashia_elephant.jpg")
elephant_img = tf.keras.preprocessing.image.load_img(file, target_size=(224, 224))
y = tf.keras.preprocessing.image.img_to_array(elephant_img)
y = np.expand_dims(y, axis=0)
y = tf.keras.applications.resnet50.preprocess_input(y)
  
@app.route('/execute/nothing')
def execute_nothing():
   return ''
  
@app.route('/execute/grace_hopper')
def execute_hopper():
   result = mobilenet(x)
   decoded = imagenet_labels[np.argsort(result)[0,::-1][:5]+1]
   return json.dumps(decoded.tolist())

@app.route('/execute/elephant')
def execute_elephant():
    preds = resnet50.predict(y)
    decoded = tf.keras.applications.resnet50.decode_predictions(preds, top=3)[0]
    decoded = [(x[1], x[2].item()) for x in decoded]
    return json.dumps(decoded)

if __name__ == '__main__':
   port = int(os.environ.get('PORT', 5000))
   app.run(debug=True, host='0.0.0.0', port=port)