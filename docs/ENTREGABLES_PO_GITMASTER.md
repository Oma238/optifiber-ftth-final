# ENTREGABLES DEL PRODUCT OWNER / SCRUM MASTER + GIT MASTER

**Nombre:** Omar Sebastián Huallpayunca Carrión  
**GitHub:** Oma238  
**Roles:** Product Owner / Scrum Master + Git Master  
**Proyecto:** OptiFiber FTTH · trabajo final construcción Software

---

## 1. GitHub Issues (PO1 y E1)

### PBI-01: Lógica de negocio FTTH

**Historia de Usuario (Gherkin):**

```
Como cliente de OptiFiber FTTH
Deseo cotizar un pedido de productos FTTH con descuentos por volumen
Para que el sistema calcule el total aplicando reglas de descuento y stock
```

**Criterios de Aceptación:**

| ID | Given | When | Then |
|---|---|---|---|
| AC-01 | Dado un catálogo de productos con precios y stock disponible | Cuando el usuario solicita un pedido con cantidades de productos | Entonces el sistema calcula el subtotal por línea usando `Decimal` |
| AC-02 | Dado un subtotal acumulado de S/ 150 o más | Cuando el usuario confirma el pedido | Entonces se aplica un descuento del 5 % sobre el total |
| AC-03 | Dado que un producto tiene stock insuficiente | Cuando el usuario intenta agregar más cantidad al pedido | Entonces el lanza `ErrorDominio: Stock insuficiente` |
| AC-04 | Dado un documento de cliente (DNI o RUC) | Cuando el sistema valida el documento | Entonces acepta formatos numéricos de 8 o 11 dígitos, quitando espacios en blanco |
| AC-05 | Dado una cantidad de producto | Cuando el usuario intenta registrar una cantidad cero o negativa | Entonces el lanza `ErrorDominio: cantidad debe ser > 0` |

---

### PBI-02: Persistencia ORM SQLAlchemy y cascada

**Historia de Usuario (Gherkin):**

```
Como administrador de OptiFiber FTTH
Deseo que el sistema persista clientes, pedidos y catálogo en SQLite
Para que los datos sobrevivan entre sesiones y las eliminaciones en cascada funcionen correctamente
```

**Criterios de Aceptación:**

| ID | Given | When | Then |
|---|---|---|---|
| AC-01 | Dado un cliente con datos válidos | Cuando se persiste en la base de datos | Entonces el cliente se recupera con su ID autoincremental |
| AC-02 | Dado un cliente con dos pedidos asociados | Cuando se elimina el cliente | Entonces sus pedidos también desaparecen (cascade `all, delete-orphan`) |
| AC-03 | Dado un producto con etiquetas N:M | Cuando se guarda el producto | Entonces se recuperan sus etiquetas y la navegación inversa funciona |
| AC-04 | Dado un pedido con detalles de producto | Cuando se elimina el pedido | Entonces sus detalles desaparecen y el producto se conserva (sin cascade) |
| AC-05 | Dado un documento de cliente único | Cuando se intenta registrar otro con el mismo documento | Entonces la restricción UNIQUE impide el commit y lanza `IntegrityError` |

---

### PBI-03: Validaciones / GUI

**Historia de Usuario (Gherkin):**

```
Como usuario de la interfaz gráfica de OptiFiber FTTH
Deseo validar campos obligatorios y entradas numéricas
Para que el sistema me muestre mensajes claros ante datos inválidos
```

**Criterios de Aceptación:**

| ID | Given | When | Then |
|---|---|---|---|
| AC-01 | Dado el formulario de alto de cliente vacío | Cuando el usuario intenta guardar | Entonces se muestra: "Por favor complete los campos obligatorios (Nombre y Documento)" |
| AC-02 | Dado un campo de documento con espacios | Cuando el sistema valida el documento | Entonces acepta y quita los espacios en blanco (`" 12345678 " → "12345678"`) |
| AC-03 | Dado un campo de cantidad cero o negativo | Cuando el usuario ingresa datos inválidos | Entonces lanza `ErrorDominio` para cantidad cero y valores negativos |
| AC-04 | Dado un stock insuficiente en el producto | Cuando el usuario intenta crear un pedido | Entonces el sistema rechaza la operación con "Stock insuficiente" |
| AC-05 | Dado un formulario con datos completos | Cuando el usuario guarda el cliente | Entonces el cliente se registra exitosamente y se confirma con mensaje |

---

### Issue: Contenerizar y automatizar pruebas

**8 puntos del contrato Docker/CI:**

1. Imagen base `python:3.12-slim` con `sqlite3` y `tkinter` incluidos para pruebas GUI.
2. `Dockerfile` que instale dependencias desde `requirements.txt` y exponga el puerto de la GUI.
3. `docker-compose.yml` con dos servicios: `app` (interfaz local) y `pruebas` (ejecución aislada de `pytest`).
4. GitHub Actions `ci.yml` que ejecute `ruff check .` y `pytest -v` en `ubuntu-latest`.
5. Perfil de compose `pruebas` que corrija `run --rm pruebas` para tests herméticos en memoria.
6. Volumen mount `data/` con la base de datos real vs `sqlite:///:memory:` para pruebas de integración.
7. ` StaticPool` en `conftest.py` para que todas las pruebas de un mismo scope vean la misma DB en memoria.
8. En Linux/Docker solo corren las pruebas; la ventana GUI debe ejecutarse en la PC local con `python src/main.py`.

---

## 2. Informe Capítulos 1 al 4 (A3 y PO4)

### A. Entidad aliada y problema operacional (2 párrafos)

**Empresa aliada:** OptiFiber FTTH, dedicada a la venta de productos FTTH (Fiber to the Home) para proveedores e instaladores. Su modelo de negocio incluye la gestión de clientes, catálogo de equipos ONT/ONU, accesorios de instalación, procesamiento de pedidos y control de stock en tiempo real.

**Problema operacional:** La empresa carecía de un sistema informatizado integrado para gestionar el ciclo completo de un cliente: desde el registro de datos personales y documento de identidad, pasando por la selección de productos y formación de pedidos, hasta el control de inventario y la emisión de reportes. El proceso era totalmente manual o disperso en archivos sin validación, lo que provocaba inconsistencia en el stock, dificultad para calcular descuentos por volumen y falta de historial confiable para la toma de decisiones.

### B. Tabla de los 5 roles

| Rol | Integrante | Responsabilidad principal |
|---|---|---|
| Git Master + PO/SM | Omar Sebastián Huallpayunca Carrión | Repositorio, ramas, PBI, revisión de PR, merges y coordinación del informe final. |
| Lead Backend Engineer | Kevin Jesus Llerena Fernandez | Reglas de negocio puras en `src/dominio`, servicios de totales/descuento/stock y capa de repositorios. |
| Database & ORM Specialist | Amaru Josue Ai-me Yunguri | ERD, modelos ORM, claves foráneas, relaciones 1:N y N:M, reglas de cascada y restricciones. |
| DevOps & QA Engineer + Frontend/UX/UI Engineer | Julio Cesar Diaz Tito | Fixture, suite pytest, Ruff, GitHub Actions, pantallas CustomTkinter, tema oscuro y evidencias del informe. |
| (Rol quinto / soporte) | — | — |

### C. Tabla de Product Backlog (Sección 1.5)

| PBI | Título | Descripción | Prioridad | Estado |
|---|---|---|---|---|
| PBI-01 | Lógica de negocio FTTH | Cálculo de subtotales, descuentos por volumen (5% S/ 150+), validación de stock y documento. | Alta | ✅ Finalizado |
| PBI-02 | Persistencia ORM SQLAlchemy y cascada | Modelos Cliente-Pedido-Detalle, relaciones N:M Producto-Etiqueta, cascada `all, delete-orphan`, restricciones UNIQUE y CHECK. | Alta | ✅ Finalizado |
| PBI-03 | Validaciones / GUI | Campos obligatorios, validación de documento, validación de cantidad, mensajes de error en interfaz CustomTkinter. | Alta | ✅ Finalizado |

### D. Tablas de evidencia TDD (Secciones 3.3 y 4.3)

#### Sección 3.3 — Evidencias de pruebas de dominio (Tabla)

| Comando | Resultado | Archivo |
|---|---|---|
| `python -m pytest tests/test_dominio.py -v` | `10 passed` | `docs/evidencias/pytest_dominio.txt` |
| `python -m pytest tests/test_persistencia_orm.py -v` | `5 passed` | `docs/evidencias/pytest_orm.txt` |
| `python -m pytest tests/test_repositorios.py -v` | `6 passed` | `docs/evidencias/pytest_repositorios.txt` |
| `python -m pytest -v` | `23 passed` | `docs/evidencias/pytest_final.txt` |

#### Sección 4.3 — Evidencias de secuencia TDD por commits

Los commits reales marcan la trayectoria RED → GREEN → REFACTOR. Los hashes que aparecen son:

| Commit | Descripción | Estado |
|---|---|---|
| `ff24499` | refactor(config): lee la ruta de la base de datos desde una variable de entorno (BE) | ✅ Aparce |
| `01833a0` | build(docker): agrega Dockerfile, docker-compose y workflow CI (DO) | ✅ Aparce |
| `92d2311` | fix(docker): agrega python3-tk para soporte de tkinter en pruebas | ✅ Aparce |
| `00576fe` | Merge pull request #5 from Oma238/fix/mejora-gui-alerta-numerica | ✅ Aparce |
| `1611d11` | docs: registrar ficha de evaluacion de peer testing semana 13 | ✅ Aparce |
| `8990336` | Corrige stock al cancelar ventas y mejora busquedas | ✅ Aparce |

> **Nota:** Si algún hash no aparece en el historial visible, completar con `???????` en la sección correspondiente.

---

## 3. Informe Docker Sección 12.3

**Análisis crítico (230 a 280 palabras):**

La reproducibilidad sin Docker en este proyecto es limitada: las 23 pruebas pasan localmente sobre SQLite en memoria, pero la configuración del entorno (versión de Python, paquetes SQLAlchemy, drivers de SQLite) puede diferir entre la PC del desarrollador y la máquina de Integración Continente. Las diferencias fundamentales entre un entorno de desarrollo en Windows y un contenedor Linux/GitHub Actions radican en la disponibilidad de bibliotecas del sistema: por ejemplo, la prueba de interfaz gráfica requiere `python3-tk` instalado en el contenedor (commit `92d2311`) para que `tkinter` no falle al importarse, y el path de la base de datos debe leerse desde variable de entorno (`ff24499`) en lugar de rutas absolutas de Windows. La decisión de usar base en memoria (`sqlite:///:memory:`) con `StaticPool` garantiza pruebas herméticas y rápidas, pero descarta la persistencia de datos reales entre ejecuciones, por lo que se recomienda un volumen mount `data/optifiber.db` para escenarios de validación contra el archivo de datos real. Finalmente, el límite de Docker en escritorio con ventana en PC es que Contenedores Linux no pueden mostrar ventanas GUI directamente en el anfitrión sin configuraciones avanzadas de X11 forwarding o XServer; la estrategia actual es ejecutar la lógica de negocio y pruebas dentro del contenedor, mientras que la interfaz CustomTkinter se inicia localmente en la PC con `python src/main.py`, reservando el servicio `pruebas` solo para el flujo de validación aislada.

---

## 4. Guion de 90 segundos (PO4)

**Resumen oral (menos de 2 minutos):**

"OptiFiber FTTH es un sistema de gestión para una empresa que vende productos de fibra óptica para el hogar. El problema operacional era que no tenían un sistema integrado para gestionar clientes, pedidos e inventario: todo era manual o disperso, lo que provocaba errores en el stock y falta de historial. El proyecto se dividió en tres PBIs: primero, la lógica de negocio con cálculo de totales y descuentos por volumen; segundo, la persistencia ORM con SQLAlchemy sobre SQLite, incluyendo relaciones 1:N y N:M con cascada; tercero, la interfaz gráfica de escritorio con CustomTkinter. Se lograron 23 pruebas passing, cubriendo dominio, persistencia y repositorios, y la aplicación tiene cinco pantallas funcionales. Como Git Master, coordiné las ramas por PBI, los pull requests con revisión de Ruff y el merge final a main con tags de entrega. **Para la exposición:** mostrarán el repositorio de GitHub, la rama `main` con los tags `pbi-02-v1.0` y `pbi-03-gui-v1.0`, y un PR ejemplar que muestre la revisión de código y los checks verdes de Ruff y pytest. Recordarán también la solicitud de cambios en PR antes del merge final."

---

**Fin del documento ENTREGABLES_PO_GITMASTER.md**