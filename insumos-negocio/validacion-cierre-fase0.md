# Validacion de cierre — insumos de negocio listos para fase 1

Este documento verifica que cada estado y cada transicion permitida de
`estados-transiciones.md` tiene al menos un caso que lo ejercita en
`datos-sinteticos/casos.json`, o deja constancia explicita de por que no,
en linea con el criterio de cierre de la seccion 24 de la propuesta
("crear un expediente sintetico valido y validar que cada estado y cada
transicion de la maquina de estados este definido").

## Caso principal de demostracion

`CASE-SYN-0001` recorre el camino feliz completo:
`received -> classifying -> investigating -> awaiting_human_review ->
approved -> executing -> resolved`. Sirve como el "expediente sintetico
valido" de referencia para la primera implementacion del grafo en fase 1.

## Cobertura de transiciones

| Transicion | Caso(s) que la ejercitan |
|---|---|
| received -> classifying | todos los casos, p. ej. CASE-SYN-0001 |
| classifying -> awaiting_information | CASE-SYN-0008 (primer paso), CASE-SYN-0016, CASE-SYN-0018, CASE-SYN-0019 |
| classifying -> investigating | CASE-SYN-0001 |
| awaiting_information -> classifying | CASE-SYN-0008 (reclasificacion tras recibir el segundo comprobante) |
| investigating -> awaiting_human_review | CASE-SYN-0001 y la mayoria de los casos con `policy_finding` |
| investigating -> escalated (escalamiento inmediato por senal de excepcion) | **no cubierta** — ver nota abajo |
| awaiting_human_review -> approved | CASE-SYN-0001 |
| awaiting_human_review -> rejected | CASE-SYN-0002, CASE-SYN-0007, CASE-SYN-0011 |
| awaiting_human_review -> awaiting_information | CASE-SYN-0012, CASE-SYN-0020 |
| awaiting_human_review -> escalated | CASE-SYN-0003, CASE-SYN-0004 |
| approved -> executing | CASE-SYN-0001 |
| executing -> resolved | CASE-SYN-0001 |
| executing -> failed | **no cubierta**, diferida |
| cualquier estado operativo -> failed | **no cubierta**, diferida |

## Transiciones y estados deliberadamente no cubiertos

- **`investigating -> escalated` (excepcion de escalamiento inmediato sin
  paso por revision humana):** no existe un caso que la modele porque el
  prototipo aun no fija cuales senales cuentan como "excepcion de
  escalamiento inmediato" (esa regla de politica se define al construir
  risk_node en fase 1/4). Los casos de riesgo alto de este dataset
  (CASE-SYN-0003, CASE-SYN-0004) pasan primero por `awaiting_human_review`,
  que es el camino seguro por defecto. Cuando fase 1 o fase 4 definan la
  regla de excepcion, agregar un caso nuevo sin modificar los existentes.
- **`executing -> failed` y `cualquier estado operativo -> failed`:** el
  estado `executing` no tiene una implementacion real hasta la fase 7
  (ejecucion real via MCP); en fase 0 no hay una accion que pueda fallar
  de forma no recuperable. Instanciar estos casos ahora obligaria a
  inventar un modo de fallo sin sistema real detras, lo que iria contra
  el principio de no fijar diseño sin evidencia (ver `threat-model-inicial.md`,
  control "DoS por loop" y su control diferido). Se cubren cuando la fase
  correspondiente exista.

## Conclusion

Con `casos.json`, `clientes.json`, `transacciones.json` y `evidencias.json`
completos, los insumos de negocio del sistema quedan cerrados: cubren el
camino feliz completo, las 4 clases de reclamo con politica aplicable y no
aplicable, ambiguedad, evidencia faltante y contradictoria, los tres niveles
de riesgo y los dos casos de prompt injection exigidos por
`dataset-evaluacion-especificacion.md`. Las unicas brechas pendientes
(escalamiento inmediato, `failed`) dependen de decisiones de diseño que
corresponden a fases posteriores y quedan documentadas, no resueltas por
adelantado.
