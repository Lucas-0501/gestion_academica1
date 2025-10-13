classDiagram
    class Usuario{
        +id: str?
        +nombre: str
        +email: str
        +password: str
        +rol: str
        +sesion_activa: bool
        +iniciarSesion(password) bool
        +cerrarSesion() void
        +to_dict() Dict
        +from_dict(data) Usuario
    }
    class Administrador{
        +crearPlan(nombre, descripcion) Plan
        +crearMateria(nombre, codigo, descripcion) Materia
        +crearCohorte(nombre, plan_id, alumnos_ids) Cohorte
        +crearCurso(nombre, materia_id, cohorte_id, docente_id) Curso
        +asignarDocente(curso, docente_id) Curso
    }
    class Alumno{
        +materiasInscripto: List~str~
        +examenesInscripto: List~str~
        +plan_id: str?
        +cohorte_id: str?
        +inscribirseMateria(materia_id) void
        +inscribirseExamen(examen_id) void
        +to_dict() Dict
        +from_dict(data) Alumno
    }
    class Docente{
        +materiasAsignadas: List~str~
        +asignarMateria(materia_id) void
        +cargarCalificacion(alumno_id,materia_id,nota) Dict
        +to_dict() Dict
        +from_dict(data) Docente
    }
    class Plan{
        +id: str?
        +nombre: str
        +descripcion: str
        +materias: List~str~
        +addList(materia_ids) void
        +to_dict() Dict
        +from_dict(data) Plan
    }
    class Materia{
        +id: str?
        +nombre: str
        +codigo: str
        +descripcion: str
        +to_dict() Dict
        +from_dict(data) Materia
    }
    class Cohorte{
        +id: str?
        +nombre: str
        +plan_id: str
        +alumnos: List~str~
        +asignarAlumno(alumno_id) void
        +to_dict() Dict
        +from_dict(data) Cohorte
    }
    class Curso{
        +id: str?
        +nombre: str
        +materia_id: str
        +cohorte_id: str?
        +docente_id: str?
        +asignarDocente(docente_id) void
        +to_dict() Dict
        +from_dict(data) Curso
    }
    class Examen{
        +id: str?
        +materia_id: str
        +fecha: str
        +cupo: int?
        +to_dict() Dict
        +from_dict(data) Examen
    }
    class Calificacion{
        +id: str?
        +alumno_id: str
        +materia_id: str
        +nota: float
        +fecha: str
        +to_dict() Dict
        +from_dict(data) Calificacion
    }
    class Asistencia{
        +id: str?
        +usuario_id: str
        +fecha: str
        +presente: bool
        +rol: str
        +to_dict() Dict
        +from_dict(data) Asistencia
        +CalcularPorcentaje(records) float
    }
    class DBBroker{
        +guardarObjeto(obj) Dict
        +obtener(clase,obj_id) Dict?
        +obtenerPorId(clase,obj_id) Dict?
        +listar(clase) List~Dict~
        +actualizarObjeto(obj) Dict
        +eliminarObjeto(clase,obj_id) void
        +addList(clase,obj_id,field,values) Dict
        +reset_store() void
    }
    class Mapper{
        +load(collection) List~Dict~
        +save(collection,data) void
    }
    Usuario <|-- Administrador
    Usuario <|-- Alumno
    Usuario <|-- Docente
    Plan "1" o-- "*" Materia : materias ids
    Cohorte "1" o-- "*" Alumno : alumnos ids
    Curso "1" -- "1" Materia : materia_id
    Curso "0..1" o-- "1" Cohorte : cohorte_id
    Curso "0..1" o-- "1" Docente : docente_id
    Examen "1" -- "1" Materia : materia_id
    Calificacion "*" -- "1" Alumno : alumno_id
    Calificacion "*" -- "1" Materia : materia_id
    Asistencia "*" -- "1" Usuario : usuario_id
    DBBroker --> Mapper
    DBBroker --> Usuario
    DBBroker --> Materia
    DBBroker --> Plan
    DBBroker --> Cohorte
    DBBroker --> Curso
    DBBroker --> Examen
    DBBroker --> Asistencia
    DBBroker --> Calificacion
