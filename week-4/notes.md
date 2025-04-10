# Lecture 4

A lo largo de este curso hemos etado viendo como dar instrucciones a un agente de IA para dar dar soluciones de a problemas como punto de entrada.

En esta leccion vamos a estar explorando la idea de `machine learning`, donde en lugar de codificar un agente mediante instrucciones explicitas, nuestro agente va a tomar sus propias decisiones basandose en una determinada informacion, patrones, etc.

El concepto de `machine laerning` es muy amplio, en primer lugar revisaremos algunos de los conceptos fundadores detras de este campo.

## Supervised Learning

Dado un conjunto datos donde se asocia un valor de entrada a un valor de salida en forma de par, `supervised learning` consiste en crear una funcion de prediccion sobre la salida dada una determinada entrada.

Tareas en `supervised learning`:

- **Classification**: Consiste en la tarea de hacer aprender una funcion de clasificacion de datos de entrada en categorias.

  Imagina la situacion donde tenemos que averiguar la autenticidad de un billete. Podriamos clasificar el billete como "falso" o "verdadero" (al haber una cantidad delimitada de clases y existir una probabilidad para cada una de ellas, estamos hablando de valores discretos)

  Siguiendo con este concepto de clasificacion, otro buen ejemplo a considerar seria el de la prediccion del tiempo. De manera semejante a los modelos probabilisticos (digase supuestos de markov y tal vez modelos sensor), hay un trabajo de inferencia dadas una observaciones. A traves de una serie de **patrones implicitos en los datos provistos**, un algoritmo de clasificacion es capaz de etiquetar ciertos escenarios.

  ![observated-data-classification](./imgs/observated-data-classification.png)
