# 🚀 Quick Start - Event Modules

Guía rápida para usar el sistema de módulos de eventos.

## 📋 Comandos Rápidos

### **Listar módulos disponibles**
```bash
python scripts/manage_event_modules.py list
```

### **Activar un módulo**
```bash
python scripts/manage_event_modules.py activate feat-semana-ciencia
```

### **Desactivar último módulo**
```bash
python scripts/manage_event_modules.py deactivate
```

### **Crear nuevo módulo**
```bash
python scripts/manage_event_modules.py create feat-concurso-literario
```

## 🎯 Workflow Típico

### **1. Activar Semana de la Ciencia**
```bash
# Verificar que estás en main
git checkout main

# Activar módulo
python scripts/manage_event_modules.py activate feat-semana-ciencia

# Verificar que funciona
# Ir a la app y verificar que aparece la pestaña "Desafío"
```

### **2. Desactivar cuando termine el evento**
```bash
# Desactivar módulo
python scripts/manage_event_modules.py deactivate

# Verificar que se desactivó
# La pestaña "Desafío" ya no debería aparecer
```

### **3. Crear nuevo evento**
```bash
# Crear nuevo módulo
python scripts/manage_event_modules.py create feat-concurso-literario

# Desarrollar funcionalidad usando templates
# Copiar y modificar archivos de /templates/
# Implementar lógica específica del evento

# Cuando esté listo, mergear
git checkout main
git merge feat-concurso-literario --no-ff -m "feat: Add Concurso Literario module"
```

## 🔧 Templates Disponibles

- `templates/event_module_template.py` - Template para rutas
- `templates/event_decorators_template.py` - Template para decorators
- `docs/EVENT_MODULES.md` - Documentación completa

## ⚠️ Notas Importantes

1. **Siempre trabajar desde `main`** para activar/desactivar módulos
2. **Usar `--no-ff`** en merges para mantener historial
3. **Probar antes de mergear** para evitar problemas
4. **Documentar cada módulo** para facilitar mantenimiento

## 🆘 Troubleshooting

### **Error: "Debes estar en main"**
```bash
git checkout main
```

### **Error: "Módulo no existe"**
```bash
# Verificar módulos disponibles
python scripts/manage_event_modules.py list
```

### **Error: "Merge conflict"**
```bash
# Resolver conflictos manualmente
git add <archivos-resueltos>
git commit -m "Resolve merge conflicts"
```

### **Error: "No se puede revertir"**
```bash
# Verificar último merge
git log --oneline --merges -1

# Revertir manualmente si es necesario
git revert -m 1 <commit-hash>
```
