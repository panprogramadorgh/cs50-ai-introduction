"""
Is highly reccomended to train the model using dedicated hardware systems, that includes at least some sort of GPU.
The model with the weights will be written in disk with .h5 format as consequent of high demand of computation needed.
"""

import os
import numpy as np
import cv2
import tensorflow as tf
import keras
from sklearn.model_selection import train_test_split
import colorama

DIR = "./gtsrb-small"
MODEL = "./models/traffic.h5"
IMAGE = f"{DIR}/0/00000_00000.ppm"  # testing image

NUM_CLASSES = 43
IMAGE_SIZE = 72
BATCH_SIZE = 16
EPOCHS = 10


def infer_directory(path: str) -> tf.data.Dataset:
    """
    Allows to infer images categories from "path"'s subdirectories and return the associated ppm files' paths.

    Returns
      It returns a `tf.data.Dataset` instance that contains two first dimension tensors, the class names and the ppm file paths vectors.
    """

    file_paths = []
    labels = []
    for classname in sorted(os.listdir(path)):
        subdir = os.path.join(path, classname)
        if not os.path.isdir(subdir):
            continue
        for fpath in os.listdir(subdir):
            if fpath.lower().endswith(".ppm"):
                fpath = os.path.join(subdir, fpath)
                file_paths.append(fpath)
                labels.append(classname)

    dataset = tf.data.Dataset.from_tensor_slices((file_paths, labels))
    return dataset


def load_ppm_image(fpath: tf.Tensor) -> tf.Tensor:
    """
    Receives `fpath`, which is an string first order and symbolic tensor, loads the image and finally returns a tensor version of a ndarray with the image data.
    """

    # Loads RGB images in ppm format and crates a ndarray with 0 to 1 np.float32 numbers.
    def _loader(b: bytes):
        fpath = b.decode(encoding="utf-8")
        image_bgr = cv2.imread(fpath)
        if image_bgr is None:
            raise ValueError(f"cv2.imread failed to load image: {fpath}")
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        image_rgb = cv2.resize(image_rgb, (IMAGE_SIZE, IMAGE_SIZE))
        image_float = image_rgb.astype(np.float32) / 255
        return image_float

    # Transforms the ndarray to a tf.Tensor
    # All input tensors become numpy interpretable objects, that means string tensors are transformed to `bytes`.
    image: tf.Tensor = tf.numpy_function(func=_loader, inp=[fpath], Tout=tf.float32)
    image.set_shape([None, None, 3])

    return image


def load_ppm_images(ds: tf.data.Dataset, batch_size: int = 16):
    """
    Creates a `tf.data.Dataset` of ppm images labeled under different class names.

    Arguments
      path -- First order tensor of an string
    """

    # Transforms the dataset to loaded the images, creates 32 batches and finally sets the prefetch configuration.
    dataset = (
        ds.map(
            map_func=lambda fpath, label: (
                load_ppm_image(fpath),
                tf.strings.to_number(label, tf.int32),
            ),
            num_parallel_calls=tf.data.AUTOTUNE,
        )
        .batch(batch_size)
        .prefetch(tf.data.AUTOTUNE)
    )

    return dataset


# Library initializations

colorama.init()

# MAIN


def main():
    # If ./models directory doesn't exist, then it creates it
    model_dirname = os.path.dirname(MODEL)
    if not os.path.isdir(model_dirname):
        os.mkdir(model_dirname)

    # Defines the model's structure
    model = keras.applications.Xception(
        weights=None,
        input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3),
        classifier_activation="softmax",
        classes=NUM_CLASSES,
    )

    # If there is not a trained model, it starts training one under the data.
    if not os.path.isfile(MODEL):

        # Loads the images
        images_ds = load_ppm_images(infer_directory(DIR), BATCH_SIZE)
        images_ndarr = np.array([split for split in images_ds.as_numpy_iterator()])
        training_split, validation_split = train_test_split(
            images_ndarr, training_split=0.9, shuffle=True
        )

        # Compiles the model with the optimizer and loss function (prepares it to training)
        model.compile(optimizer="adam", loss="sparse_categorical_crossentropy")

        # Trains the model with the provided data for training and validation
        model.fit(training_split, validation_split=validation_split, epochs=EPOCHS)

        # Saves the model to h5 format
        model.save_weights(MODEL)
    else:
        model.load_weights(MODEL)

    dummy_ds = tf.data.Dataset([IMAGE])
    input_image = next(dummy_ds.map(load_ppm_image))
    result = model.predict(input_image)
    print(result)


if __name__ == "__main__":
    main()
