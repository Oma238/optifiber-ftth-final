# OptiFiber FTTH - Instructivo de Trabajo Colaborativo N° 04

## Empresa: OPTIFER · venta de productos FTTH

## Cómo ejecutar con Docker (Anexo A2)

**Requisito:** Docker Desktop iniciado.

- **Clonar repositorio:** `git clone https://github.com/Oma238/optifiber-ftth-final.git`
- **Ejecutar pruebas aisladas en contenedor:** `docker compose --profile pruebas run --rm pruebas`
- **Ejecutar la interfaz gráfica en local:** la ventana GUI se ejecuta en la PC local con `python src/main.py` o `python -m src.main` (en Linux/Docker solo corren las pruebas; la ventana GUI debe correr en la máquina anfitriona con X11 forwarding o la consola local).
- **Detener contenedores:** `docker compose down`

### Integrantes y Roles

| Integrante | Rol principal | GitHub sugerido | Responsabilidad |
|---|---|---|---|
| **Huallpayunca Carrion Omar Sebastian** | Git Master + Product Owner / Scrum Master |  | Repositorio, ramas, PBI, revisión de PR, merges y coordinación del informe. |0.0|
| **Kevin Jesus Llerena Fernandez** | Lead Backend Engineer |  | Reglas de negocio puras en , servicios de totales/descuento/stock y capa de repositorios. |
| **Amaru Josue Ai-me Yunguri** | Database & ORM Specialist |  | ERD, modelos ORM, claves foráneas, relaciones 1:N y N:M, reglas de cascada y restricciones. |
| **Julio Cesar Diaz Tito** | DevOps & QA Engineer + Frontend/UX/UI Engineer |  | Fixture , suite pytest, Ruff, GitHub Actions, pantallas CustomTkinter, tema oscuro y evidencias del informe. |
