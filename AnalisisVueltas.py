import pandas as pd
import os
import matplotlib.pyplot as plt  # Añade esta importación al inicio

def menu_principal():
    """Muestra el menú principal y maneja la selección del archivo"""
    try:
        # Mostrar archivos disponibles
        archivos_disponibles = buscar_csvs()
        
        if not archivos_disponibles:
            print("No se encontraron archivos CSV en el directorio actual.")
            return None
        
        # Pedir al usuario que elija un archivo
        while True:
            seleccion = input("\nSeleccione el número del archivo a analizar: ")
            try:
                indice = int(seleccion) - 1
                if 0 <= indice < len(archivos_disponibles):
                    return archivos_disponibles[indice]
                print("Número inválido. Intente nuevamente.")
            except ValueError:
                print("Por favor, ingrese un número válido.")
    except Exception as e:
        print(f"Error en el menú: {e}")
        return None

def buscar_csvs():
    dir_actual = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dir_actual)
    
    csvs = [f for f in os.listdir(dir_actual) if f.lower().endswith('.csv')]
    
    if csvs:
        print("\nArchivos de datos disponibles:")
        for i, csv in enumerate(csvs, 1):
            print(f"{i}. {csv}")
    else:
        print("\nNo hay archivos de telemetría (.csv) en:", dir_actual)
    
    return csvs

def analizar_carrera(datos):
    print("\n🏎️  ANÁLISIS DE CARRERA 🏁 ")
    print(f"Vueltas totales completadas: {len(datos)}")
    
    # Vuelta más rápida
    mejor_tiempo = datos['Tiempo'].min()
    idx_mejor = datos['Tiempo'].idxmin()
    piloto = datos.loc[idx_mejor, 'Piloto']
    gomas = datos.loc[idx_mejor, 'TipoNeumatico']
    
    print(f"\n⚡ Vuelta rápida:")
    print(f"   {mejor_tiempo:.3f}s - {piloto} (vuelta {datos.loc[idx_mejor, 'Vuelta']}, {gomas})")

    # Análisis por piloto
    print("\n👨 Resumen pilotos:")
    for piloto in datos['Piloto'].unique():
        stint = datos[datos['Piloto'] == piloto]
        mejor = stint['Tiempo'].min()
        promedio = stint['Tiempo'].mean()
        
        print(f"\n{piloto}:")
        print(f"   Mejor: {mejor:.3f}s")
        print(f"   Media: {promedio:.3f}s")
        print(f"   Vueltas: {len(stint)}")

def generar_grafico(datos):
    """Genera un gráfico básico de tiempos por vuelta"""
    plt.figure(figsize=(10, 6))
    
    # Graficar tiempos para cada piloto
    for piloto in datos['Piloto'].unique():
        datos_piloto = datos[datos['Piloto'] == piloto]
        plt.plot(datos_piloto['Vuelta'], datos_piloto['Tiempo'], 
                marker='o', label=piloto)
    
    plt.title('Evolución de Tiempos por Vuelta')
    plt.xlabel('Número de Vuelta')
    plt.ylabel('Tiempo (segundos)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()

def main():
    # 1. Mostrar menú y seleccionar archivo
    archivo_seleccionado = menu_principal()
    if not archivo_seleccionado:
        return
    
    # 2. Cargar datos
    try:
        print(f"\nCargando archivo: {archivo_seleccionado}")
        df = pd.read_csv(archivo_seleccionado)
        
        # 3. Analizar datos
        analizar_carrera(df)
        
        # 4. Generar gráfico
        print("\nGenerando gráfico de tiempos...")
        generar_grafico(df)
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

if __name__ == "__main__":
    main()