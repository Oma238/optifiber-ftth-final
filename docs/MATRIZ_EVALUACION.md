# Matriz de evaluación · Trabajo Colaborativo N° 04

**Empresa:** OPTIFIBER · venta de productos **FTTH**  
**Repositorio:** `Oma238/optifiber-ftth-final` · **Commit de cierre:** `4837957`  
**Rama:** `chore/cierre-rubrica-final`  
**Equipo:** Omar Huallpayunca (`Oma238`) · Julio Diaz (`drakosa1`) · Kevin Llerena (`72184510-ai`) · Amaru Ai-me (`60456113-ops`)

---

## 1. Checklist oficial del docente

| N° | Criterio de verificación | Evidencia concreta | Archivo / ubicación | Estado |
|---:|---|---|---|---|
| 1 | Gestión ágil, PBIs y trazabilidad Git/GitHub | 7 PR integrados, Issues `#2` y `#3` cerrados, PBIs 01/02/03 trazados, flujo `main`/`develop`/`feature`/`fix`/`docs`/`chore`. | `docs/INFORME_FINAL_PROYECTO.md` §1, historial Git | ✅ |
| 2 | Diseño de producto y artefactos ágiles | Product Vision Board de 6 columnas, wireframes de 5 pantallas y Peer Testing de semana 13. | `docs/vision-board.md`, `docs/wireframes/README.md`, `docs/peer-testing-week13.pdf` | ✅ |
| 3 | Arquitectura por capas y persistencia ORM | Dominio puro, infraestructura SQLAlchemy con 1:N, N:M, `UNIQUE`, `CheckConstraint`, cascadas y `RESTRICT`; presentación desacoplada. | `docs/INFORME_FINAL_PROYECTO.md` §3 | ✅ |
| 4 | Seguridad y aislamiento de la base de datos | `RUTA_DB` por variable de entorno y `:memory:` en contenedor; consultas ORM parametrizadas sin SQL crudo. | `docker-compose.yml`, `docs/INFORME_FINAL_PROYECTO.md` §3.3 | ✅ |
| 5 | Pruebas ATDD/BDD y escenarios críticos | 11 escenarios Gherkin automatizados con `pytest-bdd`, con marcador ★ en flujos críticos. | `tests/acceptance/` | ✅ |
| 6 | Calidad de código y cobertura | **45 passed**, cobertura **75.07 %** (umbral 70 %), `ruff check .` y `ruff format --check .` limpios en **38 archivos**. | `.github/workflows/ci.yml`, `docs/INFORME_FINAL_PROYECTO.md` §4.2 | ✅ |
| 7 | CI/CD y contenedorización | Workflows `CI - Calidad y Pruebas` y `Docker CI` en verde; imagen Python 3.12 + `python3-tk` y ejecución con `--profile pruebas`. | `.github/workflows/ci.yml`, `.github/workflows/docker-ci.yml`, `Dockerfile`, `docker-compose.yml` | ✅ |
| 8 | Informe final y documentación de cierre | Informe técnico completo con portada, 4 capítulos, conclusiones y recomendaciones. | `docs/INFORME_FINAL_PROYECTO.md` | ✅ |

---

## 2. Métricas reales de cierre

| Métrica | Valor verificado |
|---|---|
| Pruebas ejecutadas / aprobadas | **45 / 45** (`45 passed` en 0.60 s) |
| Cobertura total de `src/dominio` + `src/infraestructura` | **75.07 %** (377 sentencias, 94 sin cubrir; mínimo exigido 70 %) |
| `ruff check .` | `All checks passed!` |
| `ruff format --check .` | `38 files already formatted` |
| Escenarios Gherkin | **11** (8 en PBI-01, 3 en PBI-02; 4 críticos ★) |
| GitHub Actions | `CI - Calidad y Pruebas` ✅ · `Docker CI` ✅ |

---

## 3. Artefactos reales de la entrega

| Artefacto | Contenido |
|---|---|
| `docs/vision-board.md` | Visión, grupo objetivo, necesidades, producto, valor para el negocio y métricas de éxito. |
| `docs/wireframes/README.md` | Mapeo de Dashboard, Clientes, Catálogo, Pedidos y Reportes a atributos ORM reales. |
| `docs/peer-testing-week13.pdf` | Peer testing cruzado: feedback positivo de GUI y origin de los Issues `#2` y `#3`. |
| `docs/INFORME_FINAL_PROYECTO.md` | Informe final: gestión ágil, diseño, arquitectura, calidad, CI/CD y conclusiones. |
| `tests/acceptance/` | Features Gherkin y su automatización `pytest-bdd`. |
| `Dockerfile` / `docker-compose.yml` | Imagen `python:3.12-slim` con `python3-tk` y servicio `pruebas` con perfil y BD en memoria. |
| `.github/workflows/ci.yml` / `.github/workflows/docker-ci.yml` | Calidad con Ruff + pytest/cobertura y construcción/ejecución Docker. |

---

## 4. Firma de conformidad del equipo

| Integrante | Rol | Conformidad |
|---|---|---|
| Omar Sebastián Huallpayunca Carrión | Product Owner / Scrum Master & Git Master | ☐ |
| Julio Diaz | Desarrollador Backend & Persistencia ORM | ☐ |
| Kevin Llerena | Desarrollador DevOps, CI/CD & Docker | ☐ |
| Amaru Ai-me | Desarrollador Frontend GUI & QA / ATDD | ☐ |

> Completar las casillas al momento de la entrega presencial.

---

## 5. Estado final

**PBI-01, PBI-02 y PBI-03:** implementados, probados y fusionados. **CI/CD y Docker:** en verde. **Documentación de cierre:** alineada con el commit `4837957`.
