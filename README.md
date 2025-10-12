# Sistema de Gestion Academica

## Resumen del proyecto
Aplicacion web basada en FastAPI y Jinja2 que permite a administradores, alumnos y docentes ejecutar los 16 casos de uso modelados sin depender de una base de datos externa. La persistencia se simula con un `DBBroker` en memoria respaldado por archivos JSON y el frontend ofrece vistas responsive inspiradas en paneles administrativos modernos.

## Arquitectura en capas
```
+------------+    +-------------+    +-----------+    +------------+
|  Routers   | -> |  Services   | -> |  Models   | -> |  DBBroker  |
| (FastAPI)  |    | (Aplicacion)|    | (Dominio) |    | + Mapper   |
+------------+    +-------------+    +-----------+    +------------+
        ^                 |                |                |
        +---- Templates (Jinja2) y static (CSS/JS) ---------+
```

## Tecnologias clave
- Python 3.11
- FastAPI y Starlette
- Jinja2
- Uvicorn
- Persistencia simulada con archivos JSON

## Diseno y UX
- Framework visual: HTML5 + CSS3 (plantillas Jinja2)
- Tipografia: Inter y Poppins (Google Fonts)
- Paleta: violeta institucional `#4B0082`, secundario `#8A2BE2`, neutros `#f5f5f5`, `#ffffff`, `#2c2c2c`
- Layout modular con `base.html` (header fijo + sidebar dinamico segun rol)
- Estilos responsive con Flexbox y CSS Grid
- Iconografia a traves de FontAwesome (CDN) y favicon propio en `/static/favicon.ico`
- Componentes reutilizables: tarjetas, banners de mensaje, badges, barras de progreso y spinner de carga

## Estructura de carpetas
- `app/main.py`: arranque de FastAPI, middleware de sesion, montaje de estaticos y carga de datos semilla.
- `app/router/`: controladores HTTP por rol (`auth`, `admin`, `alumno`, `docente`).
- `app/controllers/`: servicios de aplicacion que encapsulan reglas de negocio (auth, administrador, alumno, docente y asistencia).
- `app/models/`: clases de dominio (Usuario y subclases, Materia, Plan, Cohorte, Curso, Examen, Asistencia, Calificacion y `DBBroker`).
- `app/utils/`: utilidades de sesion, navegacion y mapper JSON.
- `app/templates/`: layout base y vistas modulares por rol (HTML + Jinja2).
- `app/static/`: hoja de estilos moderna, favicon y recursos compartidos.
- `data/*.json`: almacenamiento simulado que persiste entre ejecuciones.
- `requirements.txt`: dependencias de ejecucion.
- `README.md`: esta documentacion.

## Patrones aplicados

### GRASP
- **Controller**: routers (`app/router/*.py`) reciben las solicitudes y delegan en los servicios respetando los mensajes de los diagramas (por ejemplo `admin_router.crear_plan_action` -> `AdministradorService.crearPlan`).
- **Creator**: `Administrador` fabrica entidades (`crearPlan`, `crearMateria`, `crearCurso`) y `Alumno` genera sus propias inscripciones (`inscribirseMateria`, `inscribirseExamen`) antes de persistirlas.
- **Information Expert**: `Plan.addList`, `Alumno.inscribirseMateria` y `Asistencia.CalcularPorcentaje` concentran la logica en la entidad que posee los datos.
- **Low Coupling / High Cohesion**: capas separadas router -> service -> model -> persistence reducen dependencias cruzadas.
- **Polymorphism**: jerarquia `Usuario` habilita comportamientos especificos para `Alumno`, `Docente` y `Administrador`.

### GoF
- **Singleton**: `DBBroker` garantiza una unica instancia del almacenamiento en memoria.
- **Factory Method**: metodos de `Administrador` centralizan la instanciacion y validacion de entidades.
- **Template Method**: flujos de autenticacion y asistencia siguen el patron validar -> construir -> persistir con variaciones por rol.
- **Observer (futuro)**: documentado como extension para notificar eventos (ver Limitaciones).

## Casos de uso implementados

| CU | Descripcion | Rutas / Vistas | Servicio / Metodo clave |
|----|-------------|----------------|-------------------------|
| CU-001 | Administrador inicia sesion | `GET /` (`login.html`), `POST /auth/login`, `GET /dashboard` | `AuthService.iniciarSesion`, `Usuario.iniciarSesion` |
| CU-002 | Registrar docentes y alumnos | `GET/POST /admin/registrar_usuario` (`admin/registrar_usuario.html`) | `AdministradorService.registrarAlumno`, `registrarDocente`, `DBBroker.guardarObjeto` |
| CU-003 | Crear plan academico | `GET/POST /admin/crear_plan` (`admin/crear_plan.html`) | `Administrador.crearPlan`, `AdministradorService.crearPlan`, `guardarObjeto(Plan)` |
| CU-004 | Crear materias | `GET/POST /admin/crear_materia` (`admin/crear_materia.html`) | `Administrador.crearMateria`, `AdministradorService.crearMateria` |
| CU-005 | Asignar materias a plan | `GET/POST /admin/asignar_materia_plan` (`admin/asignar_materia_plan.html`) | `Plan.addList`, `DBBroker.addList`, `actualizarObjeto(Plan)` |
| CU-006 | Crear cohorte y asignar alumnos | `GET/POST /admin/crear_cohorte` (`admin/crear_cohorte.html`) | `Administrador.crearCohorte`, `AdministradorService.crearCohorte`, `actualizarObjeto(Alumno)` |
| CU-007 | Crear curso y asignar docente | `GET/POST /admin/crear_curso` (`admin/crear_curso.html`) | `Administrador.crearCurso`, `AdministradorService.crearCurso`, `asignarDocente` |
| CU-008 | Alumno inicia sesion | `POST /auth/login` (rol alumno), `GET /dashboard` | `AuthService.iniciarSesion` |
| CU-009 | Alumno se inscribe a materias | `GET/POST /alumno/inscribirse_materia` (`alumno/inscribirse_materia.html`) | `Alumno.inscribirseMateria`, `DBBroker.actualizarObjeto(Alumno)` |
| CU-010 | Alumno se inscribe a examenes | `GET/POST /alumno/inscribirse_examen` (`alumno/inscribirse_examen.html`) | `Alumno.inscribirseExamen`, `DBBroker.actualizarObjeto(Alumno)` |
| CU-011 | Alumno registra asistencia | `GET/POST /alumno/asistencia` (`alumno/asistencia.html`) | `AsistenciaService.registrarAsistencia`, `guardarObjeto(Asistencia)` |
| CU-012 | Alumno consulta asistencia | `GET /alumno/asistencia` | `AsistenciaService.consultarAsistencia`, `Asistencia.CalcularPorcentaje` |
| CU-013 | Docente inicia sesion | `POST /auth/login` (rol docente) | `AuthService.iniciarSesion` |
| CU-014 | Docente carga calificaciones | `GET/POST /docente/cargar_calificaciones` (`docente/cargar_calificaciones.html`) | `DocenteService.cargarCalificaciones`, `guardarObjeto(Calificacion)` |
| CU-015 | Docente registra asistencia propia | `GET/POST /docente/asistencia` (`docente/asistencia.html`) | `AsistenciaService.registrarAsistencia` |
| CU-016 | Docente consulta asistencia acumulada | `GET /docente/asistencia` | `AsistenciaService.consultarAsistencia`, `Asistencia.CalcularPorcentaje` |

## Como ejecutar
```bash
cd gestion_academica
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Abrir http://127.0.0.1:8000/ en el navegador para iniciar sesion.

## Datos de prueba
| Rol | Usuario | Clave |
|-----|---------|-------|
| Administrador | `admin@demo.com` | `1234` |
| Alumno | `alumno1@demo.com` | `1234` |
| Docente | `docente1@demo.com` | `1234` |

Datos semilla adicionales:
- Materias: Algoritmos (ALG101) y Bases de Datos (BD201)
- Plan: Plan Ingenieria de Software (contiene las materias anteriores)
- Examen: parcial de Algoritmos (2024-07-01)

## Limitaciones y proximos pasos
1. Persistencia JSON pensada para prototipo; migrar a una base relacional con repositorios.
2. Validaciones basicas (sin cupos ni correlatividades estrictas); agregar reglas avanzadas.
3. Gestion de permisos mas fina para evitar el acceso directo a rutas restringidas.
4. Incorporar un Observer para notificar altas de cursos, examenes o calificaciones.
5. Agregar pruebas automaticas y mejorar los mensajes de retroalimentacion en la UI.
