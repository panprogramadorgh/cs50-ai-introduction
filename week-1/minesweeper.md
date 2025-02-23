
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

