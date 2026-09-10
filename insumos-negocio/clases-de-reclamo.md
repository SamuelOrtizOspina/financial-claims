# Clases de reclamo y evidencia obligatoria

Base: sección 3.3 y FR-03 de la propuesta. Cada clase define qué evidencia
es obligatoria antes de que `completeness_node` (sección 10.3) permita pasar
de `classifying` a `investigating`. Si falta evidencia obligatoria, el caso
debe quedar en `awaiting_information`, nunca avanzar con un supuesto.

## CLASE-01: Transacción no reconocida

**Definición:** el cliente afirma no haber realizado ni autorizado una
transacción que aparece en su cuenta o producto.

**Campos obligatorios de intake:**

- identificador sintético de cuenta o producto;
- transacción exacta que se desconoce (fecha, valor, comercio o canal);
- fecha en que el cliente detectó la transacción;
- confirmación de si el medio de pago sigue en su posesión.

**Evidencia obligatoria:**

- referencia de la transacción en el sistema (transaction_ref);
- relato del cliente sobre el desconocimiento.

**Evidencia opcional pero relevante para riesgo:**

- captura o soporte del estado de cuenta;
- registro de dispositivo o ubicación de la sesión donde ocurrió la
  transacción;
- historial de transacciones reconocidas recientes del mismo medio de pago.

**Señales de riesgo típicas:** cambio reciente de dispositivo o canal,
transacción fuera del patrón habitual, múltiples reclamos del mismo cliente
en corto tiempo.

**Política aplicable:** `POLICY-2026-001`.

**Plazo sugerido de resolución:** 10 días hábiles desde el registro del
caso.

---

## CLASE-02: Transacción duplicada

**Definición:** el cliente afirma que una misma operación fue procesada o
cobrada más de una vez.

**Campos obligatorios de intake:**

- las dos o más transacciones que el cliente considera duplicadas;
- valor y fecha de cada una;
- comercio o beneficiario involucrado.

**Evidencia obligatoria:**

- referencia de cada transacción que se reclama como duplicada
  (transaction_ref por cada una);
- comprobante o registro que respalde que se trató de una sola operación
  esperada.

**Evidencia opcional pero relevante para riesgo:**

- confirmación del comercio o beneficiario, si existe;
- soporte de que el cliente autorizó solo una de las transacciones.

**Señales de riesgo típicas:** duplicidad que corresponde a un patrón
conocido de reintento técnico, o inconsistencia temporal que sugiere
manipulación en lugar de un error de procesamiento.

**Política aplicable:** `POLICY-2026-002`.

**Plazo sugerido de resolución:** 8 días hábiles desde el registro del caso.

---

## CLASE-03: Retiro o desembolso con diferencia de valor

**Definición:** el cliente afirma haber solicitado o recibido un valor
distinto al esperado en un retiro, desembolso o pago.

**Campos obligatorios de intake:**

- valor esperado según el cliente;
- valor efectivamente registrado en el sistema;
- canal o punto donde ocurrió el retiro o desembolso.

**Evidencia obligatoria:**

- referencia de la transacción con el valor registrado (transaction_ref);
- relato de la diferencia específica (monto y motivo percibido).

**Evidencia opcional pero relevante para riesgo:**

- registro del canal o dispositivo usado (cajero, corresponsal, digital);
- soporte de conciliación si el canal lo genera.

**Señales de riesgo típicas:** diferencias repetidas en el mismo canal o
dispositivo, patrones de manipulación de comprobantes, reclamo posterior a
mantenimiento o falla reportada del canal.

**Política aplicable:** `POLICY-2026-003`.

**Plazo sugerido de resolución:** 12 días hábiles desde el registro del
caso, o el plazo regulatorio del canal si es menor.

---

## CLASE-04: Producto o servicio no recibido

**Definición:** el cliente afirma haber pagado por un producto o servicio
que no fue entregado o prestado.

**Campos obligatorios de intake:**

- descripción del producto o servicio pagado;
- transacción de pago asociada;
- fecha esperada de entrega o prestación;
- canal o proveedor involucrado, si el cliente lo conoce.

**Evidencia obligatoria:**

- referencia de la transacción de pago (transaction_ref);
- relato del cliente sobre la falta de entrega o prestación.

**Evidencia opcional pero relevante para riesgo:**

- comunicación previa con el proveedor o comercio, si existe;
- comprobante de entrega o prestación emitido por el proveedor.

**Señales de riesgo típicas:** proveedor con reclamos previos similares,
patrón de reclamos coordinados sobre el mismo comercio, plazo de entrega
todavía vigente al momento del reclamo.

**Política aplicable:** `POLICY-2026-004`.

**Plazo sugerido de resolución:** 15 días hábiles desde el registro del
caso, sujeto a confirmación con el proveedor cuando exista ese contacto.

---

## Regla común a las cuatro clases

Si la clasificación inicial tiene confianza baja o el relato es compatible
con más de una clase, el workflow no debe forzar una de ellas. El caso debe
generar preguntas de aclaración (FR-02) antes de aplicarse cualquier
política.

Ninguna clase habilita, por sí misma, la ejecución de una acción financiera
real. La política aplicable define condiciones y evidencia; la decisión y la
ejecución simulada siguen las reglas de las secciones 10.5 y 12.3 de la
propuesta.
