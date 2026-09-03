# ================================================================
# SISTEMA EXPERTO: Diagnóstico de PC
# Implementación con motor de inferencia hacia adelante
# ================================================================

# ──────────────────────────────────────────────────────────────
# COMPONENTE 1: BASE DE CONOCIMIENTO
# Aquí vive el conocimiento del experto técnico.
# Cada regla tiene: id, condiciones (lista de síntomas requeridos),
# conclusión y un factor de confianza de 0 a 1.
# ──────────────────────────────────────────────────────────────

base_de_conocimiento = [
    {
        "id": "R01",
        "descripcion": "Fuente de poder dañada",
        "condiciones": ["no_enciende", "sin_luces", "sin_sonido"],
        "conclusion": "Revisar o reemplazar la fuente de poder",
        "confianza": 0.92
    },
    {
        "id": "R02",
        "descripcion": "Falla de RAM",
        "condiciones": ["enciende", "pitidos_arranque", "sin_video"],
        "conclusion": "Probar con módulos de RAM de a uno",
        "confianza": 0.88
    },
    {
        "id": "R03",
        "descripcion": "Falla de tarjeta de video",
        "condiciones": ["enciende", "pantalla_negra", "sin_pitidos"],
        "conclusion": "Revisar tarjeta de video y conexiones del monitor",
        "confianza": 0.80
    },
    {
        "id": "R04",
        "descripcion": "Problemas de almacenamiento",
        "condiciones": ["enciende", "inicia_lento", "disco_al_100"],
        "conclusion": "Verificar salud del disco duro con herramienta SMART",
        "confianza": 0.85
    },
    {
        "id": "R05",
        "descripcion": "Infección por malware",
        "condiciones": ["enciende", "inicia_lento", "ventilador_siempre_activo"],
        "conclusion": "Escanear con antivirus y revisar procesos en segundo plano",
        "confianza": 0.72
    },
    {
        "id": "R06",
        "descripcion": "Driver o RAM dañada",
        "condiciones": ["enciende", "pantalla_azul_frecuente"],
        "conclusion": "Actualizar drivers y testear memoria RAM con MemTest86",
        "confianza": 0.87
    },
    {
        "id": "R07",
        "descripcion": "Sobrecalentamiento",
        "condiciones": ["enciende", "se_apaga_solo", "calor_excesivo"],
        "conclusion": "Limpiar ventiladores y reaplicar pasta térmica",
        "confianza": 0.90
    },
    #codigo nuevo agregando reglas implementacion de Mario Villatoro
    {
       "id": "R08",
       "descripcion": "Perifericos dañados",
       "condiciones": ["puntero_no_mueve", "sin_video","teclas_no_reaccionan"],
       "conclusion": "Desconecta los perifericos y prubelos, si el problema persiste debes cambiarlos",
       "confianza": 0.90
   },
   {
       "id": "R09",
       "descripcion": "Drivers corruptos",
       "condiciones": ["fallo_audio","sin_video", "pantalla_azul_frecuente"],
       "conclusion": "Actualizar drivers o reinstalarlos si es necesario",
       "confianza": 0.85
   },
   {"id": "R010",
       "descripcion": "Perdida de fecha y hora de la BIOS",
       "condiciones": ["Hora_no_coincide", "Mensajes_de_error_al_arrancar"],
       "conclusion": "Actualizar drivers y testear memoria RAM con MemTest86",
       "confianza": 0.70
   },{
       "id": "R011",
       "descripcion": "El error esta en la silla",
       "condiciones": [],
       "conclusion": "Borrar carpeta Sistem32",
       "confianza": 1
   },

]



# ──────────────────────────────────────────────────────────────
# COMPONENTE 2: BASE DE HECHOS (Working Memory)
# Estado actual del caso. Usamos un set de Python para
# representar los síntomas presentes (eficiente para búsqueda).
# ──────────────────────────────────────────────────────────────

base_de_hechos = set()  # vacía al inicio, se llena con los síntomas

# ──────────────────────────────────────────────────────────────
# COMPONENTE 3: MOTOR DE INFERENCIA
# Funciones de equiparación y resolución de conflictos
# ──────────────────────────────────────────────────────────────
"""
def equiparar(base_conocimiento, hechos):
    Proceso de equiparación (pattern matching).
    Retorna todas las reglas cuyas condiciones están satisfechas
    por los hechos actuales. Esto es el 'conflict set'.
    
    
    conflict_set = []
    for regla in base_conocimiento:
        # Verificar si TODOS los síntomas de la regla están en los hechos
        # set.issubset() es O(len(condiciones)), más eficiente que un bucle
        if set(regla['condiciones']).issubset(hechos):
            conflict_set.append(regla)
    return conflict_set


def resolver_conflictos(conflict_set):
    
    Estrategia de resolución de conflictos: mayor confianza.
    Si hay empate, preferir la regla con más condiciones (más específica).
    
    if not conflict_set:
        return None
    return max(
        conflict_set,
        key=lambda r: (r['confianza'], len(r['condiciones']))
    )


def inferir(base_conocimiento, hechos):
    
    Motor de inferencia principal.
    Ejecuta el ciclo de equiparación → resolución → ejecución.
    
    print()
    print('━' * 55)
    print('  MOTOR DE INFERENCIA INICIADO')
    print('━' * 55)
    print(f'  Hechos ingresados: {hechos}')
    print()

    conflict_set = equiparar(base_conocimiento, hechos)

    if not conflict_set:
        print('  ⚠ No se encontraron reglas aplicables.')
        print('  Considera agregar más síntomas o revisar la base de conocimiento.')
        return

    print(f'  Reglas que aplican (conflict set): {[r["id"] for r in conflict_set]}')
    print()

    regla = resolver_conflictos(conflict_set)

    print('  DIAGNÓSTICO')
    print('  ───────────────────────────────────────────────────')
    print(f'  Regla aplicada: {regla["id"]} — {regla["descripcion"]}')
    print(f'  Recomendación:  {regla["conclusion"]}')
    print(f'  Confianza:      {regla["confianza"] * 100:.0f}%')
    print()

    # COMPONENTE 4: INTERFAZ DE EXPLICACIÓN
    print('  TRAZABILIDAD DEL RAZONAMIENTO')
    print('  ───────────────────────────────────────────────────')
    print(f'  Síntomas que activaron la regla: {regla["condiciones"]}')
    if len(conflict_set) > 1:
        descartadas = [r['id'] for r in conflict_set if r['id'] != regla['id']]
        print(f'  Reglas descartadas por menor confianza: {descartadas}')
    print('━' * 55)

"""
#codigo modificado par presentar un listado de diagnostico y no solo el de mayo r confianza
def equiparar(base_conocimiento, hechos):
    """
    Proceso de equiparación (pattern matching).
    Retorna todas las reglas cuyas condiciones están satisfechas
    por los hechos actuales.
    """
    conflict_set = []
    for regla in base_conocimiento:
        if set(regla['condiciones']).issubset(hechos):
            conflict_set.append(regla)
    return conflict_set


def ordenar_diagnosticos(conflict_set):
    """
    Ordena el conflict set de mayor a menor confianza.
    Criterio secundario: cantidad de condiciones (reglas más específicas).
    """
    if not conflict_set:
        return []
    # se cambio la propiedad max por sorted para obtener un listado de diagnosticos y no solo el de mayor confianza
    return sorted(
        conflict_set,
        key=lambda r: (r['confianza'], len(r['condiciones'])),
        reverse=True
    )



def inferir(base_conocimiento, hechos):
    """
    Motor de inferencia principal con soporte para ranking de diagnósticos.
    """
    print()
    print('━' * 60)
    print('  MOTOR DE INFERENCIA INICIADO')
    print('━' * 60)
    print(f'  Hechos ingresados: {list(hechos)}') #si obtine la lista de hechos ingresados
    print()

    conflict_set = equiparar(base_conocimiento, hechos)

    if not conflict_set:
        print('  ⚠ No se encontraron reglas aplicables.')
        print('  Considera agregar más síntomas o revisar la base de conocimiento.')
        print('━' * 60)
        return

    # Ordenar todas las reglas que aplican de mayor a menor confianza
    diagnosticos = ordenar_diagnosticos(conflict_set)

    print('  RANKING DE DIAGNÓSTICOS POSIBLES')
    print('  ───────────────────────────────────────────────────────────')
    # Mostrar cada diagnóstico con su confianza, descripción y recomendación en una lista numerada
    for i, regla in enumerate(diagnosticos, 1):
        porcentaje = regla["confianza"] * 100
        print(f'  {i}. [{porcentaje:.0f}% de Confianza] — Regla {regla["id"]}: {regla["descripcion"]}')
        print(f'     ➔ Recomendación: {regla["conclusion"]}')
        print(f'     ➔ Síntomas clave: {regla["condiciones"]}')
        if i < len(diagnosticos):
            print('  ───────────────────────────────────────────────────────────')

    print('━' * 60)

# ──────────────────────────────────────────────────────────────
# COMPONENTE 5: INTERFAZ DE USUARIO
# ──────────────────────────────────────────────────────────────

PREGUNTAS = {
    "no_enciende":              "¿El equipo NO enciende (sin luces, sin sonido)?",
    "sin_luces":                "¿No hay ninguna luz LED encendida?",
    "sin_sonido":               "¿No se escucha ningún sonido al encender?",
    "enciende":                 "¿El equipo SÍ enciende (hay luces y/o sonido)?",
    "pitidos_arranque":         "¿Se escuchan pitidos (beeps) al encender?",
    "sin_video":                "¿La pantalla no muestra absolutamente nada?",
    "pantalla_negra":           "¿La pantalla queda en negro (sin pitidos)?",
    "sin_pitidos":              "¿No se escuchan pitidos?",
    "inicia_lento":             "¿El equipo tarda más de 3 minutos en iniciar?",
    "disco_al_100":             "¿El administrador de tareas muestra disco al 100%?",
    "ventilador_siempre_activo":"¿El ventilador está siempre a máxima velocidad?",
    "pantalla_azul_frecuente":  "¿Aparece pantalla azul (BSOD) con frecuencia?",
    "se_apaga_solo":            "¿El equipo se apaga solo sin advertencia?",
    "calor_excesivo":           "¿El chasis está muy caliente al tacto?"
"puntero_no_mueve":         "¿El mouse no se mueve?",
   "teclas_no_reaccionan":     "¿Al escribir el teclado no responde?",
   "fallo_audio":              "¿El audio del equipo no funciona?",
   "Hora_no_coincide":         "¿Al iniciar la pc la hora no concuerda o cada dia cambia unos minutos?",
   "Mensajes_de_error_al_arrancar": "¿Al arrancar la maquina aparecen codigos de error que inician en CMOS?"
}

def consultar():
    print()
    print('=' * 55)
    print('  SISTEMA EXPERTO: Diagnóstico de Computador')
    print('  Responde s (sí) o n (no) a cada pregunta')
    print('=' * 55)
    print()

    for sintoma, pregunta in PREGUNTAS.items():
        resp = input(f'  {pregunta} [s/n]: ').strip().lower()
        if resp == 's':
            base_de_hechos.add(sintoma)

    inferir(base_de_conocimiento, base_de_hechos)


# Ejecutar programa
consultar()
