# IPTV List Checker

Esta aplicación permite verificar si los canales en una lista IPTV M3U están funcionando correctamente.

## Requisitos

- Python 3.7 o superior
- Paquetes Python requeridos:
  - requests
  - m3u8

## Instalación

### Como usuario

1. Clona el repositorio o descarga los archivos
2. En el directorio del proyecto, ejecuta:

```bash
pip install .
```

### Como desarrollador

1. Clona el repositorio
2. En el directorio del proyecto, ejecuta:

```bash
pip install -e .
```

## Uso

### Como módulo instalado

```bash
python -m iptvchecker ruta/a/tu/lista.m3u
```

### Como librería

```python
from iptvchecker import check_playlist

results = check_playlist("ruta/a/tu/lista.m3u")
print(f"Canales funcionando: {results['working']['count']}")
print(f"Canales no funcionando: {results['not_working']['count']}")
```

La aplicación:
1. Cargará la lista M3U
2. Extraerá la información de los canales
3. Verificará cada canal para determinar si está funcionando
4. Mostrará un resumen con el estado de cada canal

## Características

- Verificación en paralelo de múltiples canales
- Separación automática de canales en archivos working/not working
- API programática para uso como librería
- Muestra el progreso en tiempo real
- Proporciona un resumen detallado de los resultados

## Estructura del Proyecto

```
iptvchecker/
├── iptvchecker/
│   ├── __init__.py
│   ├── __main__.py
│   └── checker.py
├── pyproject.toml
└── README.md
```

## Archivos de Salida

La herramienta genera dos archivos M3U:

- `[original]_working.m3u`: Contiene solo los canales que funcionan
- `[original]_notworking.m3u`: Contiene los canales que no funcionan

## Formato de Salida

Para cada canal, la aplicación mostrará:

- Nombre del canal
- URL
- Estado (Working/Not working)

Al final, se mostrará un resumen con:

- Total de canales verificados
- Cantidad de canales funcionando
- Cantidad de canales que no funcionan
- Rutas a los archivos generados
