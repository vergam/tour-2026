# Fantasy Tour de França 2026

App de fantasy per seguir el Tour de França 2026 en temps real.

## Desplegament pas a pas

### Pas 1 — Crear el repositori a GitHub

1. Ves a [github.com](https://github.com) i inicia sessió
2. Clica el botó verd **"New"** (cantonada superior esquerra)
3. Posa de nom: `fantasy-tour-2026`
4. Marca **"Public"** (necessari per GitHub Pages gratuït)
5. Clica **"Create repository"**

---

### Pas 2 — Pujar els fitxers

Tens dues opcions:

#### Opció A — Des del navegador (més senzill)
1. Al repositori buit, clica **"uploading an existing file"**
2. Arrossega tots els fitxers d'aquesta carpeta
3. Clica **"Commit changes"**

#### Opció B — Amb Git (terminal)
```bash
git init
git add .
git commit -m "Primer commit"
git remote add origin https://github.com/EL_TEU_USUARI/fantasy-tour-2026.git
git push -u origin main
```

---

### Pas 3 — Activar GitHub Pages

1. Al repositori, clica **"Settings"** (pestanya superior)
2. Al menú esquerre, clica **"Pages"**
3. A "Source", selecciona **"Deploy from a branch"**
4. A "Branch", selecciona **"main"** i carpeta **"/ (root)"**
5. Clica **"Save"**
6. Espera 2-3 minuts. L'URL serà: `https://EL_TEU_USUARI.github.io/fantasy-tour-2026`

---

### Pas 4 — Activar les actualitzacions automàtiques

1. Al repositori, clica la pestanya **"Actions"**
2. Si veus un avís de "Workflows aren't being run", clica **"I understand my workflows, go ahead and enable them"**
3. Al menú esquerre veuràs **"Actualitzar classificacions Tour 2026"**
4. Clica-hi i prem **"Enable workflow"**

A partir d'aquí, cada hora GitHub executarà el script automàticament i actualitzarà les classificacions.

---

### Pas 5 — Prova manual

Per comprovar que funciona:
1. Ves a la pestanya **"Actions"**
2. Clica **"Actualitzar classificacions Tour 2026"**
3. Clica **"Run workflow"** → **"Run workflow"** (botó verd)
4. Espera 1-2 minuts
5. Ves a la teva URL de GitHub Pages i comprova que les dades s'han actualitzat

---

## Estructura de fitxers

```
fantasy-tour-2026/
├── index.html                    # L'app principal
├── update_data.py                # Script de scraping
├── data/
│   └── classifications.json     # Dades actualitzades automàticament
└── .github/
    └── workflows/
        └── update.yml           # Robot d'actualització horària
```

## Puntuació

| Posició | GC | Muntanya | Sprint |
|---------|-----|----------|--------|
| 1r | 25 | 18 | 15 |
| 2n | 22 | 15 | 12 |
| 3r | 19 | 12 | 10 |
| 4t | 16 | 10 | 8 |
| 5è | 13 | 8 | 6 |
| 6è | 10 | 6 | 4 |
| 7è | 7 | 4 | 3 |
| 8è | 5 | 3 | 2 |
| 9è | 3 | 2 | 1 |
| 10è | 1 | 1 | 1 |

- Victòria d'etapa: **+5 pts** (acumulatiu)
- Les classificacions GC/Muntanya/Sprint són **snapshot** (reflecteixen la posició actual, no s'acumulen)
