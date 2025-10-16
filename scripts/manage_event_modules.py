#!/usr/bin/env python3
"""
🎯 Event Modules Manager
Script para gestionar módulos de eventos temporales
"""

import subprocess
import sys
import os
from datetime import datetime

def run_command(cmd, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Completado")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def get_current_branch():
    """Obtener la rama actual"""
    try:
        result = subprocess.run("git branch --show-current", shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except:
        return "unknown"

def list_event_modules():
    """Listar módulos de eventos disponibles"""
    print("📋 Módulos de eventos disponibles:")
    try:
        result = subprocess.run("git branch -a | grep feat-", shell=True, capture_output=True, text=True)
        branches = result.stdout.strip().split('\n')
        for branch in branches:
            if branch.strip():
                print(f"  - {branch.strip()}")
    except:
        print("  No se encontraron módulos de eventos")

def activate_module(module_name):
    """Activar un módulo de evento"""
    current_branch = get_current_branch()
    
    if current_branch != "main":
        print(f"❌ Debes estar en la rama 'main' para activar módulos. Rama actual: {current_branch}")
        return False
    
    print(f"🚀 Activando módulo: {module_name}")
    
    # Verificar que el módulo existe
    if not run_command(f"git branch | grep {module_name}", f"Verificando que {module_name} existe"):
        print(f"❌ El módulo {module_name} no existe")
        return False
    
    # Hacer merge
    commit_message = f"feat: Activate {module_name} module - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    if run_command(f"git merge {module_name} --no-ff -m '{commit_message}'", f"Mergeando {module_name}"):
        print(f"✅ Módulo {module_name} activado exitosamente")
        return True
    else:
        print(f"❌ Error al activar {module_name}")
        return False

def deactivate_module():
    """Desactivar el último módulo activado"""
    current_branch = get_current_branch()
    
    if current_branch != "main":
        print(f"❌ Debes estar en la rama 'main' para desactivar módulos. Rama actual: {current_branch}")
        return False
    
    print("🔄 Desactivando último módulo...")
    
    # Obtener el último commit de merge
    try:
        result = subprocess.run("git log --oneline --merges -1", shell=True, capture_output=True, text=True)
        last_merge = result.stdout.strip()
        if "feat:" in last_merge and "module" in last_merge:
            print(f"📝 Último merge encontrado: {last_merge}")
            if run_command("git revert -m 1 HEAD", "Revirtiendo último merge"):
                print("✅ Módulo desactivado exitosamente")
                return True
            else:
                print("❌ Error al desactivar módulo")
                return False
        else:
            print("❌ No se encontró un merge de módulo para revertir")
            return False
    except:
        print("❌ Error al obtener información del último merge")
        return False

def create_module(module_name):
    """Crear un nuevo módulo de evento"""
    current_branch = get_current_branch()
    
    if current_branch != "main":
        print(f"❌ Debes estar en la rama 'main' para crear módulos. Rama actual: {current_branch}")
        return False
    
    print(f"🆕 Creando nuevo módulo: {module_name}")
    
    # Crear branch
    if run_command(f"git checkout -b {module_name}", f"Creando branch {module_name}"):
        print(f"✅ Módulo {module_name} creado exitosamente")
        print(f"📝 Ahora puedes desarrollar tu módulo en la branch {module_name}")
        print(f"💡 Usa los templates en /templates/ para empezar")
        return True
    else:
        print(f"❌ Error al crear módulo {module_name}")
        return False

def show_help():
    """Mostrar ayuda"""
    print("""
🎯 Event Modules Manager

Uso: python scripts/manage_event_modules.py <comando> [argumentos]

Comandos disponibles:
  list                    - Listar módulos disponibles
  activate <nombre>       - Activar un módulo
  deactivate             - Desactivar el último módulo
  create <nombre>        - Crear un nuevo módulo
  help                   - Mostrar esta ayuda

Ejemplos:
  python scripts/manage_event_modules.py list
  python scripts/manage_event_modules.py activate feat-semana-ciencia
  python scripts/manage_event_modules.py deactivate
  python scripts/manage_event_modules.py create feat-concurso-literario
""")

def main():
    """Función principal"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "list":
        list_event_modules()
    elif command == "activate":
        if len(sys.argv) < 3:
            print("❌ Debes especificar el nombre del módulo")
            print("Uso: python scripts/manage_event_modules.py activate <nombre>")
        else:
            activate_module(sys.argv[2])
    elif command == "deactivate":
        deactivate_module()
    elif command == "create":
        if len(sys.argv) < 3:
            print("❌ Debes especificar el nombre del módulo")
            print("Uso: python scripts/manage_event_modules.py create <nombre>")
        else:
            create_module(sys.argv[2])
    elif command == "help":
        show_help()
    else:
        print(f"❌ Comando desconocido: {command}")
        show_help()

if __name__ == "__main__":
    main()
