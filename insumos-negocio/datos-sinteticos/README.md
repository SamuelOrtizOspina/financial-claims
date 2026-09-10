# Datos sinteticos (insumo de negocio)

Registros concretos que instancian las clases, esquemas, politicas y
categorias definidas en el resto de `insumos-negocio/`. No contienen PII
real: todos los `customer_ref` son pseudonimos sinteticos y los montos,
comercios y fechas son ficticios en pesos colombianos (COP).

## Archivos

- `clientes.json` — 22 clientes sinteticos (`CUST-SYN-0001..0022`): alias,
  segmento, canal preferido, antiguedad.
- `transacciones.json` — 25 transacciones sinteticas (`TX-SYN-0001..0025`)
  ligadas a esos clientes: fecha, valor, comercio o beneficiario, canal, tipo.
- `evidencias.json` — 37 registros de evidencia (`EVID-SYN-0001..0037`) por
  caso, con `trust_label` (`contenido` o `instruccion_potencial`) para los
  casos de prompt injection, siguiendo el contrato de `Evidence` en
  `contratos-esquemas.md`.
- `casos.json` — 22 casos completos (`CASE-SYN-0001..0022`): el `Claim`, sus
  referencias de evidencia y, cuando aplica, `PolicyFinding`, `RiskAssessment`
  y `Recommendation` ya resueltos, mas el `expected_state_sequence` esperado
  segun `estados-transiciones.md`. Es el oraculo de referencia: la salida de
  cualquier implementacion (fase 1 en adelante) se compara contra este archivo.

## Cobertura frente a `dataset-evaluacion-especificacion.md`

Los 22 casos cubren exactamente las categorias marcadas como construibles
desde fase 0/1 en esa tabla: caso normal y politica aplicable/no aplicable
por cada una de las 4 clases, ambiguo, evidencia faltante, evidencia
contradictoria, riesgo bajo/medio/alto y prompt injection. Las categorias que
dependen de infraestructura A2A/MCP (timeout, tool no autorizada) no estan
instanciadas aqui; se agregan en las fases que las habilitan, sin modificar
este archivo.

## Convencion de uso

- Estos archivos son el conjunto semilla: se leen, no se regeneran, en las
  fases siguientes. Si una fase necesita mas casos, se agregan como nuevos
  `CASE-SYN-00XX` sin renumerar los existentes.
- `casos.json` es la unica fuente de verdad sobre que resultado espera cada
  caso; no se debe inferir el resultado esperado leyendo solo `evidencias.json`.
