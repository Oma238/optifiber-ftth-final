## Definición de Terminado (ATDD / DDD)

- [ ] El Issue describe los criterios de aceptación en Gherkin (Given/When/Then) y marca con ★ el flujo crítico.
- [ ] Los escenarios ATDD `.feature` automatizados están en verde (sin `@skip` ni `xfail`), incluidos los de flujo crítico ★.
- [ ] Los commits siguen la secuencia RED -> GREEN -> REFACTOR (una fase por commit).
- [ ] `ruff check .` sin errores y `ruff format --check .` limpio.
- [ ] Cobertura >= 70% en `src/dominio` y `src/infraestructura` (sin `src/presentacion`).
- [ ] Wireframe (`docs/wireframes/README.md`) y documentación (`docs/`) actualizados.
