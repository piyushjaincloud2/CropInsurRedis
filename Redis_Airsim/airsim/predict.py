"""Sample prediction script for TensorFlow 2"""
import argparse
import tensorflow as tf
import numpy as np
import PIL.Image

MODEL_FILENAME = 'model.pb'
LABELS_FILENAME = 'labels.txt'


class ObjectDetection:
    INPUT_TENSOR_NAME = 'image_tensor:0'
    OUTPUT_TENSOR_NAMES = ['detected_boxes:0', 'detected_scores:0', 'detected_classes:0']

    def __init__(self, model_filename):
        graph_def = tf.compat.v1.GraphDef()
        with open(model_filename, 'rb') as f:
            graph_def.ParseFromString(f.read())

        self.graph = tf.Graph()
        with self.graph.as_default():
            tf.import_graph_def(graph_def, name='')

        # Get input shape
        with tf.compat.v1.Session(graph=self.graph) as sess:
            self.input_shape = sess.graph.get_tensor_by_name(self.INPUT_TENSOR_NAME).shape.as_list()[1:3]

    def predict_image(self, image):
        image = image.convert('RGB') if image.mode != 'RGB' else image
        print(self.input_shape)
        image = image.resize(self.input_shape)
        print("chirag")
        print(self.input_shape)

        inputs = np.array(image, dtype=np.float32)[np.newaxis, :, :, :]
        with tf.compat.v1.Session(graph=self.graph) as sess:
            output_tensors = [sess.graph.get_tensor_by_name(n) for n in self.OUTPUT_TENSOR_NAMES]
            outputs = sess.run(output_tensors, {self.INPUT_TENSOR_NAME: inputs})
            print(outputs)
            return outputs


def predict(model_filename, image_filename):
    od_model = ObjectDetection(model_filename)

    image = PIL.Image.open(image_filename)
    return od_model.predict_image(image)


def main():
    parser = argparse.ArgumentParser('Object Detection for Custom Vision TensorFlow model')
    parser.add_argument('--image_filename', type=str, help='Filename for the input image')
    parser.add_argument('--model_filename', type=str, default=MODEL_FILENAME, help='Filename for the tensorflow model')
    parser.add_argument('--labels_filename', type=str, default=LABELS_FILENAME, help='Filename for the labels file')
    args = parser.parse_args()

    predictions = predict(args.model_filename, args.image_filename)

    with open(args.labels_filename) as f:
        labels = [l.strip() for l in f.readlines()]

    for pred in zip(*predictions):
        print(f"Class: {labels[pred[2]]}, Probability: {pred[1]}, Bounding box: {pred[0]}")

if __name__ == '__main__':
    main()
