# taxi24

Prueba tecnica.

## Inicio

El proyecto usa:

- Django.
- Django Rest Framework.
- Postgresql.
- Docker.
- Docker Compose.

El proyecto está conformado por la aplicación `core`, la cual contiene los componentes principales del proyecto: modelos, serializadores, vistas, etc.

El proyecto usa docker y docker-compose para el despliegue local. Las variables de entorno se deben registrar en un archivo `.env`.

Se ha creado un archivo `Makefile` para automatizar tareas del proyecto.

## Comandos

1. `make init`:
Inicializa el proyecto, construye imágenes `docker`, corre migraciones y carga fixtures a la base de datos.

2. `make serve`:
Despliega los servicios del proyecto haciendo uso de `docker-compose`.

3. `make bash`:
Accedemos al contenedor donde se encuentra el código del proyecto.

4. `make test`:
Corre las pruebas del proyecto. Cada requerimiento tiene un test.

5. `make lint`:
Usa pylint para la revisión de código.

6. `make coverage`:
Usa coverage para revisar cuanto código está cubierto por las pruebas.

7. `make destroy`:
Destruye contenedores creados.

8. `make migrate`:
Crea y aplica los cambios de las migraciones del proyecto.

## Endpoints

Cada endpoint puede hacer uso de un filtro `query` para obtener solo aquellos campos requeridos, ejemplo: `http://localhost:8000/drivers/?query={id,name}`

### Driver

* `http://localhost:8000/drivers/`

    - Obtiene una colección de conductores.

* `http://localhost:8000/drivers/{id}/`

    - Obtiene un recurso conductor.

* `http://localhost:8000/drivers/?status='A'`

    - Obtiene una colección de conductores filtrados por estado, retornando solo aquellos que tienen estado AVAILABLE(A)

* `http://localhost:8000/drivers/?lat={lat}&lon={lon}&distance=3`

    - Obtiene una colección de conductores retornando solo aquellos que se encuentran a una distancia de 3km dado una punto específico (latitud, longitud).

### Passenger

* `http://localhost:8000/passengers/`

    - Obtiene una colección de pasajeros.

* `http://localhost:8000/passengers/{id}/`

    - Obtiene un recurso pasajero.

* `http://localhost:8000/passengers/{id}/closest_driver/`

    - Obtiene una colección de conductores ubicados a 3km o menos de la posición del pasajero.

### Trip

* `http://localhost:8000/trips/`

    - Obtiene una colección de viajes.

* `http://localhost:8000/trips/`

    - Crea un nuevo recurso de viaje.
    - Calcula la distancia y costo del viaje dado punto de destino y punto de partida.
    - Actualiza estado de conductor a UNAVAILABLE(U).


```json
// Body example.
{
    "source_lat": -6.862689,
    "source_lon": -79.818674,
    "destination_lat": -6.862689,
    "destination_lon": -79.818674,
    "passenger": "c249c96c-e3c1-46d4-a28a-7344366678cb",
    "driver": "33a304a5-9e62-4eff-8cb9-9ed349a617a4"
}
```

* `http://localhost:8000/trips/{id}/`

    - Obtiene un recurso viaje.

* `http://localhost:8000/trips/{id}/ending/`

    - Finaliza viaje, cambia su estado a END(E).
    - Actualiza estado de conductor a AVAILABLE(A).
    - Actualiza ubicación (latitud, longitud) de conductor.
    - Actualiza ubicación (latitud, longitud) de pasajero.
    - Crea una boleta.

* `http://localhost:8000/trips/?status='A'`

    - Obtiene una colección de viajes filtrados por estado, retornando solo aquellos que tienen estado AVAILABLE(A).