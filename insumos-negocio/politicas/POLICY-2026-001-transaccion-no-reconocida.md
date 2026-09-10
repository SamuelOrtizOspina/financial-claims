# POLICY-2026-001: Transacción no reconocida

**Producto aplicable:** cuentas y medios de pago sintéticos del prototipo.
**Clase de reclamo:** CLASE-01.
**Versión vigente:** v2.
**Vigente desde:** 2026-03-01.

---

## v2 (vigente desde 2026-03-01)

### 1. Objeto

Esta política define las condiciones bajo las cuales un reclamo por
transacción no reconocida puede resolverse a favor del cliente mediante
una resolución simulada, y las condiciones bajo las cuales debe rechazarse
o escalarse.

### 2. Definiciones

**2.1.** Se entiende por transacción no reconocida aquella que el cliente
afirma no haber realizado ni autorizado, independientemente de si el medio
de pago estuvo físicamente en su posesión.

**2.2.** Se entiende por medio de pago comprometido aquel que presenta al
menos una señal de riesgo de las descritas en la sección 5 de esta
política.

### 3. Condiciones de aplicabilidad

**3.1.** La política aplica cuando existe un `transaction_ref` válido
asociado al reclamo.

**3.2.** La política aplica cuando el cliente confirma si el medio de pago
sigue en su posesión, sin importar la respuesta.

**3.3.** La política no aplica cuando el reclamo corresponde a una
transacción que el propio cliente autorizó y luego intenta desconocer sin
evidencia de compromiso del medio de pago; ese escenario se rige por
`POLICY-2026-002` si además hay duplicidad, o se rechaza por falta de
mérito bajo la sección 6.2 de esta política.

**3.4.** La política no aplica a transacciones con más de 60 días
calendario entre la fecha de la transacción y la fecha de registro del
reclamo, salvo que exista una señal de riesgo de severidad alta según la
sección 5.

### 4. Evidencia requerida

**4.1.** Referencia de la transacción reclamada.

**4.2.** Relato del cliente sobre el desconocimiento de la transacción.

**4.3.** Cuando exista, registro de dispositivo, canal o ubicación de la
sesión donde ocurrió la transacción.

### 5. Señales de riesgo relevantes para esta política

**5.1.** Cambio de dispositivo, canal o ubicación en las 24 horas previas a
la transacción reclamada.

**5.2.** Transacción fuera del patrón de valor o comercio habitual del
cliente.

**5.3.** Más de un reclamo por transacción no reconocida del mismo cliente
en los últimos 30 días.

### 6. Resultado esperado

**6.1.** Si la evidencia de las secciones 3 y 4 está completa y no hay
señales de riesgo de severidad alta, la recomendación puede ser aprobar
una resolución simulada a favor del cliente.

**6.2.** Si la evidencia es insuficiente o contradictoria, la
recomendación debe ser solicitar evidencia, nunca aprobar por defecto.

**6.3.** Si existe al menos una señal de riesgo de severidad alta según la
sección 5, el caso debe escalarse a revisión de riesgo antes de cualquier
recomendación de aprobación.

### 7. Plazo

El plazo de resolución sugerido es de 10 días hábiles desde el registro
del caso, según lo definido en `clases-de-reclamo.md`.

---

## Historial de versiones

| Versión | Vigencia | Cambio principal |
|---|---|---|
| v1 | 2026-01-01 a 2026-02-28 | El umbral de la sección 3.4 era de 90 días calendario sin excepción por severidad de riesgo. |
| v2 | desde 2026-03-01 | Se redujo el umbral a 60 días y se agregó la excepción por señal de riesgo de severidad alta (sección 3.4). |

El especialista de políticas debe citar siempre la versión vigente en la
fecha de la transacción reclamada, no la versión vigente en la fecha de
creación del caso, salvo que ambas coincidan.
