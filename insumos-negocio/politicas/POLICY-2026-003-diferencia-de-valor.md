# POLICY-2026-003: Retiro o desembolso con diferencia de valor

**Producto aplicable:** cajeros, corresponsales y canales de desembolso
sintéticos del prototipo.
**Clase de reclamo:** CLASE-03.
**Versión vigente:** v1.
**Vigente desde:** 2026-01-01.

---

## v1 (vigente desde 2026-01-01)

### 1. Objeto

Esta política define cuándo una diferencia entre el valor solicitado y el
valor registrado en un retiro o desembolso es atribuible al canal y cuándo
es atribuible a un error de percepción o a un intento indebido del
reclamo.

### 2. Definiciones

**2.1.** Se entiende por diferencia de valor la resta entre el valor que el
cliente afirma haber solicitado o recibido y el valor registrado por el
sistema para la misma transacción.

**2.2.** Se entiende por canal con incidencia reportada aquel que tiene
una alerta operativa registrada en la ventana de tiempo del reclamo.

### 3. Condiciones de aplicabilidad

**3.1.** La política aplica cuando existe un `transaction_ref` con un valor
registrado distinto de cero para la operación reclamada.

**3.2.** La política aplica tanto si la diferencia es a favor del cliente
como si es en su contra.

**3.3.** La política no aplica cuando la diferencia reclamada es menor al
1% del valor de la transacción; ese caso se considera dentro del margen de
redondeo del canal y se rechaza por falta de mérito bajo la sección 6.3.

**3.4.** La política no aplica cuando el canal involucrado no registra
ninguna transacción para la fecha y monto indicados por el cliente; en ese
caso el reclamo debe tratarse primero como una posible transacción no
reconocida (`POLICY-2026-001`).

### 4. Evidencia requerida

**4.1.** Referencia de la transacción con el valor registrado por el
sistema.

**4.2.** Relato específico del cliente sobre el monto y el motivo percibido
de la diferencia.

### 5. Señales de riesgo relevantes para esta política

**5.1.** Diferencias repetidas reportadas sobre el mismo canal o
dispositivo en un periodo corto, lo que puede indicar una falla física del
canal en lugar de reclamos individuales.

**5.2.** Reclamo presentado inmediatamente después de una falla o
mantenimiento reportado del canal.

### 6. Resultado esperado

**6.1.** Si el canal tiene una incidencia reportada según la definición
2.2 para la fecha y el monto del reclamo, la recomendación puede ser
aprobar una resolución simulada que ajusta el valor a favor del cliente.

**6.2.** Si no hay incidencia reportada pero la diferencia es significativa
y no está explicada, el caso debe pasar por revisión de riesgo antes de
recomendar una aprobación.

**6.3.** Si la diferencia está dentro del margen de la sección 3.3, la
recomendación debe ser rechazar con explicación para revisión interna.

### 7. Plazo

El plazo de resolución sugerido es de 12 días hábiles desde el registro
del caso, o el plazo regulatorio del canal si es menor, según lo definido
en `clases-de-reclamo.md`.

---

## Historial de versiones

| Versión | Vigencia | Cambio principal |
|---|---|---|
| v1 | desde 2026-01-01 | Versión inicial de la política. |
