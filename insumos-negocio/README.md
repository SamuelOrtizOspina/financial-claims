# Insumos de negocio del sistema de reclamos financieros

Este directorio no es un entregable de una fase puntual. Es el conjunto de
insumos de negocio (dominio, contratos y políticas) que se usa durante
**todas** las fases descritas en
`PROPUESTA_SIDEPROJECT_RECLAMOS_FINANCIEROS.md` (sección 23), desde el
diseño del grafo en la fase 1 hasta el endurecimiento en la fase 8.

Estos insumos no cambian de forma según la fase. Lo que cambia por fase es
qué componente los consume: en la fase 1 los usa el grafo en un solo
proceso, en la fase 5 los usan los tres especialistas A2A, en la fase 6 los
sirve el MCP de dominio, en la fase 7 los usa el approval gate. El
contenido de este directorio se mantiene estable a través de ese recorrido.

## Qué contiene

- `clases-de-reclamo.md`: las cuatro clases de reclamo con su evidencia
  obligatoria y opcional (sección 3.3, FR-03). Se usa desde la
  clasificación inicial hasta la validación final del expediente.
- `contratos-esquemas.md`: los esquemas de Claim, Evidence, PolicyFinding,
  RiskAssessment, Recommendation y AuditEvent (sección 10.1, 16.1). Es el
  contrato de datos que atraviesa el grafo, los especialistas, el MCP y la
  persistencia durable.
- `estados-transiciones.md`: los estados de negocio y las transiciones
  permitidas (sección 10.2). Rige el workflow en cualquier fase, con o sin
  red de por medio.
- `contrato-eventos.md`: el contrato de eventos para observabilidad
  (sección 13.3). Nace acotado y se amplía en fases posteriores sin romper
  su forma base.
- `threat-model-inicial.md`: el threat model del sistema (sección 17), con
  el control de diseño que aplica desde el inicio y la fase en la que se
  cierra cada amenaza.
- `politicas/`: el corpus sintético de políticas versionadas para las
  cuatro clases de reclamo (sección 12, FR-04). Es la fuente que consulta
  `claims-policy-agent` en todas las fases donde exista ese especialista.
- `dataset-evaluacion-especificacion.md`: la especificación de los casos
  que debe tener el dataset de evaluación (sección 19.1), con la fase en
  la que cada categoría de caso se vuelve ejecutable.
- `datos-sinteticos/`: los registros concretos que instancian lo anterior
  — clientes, transacciones, evidencias y 22 casos completos con su
  resultado esperado (oráculo). Es el dataset de evaluación de la sección
  19.1 ya construido para las categorías ejecutables desde fase 0/1; ver
  `datos-sinteticos/README.md`.
- `validacion-cierre-fase0.md`: verifica que cada estado y transición de
  `estados-transiciones.md` tiene un caso que lo demuestra en
  `datos-sinteticos/casos.json`, y deja constancia de las transiciones que
  se difieren a fases posteriores.

## Cómo se usa este material

1. Los changemakers reciben estos insumos como fuente de verdad de
   negocio, vigente durante todo el proyecto, no como un artefacto que se
   cierra y se archiva al terminar una fase.
2. `datos-sinteticos/casos.json` es el oráculo: la salida de cualquier
   implementación (fase 1 en adelante) se compara contra los resultados
   ya resueltos en ese archivo.
3. Cada fase (1 a 8) consulta estos mismos esquemas, estados y políticas.
   Ninguna fase debe redefinir su forma para resolver un problema local.

Cualquier cambio a un esquema, estado o política durante la implementación
debe registrarse como una nueva versión, no como una edición silenciosa del
contrato original.
