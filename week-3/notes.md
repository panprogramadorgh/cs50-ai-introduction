# Optimization Problems

Anteriormente estuvimos viendo modelos probabilisticos y como lidiar con hechos donde no existe absoluta certeza de que sucedan con el objetivo de crear conclusiones. En esta leccion vamos a dirigir nuestra atencion a otro tipo de problemas, por lo general reconocidos por el nombre de "optimization problems".

# Optimization

La optimizacion a grandes rasgos consiste en elegir la mejor opcion entre un abanico de posibilidades

# Local Search

Consiste en un tipo de algoritmo de busqueda que mantiene un unico nodo y busca moviendose a nodos vecinos.

Local search es empleado en situaciones donde encontrar la solucion mas optima es el corazon del problema. Por ejemplo encontrar la ubicacion mas adecuada para los hospitales (donde se busca que esten lo mas cerca posible de las casas).

![local-search-example](./imgs/local-search-example.png)

> Para hacer una medicion de la distancia de las casas con respecto a los hospitales utilizariamos algun tipo de funcion heuristica como la distancia de manhattan

Podemos ver este mismo problema representado de forma algo mas abstracta en un paisaje de estados con los valores generados por la funcion objetivo sobre cada estado. Volviendo al ejemplo anterior, la funcion objetivo estaria calculando la distancia de manhattan de los hospitales con respecto a las casas, siendo el valor mas bajo (global minimum) el que mas nos interesa. Nuestra tarea es por lo tanto encontrar aquel estado que tras ser pasado por la funcion objetivo, da el valor mas deseado. La funcion objetivo puede calcular la distancia de manhattan (o puede ser cualquier otra funcion heuristica)

![state-space-landscape-diagram](./imgs/state-space-landscape-diagram.png)
