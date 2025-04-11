# Lecture 4

A lo largo de este curso hemos etado viendo como dar instrucciones a un agente de IA para dar dar soluciones de a problemas como punto de entrada.

En esta leccion vamos a estar explorando la idea de `machine learning`, donde en lugar de codificar un agente mediante instrucciones explicitas, nuestro agente va a tomar sus propias decisiones basandose en una determinada informacion, patrones, etc.

El concepto de `machine laerning` es muy amplio, en primer lugar revisaremos algunos de los conceptos fundadores detras de este campo.

## Supervised Learning

Dado un conjunto de datos, se asocia un valor/s de entrada a un valor de salida en forma de par, `supervised learning` consiste en aprender una funcion de prediccion sobre la salida determinada entrada generara.

Tareas en `supervised learning`:

- **Classification**

  Consiste en la tarea de hacer aprender una funcion de clasificacion de datos de entrada en categorias.

  Imagina la situacion donde tenemos que averiguar la autenticidad de un billete. Podriamos clasificar el billete como "falso" o "verdadero" (al haber una cantidad delimitada de clases y existir una probabilidad para cada una de ellas, estamos hablando de valores discretos)

  Siguiendo con este concepto de clasificacion, otro buen ejemplo a considerar seria el de la prediccion del tiempo. De manera semejante a los modelos probabilisticos (digase supuestos de markov y tal vez modelos sensor), hay un trabajo de inferencia dadas una observaciones. A traves de una serie de **patrones implicitos en los datos provistos**, un algoritmo de clasificacion es capaz de etiquetar ciertos escenarios.

  ![observated-data-classification](./imgs/observated-data-classification.png)

  O... lo que es igual — aunque desde una perspectiva mas matematica:

  ![observated-data-classification-maths](./imgs/observated-data-classification-maths.png)

  ### Plots

  Realmente no sabemos a ciencia cierta la salida de la funcion $f(...)$, pero si podemos generar un resultado estimado con una funcion $h(...)$.

  Una forma razonable en la que podriamos ver los valores de salida generados para la `classification task` seria a traves de un grafico de $n$ dimensiones, donde cada dimension es un valor de entrada para la tarea de clasificacion ($f(...)$).

  En el anterior ejemplo de prediccion meteorologica, dos valores de entrada diferentes (humedad y presion) eran pasados a la tarea de clasificacion.

  - **Rojo**: Dias sin lluvia

  - **Azul**: Dias con lluvia

  ![two-dimension-input-plot-example](./imgs/two-dimension-input-plot-example.png)

  > El objetivo de la tarea clasificatoria por lo tanto consiste en, dado un nuevo punto en el grafico (no existente en el grafico en ese momento), ser capaz de clasificarlo (llueve o no llueve).

  ![new-two-dimension-plot-input](./imgs/new-two-dimension-plot-input.png)

  Por pura intuicion, podriamos decir que el punto azul claro debe ser clasificado como un dia lluvioso — lo cual es una nocion poco formal y que posteriormente profundizaremos mas.

  ### Classification techniques

  - **neaest-neighbour**: La funcion de clasificacion etiqueta la entrada de la misma forma que lo hico el `data point` mas cercano (valores de entrada mas parecidos).

  - **$k$-nearest-neighbour**: En ocasiones es demasiado determinante generar una clasificacion fijandonos solamente en un `data point`, por eso mismo, esta variante tiene en cuenta $k$ nodos mas cercanos.

    > Probablemente seria el mas indicado a utilizar en el problema de clasificacion meteorologica.
