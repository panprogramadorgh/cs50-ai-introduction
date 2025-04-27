## Enhancements en el calculo de recompensas

Uno de los conceptos mas fundamentales para estimar que tan rentable es tomar una determinada accion en un estado es las `future rewards`.

El calculo que se esta planteando actualmente consiste en obtener la accion para el estado actual con mayor valor q (una vez el modelo ya fue entrenado). Sin embargo esta vision no contempla ganancias a futuro y se centra en tomar la mejor decision cortoplacista.

```python
def best_future_reward(self, state: list[int]):
    """
    Given a state `state`, consider all possible `(state, action)`
    pairs available in that state and return the maximum of all
    of their Q-values.

    Use 0 as the Q-value if a `(state, action)` pair has no
    Q-value in `self.q`. If there are no available actions in
    `state`, return 0.
    """

    best = 0

    actions: set[tuple[int, int]] = Nim.available_actions(state)
    for a in actions:
        q_value = self.get_q_value(state, a)
        if q_value > best:
            best = q_value

    return best
```

Una posible solucion a este problema podria consistir en ampliar el espectro o profundidaz a traves del cual calculamos las recompensas futuras.

Para evaluar que tan valioso es tomar nuestro nodo, podriamos:

- Tomar el valor q mas codicioso para cada accion en nuestro estado actual.

- Avanzar al siguiente, tomar el valor q mas codicioso y asi sucesivamente hasta alcanzar una terminacion (maxima profundidaz o estado terminal)

- Tomar cada valor mas codicioso de cada estado que hemos transcurrido y sumarlo.

El resultado de esta suma seria en ultima instancia el "valor" para nuestro nodo inicial.

A todo este razoniamiento habria que añadir el concepto de "exploracion" con algoritmos como `epsilon greeedy`.
