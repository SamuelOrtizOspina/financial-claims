# Estados de negocio y transiciones permitidas

Base: sección 10.2 de la propuesta, con la tabla de transiciones que exige
el principio P-01: el estado no se infiere del último mensaje del modelo,
se calcula por reglas explícitas.

## Estados

| Estado | Significado |
|---|---|
| received | el caso fue creado y todavía no se procesó |
| classifying | el especialista de intake está normalizando y clasificando el relato |
| awaiting_information | falta evidencia obligatoria o la clasificación no tiene confianza suficiente |
| investigating | política y riesgo están analizando el caso |
| awaiting_human_review | el grafo se interrumpió; requiere una decisión humana |
| approved | el analista aprobó la recomendación |
| rejected | el analista rechazó la recomendación |
| escalated | el caso salió del flujo automático hacia un supervisor o fraude |
| executing | la acción aprobada se está ejecutando de forma simulada |
| resolved | el caso terminó con una acción registrada o una resolución final |
| failed | un error no recuperable detuvo el caso |

`resolved`, `rejected` y `failed` son estados terminales del prototipo.
`escalated` es terminal para el flujo automático: un supervisor lo retoma
por fuera del grafo estándar.

## Tabla de transiciones permitidas

| Desde | Hacia | Disparador |
|---|---|---|
| received | classifying | intake_node valida la solicitud |
| classifying | awaiting_information | completeness_node detecta evidencia obligatoria faltante o confianza de clasificación baja |
| classifying | investigating | completeness_node confirma evidencia obligatoria y confianza aceptable |
| awaiting_information | classifying | el cliente o el analista aporta el dato o evidencia faltante y se reclasifica |
| investigating | awaiting_human_review | policy_node o risk_node detectan alto riesgo, conflicto entre política y hechos, confianza baja, instrucción sospechosa en evidencia, o se va a ejecutar una tool de escritura (FR-07) |
| investigating | escalated | risk_node detecta una señal que la política del prototipo define como excepción de escalamiento inmediato |
| awaiting_human_review | approved | el analista aprueba la recomendación (FR-08) |
| awaiting_human_review | rejected | el analista rechaza la recomendación |
| awaiting_human_review | awaiting_information | el analista solicita más evidencia antes de decidir |
| awaiting_human_review | escalated | el analista escala el caso a un supervisor |
| approved | executing | action_node prepara y ejecuta solo la acción aprobada |
| executing | resolved | audit_node persiste el resultado y emite el evento final |
| executing | failed | la acción simulada falla de forma no recuperable |
| cualquier estado operativo (received, classifying, awaiting_information, investigating, awaiting_human_review, executing) | failed | error permanente no clasificado como transitorio (FR-12) |

No existen transiciones fuera de esta tabla. Un nodo que intente producir un
estado no listado debe fallar de forma visible en la fase 1, no quedar en un
estado ambiguo.

## Reglas de consistencia

- Toda transición debe registrar un AuditEvent con el estado anterior, el
  estado nuevo y el actor o nodo que la causó.
- `case_version` (ver `contratos-esquemas.md`) se incrementa en cada
  transición. Una mutación que llega con una versión desactualizada se
  rechaza (sección 15.5, CU-06).
- Ninguna transición hacia `approved` o `executing` puede depender
  únicamente de un mensaje del modelo; requiere el evento de decisión
  humana definido en FR-08.
