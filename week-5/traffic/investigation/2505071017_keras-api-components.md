# Keras API Components
The core two data structures of keras are Layers and models. A layer is an input / output transformation and a model is a directed acyclic graph (DAG) of layers.
# Layers
Keras makes use of `tf.keras.layers.Layer` as its fundamental abstraction which encapsulates some state in form of weights and some computation defined by the `tf.keras.layers.Layer.call`method.

Processing layers improves the portability of the model since it doesn't necessarily have to relay on external code to transform input / output data, the model is self-sufficient by its own.
# Models
A model is an object that meets multiple layers than can be trained on data.

The simplest model in keras is the `tf.keras.Sequential`, which allows to create an stack of a number of layers. However, to build more sophisticated models we can the use the [keras functional API](https://www.tensorflow.org/guide/keras/functional_api) or build our own models [from scratch with subclassing](https://www.tensorflow.org/guide/keras/making_new_layers_and_models_via_subclassing).

The `tf.keras.Model` class features built-in training and evaluation methods:
- `tf.keras.Model.fit` — method trains a model for a given number of epochs.
- `tf.keras.Model.predict` — Generates output predictions for input samples.
- `tf.keras.Model`

#programming #ai #neural_networks #machine_learning #python #tensorflow 

#literature