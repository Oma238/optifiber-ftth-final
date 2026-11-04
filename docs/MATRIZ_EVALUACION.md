# Matriz de evaluación · Trabajo Colaborativo N° 04

**Empresa:** OPTIFIBER · venta de productos FTWH
**PBI:** PBI-02 · Persistencia de clientes, pedidos y catálogo FTTH + PBI-03 · Interfaz gráfica de escritorio
**Rama:** main
**Equipo:** Omar Huallpayunta · Kevin Llerena · Amaru Ai-me · Julio Diaz

## 1. Checklist oficial del docente

| N° | Criterio de verificación | Evidencia concreta | Archivo / ubicación | Estado |
|---:|---|---|---|---|
| 1 | **Modelo ERD e infraestructura ORM:** esquema relacional en la Sección 4.1 y código funcional de los modelos. | 6 entidades, 5 relaciones, claves y restricciones; 21 pruebas. | `docs/erd_optifiber.png`, `docs/INFORME_CAPITULO_4.md` §4.1, `src/infraestructura/modelos.py` | ✅ |
| 2 | **Fixture de base de datos en memoria:** configuración aislada para pruebas herméticas. | `create_engine("sqlite:///:memory:")`, `StaticPool`, `PRAGMA foreign_keys=ON`, `scope="function"`. | `tests/conftest.py` | ✅ |
| 3 | **Pruebas de persistencia:** relación 1:N y eliminación en cascada en verde. | `21 passed`; casos 1:N, cascada, N:M y repositorios. | `tests/`, `docs/evidencias/pytest_final.txt` | ✅ |
| 4 | **Historial de commits Git:** secuencia RED → GREEN → REFACTOR en la rama del PBI. | 13 commits con autores del equipo, incluyendo 5 ciclos RED/GREEN. | `git log --graph`, `docs/evidencias/commits.md` | ✅ |
| 5 | **Pull Request y GitHub Actions:** checks de Ruff y pytest en verde, SQLAlchemy en requirements. | Workflow `ci.yml`; PR #2; merge `329b4ea`; tag `pbi-02-v1.0`; `SQLAlchemy` en `requirements.txt`. | `.github/workflows/ci.yml`, `requirements.txt`, `docs/GUIA_GIT_Y_ENTREGA.md` | ✅ |
| 6 | **Capítulo 4 del Informe completo:** secciones 4.1, 4.2 y 4.3 completas. | Este documento + `docs/Informe_Capitulo_4_OptiFiber.docx` | `docs/INFORME_CAPITULO_4.md`, `docs/Informe_Capitulo_4_OptiFiber.docx` | ✅ |

---

## 2. Cobertura de pruebas

| Tipo | Archivo | Pruebas | Estado |
|---|---|:---:|---|
| Persistencia ORM | `tests/test_persistencia_orm.py` | 5 | ✅ |
| Dominio puro | `tests/test_dominio.py` | 10 | ✅ |
| Repositorios | `tests/test_repositorios.py` | 6 | ✅ |
| **Total** | — | **21** | ✅ |

---

## 3. Commits y autores

| Integrante | Commits | Rol |
|---|:---:|---|
| Omar Huallpayunta | `cc4e5e7`, documentación, merge | Git Master + PO/SM |
| Kevin Llerena | `0bf652a`, `4f6d01c`, `27071a2` | Lead Backend |
| Amaru Ai-me | `c368e49`, `72e423d`, `df33bcd` | Database & ORM |
| Julio Diaz | `c394468`, `b292e8c`, `33febea`, `e397f22`, `417ed0f`, `9268085` | DevOps & QA + Frontend |

---

## 4. Evidencias de ejecución

| Comando | Resultado | Archivo |
|---|---|---|
| `python -m pytest -v` | `23 passed` | `docs/evidencias/pytest_final.txt` |
| `python -m ruff check .` | `All checks passed!` | `docs/evidencias/ruff_final.txt` |
| `python -m src.main --demo` | Catálogo, pedido con descuento y cascada verificada | `docs/evidencias/demo_final.txt` |

---

## 5. Firma de conformidad del equipo

| Integrante | Rol | Conformidad |
|---|---|---|
| Omar Huallpayunta | Git Master + PO/SM | ☐ |
| Kevin Llerena | Lead Backend Engineer | ☐ |
| Amaru Ai-me | Database & ORM Specialist | ☐ |
| Julio Diaz | DevOps & QA + Frontend/UX | ☐ |

> Completar las casillas al momento de la entrega. La matriz resume las evidencias que se revisarán en mesa.

---

## 6. Distribución porcentual y evidencias de participación

| Integrante | % de aporte | Evidencia principal |
|---|---:|---|
| Omar Huallpayunta | 25 % | Estructura, PBI, revisión, merge, DOCX |
| Kevin Llerena | 25 % | Dominio y repositorios (3 commits) |
| Amaru Ai-me | 25 % | ERD y modelos ORM (3 commits) |
| Julio Diaz | 25 % | Fixture, pruebas, CI, CLI y evidencias (6 commits) |

La distribución es equivalente porque cada integrante lidera una capa del proyecto y participa en la revisión de las demás. Los commits tienen autoría explícita y los archivos modificados permiten verificar el aporte.

---

## 7. Guion breve para la exposición

| Pregunta probable | Quién responde | Idea clave |
|---|---|---|
| ¿Cuál es el PBI y qué problema resuelve? | Omar | Registrar clientes, pedidos y catálogo FTTH con historial y control de stock. |
| ¿Por qué elegiste esas entidades? | Amaru | Reflejan el flujo real: cliente → pedido → detalle → producto → categoría/etiqueta. |
| ¿Dónde está la relación N:M? | Amaru | `Producto` N:M `Etiqueta` con `producto_etiqueta`; `DetallePedido` resuelve Pedido–Producto con datos extra. |
| ¿Cómo funciona la cascada? | Amaru | `cascade="all, delete-orphan"` en Cliente→Pedido y Pedido→Detalle; al borrar el cliente desaparecen sus pedidos y detalles. |
| ¿Dónde está la lógica de negocio? | Kevin | En `src/dominio/servicios.py`, sin SQLAlchemy; los repositorios solo persisten. |
| ¿Cómo se calcula el total? | Kevin | Subtotal por línea con Decimal, suma y descuento del 5 % desde S/ 1 500. |
| ¿Cómo garantizan pruebas herméticas? | Julio | Fixture `db_session` con `sqlite:///:memory:` y una sesión nueva por prueba. |
| ¿Cómo se ejecuta la calidad? | Julio | `ruff check .` y `pytest -v` localmente y en GitHub Actions. |
| ¿Qué evidencia hay del TDD? | Omar | Secuencia de commits RED → GREEN → REFACTOR en la rama del PBI. |

---

## 8. Estado del PBI

**PBI-02:** implementado, probado y aprobado. Rama `feature/PBI-02-orm-persistencia` fusionada a `main` mediante el merge **`329b4ea`** (PR #2) y tag **`pbi-02-v1.0`**. Pipeline esperado: `ruff check .` y `pytest -v` en verde.

**PBI-03:** implementado y probado en la rama `feature/PBI-03-interfaz-grafica` (commits `37b0a15` y `f2bf169`). La aplicación de escritorio abre con `python -m src.main`, cubre las cinco pantallas y mantiene la CLI. Suite final: **23 passed**; Ruff: **All checks passed!** El merge a `main` y el tag **`pbi-03-gui-v1.0`** se registran al cierre de la entrega.
