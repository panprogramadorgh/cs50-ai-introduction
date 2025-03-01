# Uncertanty

Anteriormente estuvimos cubriendo el concepto de ingenieria de conocimiento. Codificabamos conocimiento (logia proposicional o del primer orden) y a partir de ahi eramos capaces de inferir nueva informacion que nos ayudaba a llegar a nuevas conclusiones.

Hasta el momento solamente hemos considerado como validos los simbolos que encajaban al 100% como verdaderos segun el conocimiento presente en el kb. Sin embargo en esta leccion introduciremos el conceptor de probabilidad en la inferencia.

Cada una de las posibles inferencias es verdadera bajo un porcentaje de probabilidad. La probabilidad de que una inferencia determinada (universo) sea verdadera puede ser representada matematicamente:

```math
P(W)
```

Que tan probable que suceda un evento es representado por un numero que puede ir del 0 al 1. Esto significa que la probabilidad de tirar un dado y obtener un 7 es de 0, mientras que la probabilidad de tirar un dado y que el numero sea inferior a 10 es de 1.

La suma de probabilidades para todos los "universos" tiene que dar como resultado 1. Esto es representable de la siguiente forma:

![likelyhood-omega-sumation-concept](./imgs/likelihood-omega-sumation-concept.png)

Siguiendo con el ejemplo de un dado, tenemos 6 posibles; cada una de ellas es igual de igual de probable obtenerla (suponiendo que no es un dado trucado). Esto significa que cada cara tiene una probabilidad de $\frac{1}{6}$ de ser verdadera ($\frac{1}{6} * 6 = 1$).

Podriamos agregar a la ecuacion un segundo dado, esto significa una probabilidad de $\frac{1}{36}$. Ahora; si bien es igual de probable sacar 5 y 2 que 6 y 3 en los dados, no existe la misma probabilidad para sacar el mismo resultado en la suma entre ambos dados. La suma mas corriente es de 7 ($\frac{6}{36} = \frac{1}{6}$), cuya probabilidad es identica a la de cada una de las caras de un solo dado.

![two-dies-probability-example](./imgs/two-dies-probability-example.png)

# Unconditional Probability

Este tipo de deducciones de probabilidad que somos capaces de crear desde la nada (como es el caso de los dados, donde deducimos una probabilidad sin basandonos en ningun evidencia) constituyen la `unconditional probability`

# Conditional Probability

Por el contrario la probabilidad condicional se fundamenta en evidencias ya reveladas con antelacion. La informacion ya conocida altera la probabildad de que un determinado simbolo sea verdadero.

> Cual es la probabilidad de A dado el valor de B ?

![conditional-probability](./imgs/conditional-probability-repr.png)

Que es equivalente a la probabilidad de que ambos simbolso A y B sean verdaderos dividido de la probabilidad de que B sea verdadero:

```math
\frac{P(A\ Ʌ\ B)}{P(B)}
```

El valor para la probabilidad ( $[0, 1]$ ) esta directamente relacionado (por no decir que es lo mismo) al numero de universos posibles.

Siguiendo este razonamiento y en relacion a
$\frac{P(A\ Ʌ\ B)}{P(B)}$, podemos verlo como `universos posibles donde A y B` / `universos posibles donde B`. Dividimos entre $P(B)$ porque para sacar la probabilidad de $P(A\ Ʌ\ B)$ ha sido necesario calcular el producto de la probabilidad de ambos $P(A) * P(B)$; de esta manera sacamos a $P(B)$ de la ecuacion.

> En el escenario de los dados, donde es igual de probable cada combinacion, el calculo de probabilidad condicional es $P(A\ |\ B)\ =\ P(A)$.

![conditional-probability-example](./imgs/conditional-probability-example.png)

> Cual es la probabilidad de que la suma de ambos dadots sea 12 sabiendo que el dado rojo es 6

# Random Variable

En teoria de probabilidad buscamos en ocasiones representar una idea con variables que pueden asurmir un valor determinado dentro de un dominio de posibilidades.

> Espacio de valores posibles para la variable aleatoria `roll`.

![random-variable-explanations](./imgs/random-variable-explanation.png)

## Probability Distribution

Amenudo representamos la distribucion de probabilidad sobre cada uno de los valores de la variable aletoria con un vector (matriz de valores)

![probability-distribution-as-vector](./imgs/probability-distribution-as-vector.png)

# Independence

Consiste en la falta de relacion al momento de calcular la probabilidad de dos simbolos diferentes.

El juego de los dos dados es un claro ejemplo de independencia en teoria de probabilidad y es que como cada jugada es aleatoria, no existe relacion alguna entre la tirada del primer y el segundo dado.

Si estuvieramos discutiendo si esta o no lloviendo, esta probabilidad seria alterada (no independiente) del factor "el cielo esta nubloso".

Si estamos topandonos con un caso de probabilidad independiente podemos simplificar la ecuacion de probabilidad conditional

> Buscando probabilidad de `A` asumiendo que `B` es verdadero

```math
P(A\ |\ B) = \frac{P(A\ Ʌ\ B)}{P(B)}
```

De la siguiente manera

```math
P(A) = \frac{P(A\ Ʌ\ B)}{P(B)}
```

O lo que es igual

```math
P(A\ Ʌ\ B) = P(A)\ *\ P(B)
```

Volviendo al problema de los dados, podemos forzar un comportamiento no independiente si buscamos que un mismo dado tenga dos valores diferentes el mismo tiempo.

> Al mostrar un comportamiento no independiente:

```math
P(Roll\ =\ 6\ Ʌ\ Roll\ =\ 1)\ !=\ P(A)\ *\ P(B)
```

```math
0\ !=\ \frac{1}{6}\ *\ \frac{1}{6}
```

> De manera que para hacer el calculo de probabilidad condicional tenemos que tener en cuenta que tan probable es `B` si `A` es cierto.

```math
P(Roll\ =\ 6\ Ʌ\ Roll\ =\ 1)\ !=\ P(A)\ *\ P(B\ |\ A)
```

![probability-independence-concept](./imgs/probability-independence-concept.png)

# Bayes' Rule

Basandonos en lo anterior y haciendo algo de algebra podemos sacar la forma estandar del teorema de bayes.

Si sabemos que

```math
P(A\ Ʌ\ B)\ =\ P(A)\ *\ P(B\ |\ A)
```

es lo mismo que

```math
P(A\ Ʌ\ B)\ =\ P(B)\ *\ P(A\ |\ B)
```

significa por lo tanto que

```math
P(B)\ *\ P(A\ |\ B) =\ P(A)\ *\ P(B\ |\ A)
```

y por consiguiente el teorema de bayes se representa comunmente con la forma:

```math
P(A\ |\ B)\ =\ \frac{P(B\ |\ A)\ *\ P(A)}{P(B)}
```

Aqui tenemos una aplicacion del teorema de bayes dada la siguiente informacion:

- El 80% de las tardes lluviosas comenzaron con una mañana nublada.

- El 40% de los dias tienen una mañana nublada.

- El 10% de los dias tienen una tarde lluviosa

![bayes-rule-example](./imgs/bayes-rule-example.png)

> Hay un 20% de probabilidad de que llueva por la tarde si por la mañana hay nubes.