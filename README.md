# Killem

## Resumen

Killem es un videojuego retro de jugabilidad sencilla y adictiva que pone a prueba tus reflejos. El objetivo consiste en aguantar el mayor tiempo posible sin morir frente a los enemigos que se aproximan ni de los disparos enemigos. Para ello, debes defenderte con tus disparos y tu escudo.

## Controles

### Teclado

* **←** : Disparo a la izquierda
* → : Disparo a la derecha
* **A**  : Escudo a la izquierda
* **D**  : Escudo a la derecha
* **ESC** : Pausar/Retomar
* **O** : Pantalla completa/Ventana
* **M** : Silenciar/Desilenciar

### Gamepad (XBOX)

* **LB** : Disparo a la izquierda
* **RB** : Disparo a la derecha
* **←** o **X** : Escudo a la izquierda
* → o **B** : Escudo a la derecha
* **START** : Pausar/Retomar

## Modos de juego

### Humano

En este modo de juego será el propio humano el cual se enfrenta a innumerables oleadas de enemigos. Cada disparo acertado y cada disparo enemigo bloqueado suma un punto.

### Agente

En este otro modo de juego puedes observar al agente inteligente jugar después de su largo y duro entrenamiento. Su récord personal se encuentra en cerca de 5500 puntos!

## Estructura

A continuación se explica sin entrar en detalle, el árbol de directorios del código.

* `agent`: Es el directorio donde se encuentran las clases referentes al agente y al modelo de la red neuronal.
* `entities`: Aquí se definen todas las entidades y generadores de entidades.
* `game`: Directorio donde se encuentra la lógica de la partida así como botones para la interfaz grafica.
* `mixer`: Clases para el manejo de música y sonidos dinámicos.
* `model`: Es el modelo entrenado que emplea el agente para jugar al juego.
* `resources`: Todos los recursos gráficos y de sonido empleados en el juego.
* `util`: Clases y funciones auxiliares de utilidad para hacer soporte al resto del codigo
* `main.py`: Es el punto de partida del juego.