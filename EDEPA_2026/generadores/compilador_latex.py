"""
============================================
MÓDULO: COMPILADOR LaTeX
============================================
Compila archivos .tex a PDF usando pdflatex.
"""
import subprocess
import shutil
from pathlib import Path


def verificar_latex_instalado():
    """
    Verifica si pdflatex está instalado en el sistema.
    
    Returns:
        bool: True si está instalado, False en caso contrario
    """
    return shutil.which("pdflatex") is not None


def compilar_latex(tex_path, output_dir=None, clean=True):
    """
    Compila un archivo .tex a PDF usando pdflatex.
    
    Args:
        tex_path: Ruta al archivo .tex
        output_dir: Directorio de salida (None = mismo directorio del .tex)
        clean: Si True, elimina archivos auxiliares después de compilar
    
    Returns:
        tuple: (success: bool, pdf_path: Path or None, message: str)
    """
    tex_path = Path(tex_path)
    
    if not tex_path.exists():
        return False, None, f"Error: El archivo {tex_path} no existe"
    
    if not verificar_latex_instalado():
        return False, None, "Error: pdflatex no está instalado. Instale una distribución LaTeX (TeX Live, MiKTeX)"
    
    # Determinar directorio de salida
    if output_dir is None:
        output_dir = tex_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Nombre del archivo PDF resultante
    pdf_name = tex_path.stem + ".pdf"
    pdf_path = output_dir / pdf_name
    
    try:
        # Cambiar al directorio del archivo .tex para evitar problemas con rutas relativas
        working_dir = tex_path.parent
        
        # Primera compilación
        print(f"Compilando {tex_path.name}...")
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_path.name],
            cwd=working_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            error_msg = f"Error en la compilación:\n{result.stdout}\n{result.stderr}"
            return False, None, error_msg
        
        # Segunda compilación (para referencias cruzadas)
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_path.name],
            cwd=working_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Verificar que se generó el PDF
        pdf_temp = working_dir / pdf_name
        if not pdf_temp.exists():
            return False, None, "Error: No se generó el archivo PDF"
        
        # Mover PDF al directorio de salida si es diferente
        if output_dir != working_dir:
            shutil.move(str(pdf_temp), str(pdf_path))
        
        # Limpiar archivos auxiliares
        if clean:
            extensions = ['.aux', '.log', '.out', '.toc', '.nav', '.snm']
            for ext in extensions:
                aux_file = working_dir / (tex_path.stem + ext)
                if aux_file.exists():
                    aux_file.unlink()
        
        return True, pdf_path, f"✔ PDF generado: {pdf_path}"
        
    except subprocess.TimeoutExpired:
        return False, None, "Error: Tiempo de compilación excedido"
    except Exception as e:
        return False, None, f"Error inesperado: {str(e)}"



