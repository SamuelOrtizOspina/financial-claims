# POLICY-2026-004: Producto o servicio no recibido

**Producto aplicable:** pagos y compras sintéticas del prototipo.
**Clase de reclamo:** CLASE-04.
**Versión vigente:** v1.
**Vigente desde:** 2026-01-01.

Esta es la política referenciada como ejemplo en la sección 18.2 de la
propuesta ("Agente activo: policy-specialist... consultando política
POLICY-2026-004").

---

## v1 (vigente desde 2026-01-01)

### 1. Objeto

Esta política define cuándo un reclamo por producto o servicio no
recibido puede resolverse a favor del cliente y cuándo debe esperar a que
se agote el plazo de entrega vigente.

### 2. Definiciones

**2.1.** Se entiende por plazo de entrega vigente el periodo declarado por
el proveedor o comercio para entregar el producto o prestar el servicio,
contado desde la fecha de pago.

**2.2.** Se entiende por proveedor con historial relevante aquel que tiene
más de dos reclamos de esta misma clase registrados en los últimos 90
días.

### 3. Condiciones de aplicabilidad

**3.1.** La política aplica cuando existe un `transaction_ref` de pago
asociado al producto o servicio reclamado.

**3.2.** La política aplica solo cuando el plazo de entrega vigente ya
venció al momento del reclamo, salvo que exista una señal de riesgo de
proveedor según la sección 5.

**3.3.** La política no aplica cuando el plazo de entrega vigente todavía
no ha vencido y no hay señal de riesgo de proveedor; en ese caso el
resultado correcto es mantener el caso pendiente, no rechazarlo ni
aprobarlo.

**3.4.** La política no aplica cuando el cliente confirma haber recibido
el producto o servicio y el reclamo es en realidad sobre su calidad o
condición; ese escenario queda fuera del alcance de las cuatro clases del
prototipo (sección 3.3 de la propuesta).

### 4. Evidencia requerida

**4.1.** Referencia de la transacción de pago asociada.

**4.2.** Relato del cliente sobre la falta de entrega o prestación,
incluyendo la fecha esperada.

### 5. Señales de riesgo relevantes para esta política

**5.1.** Proveedor con historial relevante según la definición 2.2.

**5.2.** Patrón de varios reclamos sobre el mismo comercio en una ventana
corta de tiempo, lo que puede indicar un comercio no operativo o
fraudulento.

### 6. Resultado esperado

**6.1.** Si el plazo de entrega vigente ya venció y no hay comunicación del
proveedor que lo justifique, la recomendación puede ser aprobar una
resolución simulada a favor del cliente.

**6.2.** Si existe una señal de riesgo de proveedor según la sección 5, el
caso debe escalarse a revisión de riesgo aunque el plazo no haya vencido.

**6.3.** Si el plazo de entrega vigente todavía no ha vencido y no hay
señal de riesgo de proveedor, la recomendación debe ser mantener pendiente
por falta de información, citando la sección 3.3.

### 7. Plazo

El plazo de resolución sugerido es de 15 días hábiles desde el registro
del caso, sujeto a confirmación con el proveedor cuando exista ese
contacto, según lo definido en `clases-de-reclamo.md`.

---

## Historial de versiones

| Versión | Vigencia | Cambio principal |
|---|---|---|
| v1 | desde 2026-01-01 | Versión inicial de la política. |
