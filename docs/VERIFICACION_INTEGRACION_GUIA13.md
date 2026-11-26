# Verificación de Integración GUI – Capa de Servicio (Guía N° 13)

- **Responsable:** Kevin Jesus Llerena Fernandez (`@72184510-ai`)
- **Rol en la sesión:** Integrante 3 — Integración (Lead Backend Engineer)
- **Fecha:** 25 de noviembre de 2026

## 1. Conexión GUI con Capa de Dominio y Servicio
- **Pantalla evaluada:** `PantallaPedidos` (`src/presentacion/gui/pantallas/pedidos.py`)
- **Funciones de dominio invocadas en vivo:**
  - `calcular_subtotal(cantidad, precio)` (`src/dominio/servicios.py`)
  - `calcular_descuento(subtotal)` (`src/dominio/servicios.py`)
  - `calcular_total_pedido(lineas)` (`src/dominio/servicios.py`)
- **Servicio de aplicación / persistencia invocado al confirmar:**
  - `self.app.pedidos.crear_pedido(cliente_documento, items)` (`src/infraestructura/repositorios.py`), validando stock disponible, calculando totales y persistiendo en `optifiber.db` vía SQLAlchemy.

## 2. Validación Automatizada Previa al PR
- `python -m pytest -v`: **34 passed**
- `python -m ruff check .`: **All checks passed!**