import tkinter as tk
from tkinter import ttk, messagebox
import math
from scipy.stats import chi2

# --- CLASE PARA MANEJAR LA SALIDA DE TEXTO EN LAS PESTAÑAS ---
class ConsolaTab:
    def __init__(self, widget_texto):
        self.tw = widget_texto
        # --- COLORES ADAPTADOS AL NUEVO TEMA SLATE ---
        self.tw.tag_config('titulo', foreground='#38bdf8', font=('Consolas', 11, 'bold'))
        self.tw.tag_config('subtitulo', foreground='#cbd5e1', font=('Consolas', 10, 'bold'))
        self.tw.tag_config('exito', foreground='#4ade80', font=('Consolas', 10, 'bold'))
        self.tw.tag_config('error', foreground='#f87171', font=('Consolas', 10, 'bold'))
        self.tw.tag_config('dato', foreground='#f8fafc')

    def print(self, texto="", tag=None):
        self.tw.configure(state='normal')
        if tag:
            self.tw.insert(tk.END, texto + "\n", tag)
        else:
            self.tw.insert(tk.END, texto + "\n")
        self.tw.configure(state='disabled')
        self.tw.see(tk.END)

    def limpiar(self):
        self.tw.configure(state='normal')
        self.tw.delete('1.0', tk.END)
        self.tw.configure(state='disabled')

# =========================================================
# --- FUNCIONES DE LÓGICA (INTACTAS) ---
# =========================================================

def prueba_medias(lista_ri, z, alpha, consola):
    consola.print("="*60, 'titulo')
    consola.print("   PRUEBA DE MEDIAS", 'titulo')
    consola.print("="*60, 'titulo')

    n = len(lista_ri)
    promedio = sum(lista_ri) / n
    raiz_12n = math.sqrt(12 * n)
    error_estandar = 1 / raiz_12n
    margen = z * error_estandar

    li = 0.5 - margen
    ls = 0.5 + margen

    consola.print("\n--- DATOS Y CÁLCULOS ---", 'subtitulo')
    consola.print(f"   1. N: {n}")
    consola.print(f"   2. Promedio: {promedio:.8f}")
    consola.print(f"   3. Z: {z}")
    consola.print(f"   4. Raíz(12n): {raiz_12n:.8f}")

    consola.print("-" * 40)
    consola.print("--- RESULTADOS ---", 'subtitulo')
    consola.print(f"   Límite Inferior: {li:.8f}")
    consola.print(f"   Límite Superior: {ls:.8f}")
    consola.print("-" * 40)

    if li <= promedio <= ls:
        consola.print("   CONCLUSIÓN: APROBADO ✅", 'exito')
        return True
    else:
        consola.print("   CONCLUSIÓN: RECHAZADO ❌", 'error')
        return False

def prueba_varianza(lista_ri, alpha, consola):
    consola.print("="*60, 'titulo')
    consola.print("   PRUEBA DE VARIANZA", 'titulo')
    consola.print("="*60, 'titulo')

    n = len(lista_ri)
    gl = n - 1
    promedio = sum(lista_ri) / n
    suma_diferencias = sum((x - promedio) ** 2 for x in lista_ri)
    varianza = suma_diferencias / gl

    coef_inferior = chi2.ppf(1 - alpha / 2, gl)
    coef_superior = chi2.ppf(alpha / 2, gl)

    val_calculado_1 = coef_inferior / (12 * gl)
    val_calculado_2 = coef_superior / (12 * gl)

    valor_mayor = max(val_calculado_1, val_calculado_2)
    valor_menor = min(val_calculado_1, val_calculado_2)

    consola.print("\n--- DATOS ---", 'subtitulo')
    consola.print(f"   1. Varianza: {varianza:.8f}")
    consola.print(f"   2. Grados Libertad: {gl}")

    consola.print("-" * 40)
    consola.print("--- TABLA CHI CUADRADA ---", 'subtitulo')
    consola.print(f"   Coeficiente Inferior: {coef_inferior:.6f}")
    consola.print(f"   Coeficiente Superior: {coef_superior:.6f}")

    consola.print("-" * 40)
    consola.print("--- RESULTADOS (LÍMITES) ---", 'subtitulo')
    consola.print(f"   Límite Inferior (Resultado Mayor): {valor_mayor:.8f}")
    consola.print(f"   Límite Superior (Resultado Menor): {valor_menor:.8f}")
    consola.print("-" * 40)

    if valor_menor <= varianza <= valor_mayor:
        consola.print("   CONCLUSIÓN: APROBADO ✅", 'exito')
        return True
    else:
        consola.print("   CONCLUSIÓN: RECHAZADO ❌", 'error')
        return False

def prueba_chi_cuadrada(lista_ri, alpha, consola):
    consola.print("="*85, 'titulo')
    consola.print("   PRUEBA DE CHI-CUADRADA (DISTRIBUCIÓN)", 'titulo')
    consola.print("="*85, 'titulo')

    n = len(lista_ri)
    m_exact = math.sqrt(n)
    num_intervalos = int(m_exact)
    ancho = 1 / num_intervalos
    expected_val = m_exact

    consola.print(f"\n   Datos: N={n}, M={num_intervalos}, E={expected_val:.8f}\n")

    limites = [round(i * ancho, 2) for i in range(num_intervalos)]
    limites.append(1.00)

    counts = nano * num_intervalos
    for val in lista_ri:
        for i in range(num_intervalos):
            lower = limites[i]
            upper = limites[i+1]
            if i == num_intervalos - 1:
                if lower <= val <= upper:
                    counts[i] += 1
                    break
            else:
                if lower <= val < upper:
                    counts[i] += 1
                    break

    consola.print("-" * 85)
    consola.print(f"   {'Intervalo':<15} | {'Obs':<8} | {'Esp':<12} | {'(O-E)^2/E':<15}")
    consola.print("-" * 85)

    chi_cuadrada_calc = 0
    for i in range(num_intervalos):
        lower = limites[i]
        upper = limites[i+1]
        oi = counts[i]
        val_chi = ((oi - expected_val) ** 2) / expected_val
        chi_cuadrada_calc += val_chi
        label = f"{lower:.2f} - {upper:.2f}"
        consola.print(f"   {label:<15} | {oi:<8} | {expected_val:<12.8f} | {val_chi:<15.8f}")

    gl = num_intervalos - 1
    if gl < 1: gl = 1
    valor_critico = chi2.ppf(1 - alpha, gl)

    consola.print("-" * 85)
    consola.print(f"   Chi2 Calc (Suma): {chi_cuadrada_calc:.8f} | Chi2 Crítico: {valor_critico:.8f}")

    if chi_cuadrada_calc <= valor_critico:
        consola.print("\n   CONCLUSIÓN: APROBADO ✅", 'exito')
        return True
    else:
        consola.print("\n   CONCLUSIÓN: RECHAZADO ❌", 'error')
        return False

def prueba_kolmogorov_smirnov(lista_ri, base_ks, consola):
    consola.print("="*85, 'titulo')
    consola.print("   PRUEBA DE KOLMOGOROV-SMIRNOV (K-S)", 'titulo')
    consola.print("="*85, 'titulo')

    datos = sorted(lista_ri)
    n = len(datos)
    max_d_plus = -1.0
    max_d_minus = -1.0

    consola.print(f"\n   {'i':<4} | {'Ri(Ord)':<10} | {'i/n':<10} | {'(i-1)/n':<10} | {'D+':<12} | {'D-':<12}")
    consola.print("-" * 85)

    for i in range(1, n + 1):
        ri = datos[i-1]
        val_i_n = i / n
        val_i_minus_1_n = (i - 1) / n
        d_plus = val_i_n - ri
        d_minus = ri - val_i_minus_1_n

        if d_plus > max_d_plus: max_d_plus = d_plus
        if d_minus > max_d_minus: max_d_minus = d_minus
        consola.print(f"   {i:<4} | {ri:<10.6f} | {val_i_n:<10.5f} | {val_i_minus_1_n:<10.5f} | {max(0,d_plus):<12.6f} | {max(0,d_minus):<12.6f}")

    d_max_total = max(max_d_plus, max_d_minus)
    d_critico = base_ks / math.sqrt(n)

    consola.print("-" * 85)
    consola.print(f"   D Máximo: {d_max_total:.6f} | D Crítico: {d_critico:.6f}")

    if d_max_total < d_critico:
        consola.print("\n   CONCLUSIÓN: APROBADO ✅", 'exito')
        return True
    else:
        consola.print("\n   CONCLUSIÓN: RECHAZADO ❌", 'error')
        return False

def prueba_corridas_arriba_abajo(lista_ri, z_critico, consola):
    consola.print("="*60, 'titulo')
    consola.print("   PRUEBA DE CORRIDAS (ARRIBA Y ABAJO)", 'titulo')
    consola.print("="*60, 'titulo')

    n = len(lista_ri)
    secuencia_signos = []

    consola.print(f"\n   {'i':<4} | {'Ri':<10} | {'Ri+1':<10} | {'S'}")
    consola.print("-" * 50)

    for i in range(n - 1):
        actual = lista_ri[i]
        siguiente = lista_ri[i+1]
        if siguiente >= actual:
            signo = 1
            simbolo = "1 (+)"
        else:
            signo = 0
            simbolo = "0 (-)"
        secuencia_signos.append(signo)
        consola.print(f"   {i+1:<4} | {actual:<10.6f} | {siguiente:<10.6f} | {simbolo}")

    corridas_co = 1
    for i in range(len(secuencia_signos) - 1):
        if secuencia_signos[i] != secuencia_signos[i+1]:
            corridas_co += 1

    mu_co = (2 * n - 1) / 3
    var_co = (16 * n - 29) / 90
    sigma_co = math.sqrt(var_co)
    z_calc = (corridas_co - mu_co) / sigma_co
    z_calc_abs = abs(z_calc)

    consola.print("-" * 50)
    consola.print(f"   Corridas (Co): {corridas_co}")
    consola.print(f"   Media (Mu): {mu_co:.6f}")
    consola.print(f"   Varianza: {var_co:.6f}")
    consola.print(f"   Z Calculado (|Z|): {z_calc_abs:.6f}")
    consola.print(f"   Z Crítico: {z_critico:.6f}")

    if z_calc_abs < z_critico:
        consola.print("\n   CONCLUSIÓN: APROBADO ✅", 'exito')
        return True
    else:
        consola.print("\n   CONCLUSIÓN: RECHAZADO ❌", 'error')
        return False

def prueba_poker(lista_ri, alpha, consola):
    consola.print("="*60, 'titulo')
    consola.print("   PRUEBA DE POKER", 'titulo')
    consola.print("="*60, 'titulo')

    n = len(lista_ri)
    conteos_globales = {"TD": 0, "1P": 0, "2P": 0, "TP": 0, "T": 0, "P": 0, "Q": 0}

    consola.print(f"\n   {'i':<5} | {'Ri':<10} | {'Categoría'}")
    consola.print("-" * 40)

    for i, numero in enumerate(lista_ri):
        s_num = "{:.5f}".format(numero).split('.')
        counts = {}
        for char in s_num:
            counts[char] = counts.get(char, 0) + 1
        patron = sorted(counts.values(), reverse=True)

        cat = "Error"
        if patron ==: cat = "TD"
        elif patron ==: cat = "1P"
        elif patron ==:     cat = "2P"
        elif patron ==:     cat = "T"
        elif patron ==:        cat = "TP"
        elif patron ==:        cat = "P"
        elif patron ==:           cat = "Q" 

        conteos_globales[cat] += 1
        consola.print(f"   {i+1:<5} | {numero:.5f}  | {cat}")

    consola.print("\n--- TABLA DE FRECUENCIAS (POKER) ---", 'subtitulo')
    consola.print(f"   {'Categoría':<10} | {'Oi (Obs)':<10} | {'Ei (Esp)':<10} | {'(E-O)^2/E':<15}")
    consola.print("-" * 55)

    probs = {
        "TD": 0.3024, "1P": 0.5040, "2P": 0.1080,
        "T": 0.0720,  "TP": 0.0090, "P": 0.0045, "Q": 0.0001
    }

    chi_total = 0
    orden = ["TD", "1P", "2P", "T", "TP", "P", "Q"]

    for cat in orden:
        oi = conteos_globales[cat]
        ei = probs[cat] * n
        if ei > 0:
            chi_val = ((ei - oi) ** 2) / ei
        else:
            chi_val = 0
        chi_total += chi_val
        consola.print(f"   {cat:<10} | {oi:<10} | {ei:<10.4f} | {chi_val:<15.6f}")

    gl = 6
    valor_critico = chi2.ppf(1 - alpha, gl)

    consola.print("-" * 55)
    consola.print(f"   Chi2 Calc: {chi_total:.6f}")
    consola.print(f"   Valor Crítico (gl={gl}): {valor_critico:.6f}")

    if chi_total < valor_critico:
        consola.print("\n   CONCLUSIÓN: APROBADO ✅", 'exito')
        return True
    else:
        consola.print("\n   CONCLUSIÓN: RECHAZADO ❌", 'error')
        return False

# =========================================================
# --- INTERFAZ GRÁFICA PRINCIPAL REDISEÑADA ---
# =========================================================

class SimuladorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Software de Simulación Profesional - Pruebas Estadísticas")
        self.root.geometry("1080x720")
        
        # --- NUEVA PALETA DE COLORES (Slate Moderno) ---
        color_fondo = "#1e293b"  # Slate 800 (Fondo principal)
        color_panel = "#0f172a"  # Slate 900 (Panel izquierdo más oscuro)
        color_texto = "#f1f5f9"  # Blanco humo para textos
        color_acento = "#0284c7" # Azul profesional
        color_inputs = "#334155" # Slate 700 (Cajas de texto)
        
        self.root.configure(bg=color_fondo)

        style = ttk.Style()
        style.theme_use('clam')

        # Configuración de estilos
        style.configure('TFrame', background=color_fondo)
        style.configure('Side.TFrame', background=color_panel, borderwidth=0)

        style.configure('TLabel', background=color_fondo, foreground=color_texto, font=('Segoe UI', 10))
        style.configure('Side.TLabel', background=color_panel, foreground=color_texto, font=('Segoe UI', 10, 'bold'))

        style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'), background=color_panel, foreground='#38bdf8')

        style.configure('TButton', font=('Segoe UI', 11, 'bold'), background=color_acento, foreground='white', borderwidth=0)
        style.map('TButton', background=[('active', '#0369a1')]) 

        style.configure('TEntry', fieldbackground=color_inputs, foreground='#ffffff', font=('Segoe UI', 10), padding=6, borderwidth=0)
        style.map('TEntry', fieldbackground=[('focus', '#475569')]) 

        style.configure('TCombobox', fieldbackground=color_inputs, foreground='#ffffff', font=('Segoe UI', 10), padding=6, borderwidth=0)
        style.map('TCombobox', fieldbackground=[('readonly', color_inputs)]) 

        style.configure('TNotebook', background=color_fondo, borderwidth=0)
        style.configure('TNotebook.Tab', background=color_panel, foreground='#94a3b8', padding= nano, font=('Segoe UI', 10, 'bold'), borderwidth=0) 
        style.map('TNotebook.Tab', background=[('selected', color_fondo)], foreground=[('selected', '#38bdf8')]) 

        self.crear_widgets(color_panel, color_fondo)

    def crear_widgets(self, color_panel, color_fondo):
        # --- Panel Izquierdo (Inputs Rediseñados con Grid) ---
        panel_izq = ttk.Frame(self.root, padding="25", style='Side.TFrame')
        panel_izq.pack(side=tk.LEFT, fill=tk.Y)

        # Título
        ttk.Label(panel_izq, text="⚙️ CONFIGURACIÓN", style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=(10, 35), sticky="w")

        # Entradas alineadas con Grid
        ttk.Label(panel_izq, text="Semilla (X0):", style='Side.TLabel').grid(row=1, column=0, sticky="w", pady=12, padx=(0,10))
        self.entry_semilla = ttk.Entry(panel_izq, width=14)
        self.entry_semilla.grid(row=1, column=1, sticky="e", pady=12)

        ttk.Label(panel_izq, text="Cantidad (N):", style='Side.TLabel').grid(row=2, column=0, sticky="w", pady=12, padx=(0,10))
        self.entry_cantidad = ttk.Entry(panel_izq, width=14)
        self.entry_cantidad.grid(row=2, column=1, sticky="e", pady=12)

        ttk.Label(panel_izq, text="Confianza:", style='Side.TLabel').grid(row=3, column=0, sticky="w", pady=12, padx=(0,10))
        self.combo_confianza = ttk.Combobox(panel_izq, values=["90%", "95%", "99%"], state="readonly", width=12)
        self.combo_confianza.current(1)
        self.combo_confianza.grid(row=3, column=1, sticky="e", pady=12)

        # Botón Centrado y más amplio
        self.btn_generar = ttk.Button(panel_izq, text="▶ GENERAR Y EVALUAR", command=self.ejecutar)
        self.btn_generar.grid(row=4, column=0, columnspan=2, fill=tk.X, pady=(40, 15), ipady=8)

        # Label de Resumen
        self.lbl_resumen = ttk.Label(panel_izq, text="", font=('Segoe UI', 11, 'bold'), background=color_panel, justify="center")
        self.lbl_resumen.grid(row=5, column=0, columnspan=2, pady=20)

        # --- Panel Derecho (Pestañas de Resultados) ---
        panel_der = ttk.Frame(self.root, padding="15")
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(panel_der)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Crear pestañas con fondo adaptado al nuevo tema
        self.tabs = {}
        nombres_tabs = ["Datos (Ri)", "Medias", "Varianza", "Chi-Cuadrada", "K-S", "Corridas", "Poker", "Resumen Final"]
        
        for nombre in nombres_tabs:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=nombre)
            
            # Fondo de la consola adaptado al color general
            txt = tk.Text(frame, wrap="none", font=("Consolas", 10), bg=color_fondo, fg="#f8fafc", state='disabled', insertbackground='white', borderwidth=0, padx=10, pady=10)
            scroll_y = ttk.Scrollbar(frame, orient="vertical", command=txt.yview)
            scroll_x = ttk.Scrollbar(frame, orient="horizontal", command=txt.xview)
            txt.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
            
            scroll_y.pack(side="right", fill="y")
            scroll_x.pack(side="bottom", fill="x")
            txt.pack(side="left", fill="both", expand=True)
            
            self.tabs[nombre] = ConsolaTab(txt)

    def ejecutar(self):
        try:
            semilla = float(self.entry_semilla.get())
            cantidad = int(self.entry_cantidad.get())
            confianza_str = self.combo_confianza.get()
            
            if cantidad < 2:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 1.")
                return
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa números válidos.")
            return

        for tab in self.tabs.values():
            tab.limpiar()

        nivel = int(confianza_str.replace('%', ''))
        alpha = 1 - (nivel / 100)
        valores_z = {90: 1.645, 95: 1.960, 99: 2.576}
        z = valores_z.get(nivel, 1.960)
        valores_ks = {90: 1.22, 95: 1.36, 99: 1.63}
        base_ks = valores_ks.get(nivel, 1.36)

        xn = semilla
        a = 1103515245.0
        c = 12345.0
        m = 2147483648.0
        lista_ri = []

        consola_datos = self.tabs["Datos (Ri)"]
        consola_datos.print("="*40, 'titulo')
        consola_datos.print("   NÚMEROS GENERADOS (Ri)", 'titulo')
        consola_datos.print("="*40, 'titulo')
        consola_datos.print(f"   {'i':<5} | {'Ri'}")
        consola_datos.print("-" * 20)

        for i in range(cantidad):
            xn = (a * xn + c) % m
            ri = xn / m
            lista_ri.append(ri)
            consola_datos.print(f"   {i+1:<5} | {ri:.5f}")

        p1 = prueba_medias(lista_ri, z, alpha, self.tabs["Medias"])
        p2 = prueba_varianza(lista_ri, alpha, self.tabs["Varianza"])
        p3 = prueba_chi_cuadrada(lista_ri, alpha, self.tabs["Chi-Cuadrada"])
        p4 = prueba_kolmogorov_smirnov(lista_ri, base_ks, self.tabs["K-S"])
        p5 = prueba_corridas_arriba_abajo(lista_ri, z, self.tabs["Corridas"])
        p6 = prueba_poker(lista_ri, alpha, self.tabs["Poker"])

        consola_resumen = self.tabs["Resumen Final"]
        consola_resumen.print("="*60, 'titulo')
        consola_resumen.print("   RESUMEN FINAL DE PRUEBAS", 'titulo')
        consola_resumen.print("="*60, 'titulo')
        
        pruebas = [("1. Medias", p1), ("2. Varianza", p2), ("3. Chi-Cuadrada", p3),
                   ("4. Kolmogorov-S.", p4), ("5. Corridas", p5), ("6. Poker", p6)]
        
        todo_ok = True
        for nombre, paso in pruebas:
            if paso:
                consola_resumen.print(f"   {nombre:<20}: APROBADO ✅", 'exito')
            else:
                consola_resumen.print(f"   {nombre:<20}: RECHAZADO ❌", 'error')
                todo_ok = False

        if todo_ok:
            self.lbl_resumen.config(text="ESTADO: EXCELENTE 🌟\n(Todas las pruebas pasaron)", foreground="#4ade80")
            consola_resumen.print("\n   ESTADO FINAL: EXCELENTE (Pasan todas) 🌟", 'exito')
        else:
            self.lbl_resumen.config(text="ESTADO: ALERTA ⚠️\n(Revisar rechazos)", foreground="#f87171")
            consola_resumen.print("\n   ESTADO FINAL: ALGUNAS FALLAN ⚠️", 'error')

        self.notebook.select(7)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorApp(root)
    root.mainloop()