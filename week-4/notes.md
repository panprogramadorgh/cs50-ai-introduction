# Lecture 4 — Machine Learning

A lo largo de este curso hemos etado viendo como dar instrucciones a un agente de IA para dar dar soluciones de a problemas como punto de entrada.

En esta leccion vamos a estar explorando la idea de `machine learning`, donde en lugar de codificar un agente mediante instrucciones explicitas, nuestro agente va a tomar sus propias decisiones basandose en una determinada informacion, patrones, etc.

El concepto de `machine laerning` es muy amplio, en primer lugar revisaremos algunos de los conceptos fundadores detras de este campo.

# Supervised Learning

Dado un conjunto de datos, se asocia un valor/s de entrada a un valor de salida en forma de par, `supervised learning` consiste en aprender una funcion de prediccion sobre la salida generada dada una determinada entrada.

# Classification

Consiste en la tarea de hacer aprender una funcion de clasificacion de datos de entrada en categorias.

Imagina la situacion donde tenemos que averiguar la autenticidad de un billete. Podriamos clasificar el billete como "falso" o "verdadero" (al haber una cantidad delimitada de clases y existir una probabilidad para cada una de ellas, estamos hablando de valores discretos)

Siguiendo con este concepto de clasificacion, otro buen ejemplo a considerar seria el de la prediccion del tiempo. De manera semejante a los modelos probabilisticos (digase supuestos de markov y tal vez modelos sensor), hay un trabajo de inferencia dadas una observaciones. A traves de una serie de **patrones implicitos en los datos provistos**, un algoritmo de clasificacion es capaz de etiquetar ciertos escenarios.

![observated-data-classification](./imgs/observated-data-classification.png)

O... lo que es igual — aunque desde una perspectiva mas matematica:

![observated-data-classification-maths](./imgs/observated-data-classification-maths.png)

## Plots

Realmente no sabemos a ciencia cierta la salida de la funcion $f(...)$, pero si podemos generar un resultado estimado con una funcion $h(...)$.

Una forma razonable en la que podriamos ver los valores de salida generados para la `classification task` seria a traves de un grafico de $n$ dimensiones, donde cada dimension es un valor de entrada para la tarea de clasificacion ($f(...)$).

En el anterior ejemplo de prediccion meteorologica, dos valores de entrada diferentes (humedad y presion) eran pasados a la tarea de clasificacion.

- **Rojo** — Dias sin lluvia

- **Azul** — Dias con lluvia

![two-dimension-input-plot-example](./imgs/two-dimension-input-plot-example.png)

> El objetivo de la tarea clasificatoria por lo tanto consiste en, dado un nuevo punto en el grafico (no existente en el grafico en ese momento), ser capaz de clasificarlo (llueve o no llueve).

![new-two-dimension-plot-input](./imgs/new-two-dimension-plot-input.png)

Por pura intuicion, podriamos decir que el punto azul claro debe ser clasificado como un dia lluvioso — lo cual es una nocion poco formal y que posteriormente profundizaremos mas.

## Classification techniques

- **neaest-neighbour** — La funcion de clasificacion etiqueta la entrada de la misma forma que lo hico el `data point` mas cercano (valores de entrada mas parecidos).

- **$k$-nearest-neighbour** — En ocasiones es demasiado determinante generar una clasificacion fijandonos solamente en un `data point`, por eso mismo, esta variante tiene en cuenta $k$ nodos mas cercanos.

  > Probablemente seria el mas indicado a utilizar en el problema de clasificacion meteorologica.

  En `machine learning` existen un monton de algoritmos diferentes encargados de realizar este proceso de clasificacion y por lo general daremos con la situacion de que algunos se desenvolveran mejor ante ciertas situacion en comporacion con otros y viceversa.

- **linear regression**

  Si bien podemos emplear ciertos razonamientos / heuristicas para obtener el valor mas optimo de $k$, asi como los nodos vecinos mas determinantes y podar aquellos que solamente suponen un lastre computacinoal, podemos cambiar de enfoque de base al momento de clasificar los `data entry` en el plot.

  En el mismo grafico bidimensional donde se toman los valores para la presion y humedad (dos dimensiones / parametros) podemos dibujar un limite que separa los dias de lluvia de los dias sin lluvia.

  ![linear-regression-plot](./imgs/linear-regression-plot.png)

  Aunque por lo general nuestra linea delimitadora no sera tan buena y siempre cometera algun error:

  ![unperfect-linear-regression-plot](./imgs/unperfect-linear-regression-plot.png)

## How Linear Regression Works

Podemos ver `linear regression` desde una perspectiva mas matematica. Digamos que vamos a darle un nombre a cada uno de los parametros de nuestra `hypothesis function` $h$:

- $x_1$ — Humedity

- $x_2$ — Pressure

El objetivo de $h$ por lo tanto, consiste en averiguar si sus valores de entrada ($x_1$ y $x_2$) estan en el lado de la linea delimitadora correspondiente a los dias de lluvia, o mas bien en el lado en el que no.

De acuerdo para formalizar la linea delimitadora hemos de constituir una combinacion lineal de ambos parametros de entrada con un peso $w_n$; siendo este proporcional a la relevancia de cada uno de estos parametros para lograr el resultado.

Rain if $\ \ \ \ w_0 + x_1w_1 + x_2w_2\ >=\ 0\\$
No Rain $\ \ otherwise$

Los pesos $w$ son constantes y van a darle forma y pendiente a la linea; por lo tanto, la clave en este tipo de algoritmos de `machine learning` consiste en dar con los pesos $w$ lo mas precisos posibles, de manera que $h$ arroje buenas clasificaciones.

Por lo general (especialmente cuando hablamos de tareas de clasificacion con cientos o miles de parametros) las representaciones matematicas de este concepto se llevan a cabo con vectores (o ristras de valores).

- Weights (**W**) — $<w_0, w_1, w_2>$

- Inputs (**X**) — $<1, x_1, x_2>$

Entonces para llegar a la misma conclusion sobre la lluvia, hemos de aplicar una multiplicacion de vectores o `dot product` entre ambos.

**W · X** $\ =\ (w_0 * 1) + (w_1 * x_1) + (w_2 * x_2)$

> El motivo por el que el vector `inputs` comienza por $1$, es porque para poder hacer la multiplicacion de vectores necesitamos que sean de la misma longitud. $w_0$ lo empleamos en caso de que un desplazamiento en la ecuacion sea necesario.

Por ultimo tambien cabe destacar que para codificar cada una de las clasificaciones, es muy comun emplear numeros enteros

- Rain — $1$

- No Rain — $0$

![linear-regression-hypothesis-function-maths](./imgs/linear-regression-hypothesis-function-maths.png)

### Perceptron Learning Rule

Hasta el momento hemos estado dando por hecho que disponemos del vector **W** con los pesos ya ponderados. A continuacion cubriremos a grandes rasgos esta regla de aprendizaje para ajustar el vector de pesos de la forma mas precisa posible.

- Iteraremos por cada valor en los vectores `inputs` y `weights`

- El _valor de peso_ de la iteracion actual sera desplazado en el producto de:

  - El _valor de input_ de la iteracion actual; y

  - El _ratio de aprendizaje_ de:

    - La diferencia del _valor real_ frente al _valor estimado_

---

- _valor de peso_ — $w_n$

- _valor de input_ — $x_n$

- _valor de input_ — $x_n$

- _ratio de aprendizaje_ — $ɑ$

- _valor real_ — $y$ — valor asociado a data point **X** en datos de entrenamiento del modelo

- _valor estimado_ — $h_w($**X**$)$

> Para _valor real_ y _valor estimado_ es fundamental que que las clasificaciones este asociadas a un valor numerico, de tal manera que podemos calcular la diferencia.

![perceptron-learning-rule](./imgs/perceptron-learning-rule.png)

Actualmente estamos planteando la clasificacion con un limite muy agresivo (llueve si **W**$\ *\ $**X**$\ >=\ 0$). Esto es lo que se conoce como `hard threshold` y su representacion grafica se ve de la siguiente manera:

![hard-threshold-classification-plot](./imgs/hard-threshold-classification-plot.png)

Este metodo es simple de aplicar aunque tiene ciertas limitaciones en:

- Escalabilidad (derivaciones en la curva)

- Graduabilidad (no hay probabilidades; blanco o negro)

Los limites suaves o `soft threholds` pertimen graduacion entre las clasificaciones (valores en forma de numeros reales), dondo entrada al concepto de probabilidad.

![soft-threshold-classification-plot](./imgs/soft-threshold-classification-plot.png)
