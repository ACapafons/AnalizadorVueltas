# -*- coding: utf-8 -*-
"""
Analizador de Vueltas - Motorsport Telemetry Tool
Sesion: Clasificacion GP Monaco 2023 - F1

Autor: ACapafons
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import csv
import os
from collections import defaultdict


# --------------------------------------------------
#  UTILIDADES DE FORMATO
# --------------------------------------------------

def segundos_a_tiempo(seg):
    """Convierte segundos (float) a formato m:ss.mmm"""
    minutos = int(seg // 60)
    resto = seg - minutos * 60
    return f"{minutos}:{resto:06.3f}"


def tiempo_a_segundos(tiempo_str):
    """Convierte 'm:ss.mmm' o 'ss.mmm' a segundos (float)"""
    tiempo_str = tiempo_str.strip()
    if ':' in tiempo_str:
        partes = tiempo_str.split(':')
        return int(partes[0]) * 60 + float(partes[1])
    return float(tiempo_str)


def separador(char='-', ancho=60):
    print(char * ancho)


def titulo(texto):
    separador('=')
    print(f"  {texto}")
    separador('=')


def subtitulo(texto):
    separador()
    print(f"  {texto}")
    separador()


# --------------------------------------------------
#  CARGA DE DATOS
# --------------------------------------------------

def cargar_csv(ruta):
    """Carga el CSV y devuelve una lista de diccionarios."""
    if not os.path.exists(ruta):
        print(f"\n  Archivo no encontrado: {ruta}\n")
        return None

    vueltas = []
    with open(ruta, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for fila in reader:
            try:
                fila['tiempo_seg']  = tiempo_a_segundos(fila['tiempo'])
                fila['sector1_seg'] = float(fila['sector1'])
                fila['sector2_seg'] = float(fila['sector2'])
                fila['sector3_seg'] = float(fila['sector3'])
                vueltas.append(fila)
            except (ValueError, KeyError):
                continue
    return vueltas


# --------------------------------------------------
#  ANALISIS
# --------------------------------------------------

def vuelta_mas_rapida(vueltas, sesion=None):
    """Devuelve la vuelta mas rapida, opcionalmente filtrando por sesion."""
    filtradas = [v for v in vueltas if sesion is None or v['sesion'] == sesion]
    if not filtradas:
        return None
    return min(filtradas, key=lambda v: v['tiempo_seg'])


def estadisticas_por_piloto(vueltas, sesion=None):
    """Devuelve estadisticas agrupadas por piloto, ordenadas por mejor tiempo."""
    filtradas = [v for v in vueltas if sesion is None or v['sesion'] == sesion]
    pilotos = defaultdict(list)
    for v in filtradas:
        pilotos[v['piloto']].append(v)

    stats = {}
    for piloto, vueltas_piloto in pilotos.items():
        tiempos = [v['tiempo_seg'] for v in vueltas_piloto]
        mejor   = min(vueltas_piloto, key=lambda v: v['tiempo_seg'])
        stats[piloto] = {
            'equipo':     mejor['equipo'],
            'numero':     mejor['numero'],
            'neumaticos': mejor['neumaticos'],
            'mejor_seg':  min(tiempos),
            'promedio':   sum(tiempos) / len(tiempos),
            'vueltas':    len(vueltas_piloto),
        }
    return dict(sorted(stats.items(), key=lambda x: x[1]['mejor_seg']))


def vuelta_ideal(vueltas, sesion=None):
    """Calcula la vuelta ideal: suma de los mejores sectores individuales."""
    filtradas = [v for v in vueltas if sesion is None or v['sesion'] == sesion]
    if not filtradas:
        return None

    mejor_s1 = min(filtradas, key=lambda v: v['sector1_seg'])
    mejor_s2 = min(filtradas, key=lambda v: v['sector2_seg'])
    mejor_s3 = min(filtradas, key=lambda v: v['sector3_seg'])
    total = mejor_s1['sector1_seg'] + mejor_s2['sector2_seg'] + mejor_s3['sector3_seg']

    return {
        'sector1': {'piloto': mejor_s1['piloto'], 'tiempo': mejor_s1['sector1_seg']},
        'sector2': {'piloto': mejor_s2['piloto'], 'tiempo': mejor_s2['sector2_seg']},
        'sector3': {'piloto': mejor_s3['piloto'], 'tiempo': mejor_s3['sector3_seg']},
        'total':   total,
    }


# --------------------------------------------------
#  VISUALIZACION EN CONSOLA
# --------------------------------------------------

def mostrar_vuelta_rapida(vuelta, etiqueta="Vuelta mas rapida"):
    subtitulo(f"  {etiqueta}")
    print(f"  {'Piloto':<18} {vuelta['piloto']} #{vuelta['numero']}")
    print(f"  {'Equipo':<18} {vuelta['equipo']}")
    print(f"  {'Sesion':<18} {vuelta['sesion']}")
    print(f"  {'Tiempo':<18} {vuelta['tiempo']}")
    print(f"  {'Sector 1':<18} {vuelta['sector1']}s")
    print(f"  {'Sector 2':<18} {vuelta['sector2']}s")
    print(f"  {'Sector 3':<18} {vuelta['sector3']}s")
    print(f"  {'Neumaticos':<18} {vuelta['neumaticos']}")


def mostrar_estadisticas(stats, sesion_label=""):
    subtitulo(f"  Clasificacion por piloto{sesion_label}")
    print(f"  {'POS':<4} {'PILOTO':<14} {'EQUIPO':<22} {'MEJOR':<12} {'PROMEDIO':<12} VLT")
    separador('-')
    for pos, (piloto, s) in enumerate(stats.items(), 1):
        print(
            f"  {pos:<4} {piloto:<14} {s['equipo']:<22} "
            f"{segundos_a_tiempo(s['mejor_seg']):<12} "
            f"{segundos_a_tiempo(s['promedio']):<12} "
            f"{s['vueltas']}"
        )


def mostrar_vuelta_ideal(ideal):
    subtitulo("  Vuelta ideal (mejores sectores combinados)")
    print(f"  Sector 1: {ideal['sector1']['tiempo']:.3f}s  ->  {ideal['sector1']['piloto']}")
    print(f"  Sector 2: {ideal['sector2']['tiempo']:.3f}s  ->  {ideal['sector2']['piloto']}")
    print(f"  Sector 3: {ideal['sector3']['tiempo']:.3f}s  ->  {ideal['sector3']['piloto']}")
    separador('-')
    print(f"  TOTAL IDEAL:  {segundos_a_tiempo(ideal['total'])}")


def mostrar_diferencias_pole(stats):
    """Muestra el gap de cada piloto respecto a la pole."""
    subtitulo("  Diferencias respecto a la pole")
    pilotos = list(stats.items())
    if not pilotos:
        return
    _, pole_stats = pilotos[0]
    pole_tiempo = pole_stats['mejor_seg']

    print(f"  {'POS':<4} {'PILOTO':<14} {'MEJOR':<12} GAP")
    separador('-')
    for pos, (piloto, s) in enumerate(pilotos, 1):
        gap = s['mejor_seg'] - pole_tiempo
        gap_str = "POLE" if gap == 0 else f"+{gap:.3f}s"
        print(f"  {pos:<4} {piloto:<14} {segundos_a_tiempo(s['mejor_seg']):<12} {gap_str}")


# --------------------------------------------------
#  MENU
# --------------------------------------------------

def seleccionar_sesion(vueltas):
    sesiones = sorted(set(v['sesion'] for v in vueltas))
    print("\n  Sesiones disponibles:")
    for i, s in enumerate(sesiones, 1):
        print(f"    [{i}] {s}")
    print(f"    [{len(sesiones)+1}] Todas las sesiones")

    while True:
        try:
            op = int(input("\n  Selecciona sesion: "))
            if 1 <= op <= len(sesiones):
                return sesiones[op - 1]
            elif op == len(sesiones) + 1:
                return None
        except ValueError:
            pass
        print("  Opcion no valida.")


def menu_principal(vueltas, ruta_csv):
    while True:
        titulo("ANALIZADOR DE VUELTAS - GP MONACO 2023 F1")
        print(f"  Archivo: {os.path.basename(ruta_csv)}")
        print(f"  Vueltas cargadas: {len(vueltas)}\n")
        print("  [1]  Vuelta mas rapida de una sesion")
        print("  [2]  Estadisticas por piloto")
        print("  [3]  Vuelta ideal (mejores sectores)")
        print("  [4]  Diferencias respecto a la pole (Q3)")
        print("  [5]  Resumen completo (Q3)")
        print("  [0]  Salir")
        separador()

        op = input("  Opcion: ").strip()

        if op == '1':
            sesion = seleccionar_sesion(vueltas)
            vr = vuelta_mas_rapida(vueltas, sesion)
            if vr:
                label = "Vuelta mas rapida global" if sesion is None else f"Vuelta mas rapida - {sesion}"
                mostrar_vuelta_rapida(vr, label)
            else:
                print("  No hay datos para esa sesion.")

        elif op == '2':
            sesion = seleccionar_sesion(vueltas)
            label = " (todas)" if sesion is None else f" ({sesion})"
            stats = estadisticas_por_piloto(vueltas, sesion)
            mostrar_estadisticas(stats, label)

        elif op == '3':
            sesion = seleccionar_sesion(vueltas)
            ideal = vuelta_ideal(vueltas, sesion)
            if ideal:
                mostrar_vuelta_ideal(ideal)

        elif op == '4':
            stats = estadisticas_por_piloto(vueltas, 'Q3')
            mostrar_diferencias_pole(stats)

        elif op == '5':
            print()
            vr = vuelta_mas_rapida(vueltas, 'Q3')
            if vr:
                mostrar_vuelta_rapida(vr, "Vuelta mas rapida - Q3")
            stats = estadisticas_por_piloto(vueltas, 'Q3')
            mostrar_estadisticas(stats, " (Q3)")
            mostrar_diferencias_pole(stats)
            ideal = vuelta_ideal(vueltas, 'Q3')
            if ideal:
                mostrar_vuelta_ideal(ideal)

        elif op == '0':
            print("\n  Hasta la proxima vuelta!\n")
            break
        else:
            print("  Opcion no valida.\n")

        input("\n  Pulsa ENTER para continuar...")


# --------------------------------------------------
#  PUNTO DE ENTRADA
# --------------------------------------------------

def main():
    directorio = os.path.dirname(os.path.abspath(__file__))
    csvs = [f for f in os.listdir(directorio) if f.endswith('.csv')]

    if not csvs:
        ruta = input("  Introduce la ruta al archivo CSV: ").strip()
    elif len(csvs) == 1:
        ruta = os.path.join(directorio, csvs[0])
        print(f"\n  Archivo detectado: {csvs[0]}")
    else:
        print("\n  Archivos CSV disponibles:")
        for i, f in enumerate(csvs, 1):
            print(f"    [{i}] {f}")
        while True:
            try:
                op = int(input("  Selecciona archivo: "))
                if 1 <= op <= len(csvs):
                    ruta = os.path.join(directorio, csvs[op - 1])
                    break
            except ValueError:
                pass
            print("  Opcion no valida.")

    vueltas = cargar_csv(ruta)
    if not vueltas:
        return

    menu_principal(vueltas, ruta)


if __name__ == '__main__':
    main()
