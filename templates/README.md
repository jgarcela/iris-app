# 🎯 Event Module Templates

Este directorio contiene templates para crear nuevos módulos de eventos.

## 📁 Archivos Disponibles

### **`event_module_template.py`**
Template para crear las rutas de un nuevo evento.

**Cómo usar:**
1. Copia el archivo: `cp event_module_template.py ../web/routes/mi_evento.py`
2. Renombra todas las referencias:
   - `nombre_evento` → `mi_evento`
   - `event_required` → `mi_evento_required`
   - `DB_EVENT_COLLECTION` → `DB_MI_EVENTO`
3. Implementa la lógica específica del evento

### **`event_decorators_template.py`**
Template para crear decorators específicos del evento.

**Cómo usar:**
1. Copia el archivo: `cp event_decorators_template.py ../web/utils/mi_evento_decorators.py`
2. Renombra todas las referencias:
   - `event_required` → `mi_evento_required`
   - `nombre_evento` → `mi_evento`
3. Ajusta la lógica de permisos según necesites

## 🎨 Ejemplo: Crear Módulo "Concurso Literario"

```bash
# 1. Crear branch
git checkout main
git checkout -b feat-concurso-literario

# 2. Copiar templates
cp templates/event_module_template.py web/routes/concurso_literario.py
cp templates/event_decorators_template.py web/utils/concurso_literario_decorators.py

# 3. Renombrar referencias en los archivos
# En web/routes/concurso_literario.py:
# - nombre_evento → concurso_literario
# - event_required → concurso_literario_required
# - DB_EVENT_COLLECTION → DB_CONCURSO_LITERARIO

# En web/utils/concurso_literario_decorators.py:
# - event_required → concurso_literario_required
# - nombre_evento → concurso_literario

# 4. Crear templates HTML
mkdir -p web/templates/concurso_literario
# Crear archivos HTML específicos del evento

# 5. Crear estilos CSS
mkdir -p web/static/css/concurso_literario
# Crear archivos CSS específicos del evento

# 6. Implementar lógica específica del evento
# Modificar las funciones según las necesidades del concurso

# 7. Agregar navegación en base.html
# Agregar pestaña condicional para el evento

# 8. Registrar blueprint en __init__.py
# Agregar import y registro condicional del blueprint
```

## 📝 Checklist para Nuevos Módulos

- [ ] Copiar y renombrar templates
- [ ] Crear directorio de templates HTML
- [ ] Crear directorio de estilos CSS
- [ ] Implementar lógica específica del evento
- [ ] Agregar navegación condicional
- [ ] Registrar blueprint condicionalmente
- [ ] Crear decorators específicos
- [ ] Probar funcionalidad completa
- [ ] Documentar el módulo
- [ ] Hacer commit descriptivo

## 🔧 Personalización

### **Decorators**
Puedes crear decorators específicos para diferentes niveles de acceso:
- `event_required`: Acceso básico al evento
- `event_only`: Solo participantes del evento
- `event_admin_required`: Solo administradores del evento

### **Rutas**
Puedes agregar tantas rutas como necesites:
- Página principal del evento
- Páginas de participación
- Páginas de resultados
- API endpoints para funcionalidad dinámica

### **Templates**
Crea templates específicos para cada página del evento:
- `event_home.html`: Página principal
- `event_participate.html`: Página de participación
- `event_results.html`: Página de resultados

## 📚 Documentación Adicional

- `../docs/EVENT_MODULES.md` - Documentación completa del sistema
- `../docs/QUICK_START_EVENT_MODULES.md` - Guía rápida de uso
- `../scripts/manage_event_modules.py` - Script de gestión de módulos
