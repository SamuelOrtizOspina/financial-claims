# Planeación semana a semana del prototipo

**Base:** PROPUESTA_SIDEPROJECT_RECLAMOS_FINANCIEROS.md, sección 23 (fases 0 a 8).
**Supuesto de capacidad:** una persona, dedicación parcial, entre 8 y 10 horas por semana.
**Duración total estimada:** 18 semanas (aproximadamente 4.5 meses).

Esta duración es una estimación de planeación, no un compromiso fijo. Cada
fase cierra solo cuando cumple la evidencia mínima definida en la sección
24.2 del documento base. Si una semana no alcanza para cerrar su
demostración, la fase se extiende antes de avanzar a la siguiente.

La fase 0 (contratos y dominio mínimo) ya está cerrada: quedó resuelta como
los insumos de negocio en `changemakers/insumos-negocio/` (clases de
reclamo, esquemas, estados y transiciones, contrato de eventos, threat
model inicial, políticas sintéticas y el dataset sintético con su oráculo
en `insumos-negocio/datos-sinteticos/`). Ver
`insumos-negocio/validacion-cierre-fase0.md` para el detalle de cierre. Por
eso esta planeación arranca directamente en la fase 1.

---

## Resumen de asignación

| Fase | Semanas | Rango |
|---|---|---|
| 0. Contratos y dominio mínimo | — | cerrada (ver `insumos-negocio/`) |
| 1. Grafo LangGraph en un solo proceso | 2 | S1 a S2 |
| 2. API y Streamlit separados | 2 | S3 a S4 |
| 3. Orquestador separado, persistencia y memoria | 3 | S5 a S7 |
| 4. Primer especialista por A2A | 2 | S8 a S9 |
| 5. Especialización A2A completa | 2 | S10 a S11 |
| 6. MCP de dominio, solo lectura | 2 | S12 a S13 |
| 7. Human-in-the-loop y efectos simulados | 2 | S14 a S15 |
| 8. Endurecimiento del prototipo local | 3 | S16 a S18 |

---

## Fase 1: Grafo LangGraph en un solo proceso (S1 a S2)

**Semana 1**

- Implementar el estado tipado del grafo.
- Construir los nodos de intake, completitud e investigación con tools
  locales deterministas o mocks.
- Definir las reglas explícitas de transición entre nodos.

**Semana 2**

- Implementar los nodos de recomendación y auditoría con salida
  estructurada.
- Agregar manejo de salida inválida del modelo y una interrupción simulada
  para representar la aprobación pendiente.
- Ejecutar un caso normal, uno incompleto y uno de alto riesgo desde uv y
  verificar que cada uno siga una ruta distinta.

**Evidencia de cierre:** grafo que toma rutas distintas y rechaza estados
inválidos.

---

## Fase 2: API y Streamlit como servicios separados (S3 a S4)

**Semana 3**

- Crear el proyecto uv de claims-api con los endpoints de creación,
  consulta y envío de mensajes.
- Agregar validación de payloads y correlación por claim_id, thread_id y
  run_id.
- La API podrá iniciar el grafo de la fase 1 en el mismo proceso lógico.

**Semana 4**

- Crear el proyecto uv de frontend-streamlit con la vista de expediente y
  la vista de eventos básicos.
- Configurar Streamlit mediante CLAIMS_API_URL y montar un Docker Compose
  mínimo para API y frontend.
- Cerrar la fase: crear un reclamo desde Streamlit y consultar su
  expediente sin llamadas directas del frontend al dominio.

**Evidencia de cierre:** Streamlit crea y consulta un caso exclusivamente
mediante FastAPI.

---

## Fase 3: Orquestador separado, persistencia y memoria (S5 a S7)

**Semana 5**

- Separar claims-orchestrator como servicio independiente con un contrato
  interno API-orquestador.
- Modelar PostgreSQL para casos, expediente, auditoría y checkpoint.

**Semana 6**

- Integrar Valkey para memoria de trabajo, locks, deduplicación y eventos
  efímeros, con TTL y prefijo de entorno.
- Implementar control de concurrencia por versión del caso.

**Semana 7**

- Implementar la reconexión de Streamlit mediante snapshot y cursor de
  eventos.
- Agregar comprobaciones de salud y errores tipados.
- Cerrar la fase: pausar un caso, reiniciar el orquestador, reabrirlo y
  reanudarlo sin perder estado ni duplicar eventos.

**Evidencia de cierre:** caso pausado que sobrevive al reinicio y conserva
auditoría durable.

---

## Fase 4: Primer especialista por A2A (S8 a S9)

**Semana 8**

- Extraer claims-intake-agent como proyecto uv y servicio independiente.
- Publicar su AgentCard y definir el contrato de tarea y respuesta A2A.

**Semana 9**

- Agregar timeout, autenticación de servicio e identificadores de
  correlación.
- Manejar el caso de especialista caído o incompatible con eventos de tarea
  iniciada, completada y fallida.
- Cerrar la fase: clasificar un caso vía A2A y, al detener el especialista,
  ver el error de dependencia en la interfaz sin perder el estado.

**Evidencia de cierre:** tarea A2A de intake con AgentCard, timeout y error
visible.

---

## Fase 5: Especialización A2A completa (S10 a S11)

**Semana 10**

- Extraer claims-policy-agent con su AgentCard y esquema de salida (citas,
  versión, aplicabilidad).
- Conectar el routing explícito desde los nodos del grafo hacia este
  especialista.

**Semana 11**

- Extraer claims-risk-agent con su AgentCard y esquema de salida (señales,
  severidad, evidencia).
- Definir política de timeouts y errores por skill, y consolidar los tres
  artefactos en el orquestador de forma secuencial.
- Cerrar la fase: un caso atraviesa intake, políticas y riesgo, y la
  interfaz muestra el agente activo en cada paso.

**Evidencia de cierre:** tres especialistas producen artefactos separados y
correlacionados.

---

## Fase 6: MCP de dominio, solo lectura (S12 a S13)

**Semana 12**

- Crear case-tools-mcp como proyecto uv independiente con transporte
  Streamable HTTP en la red privada.
- Implementar las tools de lectura de contexto, transacciones y políticas.

**Semana 13**

- Implementar las tools de lectura de historial y señales, con esquemas
  estrictos y allowlist por consumidor.
- Agregar autorización por servicio, caso y sensibilidad, más eventos de
  tool call y redacción de datos sensibles.
- Cerrar la fase: una investigación obtiene datos mediante MCP y la línea
  de tiempo relaciona la tool con el agente y el caso.

**Evidencia de cierre:** investigación que consulta tools MCP de lectura
con autorización.

---

## Fase 7: Human-in-the-loop y efectos secundarios simulados (S14 a S15)

**Semana 14**

- Implementar el approval gate del grafo con pausa y reanudación por
  checkpoint.
- Construir el panel de aprobación en Streamlit (acción, evidencia,
  política, riesgo, opciones de decisión).

**Semana 15**

- Agregar las tools MCP de preparación y escritura simulada, con
  idempotency_key y concurrencia optimista.
- Implementar auditoría de solo adición y el rechazo de doble aprobación.
- Cerrar la fase: un caso llega a recomendación, se pausa, el analista
  aprueba y se ejecuta una sola acción simulada.

**Evidencia de cierre:** aprobación que permite una sola acción simulada
idempotente.

---

## Fase 8: Endurecimiento del prototipo local (S16 a S18)

**Semana 16**

- Completar logs estructurados y eventos de agente activo.
- Correlacionar trazas entre API, LangGraph, A2A y MCP, y activar streaming
  de progreso.

**Semana 17**

- Agregar middleware de límites, redacción, selección de modelo y
  guardrails, con hooks antes y después de llamadas sensibles.
- Construir la evaluación sintética y las pruebas adversariales (prompt
  injection, replay, timeout, SSRF, exfiltración).

**Semana 18**

- Acotar Deep Agents dentro de un investigator subgraph de solo lectura,
  si se decide incluirlo.
- Completar Docker Compose, comprobaciones de salud, volúmenes y
  configuración segura, y validar la operación del stack desde Portainer.
- Cerrar la fase y el prototipo: ejecutar los cinco escenarios principales
  (caso normal, evidencia faltante, riesgo alto, prompt injection,
  reanudación tras reinicio) y revisar el checklist final de la sección
  24.3.

**Evidencia de cierre:** demostración completa con trazas, evaluación,
amenazas probadas y stack operable.

---

## Notas de uso de esta planeación

- Los rangos de semanas son estimaciones para dedicación parcial. Si la
  disponibilidad real cambia, reasignar semanas por fase en lugar de
  recortar la evidencia de cierre.
- No se debe avanzar de fase sin la evidencia mínima de la tabla 24.2 del
  documento base, aunque la semana planeada ya haya terminado.
- Las fases 4 y 5 concentran el mayor riesgo de retraso por ser la primera
  vez que se introduce comunicación distribuida (A2A). Si S8 a S11 se
  atrasan, absorber el atraso ahí antes de tocar las fases posteriores.
