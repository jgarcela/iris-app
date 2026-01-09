#!/bin/bash

# Script para detener los servidores (Web y API)

echo "=========================================="
echo "  Deteniendo servidores"
echo "=========================================="
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Detener API
API_PID=$(pgrep -f "python3.11 -m api")
if [ ! -z "$API_PID" ]; then
    echo -e "${YELLOW}Deteniendo API (PID: $API_PID)...${NC}"
    kill $API_PID 2>/dev/null || true
    sleep 2
    # Si aún está corriendo, forzar
    if pgrep -f "python3.11 -m api" > /dev/null; then
        echo "Forzando detención de API..."
        pkill -9 -f "python3.11 -m api" 2>/dev/null || true
    fi
    echo -e "${GREEN}✓${NC} API detenida"
else
    echo -e "${RED}✗${NC} API no estaba corriendo"
fi

# Detener WEB
WEB_PID=$(pgrep -f "python3.11 -m web")
if [ ! -z "$WEB_PID" ]; then
    echo -e "${YELLOW}Deteniendo WEB (PID: $WEB_PID)...${NC}"
    kill $WEB_PID 2>/dev/null || true
    sleep 2
    # Si aún está corriendo, forzar
    if pgrep -f "python3.11 -m web" > /dev/null; then
        echo "Forzando detención de WEB..."
        pkill -9 -f "python3.11 -m web" 2>/dev/null || true
    fi
    echo -e "${GREEN}✓${NC} WEB detenida"
else
    echo -e "${RED}✗${NC} WEB no estaba corriendo"
fi

echo ""
echo "=========================================="
echo "  Servidores detenidos"
echo "=========================================="

