# QA individual - Semana 13

**Responsable:** Julio Diaz Ttito  
**Usuario de GitHub:** drakosa1  
**Rol:** QA  
**Rama:** test/julio-qa-week13

## Qué se hizo

Se agregó un archivo nuevo de pruebas:

- `tests/test_regresion_week13.py`

La idea fue cubrir casos que todavía no estaban en la suite y que pueden romperse
después de cambios en la interfaz o en los repositorios. No se repitieron pruebas
que ya existían en `test_gui_clientes.py`, `test_gui_numerico.py`,
`test_dominio.py` ni `test_repositorios.py`.

Las pruebas usan la fixture real `db_session` y las clases verdaderas del
proyecto. No se inventaron servicios nuevos.

## Pruebas implementadas

### 1. Recuperación del stock al cancelar una venta

Hay una prueba que crea un pedido con dos productos, lo cancela y comprueba que
el stock vuelve a su valor original. Después vuelve a vender esos mismos productos
para confirmar que el stock recuperado se puede usar otra vez.

Esto complementa las pruebas anteriores, que cancelaban pedidos de un solo
producto.

### 2. Cantidades incorrectas

Se probaron dos caminos distintos:

- Desde el repositorio: cantidades `0` y `-1` son rechazadas y no dejan pedidos
  guardados ni cambios de stock.
- Desde la interfaz: el botón "+" del carrito no deja pasar el stock disponible y
  muestra un aviso.

Las pruebas de `test_dominio.py` ya validaban la función `validar_cantidad`, y las
de `test_gui_numerico.py` ya probaban los conversores. Lo nuevo es comprobar que
esas reglas llegan al pedido y al carrito reales.

### 3. Búsqueda de registros inexistentes

Se buscó un cliente, un SKU y un pedido que no existen. Los tres devuelven
`None`, sin errores.

También se intentó crear un pedido con un documento de cliente inexistente y con
un SKU inexistente. En ambos casos se muestra el error esperado y no se guarda
ningún pedido.

### 4. Operaciones con datos inválidos

Se comprobó que no se guarden datos cuando:

- El documento del cliente tiene mala forma (`123`, `1234567A`, `123456789`).
- El precio o el stock del producto no son números (`abc`).
- Un pedido repite el mismo SKU dos veces.
- Se intenta cambiar un pedido a un estado que no existe (`REVISION`).

En los casos de la interfaz se usó el modal real, pero sin abrir Tk, de la misma
forma en que ya trabajan las pruebas de clientes.

### 5. Campos obligatorios

Se agregaron pruebas para:

- Producto sin SKU desde el modal.
- Producto sin SKU o sin nombre desde el repositorio.
- Categoría sin nombre.

La validación de cliente con nombre o documento vacío ya estaba cubierta en
`test_gui_clientes.py`, por eso no se duplicó.

## Resultados reales

Los comandos se ejecutaron desde la raíz del repositorio con el intérprete del
entorno virtual (`.venv\Scripts\python.exe`), porque el `python` global de la
máquina no tiene instalados `pytest` ni `ruff`.

```text
python -m pytest -v
52 passed in 0.43s
```

Antes de este aporte había 34 pruebas. Ahora hay 52: se agregaron 18 casos nuevos.

```text
python -m ruff check .
All checks passed!
```

Durante la primera ejecución aparecieron 3 fallos en una prueba nueva: el conteo
esperado de clientes era 1, pero esa prueba no usa la fixture con cliente base y
el valor correcto era 0. Se corrigió esa assertion y la segunda ejecución quedó
completamente en verde. No hicieron falta cambios en el código fuente.

## Conclusiones

- La recuperación de stock al cancelar funciona también con pedidos de varias
  líneas y el stock devuelto se puede volver a vender.
- Las cantidades incorrectas se detienen antes de guardar el pedido, tanto en el
  repositorio como en el carrito de la pantalla.
- Las búsquedas sin resultados no rompen la aplicación: devuelven `None` o muestran
  un error controlado.
- Los formularios y repositorios evitan guardar documentos mal formados, textos en
  campos numéricos, SKUs repetidos, estados inventados y campos obligatorios vacíos.
- La suite quedó más completa sin duplicar las pruebas que ya existían.

## Defecto preexistente informado

No se modificó, porque no corresponde a este aporte de QA:

En `ModalProducto` (`src/presentacion/gui/pantallas/catalogo.py`) las conversiones
de precio y stock siguen siendo `float()` e `int()` directos. Los helpers
`convertir_decimal_positivo` y `convertir_entero_positivo` de
`src/presentacion/gui/utilidades.py` existen, pero los formularios no los usan.
Con un precio `nan` se escapa un `IntegrityError` y la sesión queda en
`PendingRollbackError`; con `inf` el producto se guarda y luego rompe los cálculos.
Conviene tratarlo en un siguiente cambio, con su propia prueba de regresión.

## Alcance de Git

No se hicieron commits, push ni cambios de rama. Quedan creados solamente:

- `tests/test_regresion_week13.py`
- `docs/QA_JULIO_WEEK13.md`
