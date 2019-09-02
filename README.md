

# Clasificador de video



##  Instrucciones para la clasificación de un vídeo

1. En primer lugar se deberá instalar el clúster de Apache Kafka. Para ello se utilizará Docker-compose por lo que será necesario que se tenga intalado Docker en la máquina. Se deberán ejecutar los siguientes comandos dentro del directorio del proyecto:



```bash
# exportamos la variable de entorno de nuestra IP local
$ export HOST_NAME={ip local}

# dentro del directorio del proyecto, en el subdirectorio docker/ ejecutamos el siguiente comando
$ docker-compose up -d
```



2. Debemos preparar nuestro entorno de forma que cada vez que ejecutemos algun comando de Python, éste nos detecte las importaciones, por tanto deberemos tener configurada la variable de entorno PYTHONPATH:

```bash
# exportamos la variable de entorno
$ export PYTHONPATH={ruta absoluta del proyecto}
```





3. Instalar las dependencias del proyecto con Python con Pip. Ejecutando el siguiente comando:

```bash
# dentro del directorio raíz del proyecto ejecutar el siguiente comando
$ pip install -r requirements.pip
```



4. Una vez se hayan arrancado los contendores de Docker en instalado las dependencias del proyecto, deberemos arrancar el consumidor Kafka que procesará los datos de entrada. Para ello ejecutaremos el siguiente comando:

```bash
# dentro del directorio del proyecto, en el subdirectorio _kafka/ ejecutamos el siguiente comando
$ python consumer.py --servers localhost:9092 --input
```



5. Despues ejecutamos el consumidor de Apache Kafka que se encargará de procesar los datos de salida de la clasificación en una consola diferente a la del otro consumidor. Para ello ejecutamos el siguiente comando:

```bash
# dentro del directorio del proyecto, en el subdirectorio _kafka/ ejecutamos el siguiente comando
$ python consumer.py --servers localhost:9092 --output
```



6. Una vez esten los dos consumidores arrancados, en una cosola diferente se puede proceder a la clasificación de un vídeo ejecutando el siguiente comando:

```bash
# dentro de directorio raíz del proyecto ejecutar el siguiente comando
$ python manage.py {ruta del video} --servers localhost:9092
```



## Instrucciones para entrenar el modelo de Aprendizaje automático

En el módulo de Aprendizaje automático, podemos realizar tres acciones:

- Imprimir el nombre del algoritmo con el que esta entrenado el modelo en ese mismo momento. Tendremos que ejecutar el siguiente comando

```bash
# dentro del directorio raíz del proyecto, en el subdirectorio ml/ ejecutar el siguiente comando
$ python manage.py -n
```



- Entrenar el modelo con los algoritmos que soporta el sistema (LinearSVC, LogisticRegression, RandomForest, MultinomialNB)

```bash
# dentro del directorio raíz del proyecto, en el subdirectorio ml/ ejecutar el siguiente comando
$ python manage.py -t (LinearSVC|LogisticRegression|RandomForest|MultinomialNB)
```



- Realizar una predicción de un texto de forma rápida.

```bash
# dentro del directorio raíz del proyecto, en el subdirectorio ml/ ejecutar el siguiente comando
$ python manage.py -p {texto a predecir}
```



## Instrucciones para la carga de datos

Se podrán añadir mas datos de OpenSubtitles al conjunto de datos existente en el sistema. Para ello habrá que ejecutar el siguiente comando. 



```bash
# dentro del directorio raíz del proyecto, en el subdirectorio data/ ejecutar el siguiente comando
$ python main.py random
```

