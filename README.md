# Sistema de Gestion Academica
### Ingeniería de Software II 
## Descripcion general

El sistema de gestión académica, ofrece autenticacion diferenciada por rol (administrador, docente y alumno) y permite ejecutar tareas como la creacion de planes de estudio, gestion de materias, asignacion de cohortes, administracion de examenes, registro de asistencia y carga de calificaciones. Toda la interfaz se entrega con plantillas HTML y estilos responsive, mientras que la logica de negocio reside en una capa de servicios reusable.

## Funcionalidades principales

- Autenticacion por correo y password con sesiones de servidor y cierre de sesion seguro.
- Paneles diferenciados por rol con navegacion dinamica para cada tipo de usuario.
- Gestion completa de plan academico: materias, planes, cohortes y cursos.
- Inscripcion de alumnos a materias y examenes con validaciones segun cohorte.
- Registro y consulta de asistencia para alumnos y docentes, con calculos de porcentaje.
- Carga y visualizacion de calificaciones.
- Persistencia en archivos JSON que facilita la inspeccion y el versionado de los datos.

## Tecnologias y dependencias

| Tecnologia / libreria | Uso principal |
| --------------------- | ------------- |
| Python 3.12           | Lenguaje base del backend. |
| FastAPI + Starlette   | Framework HTTP asincronico, enroutamiento y middleware de sesiones. |
| Uvicorn               | Servidor ASGI para desarrollo y despliegue. |
| Jinja2                | Motor de plantillas para renderizar HTML dinamico. |
| HTML5 + CSS (static/) | Presentacion responsive del tablero y formularios. |
| Mapper JSON propio    | Persistencia ligera mediante archivos en `data/`. |
| Python `dataclasses`  | Modelado de entidades de dominio segun el diagrama de clases. |
| python-multipart      | Parseo de formularios HTML. |
| itsdangerous          | Claves de firma utilizadas por la SessionMiddleware. |

## Arquitectura de la aplicacion

### Capas y responsabilidades

1. **Routers (`app/router/`)**: definen endpoints y orquestan cada caso de uso delegando en la capa de servicios. Aplican guardas segun el rol del usuario y renderizan plantillas.
2. **Servicios (`app/controllers/`)**: encapsulan las reglas de negocio para cada tipo de actor (administrador, alumno, docente, asistencia, autenticacion). Sirven como controladores GRASP que coordinan modelos y broker.
3. **Modelos (`app/models/`)**: representan las entidades del UML como `dataclasses`, exponen comportamientos y metodos de conversion `to_dict` / `from_dict`.
4. **Persistencia (`app/models/dbbroker.py`, `app/utils/mapper.py`)**: `DBBroker` centraliza operaciones CRUD sobre colecciones JSON apoyandose en `Mapper`.
5. **Presentacion (`app/templates/`, `app/static/`)**: Jinja2 entrega paginas HTML e incluye componentes reutilizables; CSS define la experiencia visual.
6. **Datos (`data/`)**: archivos JSON versionables que actuan como almacenamiento permanente para usuarios, materias, planes, cohortes, cursos, examenes, asistencias y calificaciones.

### Estructura de carpetas relevante

```
app/
  main.py                 # Configura FastAPI, SessionMiddleware y datos seed.
  controllers/            # Servicios para cada rol y asistencias.
  models/                 # Entidades del dominio y objeto DBBroker.
  router/                 # Endpoints segmentados por rol.
  templates/              # Vistas Jinja2 por rol y componentes compartidos.
  static/                 # Recursos estaticos (CSS, iconos).
  utils/                  # Mapper JSON, autenticacion, navegacion.
data/                     # Persistencia JSON de todas las colecciones.
requirements.txt          # Dependencias del entorno.
```

### Conexion entre componentes

1. Las peticiones HTTP entran por un router especifico (`auth_router`, `admin_router`, `alumno_router`, `docente_router`).
2. El router invoca el servicio correspondiente (por ejemplo `AdministradorService`) siguiendo el patron Controller.
3. El servicio manipula modelos de dominio (Administrador, Alumno, Plan, etc.) y delega la persistencia en `DBBroker`.
4. `DBBroker` actua como Singleton y reusa el `Mapper` para leer/escribir los archivos JSON.
5. El resultado se transforma para renderizar una plantilla Jinja2 o para ejecutar una redireccion conforme al flujo definido.

## Correspondencia con el diseno previo

### Casos de uso y endpoints

| Caso de uso | Endpoint / accion | Servicio y metodo | Entidades UML involucradas |
| ----------- | ----------------- | ----------------- | -------------------------- |
| CU-001 / CU-008 / CU-013: Usuario se loguea | `POST /auth/login` | `AuthService.iniciarSesion`, `login_user` | Usuario, Administrador, Alumno, Docente |
| CU-002: Admin registra docentes y alumnos | `POST /admin/registrar_usuario` | `AdministradorService.registrarDocente` / `registrarAlumno` | Administrador, Docente, Alumno |
| CU-003: Admin crea plan academico | `POST /admin/crear_plan` | `AdministradorService.crearPlan` | Administrador, Plan |
| CU-004: Admin crea materias | `POST /admin/crear_materia` | `AdministradorService.crearMateria` | Administrador, Materia |
| CU-005: Admin asigna materias al plan | `POST /admin/asignar_materia_plan` | `AdministradorService.asignarMateriasAPlan`, `Plan.addList` | Administrador, Plan, Materia |
| CU-006: Admin asigna plan a alumnos | `POST /admin/crear_cohorte` | `AdministradorService.crearCohorte`, `_asignar_plan_y_cohorte_a_alumnos` | Administrador, Alumno, Cohorte, Plan |
| CU-007: Admin crea curso | `POST /admin/crear_curso` | `AdministradorService.crearCurso` | Administrador, Curso, Materia, Docente, Cohorte |
| CU-009: Alumno se registra a materias | `POST /alumno/inscribirse_materia` | `AlumnoService.inscribirseMateria` | Alumno, Materia, Plan |
| CU-010: Alumno se inscribe a examenes | `POST /alumno/inscribirse_examen` | `AlumnoService.inscribirseExamen` | Alumno, Examen |
| CU-011 / CU-015: Registro de asistencia | `POST /alumno/asistencia`, `POST /docente/asistencia` | `AsistenciaService.registrarAsistencia` | Alumno/Docente, Asistencia |
| CU-012 / CU-016: Consulta de asistencia | `GET /alumno/asistencia`, `GET /docente/asistencia` | `AsistenciaService.consultarAsistencia` | Alumno/Docente, Asistencia |
| CU-014: Docente carga calificaciones | `POST /docente/cargar_calificaciones` | `DocenteService.cargarCalificaciones`, `DBBroker.guardarObjeto` | Docente, Calificacion, Alumno, Materia |

### Trazabilidad entre artefactos UML y codigo

| Artefacto | Elemento UML | Implementacion en codigo | Comentario |
| --------- | ------------ | ------------------------ | ---------- |
| Diagrama de clases | Usuario, Administrador, Alumno, Docente | `app/models/USRs/*.py` | Se respetan atributos y relaciones de herencia. |
| Diagrama de clases | Materia, Plan, Curso, Examen, Asistencia, Calificacion, Cohorte | `app/models/*.py` | Cada entidad es una `dataclass` con metodos `to_dict` y `from_dict`. |
| Diagrama de secuencia | guardarObjeto, actualizarObjeto, obtener, addList | `app/models/dbbroker.py` | Los metodos definidos en el Mapper (brokers) se implementan tal como en el diagrama. |
| Paquete USRs con Factory Method | `New()` fabrica usuarios segun rol | `AuthService._build_usuario()` y `app/utils/auth._build_usuario()` | Cumplen el rol de factorias para instanciar la subclase correcta segun el atributo `rol`. |
| Casos de uso | CU-001 a CU-016 | Routers en `app/router/` + servicios en `app/controllers/` | Cada CU cuenta con un endpoint y logica dedicada. |

### Flujo detallado para CU-010 (Alumno se inscribe a examen)

1. El alumno autenticado accede al formulario `GET /alumno/inscribirse_examen`; el router carga examenes desde `AlumnoService.listarExamenes` y materias desde `AlumnoService.listarMaterias`.
2. Al enviar el formulario, `POST /alumno/inscribirse_examen` valida el rol mediante `_require_alumno`.
3. El router delega en `AlumnoService.inscribirseExamen`, que agrega el identificador en `Alumno.examenesInscripto` y persiste el cambio via `DBBroker.actualizarObjeto`.
4. `DBBroker` resuelve la coleccion `Usuario`, asegura la integridad y utiliza `Mapper.save` para escribir `data/usuarios.json`.
5. El router responde con una redireccion al dashboard, cumpliendo el escenario previsto por el diagrama de secuencia.

## Patrones de diseno identificados

### Patrones GoF

#### Singleton
- **Archivo**: `app/models/dbbroker.py`
- **Problema resuelto**: garantiza un unico punto de acceso a la persistencia JSON, evitando condiciones de carrera y duplicacion de estado.
- **Implementacion**: `DBBroker.__new__` asegura una unica instancia con bloqueo y cachea el almacenamiento en memoria.

#### Factory Method
- **Archivos**: `app/controllers/auth_service.py`, `app/utils/auth.py`
- **Problema resuelto**: construir la subclase de `Usuario` adecuada segun el rol persistido sin exponer la logica al resto de la aplicacion.
- **Implementacion**: los metodos `_build_usuario` actuan como factorias que retornan `Administrador`, `Alumno` o `Docente` a partir de los datos JSON.

#### Data Mapper
- **Archivo**: `app/utils/mapper.py`
- **Problema resuelto**: desacoplar los modelos de dominio del formato de persistencia; la escritura y lectura JSON se concentra en un componente dedicado.
- **Implementacion**: metodos `load` y `save` traducen colecciones a listas de diccionarios en archivos especificos por entidad.

### Patrones GRASP

#### Controller
- **Archivo**: `app/controllers/*.py`
- **Descripcion**: cada servicio representa el controlador de alto nivel para sus casos de uso, separando la orquestacion de la interfaz (router).

#### Creator
- **Archivo**: `app/models/USRs/administrador.py`
- **Descripcion**: la clase `Administrador` fabrica instancias de `Plan`, `Materia`, `Cohorte` y `Curso`, alineada con el principio Creator al poseer la informacion necesaria.

#### Information Expert
- **Archivo**: `app/controllers/asistencia_service.py`
- **Descripcion**: `AsistenciaService` concentra el calculo de porcentajes y la logica de filtrado por cuatrimestre, ya que posee todos los datos requeridos.

#### Low Coupling / High Cohesion
- **Aplicacion**: routers solo conocen servicios, servicios solo dependen del broker y modelos, mientras que `DBBroker` abstrae el acceso a archivos. Cada modulo persigue una unica responsabilidad, lo que facilita pruebas y mantenimiento.

## Sesiones, seguridad y almacenamiento

- **Manejo de sesiones**: `app/main.py` registra `SessionMiddleware` de Starlette con una clave propia. Las funciones `login_user`, `logout_user` y `get_current_user` en `app/utils/auth.py` guardan el identificador del usuario en la sesion firmada y reconstruyen la instancia desde el broker.
- **Control de acceso**: los routers definen helpers (`_require_admin`, `_require_alumno`, `_require_docente`) que validan el rol antes de ejecutar cada accion, retornando `403` cuando corresponde.
- **Persistencia JSON**: cada coleccion se almacena en un archivo dedicado dentro de `data/`. El metodo `seed_data` en `app/main.py` inicializa usuarios, materias, planes y examenes para simplificar las demostraciones.
- **Consideraciones**: las contraseñas se mantienen en texto plano para fines academicos; en un entorno productivo se deberia integrar hashing y control de sesiones expiradas.

## Ejecucion y entorno

1. Crear y activar el entorno virtual:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```
3. Iniciar el servidor de desarrollo:
   ```
   uvicorn app.main:app --reload
   ```
4. Acceder a `http://127.0.0.1:8000/` para utilizar el sistema con las credenciales semilla (`admin@demo.com`, `alumno1@demo.com`, `docente1@demo.com`, password `1234`).

## Conclusiones de diseno

El sistema preserva el bajo acoplamiento y la alta cohesion previstos en el diseno original: los routers manejan la capa HTTP, los servicios agrupan reglas por caso de uso, los modelos encapsulan atributos y comportamientos y el broker abstrae el detalle de persistencia. La trazabilidad entre casos de uso, diagramas de clases y secuencias se refleja en los archivos listados, demostrando que la implementacion final respeta las decisiones de la fase de analisis y diseno.
