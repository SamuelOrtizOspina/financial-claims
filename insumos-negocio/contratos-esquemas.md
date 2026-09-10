# Contratos de esquema (insumo de negocio)

Base: secciones 10.1 y 16.1 de la propuesta. Estos seis esquemas son el
contrato de datos que se usa en todas las fases: el grafo de la fase 1, los
especialistas A2A de las fases 4 y 5, el MCP de la fase 6 y la persistencia
durable de la fase 3 leen y escriben sobre esta misma forma. El resto de
entidades de la sección 16.1 (Approval, Execution, AgentRun) se formalizan
en las fases 3 y 7, cuando exista aprobación y persistencia durable; no se
anticipan aquí para no fijar un contrato sin consumidor.

Regla general: todo objeto que viaje por el estado del grafo debe ser
serializable, pequeño y versionable (sección 10.1). Los documentos grandes
(evidencia, política completa) se referencian por identificador, no se
incrustan.

## Claim

| Campo | Tipo | Obligatorio | Notas |
|---|---|---|---|
| claim_id | string (uuid) | sí | asignado por el sistema, nunca por el cliente |
| thread_id | string (uuid) | sí | continuidad del workflow (sección 16.2) |
| run_id | string (uuid) | sí | ejecución concreta actual |
| claim_class | enum: CLASE-01, CLASE-02, CLASE-03, CLASE-04 | sí, tras classify_node | nulo mientras el caso está en `received` |
| customer_ref | string | sí | identificador sintético y pseudonimizado, nunca PII directa |
| channel | enum: app, web, sucursal, call_center | sí | canal de recepción del reclamo |
| narrative | string | sí | relato libre del cliente, tratado como dato no confiable |
| transaction_refs | array de string | condicional | obligatorio según la clase (ver `clases-de-reclamo.md`) |
| amount | decimal | no | valor relevante del reclamo si aplica |
| currency | string | no | moneda sintética del prototipo |
| submitted_at | datetime | sí | fecha de creación del caso |
| status | enum de `estados-transiciones.md` | sí | estado de negocio actual |
| case_version | integer | sí | se incrementa en cada mutación relevante (sección 15.5) |

## Evidence

| Campo | Tipo | Obligatorio | Notas |
|---|---|---|---|
| evidence_id | string (uuid) | sí | |
| claim_id | string (uuid) | sí | |
| evidence_type | enum: documento, imagen, comprobante, relato, comunicacion | sí | |
| source | enum: cliente, sistema, proveedor | sí | de dónde llegó la evidencia |
| reliability_status | enum: confiable, no_confiable, sin_verificar | sí | nunca se convierte "sin_verificar" en "confiable" por defecto (FR-03) |
| trust_label | enum: contenido, instruccion_potencial | sí | todo texto libre de un adjunto se etiqueta como contenido, nunca como instrucción del sistema (sección 10.3, CU-04) |
| content_hash | string | sí | hash del contenido para detectar alteración (sección 17.2, data poisoning) |
| received_at | datetime | sí | |
| description | string | no | resumen corto, sin datos sensibles innecesarios |

## PolicyFinding

| Campo | Tipo | Obligatorio | Notas |
|---|---|---|---|
| finding_id | string (uuid) | sí | |
| claim_id | string (uuid) | sí | |
| policy_id | string | sí | ejemplo: `POLICY-2026-004` |
| policy_version | string | sí | ejemplo: `v2` |
| citations | array de string | sí | referencia a sección o cláusula exacta; no puede quedar vacío (FR-04) |
| rule_summary | string | sí | interpretación de la regla aplicable |
| conditions_met | array de string | sí | puede ser vacío si ninguna se confirmó |
| conditions_unconfirmed | array de string | sí | condiciones que no se pudieron verificar con la evidencia actual |
| applicability | enum: aplica, no_aplica, parcial | sí | permite representar el caso de "política no aplicable" (sección 19.1) |
| confidence | decimal (0 a 1) | sí | |
| created_at | datetime | sí | |

## RiskAssessment

| Campo | Tipo | Obligatorio | Notas |
|---|---|---|---|
| assessment_id | string (uuid) | sí | |
| claim_id | string (uuid) | sí | |
| signal | string | sí | señal observada, no interpretación |
| interpretation | string | sí | separado del dato observado (FR-05) |
| severity | enum: baja, media, alta | sí | |
| evidence_refs | array de evidence_id | sí | toda severidad media o alta debe tener al menos una referencia |
| recommended_action | string | sí | |
| uncertainty | string | no | razones de incertidumbre si existen |
| created_at | datetime | sí | |

## Recommendation

| Campo | Tipo | Obligatorio | Notas |
|---|---|---|---|
| recommendation_id | string (uuid) | sí | |
| claim_id | string (uuid) | sí | |
| outcome | enum: aprobar, solicitar_evidencia, rechazar, escalar_fraude, escalar_supervisor, mantener_pendiente | sí | FR-06 |
| reasons | array de string | sí | no puede estar vacío |
| policy_finding_refs | array de finding_id | sí | puede ser vacío solo si outcome es `mantener_pendiente` o `solicitar_evidencia` |
| risk_assessment_ref | assessment_id | no | obligatorio si existe al menos una señal de severidad media o alta |
| confidence | decimal (0 a 1) | sí | |
| case_version | integer | sí | versión del caso en el momento de generar la recomendación (sección 16.3) |
| created_at | datetime | sí | |

## AuditEvent

| Campo | Tipo | Obligatorio | Notas |
|---|---|---|---|
| event_id | string (uuid) | sí | |
| claim_id | string (uuid) | sí | |
| thread_id | string (uuid) | sí | |
| run_id | string (uuid) | sí | |
| event_type | string | sí | catálogo inicial en `contrato-eventos.md` |
| actor | string | sí | nodo, agente o identidad humana que produjo el evento |
| payload_ref | string | no | referencia a un objeto grande, no el objeto embebido |
| occurred_at | datetime | sí | |
| immutable | boolean | sí | siempre `true`; un AuditEvent nunca se edita ni se borra |

## Regla de validación transversal

Ningún nodo puede escribir un objeto que no cumpla su esquema. Una salida de
modelo que no valide contra estos esquemas se trata como error de salida
inválida (FR-12), no como un valor por defecto silencioso.
