#!/bin/bash

# Script para actualizar el código desde git (git pull)

echo "=========================================="
echo "  Actualizando código desde git"
echo "=========================================="
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Hacer git pull
echo -e "${YELLOW}Ejecutando git pull...${NC}"
if git pull; then
    echo -e "${GREEN}✓${NC} Código actualizado correctamente"
else
    echo -e "${RED}✗${NC} Error al hacer git pull"
    exit 1
fi
echo ""

# Verificar si hay cambios en requirements
echo -e "${YELLOW}Verificando cambios en dependencias...${NC}"
if git diff HEAD@{1} --name-only 2>/dev/null | grep -q "requirements.txt"; then
    echo "Se detectaron cambios en requirements.txt"
    read -p "¿Instalar nuevas dependencias? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Instalando dependencias de API..."
        pip3.11 install -r api/requirements.txt 2>/dev/null || echo "Advertencia: Error instalando dependencias de API"
        echo "Instalando dependencias de WEB..."
        pip3.11 install -r web/requirements.txt 2>/dev/null || echo "Advertencia: Error instalando dependencias de WEB"
        echo -e "${GREEN}✓${NC} Dependencias instaladas"
    else
        echo "Dependencias no instaladas"
    fi
else
    echo "No hay cambios en requirements.txt"
fi
echo ""

echo "=========================================="
echo -e "${GREEN}✓${NC} Actualización completada"
echo "=========================================="
echo ""
echo "Nota: Si los servidores están corriendo, puedes reiniciarlos con:"
echo "  ./server-stop.sh && ./server-start.sh"
echo ""
