#!/bin/bash

# Script para verificar el estado de la aplicación (Web y API)

API_HOST="163.117.137.135"
API_PORT="8000"
WEB_HOST="163.117.137.135"
WEB_PORT="8001"

echo "=========================================="
echo "  Verificando estado de la aplicación"
echo "=========================================="
echo ""

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para verificar proceso
check_process() {
    local module=$1
    if pgrep -f "python3.11 -m $module" > /dev/null; then
        local pid=$(pgrep -f "python3.11 -m $module")
        echo -e "${GREEN}✓${NC} Proceso $module está corriendo (PID: $pid)"
        return 0
    else
        echo -e "${RED}✗${NC} Proceso $module NO está corriendo"
        return 1
    fi
}

# Función para verificar puerto
check_port() {
    local host=$1
    local port=$2
    local service=$3
    
    if timeout 2 bash -c "echo > /dev/tcp/$host/$port" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Puerto $port ($service) está escuchando"
        return 0
    else
        echo -e "${RED}✗${NC} Puerto $port ($service) NO está escuchando"
        return 1
    fi
}

# Función para verificar healthcheck HTTP
check_healthcheck() {
    local host=$1
    local port=$2
    local service=$3
    
    response=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 "http://$host:$port/healthcheck" 2>/dev/null)
    
    if [ "$response" = "200" ]; then
        echo -e "${GREEN}✓${NC} Healthcheck $service responde correctamente (HTTP $response)"
        return 0
    else
        echo -e "${RED}✗${NC} Healthcheck $service NO responde (HTTP $response o timeout)"
        return 1
    fi
}

# Verificar procesos
echo "--- Procesos ---"
api_process_ok=$(check_process "api" && echo "ok" || echo "fail")
web_process_ok=$(check_process "web" && echo "ok" || echo "fail")
echo ""

# Verificar puertos
echo "--- Puertos ---"
api_port_ok=$(check_port "$API_HOST" "$API_PORT" "API" && echo "ok" || echo "fail")
web_port_ok=$(check_port "$WEB_HOST" "$WEB_PORT" "WEB" && echo "ok" || echo "fail")
echo ""

# Verificar healthchecks
echo "--- Healthchecks HTTP ---"
api_health_ok=$(check_healthcheck "$API_HOST" "$API_PORT" "API" && echo "ok" || echo "fail")
web_health_ok=$(check_healthcheck "$WEB_HOST" "$WEB_PORT" "WEB" && echo "ok" || echo "fail")
echo ""

# Resumen
echo "=========================================="
echo "  Resumen"
echo "=========================================="

if [ "$api_process_ok" = "ok" ] && [ "$api_port_ok" = "ok" ] && [ "$api_health_ok" = "ok" ]; then
    echo -e "API: ${GREEN}ACTIVA${NC}"
else
    echo -e "API: ${RED}INACTIVA${NC}"
fi

if [ "$web_process_ok" = "ok" ] && [ "$web_port_ok" = "ok" ] && [ "$web_health_ok" = "ok" ]; then
    echo -e "WEB: ${GREEN}ACTIVA${NC}"
else
    echo -e "WEB: ${RED}INACTIVA${NC}"
fi

echo ""
echo "Para ver los logs:"
echo "  - API: tail -f api.log"
echo "  - WEB: tail -f web.log"
echo ""

