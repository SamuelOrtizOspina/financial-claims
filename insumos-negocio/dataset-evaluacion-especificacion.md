# Especificación del dataset de evaluación

Base: sección 19.1 de la propuesta. Este documento define qué debe existir
en el dataset (30 a 50 casos etiquetados) y qué debe demostrar cada
categoría de caso. No incluye los registros sintéticos concretos de
clientes, transacciones ni evidencias: esos los construye el equipo,
usando esta tabla como especificación de aceptación.

Cada caso del dataset debe quedar etiquetado con: categoría, clase de
reclamo, política referenciada (si aplica) y resultado esperado según las
políticas de `politicas/`.

## Categorías obligatorias

| Categoría | Cantidad mínima | Clase(s) de reclamo | Política de referencia | Resultado esperado |
|---|---|---|---|---|
| Caso normal por clase | 4 (una por clase) | CLASE-01 a CLASE-04 | la que corresponda a la clase | evidencia completa, `outcome = aprobar` o `rechazar` según la política, con citas |
| Caso ambiguo | 2 o más | cualquiera, con relato compatible con más de una clase | ninguna hasta clasificar | preguntas de aclaración (FR-02), no una clasificación forzada |
| Evidencia faltante | 2 o más | cualquiera | la que corresponda | `awaiting_information`, `outcome = solicitar_evidencia` |
| Evidencia contradictoria | 2 o más | cualquiera | la que corresponda | el caso no debe "convertir no encontrado en falso" (FR-03); recomendación no definitiva |
| Política aplicable | al menos 1 por clase | CLASE-01 a CLASE-04 | la de la clase, sección 3 con `applicability = aplica` | `PolicyFinding.applicability = aplica`, citas de la sección aplicable |
| Política no aplicable | al menos 1 por clase | CLASE-01 a CLASE-04 | la de la clase, usando su sección 3.3 o 3.4 | `PolicyFinding.applicability = no_aplica`, citando la condición de exclusión exacta |
| Riesgo bajo | 2 o más | cualquiera | la que corresponda | `RiskAssessment.severity = baja`, no bloquea la recomendación |
| Riesgo medio | 2 o más | cualquiera | la que corresponda | `RiskAssessment.severity = media`, condiciona pero no impide necesariamente aprobar |
| Riesgo alto | 2 o más | cualquiera, priorizando CLASE-01 | la que corresponda | `RiskAssessment.severity = alta`, transición obligatoria a `awaiting_human_review` |
| Prompt injection | 2 o más | cualquiera | ninguna cambia por la instrucción del documento | evidencia con `trust_label = instruccion_potencial`, ninguna transición del grafo cambia por su contenido (CU-04) |
| Timeout de especialista o A2A | 1 o más | cualquiera | no aplica en fase 0 y 1, se activa desde fase 4 | error clasificado como transitorio o permanente según FR-12, nunca un `resolved` silencioso |
| Salida inválida del modelo | 1 o más | cualquiera | no aplica en fase 0 y 1 | el nodo rechaza la salida y no la fuerza contra el esquema (`contratos-esquemas.md`) |
| Reinicio en aprobación | 1 o más | cualquiera | la que corresponda | el caso se reanuda desde `awaiting_human_review` sin perder el expediente (CU-05, activo desde fase 3) |
| Doble solicitud o doble aprobación | 1 o más | cualquiera | la que corresponda | la segunda solicitud se rechaza como duplicada, `case_version` lo detecta (CU-06, activo desde fase 3) |
| Tool no autorizada | 1 o más | cualquiera | no aplica en fase 0 y 1, se activa desde fase 6 | la solicitud se rechaza por autorización, no se ejecuta y se audita |

## Cómo usar esta tabla por fase

- **Fase 0 y 1:** el equipo puede construir de inmediato los casos de
  clasificación, evidencia, política aplicable/no aplicable y riesgo,
  porque no dependen de red, A2A ni MCP.
- **Fase 3:** se agregan los casos de reinicio y doble solicitud, una vez
  exista persistencia durable.
- **Fase 4 a 6:** se agregan los casos de timeout y tool no autorizada,
  una vez existan agentes remotos y MCP.
- **Fase 8:** el dataset completo (30 a 50 casos) se ejecuta como suite de
  evaluación y pruebas adversariales, según la tabla 24.2 de la propuesta.

## Regla de etiquetado

Cada caso del dataset debe declarar explícitamente qué objetivo de
aceptación de la sección 19.3 de la propuesta verifica. Un caso que no
pueda vincularse a un objetivo de aceptación no se agrega al dataset; se
descarta o se fusiona con uno existente.
