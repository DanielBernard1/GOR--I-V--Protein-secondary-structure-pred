#!/usr/bin/biopython
import sys
import os

from train_CGI import run_train
from validate_cgi import run_validate

print("Content-type: text/html\n")

import mycgi
from Website_sec_create import run_seclib
from GOR_cgi import run_predict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
form = mycgi.Form()
action = form.getvalue("action")
output_section = ""
GOR_OUTPUT = os.path.join("uploads/temp_seqAndStructure.txt")

if action == "seclib":
    try:
        output, seclib_path = run_seclib(BASE_DIR, form)
        output_section = f"<textarea readonly rows='10' style='width:100%; resize:both;'>{output}</textarea><a href={seclib_path} download style='display:inline-block; margin-top:10px; padding:8px 16px; background:#2c3e50; color:white; border-radius:4px;'>Download</a>"
    except Exception as e:
        output_section = f"<pre>ERROR: {e}</pre>"

elif action == "predict":
    try:
        output, pp_path = run_predict(BASE_DIR, form)
        output_section = f"<textarea readonly rows='10' style='width:100%; resize:both;'>{output}</textarea>"
        output_section += f"<a href='uploads/temp_seqAndStructure.txt' download style='padding:8px 16px; background:#2c3e50; color:white; border-radius:4px; text-decoration:none; margin-top:10px; display:inline-block;'>Prediction</a>"
        if pp_path:
            output_section += f" <br><br><a href='uploads/temp_seqAndStructure_pp.txt' download style='padding:8px 16px; background:#2c3e50; color:white; border-radius:4px; text-decoration:none;'>Post-Processed</a>"
    except Exception as e:
        output_section = f"<pre>ERROR: {e}</pre>"

elif action == "visualise":
    try:
        import subprocess
        pdb_id = form.getvalue("--vis_pdb", "").strip()
        gorout_upload = form.getfile("--vis_gorout")
        if gorout_upload:
            gorout = os.path.join(BASE_DIR, "uploads", "vis_gorout.txt")
            with open(gorout, "wb") as f:
                f.write(gorout_upload)
        else:
            gorout = os.path.join(BASE_DIR, "uploads", "temp_seqAndStructure.txt")
        outdir = os.path.join(BASE_DIR, "uploads")
        subprocess.run([
            sys.executable, os.path.join(BASE_DIR, "visualisediff2.py"),
            "--pdb", pdb_id,
            "--gorout", gorout,
            "--output", outdir
        ], check=True)
        html_file = os.path.join(outdir, f"{pdb_id.upper()}.html")
        with open(html_file) as f:
            content = f.read()
        output_section = content
    except Exception as e:
        output_section = f"<pre>ERROR: {e}</pre>"

elif action == "validate":
    try:
        output = run_validate(BASE_DIR, form)
        values = [""]
        for line in output.splitlines():
            values.append(line.strip())
        output_section = f"""<br><br>
    <h2>Results</h2>
<div style="overflow-x: auto;">
    <table style="border-collapse: collapse; white-space: nowrap; width: 100%;">
        <thead>
            <tr style="background: #2c3e50; color: white;">
                <th style="padding: 8px 12px;">Fold</th>
                <th style="padding: 8px 12px;">Proteins</th>
                <th style="padding: 8px 12px;">Mean Length</th>
                <th style="padding: 8px 12px;">Sum Length</th>
                <th style="padding: 8px 12px;">Sum Predicted</th>
                <th style="padding: 8px 12px;">Q3 Mean</th>
                <th style="padding: 8px 12px;">Q3 Dev</th>
                <th style="padding: 8px 12px;">SOV Mean</th>
                <th style="padding: 8px 12px;">SOV Dev</th>
                <th style="padding: 8px 12px;">qObs H</th>
                <th style="padding: 8px 12px;">qObs E</th>
                <th style="padding: 8px 12px;">qObs C</th>
                <th style="padding: 8px 12px;">SOV H</th>
                <th style="padding: 8px 12px;">SOV E</th>
                <th style="padding: 8px 12px;">SOV C</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="padding: 8px 12px;">validation</td>
                <td style="padding: 8px 12px;">{values[1]}</td>
                <td style="padding: 8px 12px;">{values[2]}</td>
                <td style="padding: 8px 12px;">{values[3]}</td>
                <td style="padding: 8px 12px;">{values[4]}</td>
                <td style="padding: 8px 12px;">{values[5]}</td>
                <td style="padding: 8px 12px;">{values[6]}</td>
                <td style="padding: 8px 12px;">{values[7]}</td>
                <td style="padding: 8px 12px;">{values[8]}</td>
                <td style="padding: 8px 12px;">{values[9]}</td>
                <td style="padding: 8px 12px;">{values[10]}</td>
                <td style="padding: 8px 12px;">{values[11]}</td>
                <td style="padding: 8px 12px;">{values[12]}</td>
                <td style="padding: 8px 12px;">{values[13]}</td>
                <td style="padding: 8px 12px;">{values[14]}</td>
            </tr>
        </tbody>
    </table>
</div>
<a href="uploads/detailedGor.txt" download style="display:inline-block; margin-top:10px; padding:8px 16px; background:#2c3e50; color:white; text-decoration:none; border-radius:4px;">Download</a>"""
    except Exception as e:
        output_section = f"<pre>ERROR: {e}</pre>"

elif action == "train":
    try:
        output, model_path = run_train(BASE_DIR, form)
        output_section = f"<textarea readonly rows='10' style='width:100%; resize:both;'>{output}</textarea><a href={model_path} download style='display:inline-block; margin-top:10px; padding:8px 16px; background:#2c3e50; color:white; border-radius:4px;'>Download</a>"
    except Exception as e:
        output_section = f"<pre>ERROR: {e}</pre>"

elif action == "kfold":
    try:
        from Kfold_cgi import kfold
        output_section = kfold(BASE_DIR, form)
    except Exception as e:
        output_section = f"<pre>ERROR: {e}</pre>"


# ── CSS laden ──
css_path = os.path.join(BASE_DIR, "style.css")
try:
    with open(css_path) as _css:
        css = _css.read()
except Exception:
    css = ""

print(f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>GOR &mdash; propraGruppe15</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
{css}
    </style>
</head>
<body>

<!-- ── Navbar ─────────────────────────────────────── -->
<nav>
    <a class="nav-logo" href="https://bioclient1.bio.ifi.lmu.de/~martinla/propragruppe15/index.html">
        <svg viewBox="0 0 22 22" fill="none" width="20" height="20">
            <ellipse cx="11" cy="11" rx="4"  ry="10" stroke="#2e7d52" stroke-width="1.8" fill="none"/>
            <ellipse cx="11" cy="11" rx="10" ry="4"  stroke="#4caf80" stroke-width="1.8" fill="none"/>
            <circle  cx="11" cy="11" r="2"           fill="#2e7d52"/>
        </svg>
        propraGruppe15
    </a>
    <ul class="nav-links">
        <li><a href="https://bioclient1.bio.ifi.lmu.de/~martinla/propragruppe15/index.html">Home</a></li>
        <li><a href="https://bioclient1.bio.ifi.lmu.de/~martinla/propragruppe15/Solution3/Alignment/Alignment_CGI.py">Alignment</a></li>
        <li><a href="https://bioclient1.bio.ifi.lmu.de/~martinla/propragruppe15/Solution3/GOR/GOR_final/Test2.py" class="active">GOR</a></li>
    </ul>
</nav>

<!-- ── Hero ───────────────────────────────────────── -->
<div class="hero">
    <h1>GOR Prediction</h1>
    <p>GOR I &nbsp;&middot;&nbsp; GOR III &nbsp;&middot;&nbsp; GOR IV</p>
</div>

<!-- ── Content ────────────────────────────────────── -->
<div class="page-wrapper">

    <!-- Sec Library -->
    <p class="section-label">Sec Library</p>
    <div class="card">
        <h2>Sec Library</h2>
        <p>Erstellt eine Sequenz-Struktur-Datenbank aus PDB-IDs via DSSP.</p>
        <form method="post" enctype="multipart/form-data">
            <input type="hidden" name="action" value="seclib">
            <label class="field-label">Protein ID</label>
            <input type="text" name="--id" placeholder="z.B. 2MZ9">
            <label class="field-label">oder ID-Liste (File)</label>
            <input type="file" name="--idlist">
            <button type="submit">Run</button>
        </form>
        {output_section if action == "seclib" else ""}
    </div>

    <!-- Training & Prediction -->
    <p class="section-label">Training &amp; Prediction</p>

    <div class="card">
        <h2>Train</h2>
        <p>Trainiert ein GOR-Modell auf einer Sequenz-Struktur-Datenbank.</p>
        <form method="post" enctype="multipart/form-data">
            <input type="hidden" name="action" value="train">
            <div class="param-grid">
                <div>
                    <label class="field-label">GOR Methode</label>
                    <select name="--method">
                        <option value="1">GOR1</option>
                        <option value="3">GOR3</option>
                        <option value="4">GOR4</option>
                    </select>
                </div>
                <div>
                    <label class="field-label">Database File</label>
                    <input type="file" name="--db">
                </div>
            </div>
            <button type="submit">Run</button>
        </form>
        {output_section if action == "train" else ""}

        <hr class="card-divider">

        <h2>Predict</h2>
        <p>Sagt die Sekund&auml;rstruktur einer Proteinsequenz vorher.</p>
        <form method="post" enctype="multipart/form-data">
            <input type="hidden" name="action" value="predict">
            <div class="param-grid">
                <div>
                    <label class="field-label">GOR Typ</label>
                    <select name="--Gor_type">
                        <option value="--GOR1">GOR1</option>
                        <option value="--GOR3">GOR3</option>
                        <option value="--GOR4">GOR4</option>
                    </select>
                </div>
                <div>
                    <label class="field-label">Custom Model</label>
                    <input type="file" name="--model_file">
                </div>
                <div>
                    <label class="field-label">FASTA (File)</label>
                    <input type="file" name="--fasta">
                </div>
                <div>
                    <label class="field-label">MAF (File)</label>
                    <input type="file" name="--maf">
                </div>
                <div>
                    <label class="field-label">Probabilities</label>
                    <select name="--probabilities">
                        <option value="no">No</option>
                        <option value="yes">Yes</option>
                    </select>
                </div>
                <div>
                    <label class="field-label">&nbsp;</label>
                    <label><input type="checkbox" name="--postprocess" value="yes" style="width:auto;"> Post-Processing</label>
                </div>
            </div>
            <button type="submit">Run</button>
        </form>
        {output_section if action == "predict" else ""}
    </div>

    <!-- Validation -->
    <p class="section-label">Validation</p>

    <div class="card">
        <h2>Validate</h2>
        <p>Vergleicht eine Prediction mit einer Referenzstruktur und berechnet Q3, SOV und weitere Metriken.</p>
        <form method="post" enctype="multipart/form-data">
            <input type="hidden" name="action" value="validate">
            <div class="param-grid">
                <div>
                    <label class="field-label">Prediction</label>
                    <textarea name="--prediction" rows="4"></textarea>
                    <input type="file" name="--prediction_file">
                </div>
                <div>
                    <label class="field-label">Reference</label>
                    <textarea name="--reference" rows="4"></textarea>
                    <input type="file" name="--reference_file">
                </div>
            </div>
            <button type="submit">Run</button>
        </form>
        {output_section if action == "validate" else ""}

        <hr class="card-divider">

        <h2>K-Fold</h2>
        <p>K-Fold Cross-Validation auf einer Datenbank.</p>
        <form method="post" enctype="multipart/form-data">
            <input type="hidden" name="action" value="kfold">
            <div class="param-grid">
                <div>
                    <label class="field-label">GOR Typ</label>
                    <select name="--gorType">
                        <option value="gor1">GOR1</option>
                        <option value="gor3">GOR3</option>
                        <option value="gor4">GOR4</option>
                    </select>
                </div>
                <div>
                    <label class="field-label">Fold Count</label>
                    <input type="number" name="--foldcount" value="5" min="2" max="20">
                </div>
            </div>
            <label class="field-label">Input Database</label>
            <input type="file" name="--input_seclib">
            <button type="submit">Run</button>
        </form>
        {output_section if action == "kfold" else ""}
    </div>

    <!-- 3D Visualisation -->
    <p class="section-label">3D Visualisation</p>

    <div class="card">
        <h2>Struktur-Vergleich</h2>
        <p>Vergleicht GOR-Prediction mit PDB-Referenzstruktur in 3D (JSmol). Erst Predict ausf&uuml;hren.</p>
        <script type="text/javascript" src="jsmol/JSmol.min.js"></script>
        <form method="post" enctype="multipart/form-data">
            <input type="hidden" name="action" value="visualise">
            <div class="param-grid">
                <div>
                    <label class="field-label">PDB-ID</label>
                    <input type="text" name="--vis_pdb" placeholder="z.B. 1a2p" required>
                </div>
                <div>
                    <label class="field-label">GOR-Output (optional)</label>
                    <input type="file" name="--vis_gorout">
                </div>
            </div>
            <button type="submit">Visualise</button>
        </form>
        {output_section if action == "visualise" else ""}
    </div>

    <!-- Performance -->
    <p class="section-label">Performance</p>

    <div class="card">
        <h2>GOR Performance</h2>
        <p>Vergleich der Vorhersagegenauigkeit verschiedener GOR-Varianten.</p>
        <div style="max-width:920px; margin:0 auto;">
            <canvas id="perfChart"></canvas>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
        (function(){{
            const data = [
                {{label:'Reference (PSIPRED)', color:'91,122,94',  means:[.78,.72,.82,.65,.80,.75,.62,.76], sds:[.05,.07,.08,.10,.06,.08,.09,.07]}},
                {{label:'GOR k-fold',          color:'198,164,110', means:[.62,.55,.70,.40,.65,.60,.38,.58], sds:[.08,.10,.12,.15,.09,.11,.14,.10]}},
                {{label:'GOR Whole DB',        color:'110,153,160', means:[.68,.60,.74,.50,.70,.64,.45,.63], sds:[.06,.08,.10,.12,.07,.09,.11,.08]}}
            ];
            new Chart(document.getElementById('perfChart'), {{
                type:'bar',
                data: {{
                    labels:['Q3','SOV','QC','QE','QH','SOVC','SOVE','SOVH'],
                    datasets: data.map(d => ({{
                        label:d.label, data:d.means, sds:d.sds,
                        backgroundColor:`rgba(${{d.color}},.92)`,
                        borderColor:`rgba(${{d.color}},1)`, borderWidth:1
                    }}))
                }},
                options: {{
                    animation:{{duration:1200,easing:'easeOutQuart'}},
                    scales:{{
                        y:{{min:0,max:1,ticks:{{color:'#5b7a5e'}},grid:{{color:'rgba(0,0,0,.06)'}},title:{{display:true,text:'Score',color:'#5b7a5e'}}}},
                        x:{{ticks:{{color:'#5b7a5e'}}}}
                    }},
                    plugins:{{
                        legend:{{labels:{{color:'#2d3a2e',font:{{size:14}}}}}},
                        tooltip:{{callbacks:{{label(c){{return `${{c.dataset.label}}: ${{c.raw.toFixed(2)}} ± ${{c.dataset.sds[c.dataIndex].toFixed(2)}}`}}}}}}
                    }}
                }},
                plugins:[{{id:'eb',afterDraw(ch){{
                    const ctx=ch.ctx;
                    ch.data.datasets.forEach((ds,di)=>{{
                        const meta=ch.getDatasetMeta(di);
                        ctx.save(); ctx.strokeStyle='#444'; ctx.lineWidth=2;
                        meta.data.forEach((bar,i)=>{{
                            const y=ch.scales.y, top=y.getPixelForValue(ds.data[i]+ds.sds[i]), bot=y.getPixelForValue(ds.data[i]-ds.sds[i]);
                            ctx.beginPath();ctx.moveTo(bar.x,top);ctx.lineTo(bar.x,bot);ctx.stroke();
                            [top,bot].forEach(p=>{{ctx.beginPath();ctx.moveTo(bar.x-6,p);ctx.lineTo(bar.x+6,p);ctx.stroke()}});
                        }});
                        ctx.restore();
                    }});
                }}}}]
            }});
        }})();
        </script>
    </div>

</div>

<footer>
    <span>propraGruppe15 &mdash; Bioinformatik-Praktikum &middot; LMU/TUM &middot; Gruppe 15</span>
    <span>Laura Martin &middot; Lucas Nassonov &middot; Daniel Bernadi &middot; Toan David Huynh Ngoc</span>
</footer>

</body>
</html>""")