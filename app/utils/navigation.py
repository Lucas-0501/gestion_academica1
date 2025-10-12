"""Navigation helpers for building role-based menus."""

from __future__ import annotations

from typing import List, Tuple


MenuItem = Tuple[str, str, str]


def menu_for_role(rol: str) -> List[MenuItem]:
    """Return label, icon class, and route for sidebar navigation."""
    common: List[MenuItem] = [
        ("Inicio", "fas fa-home", "/dashboard"),
        ("Salir", "fas fa-sign-out-alt", "/auth/logout"),
    ]
    role_specific = {
        "administrador": [
            ("Materias", "fas fa-book", "/admin/crear_materia"),
            ("Planes", "fas fa-diagram-project", "/admin/crear_plan"),
            ("Asignaciones", "fas fa-sitemap", "/admin/asignar_materia_plan"),
            ("Cohortes", "fas fa-users", "/admin/crear_cohorte"),
            ("Cursos", "fas fa-chalkboard-teacher", "/admin/crear_curso"),
            ("Usuarios", "fas fa-user-plus", "/admin/registrar_usuario"),
        ],
        "alumno": [
            ("Materias", "fas fa-book-open", "/alumno/inscribirse_materia"),
            ("Examenes", "fas fa-file-alt", "/alumno/inscribirse_examen"),
            ("Asistencia", "fas fa-calendar-check", "/alumno/asistencia"),
            ("Notas", "fas fa-graduation-cap", "/alumno/notas"),
        ],
        "docente": [
            ("Asistencia", "fas fa-calendar-check", "/docente/asistencia"),
            ("Calificaciones", "fas fa-marker", "/docente/cargar_calificaciones"),
        ],
    }
    combined = role_specific.get(rol, [])
    # Combine unique items preserving order, avoid duplicates for Inicio/Salir
    menu: List[MenuItem] = []
    seen_routes = set()
    for label, icon, route in combined + common:
        if route not in seen_routes:
            menu.append((label, icon, route))
            seen_routes.add(route)
    return menu
