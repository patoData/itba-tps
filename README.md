# TP intermedio: Foundations ITBA - Cloud Data Engineering

## El trabajo practico es una pequeña implementacion de una base de datos PostgreSQL en Docker poniendo en practica temas vistos tales en el curso como: cmd line, python, docker, rl bbdd.

## Link al enunciado para más información.
- [Enunciado](enunciado-itba.pdf)

### Parte 1:
La base de datos elegida es Chinook. La base de datos "Chinook" es un conjunto de datos de ejemplo diseñado para simular el funcionamiento de una tienda de música digital.

Tablas principales:

- Albums: Contiene información sobre los álbumes disponibles en la tienda, como título y artista.
- Artists: Tabla que almacena información sobre los artistas cuyos álbumes están disponibles en la tienda.
- Tracks: Detalla cada pista de música disponible para la venta, incluyendo nombre, álbum al que pertenece, duración y género.
- Customers: Información de los clientes registrados en la tienda, como nombre, dirección y país.
- Invoices: Registros de cada compra realizada por los clientes, incluyendo detalles como fecha, total de compra y método de pago.
- InvoiceItems: Detalle de cada artículo comprado en una factura, incluyendo la cantidad y el precio unitario.
- Genres: Tabla que enumera los diferentes géneros musicales disponibles en la tienda.

### ¿Preguntas de negocio que podemos responder con esta base?
- ¿Cuáles son los artistas más populares por cantidad de ventas?
- ¿Cuál es el género musical con más ventas?
- ¿Cuál es el cliente que más plata gastó en la tienda?
- ¿Cuáles son las canciones más reproducidas?
- ¿Cuál es la ciudad con más compras de música?

### Parte 2: Un docker compose con la imagen de postgreSQL 12.7:
[Docker Compose](docker-compose.yml)
El puerto 5666 fue elegido para ser mapeado para conexiones externas, dentro del contenedor el puerto usado es por defecto 5432

### Parte 3: Script SQL para crear las tablas (sin poblarlas)
[Script](scripts/chinook.sql)

### Parte 4: Popular la base de datos
[Docker Compose](docker-compose.yml)
En el mismo archivo docker compose, se configura la App data_loader que se encarga de popular la base de datos SQL, esta recibe como
parametros las credenciales de la base de datos como variables de entorno, los CSV en un volumen y un archivo de configuracion para
saber que tablas ingestar. 
En el codigo [Data Loader](csv_to_sql.py) se incluye 2 funciones comentadas para activar/desactivar las constraints en caso de que el usuario agregue mas tablas o use datos diferentes a los expuestos en este repositorio. En el caso de este repositorio no es necesario ya que el orden
de las ingestas es el correcto para no crear conflictos entre llaves de las tablas.

### Parte 5: Consultas a la base de datos
[Docker Compose](docker-compose.yml)
En el mismo archivo docker compose, se configura la App query_database que se encarga de realizar consultas SQL a la base, recibe como parametros
las credenciales de la base de datos, y un archivo JSON con las consultas a realizar, agregando a este JSON nuevas consultas, estas se realizaran
de manera automatica a la base al correr el contenedor.
La variable de entorno WAIT_TIME espera tantos segundos como se le pase en el [Docker Compose](docker-compose.yml) y es necesaria si se ejecuta en
conjunto para esperar a que la base sea populada antes de realizar las consultas, sino puede correrse esta imagen con el cmd = 'Docker run' luego
de que haya finalizado la creacion y carga de la base de datos.

### Parte 6: Documentación y ejecución end2end
