import mysql.connector
import difflib

# Configura la conexión a tu base de datos
conn = mysql.connector.connect(
    host="192.168.1.129",        # cambia por tu host
    user="root",       # cambia por tu usuario
    password="Winner2020",  # cambia por tu password
    database="infoprepost"       # cambia por tu base de datos
)
cursor = conn.cursor(dictionary=True)

# Leer los dos registros
cursor.execute("SELECT * FROM reporte_detalle WHERE u_id IN (14, 16)")
rows = cursor.fetchall()
data = {row["u_id"]: row for row in rows}
registro1 = data.get(14, {})
registro2 = data.get(16, {})

# Comparador HTML
html_diff = difflib.HtmlDiff(tabsize=4, wrapcolumn=100)

# HTML base
html_output = """
<html>
<head>
<meta charset="utf-8">
<title>Comparación reporte_detalle (u_id=14 vs u_id=16)</title>
<style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    h2 { background: #f0f0f0; padding: 5px; }
    table.diff { font-family: Courier; border: medium; }
    .diff_header { background-color: #e0e0e0 }
    .diff_next { background-color: #c0c0c0 }
    .diff_add { background-color: #aaffaa }
    .diff_chg { background-color: #ffff77 }
    .diff_sub { background-color: #ffaaaa }
</style>
</head>
<body>
<h1>Comparación de registros (u_id=14 vs u_id=16)</h1>
"""

# Recorrer campos
for campo in registro1.keys():
    if campo == "u_id":
        continue

    # Convertir todo a str para evitar errores
    val1 = str(registro1.get(campo) or "").strip()
    val2 = str(registro2.get(campo) or "").strip()

    if val1 == val2:
        continue  # campo idéntico

    # Dif por líneas si el contenido es multilínea, si no carácter a carácter
    if "\n" in val1 or "\n" in val2:
        diff_table = html_diff.make_table(
            val1.splitlines(),
            val2.splitlines(),
            fromdesc=f"u_id=14 ({campo})",
            todesc=f"u_id=16 ({campo})",
            context=True,
            numlines=3
        )
    else:
        diff_table = html_diff.make_table(
            list(val1),
            list(val2),
            fromdesc=f"u_id=14 ({campo})",
            todesc=f"u_id=16 ({campo})",
            context=True,
            numlines=20
        )

    html_output += f"<h2>{campo}</h2>\n{diff_table}\n"

html_output += "</body></html>"

# Guardar en archivo
with open("reporte_diff.html", "w", encoding="utf-8") as f:
    f.write(html_output)

print("✅ Reporte generado: reporte_diff.html")

cursor.close()
conn.close()