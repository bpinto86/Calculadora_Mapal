import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Parâmetros de Corte MAPAL", page_icon="⚙️", layout="wide")

html_content = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <title>Parâmetros de Corte MAPAL</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; background-color: #0f172a; color: #f8fafc; }
    </style>
</head>
<body class="p-4 md:p-6">
    <div class="max-w-7xl mx-auto space-y-6">
        <!-- Header com seletor Principal de Operação -->
        <header class="bg-slate-800 p-4 rounded-xl border border-slate-700 flex flex-col md:flex-row justify-between items-center gap-4">
            <h1 class="text-xl font-bold text-white flex items-center gap-2">
                <span>⚙️</span> Parâmetros de Corte MAPAL
            </h1>
            <div class="flex bg-slate-900 p-1 rounded-lg border border-slate-700 text-xs font-semibold">
                <button type="button" onclick="setModo('furacao')" id="modo-furacao" class="px-4 py-2 rounded-md bg-blue-600 text-white transition">Furação</button>
                <button type="button" onclick="setModo('fresagem')" id="modo-fresagem" class="px-4 py-2 rounded-md text-slate-400 hover:text-white transition">Fresagem</button>
            </div>
        </header>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <!-- Painel de Controlo (Esquerda) -->
            <div class="lg:col-span-4 bg-slate-800 p-5 rounded-xl border border-slate-700 space-y-5">
                <h2 class="text-sm font-semibold text-blue-400 uppercase tracking-wider">Configuração da Operação</h2>
                
                <!-- Secção Furação -->
                <div id="painel-furacao" class="space-y-4">
                    <div class="space-y-2">
                        <label class="text-xs font-medium text-slate-300">1. BROCA DE METAL DURO INTEGRAL</label>
                        <select id="broca" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-blue-500" onchange="atualizarCalculo()">
                            <option value="scd661">SCD661 (Tritan-Drill-Steel)</option>
                            <option value="scd621">SCD621 (MEGA-Speed-Drill-Steel)</option>
                        </select>
                    </div>
                </div>

                <!-- Secção Fresagem (Oculta por defeito) -->
                <div id="painel-fresagem" class="space-y-4 hidden">
                    <div class="space-y-2">
                        <label class="text-xs font-medium text-slate-300">1. LINHA DE FRESA OPTIMILL</label>
                        <select id="fresa-modelo" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-blue-500" onchange="atualizarCalculo()">
                            <option value="opti-steel">OptiMill-Steel (HSC/HPC)</option>
                            <option value="opti-alu">OptiMill-Alu</option>
                        </select>
                    </div>

                    <div class="space-y-2">
                        <label class="text-xs font-medium text-slate-300">TIPOLOGIA DE FRESAGEM</label>
                        <select id="fresagem-tipo" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-blue-500" onchange="mudarTipologiaFresagem()">
                            <option value="desbaste">Desbaste (Standard)</option>
                            <option value="acabamento_3d">Acabamento 3D</option>
                            <option value="acabamento_planos">Acabamento Planos</option>
                            <option value="trocoidal">Desbaste Trocoidal</option>
                        </select>
                    </div>

                    <!-- Sub-tipologia Trocoidal (Condicional) -->
                    <div id="sub-trocoidal-container" class="space-y-2 hidden bg-slate-900/60 p-3 rounded-lg border border-slate-700">
                        <label class="text-xs font-medium text-amber-400">DINÂMICA DE DESBASTE TROCOIDAL</label>
                        <select id="fresagem-subtipo" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-xs text-white focus:outline-none focus:border-blue-500" onchange="atualizarCalculo()">
                            <option value="trocoidal_std">Desbaste Trocoidal (Geral)</option>
                            <option value="alta_carga">Desbaste Alta Carga</option>
                            <option value="low_dyn">LOW Dynamics</option>
                            <option value="med_dyn">MEDIUM Dynamics</option>
                        </select>
                    </div>

                    <div class="grid grid-cols-2 gap-3">
                        <div class="space-y-1">
                            <label class="text-[11px] text-slate-400">Z (Dentes)</label>
                            <input type="number" id="fresa-z" value="4" min="1" max="10" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-center text-sm font-bold text-white" oninput="atualizarCalculo()">
                        </div>
                        <div class="space-y-1">
                            <label class="text-[11px] text-slate-400">Nº de Cortes (ae/ap)</label>
                            <input type="text" id="fresa-ae-ap" value="ap: 1xD | ae: 0.1xD" disabled class="w-full bg-slate-900/50 border border-slate-700/50 rounded-lg p-2 text-center text-[11px] text-slate-400">
                        </div>
                    </div>
                </div>

                <!-- Grupo de Materiais (MMG) -->
                <div class="space-y-2">
                    <label class="text-xs font-medium text-slate-300">2. GRUPO DE MATERIAIS (MMG)</label>
                    <select id="grupo" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-blue-500" onchange="atualizarCalculo()">
                        <option value="P1.1">P1.1 — Aços estruturais (< 700 N/mm²)</option>
                        <option value="P1.2" selected>P1.2 — Aços estruturais (< 1200 N/mm²)</option>
                        <option value="P2.1">P2.1 — Aços de têmpera (< 900 N/mm²)</option>
                        <option value="P2.2">P2.2 — Aços de têmpera (< 1400 N/mm²)</option>
                        <option value="P3.1">P3.1 — Aços para ferramentas (< 800 N/mm²)</option>
                        <option value="M1.1">M1.1 — Inoxidáveis austeníticos</option>
                        <option value="K1.1">K1.1 — Ferro fundido lamelar GJL</option>
                    </select>
                </div>

                <!-- Checkbox regra de liga MAPAL -->
                <div id="bloco-liga" class="bg-slate-900 p-3 rounded-lg border border-slate-700/80 space-y-1">
                    <label class="flex items-start gap-2 cursor-pointer text-xs text-slate-300">
                        <input type="checkbox" id="liga-check" class="mt-0.5 rounded bg-slate-800 border-slate-600 text-blue-600 focus:ring-0" onchange="atualizarCalculo()">
                        <span><strong>Soma de elementos de liga > 8%</strong><br><span class="text-[10px] text-amber-400">Regra MAPAL: avança grupo seguinte.</span></span>
                    </label>
                </div>

                <!-- Refrigeração -->
                <div class="space-y-2">
                    <label class="text-xs font-medium text-slate-300">3. REFRIGERAÇÃO</label>
                    <div class="grid grid-cols-4 gap-1 bg-slate-900 p-1 rounded-lg border border-slate-700 text-xs text-center font-medium">
                        <button type="button" onclick="setRefrig('int')" id="ref-int" class="py-2 rounded bg-blue-600 text-white transition">Int</button>
                        <button type="button" onclick="setRefrig('ext')" id="ref-ext" class="py-2 rounded text-slate-400 hover:text-white transition">Ext</button>
                        <button type="button" onclick="setRefrig('mql')" id="ref-mql" class="py-2 rounded text-slate-400 hover:text-white transition">MQL</button>
                        <button type="button" onclick="setRefrig('ar')" id="ref-ar" class="py-2 rounded text-slate-400 hover:text-white transition">Ar</button>
                    </div>
                </div>

                <!-- Diâmetro Pretendido -->
                <div class="space-y-2">
                    <div class="flex justify-between items-center">
                        <label class="text-xs font-medium text-slate-300">4. DIÂMETRO (Ø)</label>
                        <span id="badge-metodo" class="text-[10px] bg-blue-900/60 text-blue-300 px-2 py-0.5 rounded border border-blue-700">Interpolação Linear</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <button onclick="ajustarDiametro(-0.5)" class="bg-slate-700 hover:bg-slate-600 px-3 py-2 rounded-lg text-white font-bold">-</button>
                        <input type="number" id="diametro" value="10.00" step="0.5" min="1" max="50" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-center text-lg font-bold text-white focus:outline-none focus:border-blue-500" oninput="atualizarCalculo()">
                        <button onclick="ajustarDiametro(0.5)" class="bg-slate-700 hover:bg-slate-600 px-3 py-2 rounded-lg text-white font-bold">+</button>
                    </div>
                </div>
            </div>

            <!-- Resultados e Indicadores (Direita) -->
            <div class="lg:col-span-8 space-y-6">
                <!-- Grid de Métricas CNC -->
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div class="bg-slate-800 p-4 rounded-xl border border-slate-700">
                        <span class="text-xs text-slate-400" id="lbl-f-unit">Avanço / Dente (fz)</span>
                        <div class="text-2xl font-bold text-white mt-1" id="res-f">0.0850</div>
                        <span class="text-[10px] text-blue-400" id="lbl-f-unidade">mm/dente</span>
                    </div>
                    <div class="bg-slate-800 p-4 rounded-xl border border-slate-700">
                        <span class="text-xs text-slate-400">Velocidade de Corte</span>
                        <div class="text-2xl font-bold text-white mt-1" id="res-vc">180</div>
                        <span class="text-[10px] text-slate-400">m/min</span>
                    </div>
                    <div class="bg-slate-800 p-4 rounded-xl border border-slate-700">
                        <span class="text-xs text-slate-400">Rotações (Spindle)</span>
                        <div class="text-2xl font-bold text-white mt-1" id="res-n">5729</div>
                        <span class="text-[10px] text-slate-400">rpm</span>
                    </div>
                    <div class="bg-slate-800 p-4 rounded-xl border border-slate-700">
                        <span class="text-xs text-slate-400">Avanço de Trabalho</span>
                        <div class="text-2xl font-bold text-white mt-1" id="res-vf">1948</div>
                        <span class="text-[10px] text-slate-400">mm/min</span>
                    </div>
                </div>

                <!-- Valores auxiliares -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div class="bg-slate-800 p-4 rounded-xl border border-slate-700">
                        <span class="text-xs text-slate-400">Parâmetro A</span>
                        <div class="font-mono text-lg font-bold text-white mt-1" id="val-a">-</div>
                    </div>
                    <div class="bg-slate-800 p-4 rounded-xl border border-slate-700">
                        <span class="text-xs text-slate-400">Parâmetro B</span>
                        <div class="font-mono text-lg font-bold text-white mt-1" id="val-b">-</div>
                    </div>
                    <div class="bg-slate-800 p-4 rounded-xl border border-slate-700">
                        <span class="text-xs text-slate-400">Estado do Cálculo</span>
                        <div class="text-sm font-bold text-emerald-400 mt-1.5" id="val-estado">Ativo</div>
                    </div>
                </div>

                <!-- Tabela de Referência e Gráfico -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="bg-slate-800 p-5 rounded-xl border border-slate-700 space-y-3">
                        <h3 class="text-xs font-semibold text-slate-400 uppercase">Tabela de Referência</h3>
                        <div class="overflow-x-auto">
                            <table class="w-full text-left text-xs">
                                <thead>
                                    <tr class="border-b border-slate-700 text-slate-400">
                                        <th class="pb-2">Ø (mm)</th>
                                        <th class="pb-2" id="th-f-label">f Cat.</th>
                                        <th class="pb-2">RPM (n)</th>
                                        <th class="pb-2">Avanço (v_f)</th>
                                    </tr>
                                </thead>
                                <tbody id="tabela-ref" class="divide-y divide-slate-700/50"></tbody>
                            </table>
                        </div>
                    </div>

                    <div class="bg-slate-800 p-5 rounded-xl border border-slate-700 space-y-3 flex flex-col justify-between">
                        <div class="flex justify-between items-center">
                            <h3 class="text-xs font-semibold text-slate-400 uppercase">Representação Gráfica</h3>
                            <span class="text-[10px] text-slate-400">SVG Interativo</span>
                        </div>
                        <div class="relative w-full h-48 bg-slate-900 rounded-lg border border-slate-700 p-2 flex items-center justify-center">
                            <svg id="svg-grafico" class="w-full h-full" viewBox="0 0 400 180"></svg>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Rodapé -->
        <footer class="bg-slate-800/80 p-4 rounded-xl border border-slate-700/80 flex justify-between items-center text-xs text-slate-400">
            <div>Created by <span class="text-white font-semibold">Bruno Pinto</span></div>
            <div><span>✉️</span> bruno.pinto@alamo-ferramentas.com</div>
        </footer>
    </div>

    <script>
        let modoAtual = 'furacao';
        let refrigAtual = 'int';

        const baseDados = {
            furacao: {
                scd661: {
                    diametros: [4.00, 5.50, 7.50, 10.50, 14.50, 20.00],
                    gruposList: ["P1.1", "P1.2", "P2.1", "P2.2", "P3.1", "M1.1", "K1.1"],
                    grupos: {
                        "P1.1": { vc: {int:115, ext:105, mql:105, ar:100}, f: [0.24, 0.30, 0.37, 0.46, 0.56, 0.65] },
                        "P1.2": { vc: {int:105, ext:85, mql:85, ar:80}, f: [0.30, 0.37, 0.46, 0.58, 0.70, 0.81] },
                        "P2.1": { vc: {int:115, ext:100, mql:100, ar:90}, f: [0.28, 0.35, 0.44, 0.55, 0.66, 0.77] },
                        "P2.2": { vc: {int:80, ext:70, mql:70, ar:60}, f: [0.24, 0.29, 0.36, 0.44, 0.53, 0.61] },
                        "P3.1": { vc: {int:85, ext:75, mql:75, ar:70}, f: [0.25, 0.31, 0.39, 0.49, 0.60, 0.69] },
                        "M1.1": { vc: {int:55, ext:35, mql:35, ar:30}, f: [0.11, 0.14, 0.18, 0.22, 0.27, 0.31] },
                        "K1.1": { vc: {int:185, ext:115, mql:140, ar:100}, f: [0.34, 0.43, 0.55, 0.70, 0.85, 1.00] }
                    }
                },
                scd621: {
                    diametros: [3.00, 4.50, 6.50, 9.50, 14.00, 20.00],
                    gruposList: ["P1.1", "P1.2", "P2.1", "P2.2", "P3.1", "M1.1", "K1.1"],
                    grupos: {
                        "P1.1": { vc: {int:170, ext:155, mql:155, ar:150}, f: [0.13, 0.17, 0.22, 0.29, 0.36, 0.43] },
                        "P1.2": { vc: {int:155, ext:130, mql:130, ar:120}, f: [0.16, 0.21, 0.28, 0.36, 0.45, 0.54] },
                        "P2.1": { vc: {int:170, ext:145, mql:145, ar:130}, f: [0.15, 0.20, 0.26, 0.34, 0.43, 0.51] },
                        "P2.2": { vc: {int:120, ext:100, mql:100, ar:90}, f: [0.13, 0.17, 0.21, 0.27, 0.34, 0.40] },
                        "P3.1": { vc: {int:130, ext:110, mql:110, ar:100}, f: [0.13, 0.18, 0.23, 0.30, 0.39, 0.46] },
                        "M1.1": { vc: {int:65, ext:40, mql:40, ar:35}, f: [0.07, 0.09, 0.12, 0.15, 0.19, 0.23] },
                        "K1.1": { vc: {int:150, ext:105, mql:105, ar:95}, f: [0.14, 0.21, 0.28, 0.38, 0.49, 0.59] }
                    }
                }
            },
            fresagem: {
                opti_steel: {
                    diametros: [6.00, 8.00, 10.00, 12.00, 16.00, 20.00],
                    gruposList: ["P1.1", "P1.2", "P2.1", "P2.2", "P3.1", "M1.1", "K1.1"],
                    grupos: {
                        "P1.1": { vc: {int:220, ext:200, mql:200, ar:180}, fz: [0.04, 0.06, 0.08, 0.10, 0.13, 0.16] },
                        "P1.2": { vc: {int:180, ext:160, mql:160, ar:140}, fz: [0.035, 0.05, 0.07, 0.09, 0.11, 0.14] },
                        "P2.1": { vc: {int:160, ext:140, mql:140, ar:120}, fz: [0.03, 0.045, 0.06, 0.08, 0.10, 0.12] },
                        "P2.2": { vc: {int:120, ext:100, mql:100, ar:90}, fz: [0.025, 0.035, 0.05, 0.065, 0.08, 0.10] },
                        "P3.1": { vc: {int:140, ext:120, mql:120, ar:100}, fz: [0.03, 0.045, 0.06, 0.075, 0.095, 0.12] },
                        "M1.1": { vc: {int:110, ext:90, mql:90, ar:80}, fz: [0.025, 0.035, 0.045, 0.06, 0.075, 0.09] },
                        "K1.1": { vc: {int:200, ext:170, mql:170, ar:150}, fz: [0.045, 0.065, 0.085, 0.11, 0.14, 0.17] }
                    }
                }
            }
        };

        function setModo(modo) {
            modoAtual = modo;
            document.getElementById('modo-furacao').className = modo === 'furacao' ? "px-4 py-2 rounded-md bg-blue-600 text-white transition" : "px-4 py-2 rounded-md text-slate-400 hover:text-white transition";
            document.getElementById('modo-fresagem').className = modo === 'fresagem' ? "px-4 py-2 rounded-md bg-blue-600 text-white transition" : "px-4 py-2 rounded-md text-slate-400 hover:text-white transition";
            
            document.getElementById('painel-furacao').classList.toggle('hidden', modo !== 'furacao');
            document.getElementById('painel-fresagem').classList.toggle('hidden', modo !== 'fresagem');
            document.getElementById('bloco-liga').classList.toggle('hidden', modo === 'fresagem');

            if(modo === 'fresagem') {
                document.getElementById('lbl-f-unit').innerText = "Avanço / Dente (fz)";
                document.getElementById('lbl-f-unidade').innerText = "mm/dente";
                document.getElementById('th-f-label').innerText = "fz Cat.";
            } else {
                document.getElementById('lbl-f-unit').innerText = "Avanço / Rotação";
                document.getElementById('lbl-f-unidade').innerText = "mm/rot";
                document.getElementById('th-f-label').innerText = "f Cat.";
            }
            atualizarCalculo();
        }

        function mudarTipologiaFresagem() {
            const tipo = document.getElementById('fresagem-tipo').value;
            const containerSub = document.getElementById('sub-trocoidal-container');
            containerSub.classList.toggle('hidden', tipo !== 'trocoidal');
            atualizarCalculo();
        }

        function setRefrig(tipo) {
            refrigAtual = tipo;
            ['int', 'ext', 'mql', 'ar'].forEach(t => {
                const btn = document.getElementById(`ref-${t}`);
                btn.className = t === tipo ? "py-2 rounded bg-blue-600 text-white transition" : "py-2 rounded text-slate-400 hover:text-white transition";
            });
            atualizarCalculo();
        }

        function ajustarDiametro(val) {
            const input = document.getElementById('diametro');
            let atual = parseFloat(input.value) || 0;
            input.value = Math.max(1, Math.min(50, atual + val)).toFixed(1);
            atualizarCalculo();
        }

        function atualizarCalculo() {
            const diamPrat = parseFloat(document.getElementById('diametro').value) || 10;
            let grupoKey = document.getElementById('grupo').value;
            const ligaChecked = document.getElementById('liga-check').checked;

            let toolData, diametros, gruposList, fValores, vc;

            if (modoAtual === 'furacao') {
                const brocaKey = document.getElementById('broca').value;
                toolData = baseDados.furacao[brocaKey];
                diametros = toolData.diametros;
                gruposList = toolData.gruposList;

                if (ligaChecked) {
                    let idxG = gruposList.indexOf(grupoKey);
                    if (idxG !== -1 && idxG < gruposList.length - 1) grupoKey = gruposList[idxG + 1];
                }

                const gData = toolData.grupos[grupoKey] || toolData.grupos["P1.2"];
                fValores = gData.f;
                vc = gData.vc[refrigAtual] || gData.vc['int'];
            } else {
                const fresaKey = document.getElementById('fresa-modelo').value;
                const tipologia = document.getElementById('fresagem-tipo').value;
                const subtipo = document.getElementById('fresagem-subtipo').value;
                const z = parseInt(document.getElementById('fresa-z').value) || 4;

                toolData = baseDados.fresagem[fresaKey];
                diametros = toolData.diametros;
                gruposList = toolData.gruposList;

                const gData = toolData.grupos[grupoKey] || toolData.grupos["P1.2"];
                let fzBase = gData.fz;
                vc = gData.vc[refrigAtual] || gData.vc['int'];

                // Fatores multiplicativos de correção consoante a tipologia de fresagem
                let fatorFz = 1.0, fatorVc = 1.0;
                if (tipologia === 'acabamento_3d') { fatorFz = 0.7; fatorVc = 1.2; }
                else if (tipologia === 'acabamento_planos') { fatorFz = 0.8; fatorVc = 1.1; }
                else if (tipologia === 'trocoidal') {
                    fatorVc = 1.3; // Trocoidal permite maior Vc devido ao envolvimento radial reduzido
                    if (subtipo === 'alta_carga') { fatorFz = 1.2; }
                    else if (subtipo === 'low_dyn') { fatorFz = 0.8; }
                    else if (subtipo === 'med_dyn') { fatorFz = 1.0; }
                }

                vc = Math.round(vc * fatorVc);
                fValores = fzBase.map(val => val * fatorFz);
            }

            // Interpolação Linear de Avanço (f ou fz)
            let fCalc = 0, a = 0, b = 0;
            if (diametros.includes(diamPrat)) {
                let idx = diametros.indexOf(diamPrat);
                fCalc = fValores[idx];
            } else {
                let seg = false;
                for (let i = 0; i < diametros.length - 1; i++) {
                    if (diametros[i] <= diamPrat && diamPrat <= diametros[i+1]) {
                        let d1 = diametros[i], d2 = diametros[i+1];
                        let f1 = fValores[i], f2 = fValores[i+1];
                        b = (f2 - f1) / (d2 - d1);
                        a = f1 - b * d1;
                        fCalc = a + b * diamPrat;
                        seg = true;
                        break;
                    }
                }
                if (!seg) {
                    let i = diamPrat < diametros[0] ? 0 : diametros.length - 2;
                    b = (fValores[i+1] - fValores[i]) / (diametros[i+1] - diametros[i]);
                    a = fValores[i] - b * diametros[i];
                    fCalc = a + b * diamPrat;
                }
            }

            document.getElementById('val-a').innerText = a ? a.toFixed(4) : "-";
            document.getElementById('val-b').innerText = b ? b.toFixed(4) : "-";

            const n = (vc * 1000) / (Math.PI * diamPrat);
            let vf = 0;

            if (modoAtual === 'furacao') {
                vf = n * fCalc;
                document.getElementById('res-f').innerText = fCalc.toFixed(4);
            } else {
                const z = parseInt(document.getElementById('fresa-z').value) || 4;
                vf = n * fCalc * z; // vf = n * fz * z
                document.getElementById('res-f').innerText = fCalc.toFixed(4);
            }

            document.getElementById('res-vc').innerText = vc;
            document.getElementById('res-n').innerText = n.toFixed(0);
            document.getElementById('res-vf').innerText = vf.toFixed(0);

            // Tabela
            const tbody = document.getElementById('tabela-ref');
            tbody.innerHTML = '';
            for(let i=0; i<diametros.length; i++) {
                let d = diametros[i];
                let fVal = fValores[i];
                let nRef = (vc * 1000) / (Math.PI * d);
                let vfRef = modoAtual === 'furacao' ? nRef * fVal : nRef * fVal * (parseInt(document.getElementById('fresa-z').value) || 4);
                let highlight = diamPrat === d ? 'bg-blue-900/30 text-blue-300 font-semibold' : '';
                tbody.innerHTML += `<tr class="border-b border-slate-700/50 ${highlight}">
                    <td class="py-2 px-1">Ø ${d.toFixed(1)}</td>
                    <td class="py-2 px-1">${fVal.toFixed(3)}</td>
                    <td class="py-2 px-1">${nRef.toFixed(0)}</td>
                    <td class="py-2 px-1">${vfRef.toFixed(0)}</td>
                </tr>`;
            }

            desenharGrafico(diametros, fValores, diamPrat, fCalc);
        }

        function desenharGrafico(diametros, valores, diamPrat, fCalc) {
            const svg = document.getElementById('svg-grafico');
            const w = 400, h = 180, pad = 30;
            const minX = diametros[0] - 2, maxX = diametros[diametros.length - 1] + 2;
            const minY = 0, maxY = Math.max(...valores) * 1.2;

            const sx = d => pad + (d - minX) / (maxX - minX) * (w - 2 * pad);
            const sy = f => h - pad - (f - minY) / (maxY - minY) * (h - 2 * pad);

            let svgHTML = `<line x1="${pad}" y1="${h-pad}" x2="${w-pad}" y2="${h-pad}" stroke="#475569" stroke-width="1" />
                           <line x1="${pad}" y1="${pad}" x2="${pad}" y2="${h-pad}" stroke="#475569" stroke-width="1" />`;

            let pathD = "";
            for(let i=0; i<diametros.length; i++) {
                let cx = sx(diametros[i]), cy = sy(valores[i]);
                pathD += (i === 0 ? `M ${cx} ${cy}` : ` L ${cx} ${cy}`);
            }
            svgHTML += `<path d="${pathD}" fill="none" stroke="#3b82f6" stroke-width="2" />`;

            for(let i=0; i<diametros.length; i++) {
                svgHTML += `<circle cx="${sx(diametros[i])}" cy="${sy(valores[i])}" r="4" fill="#3b82f6" />`;
            }

            let px = sx(diamPrat), py = sy(fCalc);
            svgHTML += `<line x1="${px}" y1="${h-pad}" x2="${px}" y2="${py}" stroke="#f97316" stroke-dasharray="3,3" stroke-width="1.5" />
                        <line x1="${pad}" y1="${py}" x2="${px}" y2="${py}" stroke="#f97316" stroke-dasharray="3,3" stroke-width="1.5" />
                        <circle cx="${px}" cy="${py}" r="5" fill="#f97316" />
                        <text x="${Math.min(px + 8, w - 70)}" y="${Math.max(py - 8, 20)}" fill="#f8fafc" font-size="10" font-weight="bold">Ø${diamPrat.toFixed(1)}</text>`;

            svg.innerHTML = svgHTML;
        }

        window.onload = atualizarCalculo;
    </script>
</body>
</html>
"""

components.html(html_content, height=950, scrolling=True)
