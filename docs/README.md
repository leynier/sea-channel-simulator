# Simulación de un Canal Marítimo

## Autor

* **Nombre:** Leynier Gutiérrez González
* **Grupo:** C412
* **Correo Electrónico:** leynier41@gmail.com

## Problema

Un canal marı́timo consiste en una o más exclusas colocadas en diques consecutivos de manera que la combinación de estas permite el ascenso o descenso de los barcos, permitiendo el acceso del barco al dique siguiente. Estos canales son usados para la navegación a través de aguas turbulentas o para atravesar terrenos terrestres. Se desea conocer el tiempo de espera de los barcos para el uso de un canal con 5 diques para su funcionamiento. La operación de un canal puede ser dividido en dos ciclos muy similares que llamaremos ciclo de subida y ciclo de bajada. El ciclo de subida comienza con la compuerta del nivel superior cerrada y la compuerta del nivel inferior abierta. Los barcos esperando en el nivel inferior entran en el dique. Cuando los barcos se acomodan dentro del dique las puertas del nivel inferior se cierran y las puertas del nivel superior se abren y el agua del nivel superior inunda el dique, haciendo la función de un elevador marı́timo. Luego los barcos pasan al nivel superior, dejando el dique vacı́o. El ciclo de bajada consiste en el funcionamiento opuesto del ciclo descrito.

Ambos ciclos tienen las mismas 3 fases para su cumplimento, que se pueden llamar como fase de entrada, fase de transporte y fase de salida respectivamente. La fase de entrada consiste en abrir las puertas del nivel inferior y dejar entrar a los barcos esperando hasta que estos se acomodan dentro del dique, la duración de este proceso depende del tiempo de apertura de las compuertas que distribuye de manera exponencial con λ = 4 minutos y el tiempo que se demora cada barco en entrar al dique, que distribuye de manera exponencial con λ = 2 minutos independientemente del tamaño de cada barco. Los barcos a entrar en el dique son tomados de manera secuencial de la cola de arribo de los barcos y en caso de que algún barco no quepa en el dique, el siguiente en la cola toma su lugar, en caso de que ningún barco quepa en el dique, la fase comienza sin llenar la capacidad del dique.

La fase de transporte incluye cerrar la compuerta del nivel inferior, la apertura del nivel superior y el llenado del dique, esta fase tiene un tiempo de duración que distribuye de manera exponencial con λ = 7 minutos. La fase de salida se compone por la salida de los barcos del dique ası́ como el cerrar la puerta del nivel superior, esta fase tarda un tiempo que distribuye de manera exponencial con λ = 1,5 minutos por cada barco en el dique. El número total de barcos que pueden ser acomodados en un dique depende del tamaño fı́sico de los barcos. Estos tienen 3 tamaños distintos: pequeño, mediano y grande y el tamaño de cada uno de estos corresponde a la mitad del anterior. Cada dique puede albergar 2 filas con espacio para el equivalente a 3 barcos medianos (1 grande y dos pequeños).

El tiempo de arribo de los barcos distribuye de acuerdo con la función Normal y dependen del tamaño del barco ası́ como de la hora del dı́a (el canal funciona de 8 am a 8 pm), los parámetros de la función se resumen a continuación.

| Tamaño  | 8:00 AM - 11:00 AM | 11:00 AM - 5:00 PM | 5:00 PM - 8:00 PM  |
|---------|--------------------|--------------------|--------------------|
| Pequeño | mu = 5, sigma = 2  | mu = 3, sigma = 1  | mu = 10, sigma = 2 |
| Mediano | mu = 15, sigma = 3 | mu = 10, sigma = 5 | mu = 20, sigma = 5 |
| Grande  | mu = 45, sigma = 3 | mu = 35, sigma = 7 | mu = 60, sigma = 9 |

## Principales ideas

Se utilizó un modelo de simulación en eventos discretos de `N` servidores en serie. Cada grupo de barcos que pueden acomodarse en un dique según su tamaño y el orden en que arribaron al canal se considera como un cliente. La modelación sigue la siguiente idea, se generan los barcos con su tamaño y tiempo de arribo al canal mientras este sea menor que el horario de cierre. Cuando un grupo de barcos está listo para ingresar a un dique, lo hacen y en ese momento se generá el evento de traslado hacia el siguiente dique, y así sucesivamente hasta que no hayan más barcos entrando y todos hayan salido del canal.

## Modelación

### Variables

```python
t # Tiempo actual de la simulación.
c  # Indica si el canal cerró.
Na # Número de arribos al canal (un arribo esta
   # compuesto por un grupo de barcos que entran
   # en el primer dique).
Nd # Número de salidas del canal (una salida esta
   # compuesta por un grupo de barcos que salen
   # del último dique).
n # Colas para cada dique.
Ta # Lista de los grupos de barcos con su tiempo
   # de arribo al primer dique.
Td # Lista de los grupos de barcos con su tiempo
   # de salida del ultimo dique.
ta # Grupo de barcos con su tiempo de arribo al
   # primer dique.
ti # Lista de los grupos de barcos con su tiempo
   # de salida por dique.
```

### Inicialización

```python
t <- 0
c <- False
Na <- 0
Nd <- 0
n <- [[], [], [], [], []]
Ta <- [[], [], [], [], []]
Td <- []
ta <- G() # Generador de grupos de barcos con su tiempo de arribo al primer
          # dique, termina cuando el tiempo de arribo excede el horario
          # definido del canal.
ti <- [INF, INF, INF, INF, INF]
```

### Eventos

Evento de arribo de un grupo de barcos al primer dique. Si es el primer dique solo tiene un grupo de barcos en la cola, se genera el evento de traslado de ese dique al siguiente.

```python
if not c and ta.time <= min(ti):
    t <- ta.time
    Na <- Na + 1
    push(n[1]) <- ta.ships
    Ta <- time, ta.ships
    if len(n[1]) = 1:
        ti[1] <- H() # Generar el evento de salida del primer dique
    try ta <- G() else c <- True
```

Evento de traslado de un dique hacia el siguiente. Si la cola del dique desde donde se realiza el traslado no se queda vacia entonces se general el siquiente evento de traslado de ese dique.

```python
if ti[i] = min(ti) and len(n[i]) > 0 for i in range(4):
    t <- ti[i]
    ships <- pop(n[i])
    push(n[i + 1]) <- ships
    push(Ta[i + 1]) <- t, ships
    if len(n[i]) > 0:
        ti[i] <- H()
    else:
        ti[i] <- INF
    if len(n[p + 1]) = 1:
        ti[p + 1] <- H()
```

Evento de salida del canal en el último dique. Si aún quedan en la cola de último dique grupos de barcos, se genera el siguiente evento de salida del canal.

```python
if len(n[5]) > 0:
    t <- ti[5]
    Nd <- Nd + 1
    push(Td) <- t, pop(n[5])
    if len(n[5]) > 0:
        ti[5] <- H()
    else:
        ti[4] <- INF
```

Si ninguna de las condiciones de los restantes eventos se cumplen, entonces se finaliza la simulación.

```python
if len(n[5]) = 0:
    return
```

## Consideraciones

El modelo anterior fue probado tomando como consideración que una unidad de tiempo se tomó como un minuto. Se probó realizando unas mil corridas de la simulación y estos fueron algunos resultados obtenidos.

* Número de diques: 1, Filas de los diques: 2, Tamaño de las filas: 06 -> 03750 minutos
* Número de diques: 2, Filas de los diques: 2, Tamaño de las filas: 06 -> 04699 minutos
* Número de diques: 3, Filas de los diques: 2, Tamaño de las filas: 06 -> 05648 minutos
* Número de diques: 4, Filas de los diques: 2, Tamaño de las filas: 06 -> 06596 minutos
* Número de diques: 5, Filas de los diques: 2, Tamaño de las filas: 06 -> 07546 minutos
* Número de diques: 6, Filas de los diques: 2, Tamaño de las filas: 06 -> 08496 minutos
* Número de diques: 7, Filas de los diques: 2, Tamaño de las filas: 06 -> 09448 minutos
* Número de diques: 8, Filas de los diques: 2, Tamaño de las filas: 06 -> 10411 minutos
* Número de diques: 9, Filas de los diques: 2, Tamaño de las filas: 06 -> 11385 minutos

* Número de diques: 5, Filas de los diques: 1, Tamaño de las filas: 06 -> 04397 minutos
* Número de diques: 5, Filas de los diques: 2, Tamaño de las filas: 06 -> 07538 minutos
* Número de diques: 5, Filas de los diques: 3, Tamaño de las filas: 06 -> 10731 minutos
* Número de diques: 5, Filas de los diques: 4, Tamaño de las filas: 06 -> 14263 minutos
* Número de diques: 5, Filas de los diques: 5, Tamaño de las filas: 06 -> 17937 minutos

* Número de diques: 5, Filas de los diques: 2, Tamaño de las filas: 04 -> 05379 minutos
* Número de diques: 5, Filas de los diques: 2, Tamaño de las filas: 06 -> 07550 minutos
* Número de diques: 5, Filas de los diques: 2, Tamaño de las filas: 08 -> 09789 minutos
* Número de diques: 5, Filas de los diques: 2, Tamaño de las filas: 10 -> 11989 minutos
* Número de diques: 5, Filas de los diques: 2, Tamaño de las filas: 12 -> 14258 minutos

## Implementación

[Enlace al repositorio de GitHub](https://github.com/leynier/sea-channel-simulator)
