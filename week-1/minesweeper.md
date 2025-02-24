
# Background

Buscaminas es un puzle juego que consiste en una regilla de celdas, donde algunas de las celdas contienen minas escondidas. Hacer click en una celda que contiene una celda provoca que esta sea detonada y provoca que el usuario pierda el juego. Hacer click en una celda "segura" (en otra palabras, una celda que no contiene mina) revela un numero que indica cuantas celdas vecinas (donde una cleda vecina es aquella ubicada un cuadrado a la izquierda, derecha, abajo, arriba y en diagonal de la celda actual) contienen mina.

Un metodo que podriamos utilizar para representar el conocimiento de nuetro agente IA buscaminas consistiria en hacer que a cada celda le corresponda una variable proposicional que es true cuando la celda contiene una mina y false en caso contrario.

A que informacion tiene acceso la IA ? La IA sabria en todo momento cuando una celda segura fue clicada asi como el valor para esa celda. Considera el siguiente tablero de buscaminas, donde la celda del medio ha sido revelada, y las otras celdas han sido etiquetadas con una letra identificatorio con el fin de esta discusion.

Que informacion tenemos ahora ? Al parecer ahora sabemos que una de las ocho celdas vecinas es una mina. De ese modo, nosotros podriamos escribir una expresion logica como la de abajo para indicar que una de las celdas vecinas es una mina.

```math
Or(A, B, C, D, E, F, G, H)
```

Pero nosotros realmente sabemos mas de los que esta expresion dice. La logical sentence de arriba expresa la idea de que al menos una de las ocho variables es verdadera. Aunque nosotros podemos hacer mas fuerte esta proposicion de manera que: Nosotros sabemos que exactamente (or exclusivo) uno de las ocho variables es verdadera. Esto noes da una frase proposcicional logica como la de abajo:

```python
Or(
    And(A, Not(B), Not(C), Not(D), Not(E), Not(F), Not(G), Not(H)),
    And(Not(A), B, Not(C), Not(D), Not(E), Not(F), Not(G), Not(H)),
    And(Not(A), Not(B), C, Not(D), Not(E), Not(F), Not(G), Not(H)),
    And(Not(A), Not(B), Not(C), D, Not(E), Not(F), Not(G), Not(H)),
    And(Not(A), Not(B), Not(C), Not(D), E, Not(F), Not(G), Not(H)),
    And(Not(A), Not(B), Not(C), Not(D), Not(E), F, Not(G), Not(H)),
    And(Not(A), Not(B), Not(C), Not(D), Not(E), Not(F), G, Not(H)),
    And(Not(A), Not(B), Not(C), Not(D), Not(E), Not(F), Not(G), H)
)
```

Esto es una expresion bastante complicada. Y esto es simplemente viene a expresar lo que significa para una celda tener un `1`. Si una celda tiene `2` o `3`  o cualquier otro valor, la expresion podria ser incluso mas grande.

Intentar ejecutara model checing en este tipo de problema, rapidamente lo convertira en algo intratable. En un tablero 8x8, utilizado por Microsoft para el nivel de principiantes, de esta manera tendriamos 64 variables, y por lo tanto 2^64 posibles modelos para comprobar (demasiadas por mucho para que una calculadora pueda calcularlo en una cantidad de tiempo razonable. Necesitamos una mejor forma de representacion de conocimiento)

# Representacion de conocimiento

En su lugar representaremos cada simbolo del conocimiento de nuestra IA de la siguiente manera:

```python
{A, B, C, D, E, F, G, H} = 1
```

Cada logical sentence en esta representacion tiene dos partes diferentes: un conjunto de cells en el tablero que son involucradas  en la frase, y un numero `count`, representando la cantidad de aquellas celdas que son minas. La anterior logica sentence dice que alguna de las frases A, B, C, D, E, F, G, H es una mina.

Por intuicion podriamos inferir que todas las celdas alrededor de una celda con valor cero son celdas "seguras"

Por el contrario, si el valor para la celda actual es el mismo que el numero de celdas vecinas, todas las celdas alredor de la celda actual las podemos considerar como "no seguras".

Por lo general nos interesa que nuestras frases sobre las celdas que todavia no han sido descubiertas sean marcadas como minas o seguras.

De la misma manera, if nuestra IA supiese que la frase `{A, B, C} = 2`, y posterirmente descubrieramos que C es una mina, podriamos elimiar C de la frase y decrementar el valor `count`. (puesto que C fue una mina que contruyo a este `count`).

Existe otro tipo de inferencia que podemos hacer.

Considera simplemente las dos frases que nuestra IA conoceria basandose en la ficha media inferior y media superior. Para la celda media superior tenemos {A, B, C} = 1. Desde la celda media inferior tenemos {A, B, C, D, E} = 2. Si sabemos que {A, B, C} = 1, entonces la mina faltante tiene que encontrarse en {D, E}.

Poniendo esta idea en un plano general podriamos podemos representar este conecpto de la siguiente forma `set2 - set1 = count2 - count1` donde `set1` es un subset de `set2`.

Entonces usando este metodo representacion de conocimiento, podemos escribir un agente de IA que puede reunir el conociemiento sobre un tablero de buscaminas, y con suerte seleccionar las celdas seguras.