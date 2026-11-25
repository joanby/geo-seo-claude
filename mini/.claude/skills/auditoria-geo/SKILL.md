---
name: auditoria-geo
description: Auditoría GEO mínima de una web, es decir, cómo de bien la pueden leer y citar ChatGPT, Claude o Gemini. Úsala cuando el usuario pida auditar, revisar o puntuar una web para buscadores de IA.
argument-hint: [url]
allowed-tools: Bash(uv run *) Read Write
---

# Auditoría GEO mínima de $ARGUMENTS

## 1. Recoge los datos (todavía no opines)

Ejecuta:

```bash
uv run ${CLAUDE_SKILL_DIR}/scripts/recoger.py $ARGUMENTS
```

El script imprime la ruta de un JSON. Si falla, para y enséñame el error.

## 2. Lanza los tres subagentes a la vez

En un solo mensaje, lanza en paralelo `mini-rastreadores`, `mini-contenido` y
`mini-schema`. A cada uno pásale solo la ruta del JSON. Espera a tener los tres
informes antes de seguir.

## 3. Escribe el informe

Con los tres informes, escribe `informes/<dominio>-<AAAA-MM-DD>.md` con:

1. **Nota GEO** = rastreadores × 0,3 + contenido × 0,4 + schema × 0,3, y una
   tabla con las tres notas.
2. **Cinco arreglos**, ordenados de más a menos urgente (crítico, alto, medio).
   Cada uno con la evidencia del JSON y el cambio concreto que hay que hacer.
3. **Lo que ya está bien**, en tres líneas como máximo.

No inventes datos: cada hallazgo cita un campo del JSON. Al acabar, resume en
el chat la nota y los tres primeros arreglos.
