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
                            <option value="scm942">OptiMill-Tro-Uni (SCM942)</option>
                        </select>
                    </div>

                    <div class="space-y-2">
                        <label class="text-xs font-medium text-slate-300">TIPOLOGIA DE FRESAGEM</label>
                        <select id="fresagem-tipo" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-blue-500" onchange="mudarTipologiaFresagem()">
                            <option value="desbaste">Desbaste (Standard)</option>
                            <option value="acabamento_3d">Acabamento 3D</option>
                            <option value="acabamento_planos">Acabamento Planos</option>
                            <option value="trocoidal" selected>Desbaste Trocoidal</option>
                        </select>
                    </div>

                    <!-- Sub-tipologia Trocoidal (Condicional) -->
                    <div id="sub-trocoidal-container" class="space-y-2 bg-slate-900/60 p-3 rounded-lg border border-slate-700">
                        <label class="text-xs font-medium text-amber-400">DINÂMICA DE DESBASTE TROCOIDAL</label>
                        <select id="fresagem-subtipo" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-xs text-white focus:outline-none focus:border-blue-500" onchange="atualizarCalculo()">
                            <option value="low">LOW Dynamics</option>
                            <option value="med">MEDIUM Dynamics</option>
                            <option value="high">HIGH Dynamics</option>
                        </select>
                    </div>

                    <div class="grid grid-cols-2 gap-3">
                        <div class="space-y-1">
                            <label class="text-[11px] text-slate-400">Z (Dentes)</label>
                            <input type="number" id="fresa-z" value="4" min="1" max="10" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-center text-sm font-bold text-white" oninput="atualizarCalculo()">
                        </div>
                        <div class="space-y-1">
                            <label class="text-[11px] text-slate-400">Nº de Cortes (ae/ap)</label>
                            <input type="text" id="fresa-ae-ap" value="ap: máx | ae: ver cat." disabled class="w-full bg-slate-900/50 border border-slate-700/50 rounded-lg p-2 text-center text-[11px] text-slate-400">
                        </div>
                    </div>
                </div>

                <!-- Grupo de Materiais (MMG) -->
                <div class="space-y-2">
                    <label class="text-xs font-medium text-slate-300">2. GRUPO DE MATERIAIS (MMG)</label>
                    <select id="grupo" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-blue-500" onchange="atualizarCalculo()">
                        <option value="P1.1">P1.1 — Aços estruturais ≤ 0.15% C (420 N/mm²)</option>
                        <option value="P1.2" selected>P1.2 — Aços estruturais ≤ 0.45% C (650 N/mm²)</option>
                        <option value="P2.1">P2.1 — Aços de têmpera (850 N/mm²)</option>
                        <option value="P2.2">P2.2 — Aços de têmpera (900-1000 N/mm²)</option>
                        <option value="P3.1">P3.1 — Aços para ferramentas (600 N/mm²)</option>
                        <option value="M1.1">M1.1 — Inoxidáveis austeníticos</option>
                        <option value="K1.1">K1.1 — Ferro fundido lamelar GJL</option>
