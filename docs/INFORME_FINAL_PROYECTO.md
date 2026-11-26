# Informe Final de Proyecto · OptiFiber FTTH

**Trabajo Colaborativo N° 04 — Construcción de Software**  
**Repositorio:** `Oma238/optifiber-ftth-final` · **Commit de cierre:** `4837957`  
**Rama de cierre:** `chore/cierre-rubrica-final` · **Estado:** CI y Docker CI en verde

---

## Portada y equipo

| Integrante | Usuario GitHub | Rol asignado | Responsabilidad principal |
|---|---|---|---|
| Omar Sebastián Huallpayunca Carrión | `Oma238` | Product Owner / Scrum Master & Git Master | Visión del producto, PBIs, PB y gobernanza de ramas, PR y cierre. |
| Julio Diaz | `drakosa1` | Desarrollador Backend & Persistencia ORM | Servicios de dominio, modelos SQLAlchemy, repositorios y fixture de pruebas. |
| Kevin Llerena | `72184510-ai` | Desarrollador DevOps, CI/CD & Docker | GitHub Actions, contenedorización y protección de `main`. |
| Amaru Ai-me | `60456113-ops` | Desarrollador Frontend GUI & QA / ATDD | Pantallas CustomTkinter, escenarios Gherkin y verificación de calidad. |

---

## Capítulo 1 — Gestión Ágil, PBIs y Trazabilidad en Git/GitHub

### 1.1 Flujo Gitflow simplificado

El equipo adoptó un flujo ramificado ligero con integración continua:

- `main`: rama protegida; solo recibe merges mediante Pull Request y exige los checks de GitHub Actions en verde.
- `develop`: rama de integración de los PBIs terminados antes del pase a `main`.
- `feature/*`: PBIs en desarrollo (`feature/PBI-03-gui-integracion`).
- `fix/*`: correcciones de UX y validación (`fix/mejora-ux-alerta-campos`, `fix/mejora-gui-alerta-numerica`).
- `docs/*`: documentación del Product Owner (`docs/po-readme-entregables`).
- `chore/*`: cierre de rúbrica y alineación final (`chore/cierre-rubrica-final`).

El historial incluye los merges de PR `#4` (`bafa5dc`), PR `#5` (`00576fe`) y PR `#6` (`6d641a2`), además de los commits de cierre `ffce13f`, `c1dc624`, `11686ed` y `4837957`.

### 1.2 Pull Requests e Issues

Se integraron **7 Pull Requests (PR #1 a PR #7)** siguiendo la secuencia RED → GREEN → REFACTOR y con revisión antes del merge a `develop`/`main`. Los issues de calidad surgidos del Peer Testing cruzado se cerraron con evidencia en el historial:

- **Issue #2** — validación de campos obligatorios en el registro de clientes: commit `0ba95ac` (`fix: validar campos obligatorios y mostrar alerta visual en clientes (closes #2)`), integrado en PR `#4`.
- **Issue #3** — validación numérica de cantidades y precios: commit `d1d01d6` (`fix: validar entradas numéricas y mostrar mensaje claro ante datos invalidos (closes #3)`), integrado en PR `#5`.

### 1.3 Trazabilidad de los PBIs

| PBI | Objetivo | Evidencia de cierre |
|---|---|---|
| **PBI-01 — Cotización FTTH** | Calcular subtotales y totales con descuento por volumen desde **S/ 1500** y validar stock y documento. La regla implementada en `src/dominio/servicios.py` aplica **5 %** (`PORCENTAJE_DESCUENTO = Decimal("0.05")`) sobre el total que alcanza el umbral. | `tests/acceptance/features/pbi01_cotizacion_ftth.feature`, `tests/test_dominio.py`. |
| **PBI-02 — Persistencia ORM y catálogo N:M** | Modelar 6 entidades, relaciones 1:N, N:M entre Producto y Etiqueta, cascadas, restricciones y repositorios parametrizados. | `tests/acceptance/features/pbi02_persistencia_orm.feature`, `tests/test_persistencia_orm.py`, `tests/test_repositorios.py`. |
| **PBI-03 — Interfaz gráfica y reportes** | Cinco pantallas CustomTkinter (Dashboard, Clientes, Catálogo, Pedidos, Reportes), tema oscuro, validaciones y CLI de respaldo. | `src/presentacion/gui/app.py`, `src/presentacion/gui/pantallas/`, `src/presentacion/cli.py`, `tests/test_gui_clientes.py`, `tests/test_gui_numerico.py`. |

> **Nota de verificación:** el porcentaje de descuento vigente en el código es 5 %, no 8 %. Los escenarios de aceptación (por ejemplo, 2 × S/ 100 + 4 × S/ 400 = S/ 1800 → descuento S/ 90 → total S/ 1710) confirman ese valor.

---

## Capítulo 2 — Diseño de Producto y Artefactos Ágiles

### 2.1 Product Vision Board

`docs/vision-board.md` resume el producto en seis columnas: **Visión, Grupo objetivo, Necesidades, Producto, Valor para el negocio y Métricas de éxito**. La visión es gestionar cotizaciones, catálogo, pedidos y reportes FTTH en una herramienta confiable; las métricas exigidas son 100 % de pruebas en verde y cobertura ≥ 70 % en dominio e infraestructura.

### 2.2 Wireframes funcionales

`docs/wireframes/README.md` mapea las cinco pantallas a atributos reales de `src/infraestructura/modelos.py`:

| Pantalla | Atributos representativos |
|---|---|
| Dashboard | `PedidoModel.id`, `PedidoModel.fecha`, `PedidoModel.estado`, `PedidoModel.total`, `DetallePedidoModel.subtotal`. |
| Clientes | `ClienteModel.id`, `ClienteModel.nombre`, `ClienteModel.documento`, `ClienteModel.telefono`, `ClienteModel.email`, `ClienteModel.direccion`, `ClienteModel.creado_en`. |
| Catálogo | `ProductoModel.sku`, `ProductoModel.nombre`, `ProductoModel.precio`, `ProductoModel.stock`, `ProductoModel.activo`, `CategoriaModel.nombre`, `EtiquetaModel.nombre`, `producto_etiqueta`. |
| Pedidos | `PedidoModel.estado`, `PedidoModel.total`, `PedidoModel.cliente_id`, `DetallePedidoModel.producto_id`, `DetallePedidoModel.cantidad`, `DetallePedidoModel.precio_unitario`, `DetallePedidoModel.subtotal`. |
| Reportes | `PedidoModel.fecha`, `PedidoModel.total`, `DetallePedidoModel.cantidad`, `DetallePedidoModel.subtotal`, `ProductoModel.categoria_id`, `ProductoModel.nombre`. |

### 2.3 Peer Testing cruzado — Semana 13

`docs/peer-testing-week13.pdf` registra la evaluación cruzada del equipo anfitrión OptiFiber FTTH:

- **Aspecto positivo:** interfaz minimalista y moderna con CustomTkinter en tema oscuro.
- **Mejora 1:** validar visualmente los campos vacíos al registrar clientes → Issue `#2` / PR `#4`.
- **Mejora 2:** manejar valores no numéricos en cantidades y precios sin congelar la aplicación → Issue `#3` / PR `#5`.
- **Calidad observada:** 29 pruebas aprobadas y linter Ruff en verde al momento de la sesión; cifra posteriormente superada por la suite final de 45 pruebas.

---

## Capítulo 3 — Arquitectura por Capas, Persistencia ORM y Seguridad

### 3.1 Separación estricta de capas

- **`src/dominio/servicios.py`**: lógica de negocio pura. Sus únicos imports son `annotations`, `collections.abc.Iterable` y `decimal`; no conoce SQLAlchemy ni la base de datos. Implementa `calcular_subtotal`, `calcular_descuento`, `calcular_total_pedido`, `validar_stock`, `validar_documento` y `validar_cantidad`, con redondeo `ROUND_HALF_UP` y `ErrorDominio` para reglas incumplidas.
- **`src/infraestructura/`**: `modelos.py` (mapeo ORM), `db.py` (engine y sesiones), `repositorios.py` (consultas) y `seed.py` (datos demo).
- **`src/presentacion/`**: `cli.py`, `gui/app.py` y `gui/pantallas/` consumen el dominio y los repositorios; la GUI no contiene reglas de negocio.

### 3.2 Modelo de datos e integridad

`src/infraestructura/modelos.py` declara seis entidades: `ClienteModel`, `CategoriaModel`, `EtiquetaModel`, `ProductoModel`, `PedidoModel` y `DetallePedidoModel`.

- **1:N:** `ClienteModel.pedidos` (`cascade="all, delete-orphan"`) y `PedidoModel.detalles` (`cascade="all, delete-orphan"`).
- **N:M:** tabla asociativa `producto_etiqueta` con `ForeignKey(... ondelete="CASCADE")` y relaciones `secondary=` en Producto y Etiqueta; `DetallePedidoModel` resuelve Pedido–Producto con atributos propios.
- **UNIQUE:** `ClienteModel.documento`, `CategoriaModel.nombre`, `EtiquetaModel.nombre`, `ProductoModel.sku` y `UniqueConstraint("pedido_id", "producto_id")`.
- **CheckConstraint:** `precio >= 0`, `stock >= 0`, `total >= 0`, `cantidad > 0`, `precio_unitario >= 0`, `subtotal >= 0`.
- **Integridad referencial:** `CASCADE` en cliente→pedido, pedido→detalle y tabla asociativa; `RESTRICT` en producto→categoría y detalle→producto.

### 3.3 Aislamiento y seguridad de consultas

- `src/infraestructura/db.py` obtiene la ruta de la base de datos desde `os.environ["RUTA_DB"]` (`:16`), con valor por defecto `data/optifiber.db`; el valor `:memory:` produce `sqlite:///:memory:` (`:18`) y `crear_engine` activa `PRAGMA foreign_keys=ON`.
- `docker-compose.yml` fija `RUTA_DB: ":memory:"` para el servicio de pruebas, de modo que la base real nunca se toca.
- `tests/conftest.py` usa `create_engine("sqlite:///:memory:")`, `StaticPool`, `scope="function"` y cierra la sesión en `finally`.
- `src/infraestructura/repositorios.py` construye consultas con `select()`, `where()` y parámetros enlazados por SQLAlchemy. No hay SQL crudo, `text()` ni interpolación de cadenas (`grep` de `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `.format(` → 0 coincidencias).

---

## Capítulo 4 — Calidad de Software, ATDD/BDD, CI/CD y Contenedorización

### 4.1 Escenarios de aceptación

`tests/acceptance/features/` contiene dos archivos Gherkin no vacíos y automatizados con `pytest-bdd` en `tests/acceptance/test_acceptance.py`:

- `pbi01_cotizacion_ftth.feature`: 8 escenarios de subtotal, umbral con/sin descuento, total del pedido, documento DNI/RUC y stock; ★ en total con descuento, documento inválido y stock insuficiente.
- `pbi02_persistencia_orm.feature`: 3 escenarios de cascada Cliente→Pedido→Detalle, relación N:M y restricción de integridad; ★ en el escenario de cascada.

Total: **11 escenarios Gherkin**, los 11 automatizados y aprobados.

### 4.2 Ejecución y métricas

| Verificación | Resultado |
|---|---|
| Suite completa | **45 pruebas recopiladas y 45 aprobadas** en 0.60 s (`45 passed`). |
| Cobertura | **75.07 % TOTAL** (377 sentencias, 94 no cubiertas) con `--cov=src/dominio --cov=src/infraestructura --cov-fail-under=70`. |
| Cobertura por módulo | `servicios.py` 94 %, `modelos.py` 92 %, `repositorios.py` 61 %, `db.py` 50 %, `seed.py` 96 %. |
| Ruff | `ruff check .` → `All checks passed!`; `ruff format --check .` → **38 archivos ya formateados**. |
| Dependencias | `pytest-bdd>=9.0,<10.0` y `pytest-cov>=5.0,<8.0` en `requirements.txt`. |

### 4.3 Automatización y contenedores

- `.github/workflows/ci.yml`: en push y pull_request hacia `main` y `develop` instala `python3-tk`, las dependencias, ejecuta `ruff check .`, `ruff format --check .` y `pytest --cov=src/dominio --cov=src/infraestructura --cov-report=term-missing --cov-fail-under=70`.
- `.github/workflows/docker-ci.yml`: en pull_request y push hacia `main` construye la imagen con `docker compose --profile pruebas build` y ejecuta `docker compose --profile pruebas run --rm pruebas`.
- `Dockerfile`: `python:3.12-slim` + `python3-tk`, `pip install --no-cache-dir -r requirements.txt`, CMD con cobertura.
- `docker-compose.yml`: servicio `pruebas`, `profiles: ["pruebas"]`, `RUTA_DB=":memory:"`.
- `.github/pull_request_template.md`: checklist de Definición de Terminado con Gherkin en el Issue, escenarios ★ en verde, RED → GREEN → REFACTOR, Ruff limpio, cobertura ≥ 70 % sin `src/presentacion`, wireframe y documentación actualizados.
- Protección de `main`: integración exclusiva vía PR con los dos workflows en verde.

---

## Conclusiones y recomendaciones técnicas

El cierre `4837957` cumple la rúbrica: arquitectura por capas, ORM con integridad referencial, aislamiento de base de datos, ATDD/BDD con escenarios críticos, 45 pruebas en verde, 75.07 % de cobertura, Ruff limpio en 38 archivos y CI/Docker automatizados.

Recomendaciones para iteraciones posteriores:

1. Elevar la cobertura de `db.py` (50 %) y `repositorios.py` (61 %) con pruebas de engine y casos de repositorio aún no ejercitados.
2. Normalizar la cifra de descuento documentada: el código implementa 5 % desde S/ 1500; cualquier cambio a 8 % debe realizarse primero en `src/dominio/servicios.py` y en los `.feature`.
3. Mantener el aislamiento de la base de datos mediante `RUTA_DB=":memory:"` en todo entorno de pruebas.
4. Preservar la secuencia RED → GREEN → REFACTOR y el checklist del PR template en cada nuevo PBI.
