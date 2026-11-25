# mini (geo-mini)

Versión mínima del agente de auditoría GEO de [geo-seo-claude](https://github.com/joanby/geo-seo-claude),
construida desde cero en el vídeo «Reconstruyo desde cero el agente de 450.000 visitas».

Una skill, un script y tres subagentes en paralelo que escriben un informe.

```
.claude/
├── skills/auditoria-geo/
│   ├── SKILL.md            # la receta: qué hacer y en qué orden
│   └── scripts/recoger.py  # recoge los hechos (robots, llms.txt, schema...)
└── agents/
    ├── mini-rastreadores.md
    ├── mini-contenido.md
    └── mini-schema.md
```

## Uso

Necesitas [Claude Code](https://code.claude.com) y [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/joanby/geo-seo-claude && cd geo-seo-claude/mini
claude
```

Dentro de Claude Code:

```
/auditoria-geo https://tuweb.com
```

Los datos quedan en `datos/` y el informe en `informes/`.

Para la auditoría completa (cinco subagentes, PDF, propuestas para clientes) usa
[geo-seo-claude](https://github.com/joanby/geo-seo-claude).
