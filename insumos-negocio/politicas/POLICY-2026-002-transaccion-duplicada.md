# POLICY-2026-002: Transacción duplicada

**Producto aplicable:** cuentas y medios de pago sintéticos del prototipo.
**Clase de reclamo:** CLASE-02.
**Versión vigente:** v1.
**Vigente desde:** 2026-01-01.

---

## v1 (vigente desde 2026-01-01)

### 1. Objeto

Esta política define cuándo dos o más transacciones se consideran una
duplicidad indebida y cuándo corresponden a operaciones distintas que el
cliente confunde entre sí.

### 2. Definiciones

**2.1.** Se entiende por transacciones candidatas a duplicidad aquellas con
el mismo beneficiario o comercio, el mismo valor y una diferencia de tiempo
menor a 24 horas entre ellas.

**2.2.** Se entiende por reintento técnico la duplicidad producida por un
error de procesamiento del canal, no por una segunda autorización del
cliente.

### 3. Condiciones de aplicabilidad

**3.1.** La política aplica cuando el cliente identifica al menos dos
transacciones candidatas a duplicidad según la definición 2.1.

**3.2.** La política aplica tanto si la duplicidad corresponde a un
reintento técnico como si corresponde a un error humano en el canal.

**3.3.** La política no aplica cuando las transacciones señaladas por el
cliente tienen beneficiarios distintos o una diferencia de valor mayor al
5%; en ese caso el reclamo debe reclasificarse, típicamente como CLASE-01
o CLASE-03.

**3.4.** La política no aplica cuando el cliente autorizó explícitamente
ambas transacciones como pagos independientes; ese escenario se rechaza
por falta de mérito bajo la sección 6.3.

### 4. Evidencia requerida

**4.1.** Referencia de cada transacción señalada como duplicada
(`transaction_ref` por cada una, mínimo dos).

**4.2.** Comprobante o registro que respalde que el cliente esperaba una
sola operación.

### 5. Señales de riesgo relevantes para esta política

**5.1.** Duplicidad que no coincide con ningún patrón de reintento técnico
conocido del canal, lo que sugiere manipulación en lugar de error.

**5.2.** Historial de más de dos reclamos de duplicidad del mismo cliente
en 90 días, lo que puede indicar uso indebido del proceso de reclamo en
lugar de una falla real.

### 6. Resultado esperado

**6.1.** Si la duplicidad corresponde a un reintento técnico identificado
del canal, la recomendación puede ser aprobar una resolución simulada que
reversa la transacción duplicada.

**6.2.** Si la duplicidad no corresponde a un patrón de reintento técnico
conocido, el caso debe pasar por revisión de riesgo antes de recomendar
una aprobación.

**6.3.** Si el cliente autorizó ambas transacciones como operaciones
independientes, la recomendación debe ser rechazar con explicación para
revisión interna, citando la sección 3.4.

### 7. Plazo

El plazo de resolución sugerido es de 8 días hábiles desde el registro del
caso, según lo definido en `clases-de-reclamo.md`.

---

## Historial de versiones

| Versión | Vigencia | Cambio principal |
|---|---|---|
| v1 | desde 2026-01-01 | Versión inicial de la política. |
