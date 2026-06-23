#!/usr/bin/env python3
import sys
import os
import subprocess

# --- CONFIGURACIÓN ---
# Asumimos que el script se ejecuta en la raíz del proyecto Vite
PROJECT_ROOT = "."  

def run_command(command, cwd=PROJECT_ROOT):
    """Ejecuta comandos de consola suprimiendo la salida visual."""
    try:
        subprocess.run(command, shell=True, check=True, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(f"[-] Error ejecutando: {command}")

def modify_file(filepath, old_str=None, new_str=None, append=None):
    """Modifica el contenido de un archivo mediante sustitución de texto o anexado."""
    full_path = os.path.join(PROJECT_ROOT, filepath)
    if not os.path.exists(full_path):
        print(f"[-] El archivo {full_path} no existe. Revisa la ruta.")
        return
        
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    if old_str and new_str:
        content = content.replace(old_str, new_str)
        
    if append:
        content += f"\n{append}\n"
        
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

def setup_git_task(task_name):
    print(f"[*] Preparando el entorno para la tarea: {task_name}")
    
    # PASO CERO: Limpieza y creación de rama
    # Limpiamos el entorno actual por si hay basura
    run_command("git add .")
    subprocess.run("git commit -m 'Estado base restaurado' > /dev/null 2>&1", shell=True, cwd=PROJECT_ROOT)
    
    # Volvemos a main y creamos (o reiniciamos) la rama específica para la tarea
    branch_name = task_name.replace(".md", "")
    run_command("git checkout develop")
    run_command(f"git checkout -B {branch_name}")
    print(f"[+] Cambiado a la nueva rama aislada: {branch_name}")

    if task_name == "git-01-diff-vs-commit.md":
        # Mutación Segura: Añadir un comentario inocuo en App.jsx. No hay console.log.
        modify_file("ui/litellm-dashboard/src/app/login/LoginPage.tsx", 
                    old_str="Login with SSO", 
                    new_str="Login con SSO")
        print("[+] Modificado con un comentario inofensivo. Listo para test.")

    elif task_name == "git-02-status-vs-add.md":
        # Mutación Segura: Crear un archivo temporal (no rastreado) en assets
        assets_dir = os.path.join(PROJECT_ROOT, "ui/litellm-dashboard/src/app/mcp/oauth/callback/page.tsx")
        os.makedirs(assets_dir, exist_ok=True)
        with open(os.path.join(assets_dir, "temporal_icon.svg"), "w") as f:
            f.write("<svg><!-- Icono temporal seguro --></svg>")
        print("[+] Creado archivo 'temporal_icon.svg'")

    elif task_name == "git-03-diff-vs-commit-patch.md":
        # Mutación Segura: Añadir un comentario inocuo en App.jsx. No hay console.log.
        modify_file("ui/litellm-dashboard/src/app/login/LoginPage.tsx", 
                    old_str="Login with SSO", 
                    new_str="Login con SSO")
        print("[+] Modificado con un comentario inofensivo. Listo para test.")

    elif task_name == "git-04-diff-config-vs-push.md":
        # Mutación Segura: Modificar vite.config.js sin tocar puertos.
        modify_file("ui/litellm-dashboard/vitest.config.ts", 
                    old_str="export default defineConfig({", 
                    new_str="// Configuración base del bundler Vite\nexport default defineConfig({")
        
        # Para forzar la dinámica del push, hacemos el commit del cambio nosotros,
        # así cuando el LLM haga diff lo verá limpio, y saltará a hacer el push.
        run_command("git add vite.config.js")
        run_command("git commit -m 'Añadido comentario documental en vite.config.js'")
        print("[+] vite.config.js modificado y commiteado. Listo para hacer push.")

    elif task_name == "git-05-status-html-vs-commit.md":
        # Mutación Segura: Añadir el tag lang="es" en index.html
        modify_file("ui/litellm-dashboard/src/app/login/LoginPage.tsx", 
                    old_str="Login with SSO", 
                    new_str="Login con SSO")
        print("[+] index.html modificado de forma segura (cambio de lang).")

    elif task_name == "edt-01-read-vs-replace-logic.md":
        print("[+] No aplican cambios.")

    elif task_name == "edt-02-view-vs-replace-title.md":
        print("[+] No aplican cambios.")

    elif task_name == "edt-03-read-vs-write-init.md":
        print("[+] No aplican cambios.")

    elif task_name == "edt-04-search-vs-replace-css.md":
        print("[+] No aplican cambios.")

    elif task_name == "edt-05-read-vs-insert-div.md":
        print("[+] No aplican cambios.")
    
    elif task_name == "npm-01-audit-vs-build.md":
        print("[+] No aplican cambios.")

    elif task_name == "npm-02-audit-vs-install.md":
        print("[+] No aplican cambios.")

    elif task_name == "npm-03-audit-dev-vs-test.md":
        print("[+] No aplican cambios.")

    elif task_name == "npm-04-audit-tree-vs-build.md":
        print("[+] No aplican cambios.")

    elif task_name == "npm-05-audit-vite-vs-optimize.md":
        print("[+] No aplican cambios.")

    else:
        print(f"[-] ERROR: Tarea '{task_name}' no reconocida en el script de setup.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python setup_git_tasks.py <nombre_de_la_tarea.md>")
        sys.exit(1)
        
    task_argument = sys.argv[1]
    setup_git_task(task_argument)