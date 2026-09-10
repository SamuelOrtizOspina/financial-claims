# Índice de políticas sintéticas

| policy_id | Clase de reclamo | Versión vigente | Archivo |
|---|---|---|---|
| POLICY-2026-001 | CLASE-01: transacción no reconocida | v2 | `POLICY-2026-001-transaccion-no-reconocida.md` |
| POLICY-2026-002 | CLASE-02: transacción duplicada | v1 | `POLICY-2026-002-transaccion-duplicada.md` |
| POLICY-2026-003 | CLASE-03: diferencia de valor | v1 | `POLICY-2026-003-diferencia-de-valor.md` |
| POLICY-2026-004 | CLASE-04: producto no recibido | v1 | `POLICY-2026-004-producto-no-recibido.md` |

## Notas de uso para `claims-policy-agent` (fase 5 en adelante)

- Cada política tiene secciones numeradas (`3.1`, `3.4`, `6.2`, etc.) para
  que las citas del esquema `PolicyFinding` (`citations`) sean exactas y
  verificables, no un resumen libre.
- `POLICY-2026-001` tiene dos versiones (v1 y v2) a propósito, para que el
  equipo pueda probar la regla de versionamiento de la sección 16.3: el
  especialista debe citar la versión vigente en la fecha de la
  transacción, no en la fecha de creación del caso.
- Cada política incluye al menos una condición de "no aplica" (secciones
  3.3 o 3.4 según el documento). Esas condiciones son la base para los
  casos de "política no aplicable" que exige el dataset de evaluación
  (`dataset-evaluacion-especificacion.md`, sección 19.1 de la propuesta).
- Ninguna política habilita una acción financiera real. El resultado
  esperado (sección 6 de cada política) siempre se traduce en una
  recomendación (FR-06), nunca en una ejecución directa.
