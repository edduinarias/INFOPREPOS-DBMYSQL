# script_genera_diferencial.py

import sys
import mysql.connector
import difflib

# ✅ Validar que se pasen 2 parámetros (u_id1 y u_id2)
if len(sys.argv) != 3:
    print("Uso: python script_genera_diferencial.py <u_id1> <u_id2>")
    sys.exit(1)

# Capturar los u_id desde los argumentos
try:
    u_id1 = int(sys.argv[1])
    u_id2 = int(sys.argv[2])
except ValueError:
    print("Error: los parámetros deben ser números enteros.")
    sys.exit(1)

# Conexión a la base de datos
conn = mysql.connector.connect(
    host="192.168.1.129",
    user="root",
    password="Winner2020",
    database="infoprepost"
)
cursor = conn.cursor(dictionary=True)

# Leer los dos registros
cursor.execute("SELECT * FROM reporte_detalle WHERE u_id IN (%s, %s)", (u_id1, u_id2))
rows = cursor.fetchall()
data = {row["u_id"]: row for row in rows}
registro1 = data.get(u_id1, {})
registro2 = data.get(u_id2, {})

if not registro1 or not registro2:
    print(f"❌ No se encontraron ambos registros (u_id={u_id1} y u_id={u_id2})")
    sys.exit(1)

# Comparador HTML
html_diff = difflib.HtmlDiff(tabsize=4, wrapcolumn=100)

# HTML base
html_output = f"""
<html>
<head>
<meta charset="utf-8">
<title>Comparación reporte_detalle (u_id={u_id1} vs u_id={u_id2})</title>
<style>
    body {{ font-family: Arial, sans-serif; margin: 20px; }}
    h2 {{ background: #f0f0f0; padding: 5px; }}
    table.diff {{ font-family: Courier; border: medium; }}
    .diff_header {{ background-color: #e0e0e0 }}
    .diff_next {{ background-color: #c0c0c0 }}
    .diff_add {{ background-color: #aaffaa }}
    .diff_chg {{ background-color: #ffff77 }}
    .diff_sub {{ background-color: #ffaaaa }}
</style>
</head>
<body>
<h1>Comparación de registros (u_id={u_id1} vs u_id={u_id2})</h1>
"""

# Comparar campo por campo
for campo in registro1.keys():
    if campo == "u_id":
        continue

    val1 = str(registro1.get(campo) or "").strip()
    val2 = str(registro2.get(campo) or "").strip()

    if val1 == val2:
        continue

    if "\n" in val1 or "\n" in val2:
        diff_table = html_diff.make_table(
            val1.splitlines(),
            val2.splitlines(),
            fromdesc=f"u_id={u_id1} ({campo})",
            todesc=f"u_id={u_id2} ({campo})",
            context=True,
            numlines=3
        )
    else:
        diff_table = html_diff.make_table(
            list(val1),
            list(val2),
            fromdesc=f"u_id={u_id1} ({campo})",
            todesc=f"u_id={u_id2} ({campo})",
            context=True,
            numlines=20
        )

    html_output += f"<h2>{campo}</h2>\n{diff_table}\n"

html_output += "</body></html>"

# Guardar el archivo HTML
output_filename = f"reporte_diff_{u_id1}_vs_{u_id2}.html"
with open(output_filename, "w", encoding="utf-8") as f:
    f.write(html_output)

print(f"✅ Reporte generado: {output_filename}")

cursor.close()
conn.close()

