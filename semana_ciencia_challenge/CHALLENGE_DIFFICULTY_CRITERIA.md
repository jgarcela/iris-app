# Criterios de Dificultad - Desafío IRIS 2025

## 📊 **Sistema de Clasificación de Dificultad**

### 🟢 **FÁCIL** - Sesgos evidentes y obvios
**Criterios:**
- **Sesgos explícitos**: Frases como "primera mujer", "exclusivamente por mérito"
- **Desequilibrio claro**: Pocas fuentes, desbalance de género evidente
- **Lenguaje redundante**: Adjetivos innecesarios que enfatizan género
- **Estructura simple**: Texto corto, variables fáciles de identificar

**Ejemplos de indicadores:**
- "Es la primera mujer en..."
- "Exclusivamente por mérito" (redundante)
- Solo 1-2 fuentes citadas
- Desbalance evidente en personas mencionadas

---

### 🟡 **MEDIO** - Sesgos sutiles pero detectables
**Criterios:**
- **Sesgos implícitos**: Diferencias en tratamiento, no explícitas
- **Desequilibrio moderado**: 2-3 fuentes, balance parcial
- **Lenguaje complejo**: Términos técnicos, estructura más elaborada
- **Múltiples variables**: Requiere análisis de varias categorías

**Ejemplos de indicadores:**
- "deportistas" vs "atletas" (diferencia sutil)
- Desbalance moderado en fuentes
- Lenguaje más técnico o formal
- Múltiples variables a analizar

---

### 🔴 **DIFÍCIL** - Sesgos muy sutiles o complejos
**Criterios:**
- **Sesgos encubiertos**: Difíciles de detectar sin conocimiento especializado
- **Desequilibrio sutil**: Balance aparente pero sesgado
- **Lenguaje sofisticado**: Términos técnicos, argumentos complejos
- **Múltiples capas**: Requiere análisis profundo de todas las categorías

**Ejemplos de indicadores:**
- Argumentos aparentemente neutrales pero sesgados
- Balance aparente pero desigual en el fondo
- Lenguaje muy técnico o académico
- Requiere análisis de todas las variables

---

## 🎯 **Variables por Categoría**

### **Contenido General**
- `personas_mencionadas`: Nombres y género de personas citadas
- `genero_periodista`: Género del periodista/autor
- `tema`: Tipo de noticia/tema tratado

### **Lenguaje**
- `lenguaje_sexista`: Uso de términos o frases sexistas
- `androcentrismo`: Centrismo en perspectiva masculina
- `asimetria`: Tratamiento desigual en el lenguaje
- `infantilizacion`: Tratamiento infantil hacia las mujeres
- `denominacion_sexualizada`: Referencias sexualizadas innecesarias
- `denominacion_redundante`: Adjetivos redundantes por género
- `denominacion_dependiente`: Referencias dependientes del género
- `masculino_generico`: Uso del masculino como genérico
- `dual_aparente`: Dualidad aparente en el tratamiento
- `hombre_humanidad`: Uso de "hombre" para referirse a la humanidad
- `cargos_mujeres`: Enfoque en cargos ocupados por mujeres
- `sexismo_social`: Reflejo de sexismo social en el lenguaje
- `comparacion_mujeres_hombres`: Comparaciones explícitas de género
- `criterios_excepcion_noticiabilidad`: Criterios excepcionales para noticias de mujeres

### **Fuentes**
- `nombre_fuente`: Nombres de las fuentes citadas
- `genero_fuente`: Género de las fuentes
- `tipo_fuente`: Tipo de fuente (oficial, experta, ciudadana, etc.)

---

## 📈 **Puntuación del Desafío**

### **Cálculo de Puntuación:**
- **Precisión**: % de variables correctamente identificadas
- **Cobertura**: % de sesgos detectados vs total existente
- **Puntuación Total**: Promedio ponderado de ambas métricas

### **Pesos por Categoría:**
- **Contenido General**: 40% (más visible)
- **Lenguaje**: 40% (requiere análisis detallado)
- **Fuentes**: 20% (más técnico)

---

## 🏆 **Niveles de Logro**

- **90-100%**: 🥇 **Experto** - "Eres un experto en análisis de sesgos"
- **75-89%**: 🥈 **Avanzado** - "Tienes un buen ojo para detectar sesgos"
- **60-74%**: 🥉 **Intermedio** - "Sigue practicando para mejorar"
- **0-59%**: 📚 **Principiante** - "La práctica hace al maestro"

---

## 🔍 **Ejemplos de Análisis**

### **Texto Fácil:**
> "María es la primera mujer CEO de la empresa"
- ✅ **Sesgo evidente**: "primera mujer" (excepcionalidad)
- ✅ **Fácil de detectar**: Redundante y estereotípico

### **Texto Medio:**
> "Los deportistas masculinos compiten en categorías de peso, mientras que las deportistas femeninas tienen categorías separadas"
- ⚠️ **Sesgo sutil**: "deportistas" vs "deportistas" (aparentemente igual)
- ⚠️ **Desequilibrio**: Tratamiento diferente implícito

### **Texto Difícil:**
> "La implementación de políticas de diversidad requiere un análisis exhaustivo de los factores socioeconómicos que influyen en la representación equitativa"
- 🔍 **Sesgo encubierto**: Lenguaje aparentemente neutral
- 🔍 **Complejo**: Requiere análisis profundo del contexto

---

## 🔍 **Ejemplos de Variables de Lenguaje**

### **Infantilización:**
- ❌ "La pequeña María" (vs "María")
- ❌ "Se comportó como una niña" (vs "Se comportó de manera inmadura")

### **Denominación Sexualizada:**
- ❌ "La atractiva directora" (vs "La directora")
- ❌ "La hermosa científica" (vs "La científica")

### **Denominación Redundante:**
- ❌ "Mujer doctora" (vs "Doctora")
- ❌ "Hombre enfermero" (vs "Enfermero")

### **Masculino Genérico:**
- ❌ "Los ciudadanos" (vs "La ciudadanía")
- ❌ "Todos los trabajadores" (vs "Todas las personas trabajadoras")

### **Dual Aparente:**
- ❌ "A pesar de ser mujer, es competente" (vs "Es competente")
- ❌ "Aunque es joven, tiene experiencia" (vs "Tiene experiencia")

### **Hombre Humanidad:**
- ❌ "El hombre ha evolucionado" (vs "La humanidad ha evolucionado")
- ❌ "Los derechos del hombre" (vs "Los derechos humanos")

### **Cargos Mujeres:**
- ❌ "Es la primera mujer en..." (vs "Es la primera persona en...")
- ❌ "Rompieron el techo de cristal" (vs "Ocuparon el cargo")

### **Sexismo Social:**
- ❌ "Es muy agresiva para ser mujer" (vs "Es muy agresiva")
- ❌ "No es muy femenina" (vs "Tiene su propio estilo")

### **Comparación Mujeres-Hombres:**
- ❌ "Las mujeres son más emocionales que los hombres" (vs "Las personas tienen diferentes formas de expresar emociones")
- ❌ "Los hombres son más racionales" (vs "Las personas tienen diferentes estilos de pensamiento")

### **Criterios Excepción Noticiabilidad:**
- ❌ "Es noticia porque es mujer" (vs "Es noticia por su logro")
- ❌ "Es excepcional para una mujer" (vs "Es excepcional")

---

*Este sistema de dificultad está diseñado para proporcionar una experiencia de aprendizaje progresiva en el análisis de sesgos de género en medios de comunicación.*
