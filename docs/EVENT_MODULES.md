# 🎯 Event Modules - Branch Strategy

Este documento explica cómo crear y gestionar módulos temporales para eventos usando la estrategia de branches.

## 📋 Concepto

Los **Event Modules** son funcionalidades temporales que se pueden activar/desactivar fácilmente para eventos específicos (concursos, desafíos, maratones, etc.).

## 🌳 Estructura de Branches

```
main (estable, sin módulos temporales)
├── feat-semana-ciencia (módulo challenge)
├── feat-concurso-literario (futuro módulo)
├── feat-maraton-programacion (futuro módulo)
└── feat-otro-evento (futuro módulo)
```

## 🚀 Workflow

### 1. **Activar un Event Module**
```bash
# Mergear el módulo a main
git checkout main
git merge feat-semana-ciencia --no-ff -m "feat: Activate Semana de la Ciencia module"
```

### 2. **Desactivar un Event Module**
```bash
# Opción A: Revertir el merge
git revert -m 1 <merge-commit-hash>

# Opción B: Reset al commit anterior
git reset --hard <commit-antes-del-merge>
```

### 3. **Crear un Nuevo Event Module**
```bash
# Crear branch desde main
git checkout main
git checkout -b feat-nuevo-evento

# Desarrollar el módulo...
# Luego mergear cuando esté listo
```

## 📁 Estructura de un Event Module

```
feat-nombre-evento/
├── web/routes/nombre_evento.py          # Rutas del evento
├── web/templates/nombre_evento/         # Templates
├── web/utils/nombre_evento_decorators.py # Decorators específicos
├── web/static/css/nombre_evento.css     # Estilos específicos
├── web/static/js/nombre_evento.js       # JavaScript específico
├── database/collections/nombre_evento.py # Colecciones de DB
└── docs/nombre_evento/                  # Documentación específica
```

## 🔧 Checklist para Nuevos Event Modules

### **Antes de Crear el Branch:**
- [ ] Definir la funcionalidad del evento
- [ ] Identificar qué archivos necesitas modificar
- [ ] Planificar la navegación y permisos

### **Durante el Desarrollo:**
- [ ] Crear branch desde `main`
- [ ] Implementar funcionalidad en archivos separados
- [ ] Usar decorators para permisos específicos
- [ ] Agregar navegación condicional en `base.html`
- [ ] Registrar blueprints condicionalmente en `__init__.py`
- [ ] Crear templates específicos
- [ ] Agregar estilos específicos

### **Antes del Merge:**
- [ ] Probar funcionalidad completa
- [ ] Verificar que no rompe funcionalidad existente
- [ ] Documentar el módulo
- [ ] Crear commit descriptivo

### **Después del Merge:**
- [ ] Probar en producción
- [ ] Documentar cómo desactivar
- [ ] Preparar plan de rollback

## 🎨 Ejemplo: Crear un Módulo de Concurso Literario

```bash
# 1. Crear branch
git checkout main
git checkout -b feat-concurso-literario

# 2. Crear archivos
mkdir -p web/routes web/templates/concurso web/utils web/static/css/concurso
touch web/routes/concurso.py
touch web/templates/concurso/concurso_home.html
touch web/utils/concurso_decorators.py
touch web/static/css/concurso/concurso.css

# 3. Desarrollar funcionalidad...

# 4. Mergear cuando esté listo
git checkout main
git merge feat-concurso-literario --no-ff -m "feat: Add Concurso Literario module"
```

## 🔄 Ventajas de esta Estrategia

- ✅ **Aislamiento completo**: Cada módulo en su branch
- ✅ **Fácil activar/desactivar**: Un merge/revert
- ✅ **Historial limpio**: Cada evento tiene su historia
- ✅ **Escalable**: Puedes tener N módulos sin conflictos
- ✅ **Rollback fácil**: Si algo falla, vuelves atrás
- ✅ **Testing independiente**: Cada módulo se testea por separado

## 📝 Notas Importantes

1. **Siempre mergear con `--no-ff`** para mantener el historial del módulo
2. **Usar commits descriptivos** para facilitar el rollback
3. **Probar antes de mergear** para evitar problemas en producción
4. **Documentar cada módulo** para facilitar el mantenimiento
5. **Mantener main estable** - solo mergear módulos completos y probados

## 🆘 Troubleshooting

### **Problema: Merge conflict**
```bash
# Resolver conflictos manteniendo la lógica del módulo
git add <archivos-resueltos>
git commit -m "Resolve merge conflicts for <nombre-modulo>"
```

### **Problema: Módulo roto en producción**
```bash
# Rollback rápido
git revert -m 1 <merge-commit-hash>
git push origin main
```

### **Problema: Necesito modificar un módulo activo**
```bash
# Crear hotfix branch
git checkout main
git checkout -b hotfix-nombre-modulo
# Hacer cambios...
git checkout main
git merge hotfix-nombre-modulo
```
