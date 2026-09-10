# Contrato inicial de eventos

Base: sección 13.3 de la propuesta, reducido al alcance de la fase 0 (un
solo proceso, sin API, A2A ni MCP todavía). El contrato completo con
streaming y SSE se activa en la fase 2 y siguientes; aquí solo se fija la
forma del evento para que ningún nodo futuro tenga que redefinirla.

## Esquema del evento

| Campo | Tipo | Obligatorio | Notas |
|---|---|---|---|
| event_id | string (uuid) | sí | |
| event_type | string | sí | ver catálogo abajo |
| claim_id | string (uuid) | sí | |
| thread_id | string (uuid) | sí | |
| run_id | string (uuid) | sí | |
| service | string | sí | en fase 0 siempre `claims-orchestrator` |
| graph_node | string | no | nombre del nodo que emitió el evento, si aplica |
| status | enum: started, completed, failed | sí | |
| safe_message | string | sí | mensaje seguro para mostrar al analista, sin prompts ni PII (P-06) |
| occurred_at | datetime | sí | |
| duration_ms | integer | no | solo cuando `status` es `completed` o `failed` |
| error_code | string | no | solo cuando `status` es `failed` |

`agent_name`, `tool_name` y `a2a_task_id` se agregan al esquema en las
fases 4 y 6, cuando existan agentes remotos y tools MCP reales. No se
declaran vacíos desde ahora para evitar un contrato con campos sin
consumidor (sección 10.5.4 del anexo de prácticas).

## Catálogo mínimo de event_type para la fase 0 y 1

| event_type | Cuándo se emite |
|---|---|
| run.started | se crea el caso y arranca el grafo |
| node.started | un nodo del grafo comienza a ejecutarse |
| node.completed | un nodo termina sin error |
| node.failed | un nodo termina con error |
| classification.completed | classify_node produjo una clasificación estructurada |
| evidence.insufficient | completeness_node determinó que falta evidencia obligatoria |
| policy.finding.recorded | policy_node registró un PolicyFinding |
| risk.assessment.recorded | risk_node registró un RiskAssessment |
| recommendation.generated | recommendation_node produjo una Recommendation |
| approval.required | approval_gate interrumpió el grafo |
| approval.recorded | se registró una decisión humana simulada (mock en fase 1) |
| run.interrupted | el grafo quedó en `awaiting_human_review` |
| run.completed | el caso llegó a un estado terminal exitoso |
| run.failed | el caso llegó a `failed` |

Este catálogo se ampliará en fases posteriores (agent.task.*, tool.call.*)
cuando existan A2A y MCP reales, siguiendo el catálogo completo de la
sección 13.3.

## Regla de uso

Todo evento debe corresponder a un hecho real del backend. Ningún mensaje
de actividad se genera para simular progreso que no ocurrió (P-06).
