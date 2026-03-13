# GUI de configuração para edenQuests

import os
import re
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

# ==============================
# Constantes
# ==============================
EMPTY_LABEL = "(vazio)"

# ==============================
# Layout (tamanhos) – ajuste centralizado
# ==============================
WINDOW_WIDTH  = 900
WINDOW_HEIGHT = 600
MIN_WIDTH     = 900
MIN_HEIGHT    = 600

# Lado esquerdo (configurações) e direito (descrição)
LEFT_W        = 300   # largura mínima painel de Configuração/Valor
RIGHT_W       = 500   # largura mínima painel de descrição

LABEL_WRAP    = 200   # wraplength dos rótulos de configuração
COMBO_WIDTH   = 7     # largura dos Combobox em caracteres

# ==============================
# Caminhos
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OPENKORE_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
CONTROL_DIR = os.path.join(OPENKORE_DIR, "control")
PROFILES_DIR = os.path.join(OPENKORE_DIR, "profiles")
CONFIG_FILE = os.path.join(CONTROL_DIR, "config.txt")

if not os.path.isdir(CONTROL_DIR):
    os.makedirs(CONTROL_DIR, exist_ok=True)

# ==============================
# Helpers numéricos
# ==============================
def num_range(start, end_inclusive):
    """Gera {'start', 'start+1', ..., 'end_inclusive'} como strings."""
    return {str(i) for i in range(start, end_inclusive + 1)}

def quest_off(start, end_inclusive):
    """Gera {'start', ..., 'end_inclusive', 'off'} como strings."""
    vals = num_range(start, end_inclusive)
    vals.add("off")
    return vals

# ==============================
# Opções e regras de validação
# ==============================
options = {
    "lvlQuest03": {
        "group": "Arma do Éden I",
        "label": "Nível da Quest [26–32]",
        "desc": "QUEST ARMA DO ÉDEN I - LVL [26-32] \n\nEscolha o nível em que seu personagem vai começar a quest.\nÉ possível fazer apenas a Quest [23-32] ou [33-39].\n26 = (padrão)\noff = Desativa a Quest",
        "default": "26",
        "allowed": quest_off(26, 32),
    },
    "lvlQuest04": {
        "group": "Arma do Éden I",
        "label": "Nível da Quest [33–39]",
        "desc": "QUEST ARMA DO ÉDEN I - LVL [33-39] \n\nEscolha o nível em que seu personagem vai começar a quest.\nÉ possível fazer apenas a Quest [23-32] ou [33-39].\n33 = (padrão)\noff = Desativa a Quest",
        "default": "33",
        "allowed": quest_off(33, 39),
    },
    "armaI": {
        "group": "Arma do Éden I",
        "label": "Arma do Éden I",
        "desc": "ESCOLHA A ARMA DO ÉDEN I \n\nArmas para as classes:\nEspadachim, Noviço, Mercador.\n(https://browiki.org/wiki/Equipamentos_do_Éden#Armas) \n\nOpções: \n0 = Espada / Cetro (padrão)\n1 = Sabre / Maça",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "lvlQuest05": {
        "group": "Arma do Éden II",
        "label": "Nível da Quest [40–49]",
        "desc": "QUEST ARMA DO ÉDEN II - LVL [40-49] \n\nEscolha o nível em que seu personagem vai começar a quest.\nÉ possível fazer apenas a Quest [40-49] ou [75+].\n40 = (padrão)\noff = Desativa a Quest",
        "default": "40",
        "allowed": quest_off(40, 49),
    },
    "lvlQuest07": {
        "group": "Arma do Éden II",
        "label": "Nível da Quest [75+] ",
        "desc": "QUEST ARMA DO ÉDEN II - LVL [75+] \n\nEscolha o nível em que seu personagem vai começar a quest.\nÉ possível fazer apenas a Quest [40-49] ou [75+].\n75 = (padrão)\noff = Desativa a Quest\n\nObservação: Essa Quest é redundante, pois é possível adquirir a Arma III no nível 60.",
        "default": "75",
        "allowed": quest_off(75, 99),
    },
    "armaII": {
        "group": "Arma do Éden II",
        "label": "Arma do Éden II",
        "desc": "ESCOLHA A ARMA DO ÉDEN II \n\nArmas para as classes: \nEspadachim, Cavaleiro, Templário, Noviço, Sacerdote, Monge, Mercador, Ferreiro, Alquimista, Espiritualista.\n(https://browiki.org/wiki/Equipamentos_do_Éden#Armas) \n\nOpções: \n0 = Sabre / Cetro / Adaga (padrão) \n1 = Espada / Maça / Cetro",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "lvlQuest08": {
        "group": "Arma do Éden III",
        "label": "Nível da Quest [60–69]",
        "desc": "QUEST ARMA DO ÉDEN III - LVL [60-69] \n\nEscolha o nível em que seu personagem vai começar a Quest.\n60 = (padrão)\noff = Desativa a Quest",
        "default": "60",
        "allowed": quest_off(60, 69),
    },
    "armaIII": {
        "group": "Arma do Éden III",
        "label": "Arma do Éden III",
        "desc": "ESCOLHA A ARMA DO ÉDEN III \n\nArmas para as classes: \nCavaleiro, Templário, Sacerdote, Monge, Sábio, Bardo, Odalisca, Ferreiro, Alquimista, Mercenário, Espiritualista, Ninja.\n(https://browiki.org/wiki/Equipamentos_do_Éden#Armas) \n\nOpções: \n0 = Espada / Cetro / Maça / Arco / Adaga (padrão) \n1 = Sabre / Maça / Dicionário / Soqueira / Violino / Chicote / Katar / Cetro / Humma \n2 = Lança / Dicionário / Machado",
        "default": "0",
        "allowed": {"0", "1", "2"},
    },
    "lvlQuest09": {
        "group": "Encantamentos e Cartas",
        "label": "Nível da Quest [70–79]",
        "desc": "QUEST ENCANTAMENTO - LVL [70-79] \n\nEscolha o nível em que seu personagem vai começar a Quest.\n70 = (padrão)\noff = Desativa a Quest",
        "default": "70",
        "allowed": quest_off(70, 79),
    },
    "encant": {
        "group": "Encantamentos e Cartas",
        "label": "Tipo de Encantamento",
        "desc": "ESCOLHA O ENCANTAMENTO +3% ATQ/ATQM\n\nOpções: \n0 = Ataque Físico (padrão) \n1 = Ataque Mágico",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "lvlQuest10": {
        "group": "Encantamentos e Cartas",
        "label": "Nível da Quest [80–89]",
        "desc": "QUEST DE CARTA - LVL [80-89] \n\nEscolha o nível em que seu personagem vai começar a Quest.\n80 = (padrão)\noff = Desativa a Quest",
        "default": "80",
        "allowed": quest_off(80, 89),
    },
    "carta": {
        "group": "Encantamentos e Cartas",
        "label": "Tipo de Carta",
        "desc": "ESCOLHA AS CARTAS \n\n+20% DMG / +10% MDMG ou +3% HEAL. \n\nOpções: \n0 = Bruto(padrão) \n1 = Planta \n2 = Inseto \n3 = Peixe \n4 = Dragão \n5 = Cura",
        "default": "0",
        "allowed": num_range(0, 5),
    },
    "lvlQuest11": {
        "group": "Encantamentos e Cartas",
        "label": "Nível da Quest [90–99]",
        "desc": "QUEST ENCANTAMENTO COM CARTAS II - LVL [90-99] \n\nEscolha o nível em que seu personagem vai começar a Quest.\n90 = (padrão)\noff = Desativa a Quest",
        "default": "90",
        "allowed": quest_off(90, 99),
    },
    # 100–110
    "quests100": {
        "group": "Quests [100+]",
        "label": "Ativar Quests [100+]",
        "desc": "Permite o personagem fazer as Quests do Éden de nível 100+.\n\nEvite saturar a quantidade de Quests. Seu personagem pode não dar conta.\nComo as Quests anteriores, essas usam telesearch.\nAsa de Mosca (ou relativos) são indispensáveis para conclusão dessas Quests.\nA configuração de autoBuy de consumíveis é de responsabilidade do usuário.\nNão ative essa opção sem items que possibilitam o teleporte.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "magma100_0": {
        "group": "Caverna de Magma [100]",
        "label": "Pesadelo Sombrio",
        "desc": "Localização: Calabouço da Caverna de Magma.\nObjetivo: Derrotar 30 Pesadelos sombrios.\nRecompensa: Exp 160000, Exp Classe 160000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "magma100_1": {
        "group": "Caverna de Magma [100]",
        "label": "Deletério|Exterminador",
        "desc": "Localização: Calabouço da Caverna de Magma.\nObjetivo: Derrotar 30 Deletérios e 30 Exterminadores.\nRecompensa: Exp 160000, Exp Classe 160000, 2 Moedas do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "magma100_2": {
        "group": "Caverna de Magma [100]",
        "label": "Pedra Pome",
        "desc": "Localização: Calabouço da Caverna de Magma.\nObjetivo: Coletar 10 Pedras Pomes.\nRecompensa: Exp 160000, Exp Classe 160000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "gl100_0": {
        "group": "Glast Heim [100]",
        "label": "Carat",
        "desc": "Localização: Glastheim.\nObjetivo: Derrotar 30 Carats.\nRecompensa: Exp 160000, Exp Classe 160000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "gl100_1": {
        "group": "Glast Heim [100]",
        "label": "Arclouse",
        "desc": "Localização: Glastheim.\nObjetivo: Derrotar 30 Arclouse.\nRecompensa: Exp 160000, Exp Classe 160000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "gl100_2": {
        "group": "Glast Heim [100]",
        "label": "Anolian",
        "desc": "Localização: Glastheim.\nObjetivo: Derrotar 30 Anolianos.\nRecompensa: Exp 200000, Exp Classe 200000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "gl100_3": {
        "group": "Glast Heim [100]",
        "label": "Sting",
        "desc": "Localização: Glastheim.\nObjetivo: Derrotar 30 Stings.\nRecompensa: Exp 200000, Exp Classe 200000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "gl100_4": {
        "group": "Glast Heim [100]",
        "label": "Majoruros",
        "desc": "Localização: Glastheim.\nObjetivo: Derrotar 30 Majoruros.\nRecompensa: Exp 260000, Exp Classe 260000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "gl110_5": {
        "group": "Glast Heim [110]",
        "label": "Raydric",
        "desc": "Localização: Glastheim.\nObjetivo: Derrotar 30 Raydrics.\nRecompensa: Exp 300000, Exp Classe 300000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "gl110_6": {
        "group": "Glast Heim [110]",
        "label": "Khalitzburg",
        "desc": "Localização: Glastheim.\nObjetivo: Derrotar 30 Khalitzburgs.\nRecompensa: Exp 300000, Exp Classe 300000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "gl110_7": {
        "group": "Glast Heim [110]",
        "label": "Andarilho",
        "desc": "Localização: Glastheim.\nObjetivo: Derrotar 30 Andarilhos.\nRecompensa: Exp 300000, Exp Classe 300000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "gl110_8": {
        "group": "Glast Heim [110]",
        "label": "Cavaleiro do Abismo",
        "desc": "Localização: Glastheim.\nObjetivo: Derrotar 10 Cavaleiros do Abismo.\nRecompensa: Exp 300000, Exp Classe 300000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "ash100_0": {
        "group": "Ash Vacuum [100]",
        "label": "Pinguicula",
        "desc": "Localização: Campo dos Esplendores.\nObjetivo: Derrotar 30 Pinguiculas.\nRecompensa: Exp 160000, Exp Classe 160000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "ash100_1": {
        "group": "Ash Vacuum [100]",
        "label": "Vespa Vagalume",
        "desc": "Localização: Campo dos Esplendores.\nObjetivo: Derrotar 30 Vespas Vagalume.\nRecompensa: Exp 200000, Exp Classe 200000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "ash100_2": {
        "group": "Ash Vacuum [100]",
        "label": "Leão de Vinhas",
        "desc": "Localização: Campo dos Esplendores.\nObjetivo: Derrotar 1 Leão de Vinhas.\nRecompensa: Exp 260000, Exp Classe 260000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "ash110_3": {
        "group": "Ash Vacuum [110]",
        "label": "Pinguicula Sombria",
        "desc": "Localização: Campo dos Esplendores.\nObjetivo: Derrotar 30 Pinguiculas Sombrias.\nRecompensa: Exp 300000, Exp Classe 300000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "ash110_4": {
        "group": "Ash Vacuum [110]",
        "label": "Nepenthes",
        "desc": "Localização: Montanhas dos Manuka.\nObjetivo: Derrotar 30 Nepenthes.\nRecompensa: Exp 300000, Exp Classe 300000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "ash110_5": {
        "group": "Ash Vacuum [110]",
        "label": "Naga",
        "desc": "Localização: Campo dos Esplendores.\nObjetivo: Derrotar 30 Nagas.\nRecompensa: Exp 300000, Exp Classe 300000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "ash110_6": {
        "group": "Ash Vacuum [110]",
        "label": "Cornus",
        "desc": "Localização: Campo dos Esplendores.\nObjetivo: Derrotar 30 Cornus.\nRecompensa: Exp 300000, Exp Classe 300000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "ash110_7": {
        "group": "Ash Vacuum [110]",
        "label": "Larva Centopeia",
        "desc": "Localização: Montanhas dos Manuka.\nObjetivo: Derrotar 20 Larvas Centopeia.\nRecompensa: Exp 300000, Exp Classe 300000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "ash110_8": {
        "group": "Ash Vacuum [110]",
        "label": "Chifre Místico",
        "desc": "Localização: Campo dos Esplendores.\nObjetivo: Coletar 20 Chifres Místicos.\nRecompensa: Exp 300000, Exp Classe 300000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "aruna100_0": {
        "group": "Arunafeltz [100]",
        "label": "Kobold(Machado|Martelo|Maça)",
        "desc": "Localização: Pradaria Audhumbla.\nObjetivo: Derrotar 20 Kobolds (Machado), 20 Kobolds (Martelo) e 20 Kobolds (Maça).\nRecompensa: Exp 250000, Exp Classe 250000, 2 Moedas do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "aruna100_1": {
        "group": "Arunafeltz [100]",
        "label": "Vento da Colina",
        "desc": "Localização: Planícies de Ida.\nObjetivo: Derrotar 30 Ventos da Colina.\nRecompensa: Exp 150000, Exp Classe 150000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "aruna100_2": {
        "group": "Arunafeltz [100]",
        "label": "Lobo do Deserto",
        "desc": "Localização: Pradaria Audhumbla.\nObjetivo: Derrotar 30 Lobos do Deserto.\nRecompensa: Exp 150000, Exp Classe 150000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "aruna100_3": {
        "group": "Arunafeltz [100]",
        "label": "Cabelo Azul",
        "desc": "Localização: Pradaria Audhumbla.\nObjetivo: Coletar 20 Cabelos azuis.\nRecompensa: Exp 100000, Exp Classe 100000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "aruna100_4": {
        "group": "Arunafeltz [100]",
        "label": "Drosera|Muscipular",
        "desc": "Localização: Campo de Veins.\nObjetivo: Derrotar 30 Droseras e 30 Muscipulares.\nRecompensa: Exp 300000, Exp Classe 300000, 2 Moedas do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "aruna100_5": {
        "group": "Arunafeltz [100]",
        "label": "Magmaring",
        "desc": "Localização: Campo de Veins.\nObjetivo: Derrotar 30 Magmarings.\nRecompensa: Exp 150000, Exp Classe 150000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "aruna100_6": {
        "group": "Arunafeltz [100]",
        "label": "Coração Glacial",
        "desc": "Localização: Caverna de Gelo.\nObjetivo: Derrotar 20 Corações Glaciais.\nRecompensa: Exp 100000, Exp Classe 100000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "aruna100_7": {
        "group": "Arunafeltz [100]",
        "label": "Yeti",
        "desc": "Localização: Caverna de Gelo.\nObjetivo: Derrotar 30 Yetis.\nRecompensa: Exp 150000, Exp Classe 150000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "aruna100_8": {
        "group": "Arunafeltz [100]",
        "label": "Titã de Gelo|Gazeti",
        "desc": "Localização: Caverna de Gelo.\nObjetivo: Derrotar 30 Titãs de Gelo e 10 Gazetis.\nRecompensa: Exp 300000, Exp Classe 300000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "thana110_0": {
        "group": "Torre de Thanatos [110]",
        "label": "Mímico Antigo",
        "desc": "Localização: Torre de Thanatos.\nObjetivo: Derrotar 30 Mímicos Antigos.\nRecompensa: Exp 400000, Exp Classe 400000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "thana110_1": {
        "group": "Torre de Thanatos [110]",
        "label": "Palavra Morta",
        "desc": "Localização: Torre de Thanatos.\nAlvo: Derrotar 30 Palavras Mortas.\nRecompensa: Exp 400000, Exp Classe 400000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "thana110_2": {
        "group": "Torre de Thanatos [110]",
        "label": "Barão Coruja",
        "desc": "Localização: Torre de Thanatos.\nObjetivo: Derrotar 20 Barões Corujas.\nRecompensa: Exp 500000, Exp Classe 500000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "thana110_3": {
        "group": "Torre de Thanatos [110]",
        "label": "Página Sangrenta",
        "desc": "Localização: Torre de Thanatos.\nObjetivo: Coletar 10 Páginas Sangrentas.\nRecompensa: Exp 400000, Exp Classe 400000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "thana110_4": {
        "group": "Torre de Thanatos [110]",
        "label": "Pergaminho Antigo",
        "desc": "Localização: Torre de Thanatos.\nObjetivo: Coletar 10 Pergaminhos Antigos.\nRecompensa: Exp 400000, Exp Classe 400000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "thana110_5": {
        "group": "Torre de Thanatos [110]",
        "label": "Farrapos",
        "desc": "Localização: Torre de Thanatos.\nObjetivo: Coletar 30 Farrapos.\nRecompensa: Exp 400000, Exp Classe 400000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "jupe110_0": {
        "group": "Ruínas de Juperos [110]",
        "label": "Venatu(Laranja|Azul)",
        "desc": "Localização: Calabouço de Juperos.\nObjetivo: Derrotar 20 Venatus (laranjas) e 20 Venatus (azuis).\nRecompensa: Exp 300000, Exp Classe 250000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "jupe110_1": {
        "group": "Ruínas de Juperos [110]",
        "label": "Venatu(Roxo|Verde)",
        "desc": "Localização: Calabouço de Juperos.\nObjetivo: Derrotar 20 Venatus (roxos) e 20 Venatus (verdes).\nRecompensa: Exp 300000, Exp Classe 250000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "jupe110_2": {
        "group": "Ruínas de Juperos [110]",
        "label": "Dimik(Verde|Azul)",
        "desc": "Localização: Calabouço de Juperos.\nObjetivo: Derrotar 10 Dimiks (verdes) e 10 Dimiks (azuis).\nRecompensa: Exp 300000, Exp Classe 250000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "jupe110_3": {
        "group": "Ruínas de Juperos [110]",
        "label": "Dimik(Vermelho|Laranja)",
        "desc": "Localização: Calabouço de Juperos.\nObjetivo: Derrotar 10 Dimiks (vermelhos) e 10 Dimiks (laranjas).\nRecompensa: Exp 300000, Exp Classe 250000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "quests100": {
        "group": "Quests [100+]",
        "label": "Ativar Quests [100+]",
        "desc": "Permite o personagem fazer as Quests do Éden de nível 100+.\n\nEvite saturar a quantidade de Quests. Seu personagem pode não dar conta.\nComo as Quests anteriores, essas usam telesearch.\nAsa de Mosca (ou relativos) são indispensáveis para conclusão dessas Quests.\nA configuração de autoBuy de consumíveis é de responsabilidade do usuário.\nNão ative essa opção sem items que possibilitam o teleporte.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "odin120_0": {
        "group": "Templo de Odin [120]",
        "label": "Skogul",
        "desc": "Localização: Templo de Odin.\nObjetivo: Derrotar 20 Skogul.\nRecompensa: Exp 600000, Exp Classe 600000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "odin120_1": {
        "group": "Templo de Odin [120]",
        "label": "Frus",
        "desc": "Localização: Templo de Odin.\nObjetivo: Derrotar 20 Frus.\nRecompensa: Exp 600000, Exp Classe 600000, 1 Moedas do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "odin120_2": {
        "group": "Templo de Odin [120]",
        "label": "Skeggiold(Azul|Marrom)",
        "desc": "Localização: Templo de Odin.\nObjetivo: Derrotar 5 Skeggiold (Azul) e 5 Skeggiold (Marrom).\nRecompensa: Exp 600000, Exp Classe 600000, 2 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "abyss120_0": {
        "group": "Lago do Abismo [120]",
        "label": "Ferus(Verde|Escarlate)",
        "desc": "Localização: Caverna Subterrânea do Lado do Abismo.\nObjetivo: Derrotar 20 30 Ferus Verde e 30 Ferus Escarlate.\nRecompensa: Exp 500000, Exp Classe 500000, 2 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "abyss120_1": {
        "group": "Lago do Abismo [120]",
        "label": "Acidus(Azul|Dourado)",
        "desc": "Localização: Caverna Subterrânea do Lado do Abismo.\nObjetivo: Derrotar 30 Acidus Azul e 30 Acidus Dourado.\nRecompensa: Exp 500000, Exp Classe 500000, 2 Moedas do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "abyss120_2": {
        "group": "Lago do Abismo [120]",
        "label": "Hydrolancer",
        "desc": "Localização: Caverna Subterrânea do Lado do Abismo.\nObjetivo: Derrotar 1 Hydrolancer.\nRecompensa: Exp 500000, Exp Classe 500000, 1 Moeda do Grupo Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    # Acessórios / equips / consumíveis
    "tipoAcc": {
        "group": "Acessórios [100+]",
        "label": "Tipos de Acessórios",
        "desc": "Escolha qual tipo de acessório (anel e colar) gostaria de resgatar.\nEssa opção determina o tipo de todos os futuros acessórios também.\n\nOpções:\n0 = Forte (str) (padrão) \n1 = Mágico (int) \n2 = Ágil (dex) \n3 = Vital (vit)",
        "default": "0",
        "allowed": {"0", "1", "2", "3"},
    },
    "equips100": {
        "group": "Equipamentos [100]",
        "label": "Ativar Equipamentos [100]",
        "desc": "Permite o personagem fazer troca de moedas por equipamentos do éden de nível 100.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "anelI": {
        "group": "Equipamentos [100]",
        "label": "Anel do Éden I",
        "desc": "Permite o personagem fazer troca de moedas pelo Anel do Éden I.\nCusto: 20 Moedas.\n\nOpções:\n0 = Desativado (padrão) \n1-5 = Ativado (Maior prioridade-Menor prioridade)",
        "default": "0",
        "allowed": num_range(0, 5),
    },
    "colarI": {
        "group": "Equipamentos [100]",
        "label": "Colar do Éden I",
        "desc": "Permite o personagem fazer troca de moedas pelo Colar do Éden I.\nCusto: 20 Moedas.\n\nOpções:\n0 = Desativado (padrão) \n1-5 = Ativado (Maior prioridade-Menor prioridade)",
        "default": "0",
        "allowed": num_range(0, 5),
    },
    "fardaI": {
        "group": "Equipamentos [100]",
        "label": "Farda do Éden I",
        "desc": "Permite o personagem fazer troca de moedas pela Farda do Éden I.\nCusto: 20 Moedas.\n\nOpções:\n0 = Desativado (padrão) \n1-5 = Ativado (Maior prioridade-Menor prioridade)",
        "default": "0",
        "allowed": num_range(0, 5),
    },
    "coturI": {
        "group": "Equipamentos [100]",
        "label": "Coturno do Éden I",
        "desc": "Permite o personagem fazer troca de moedas pelo Coturno do Éden I.\nCusto: 20 Moedas.\n\nOpções:\n0 = Desativado (padrão) \n1-5 = Ativado (Maior prioridade-Menor prioridade)",
        "default": "0",
        "allowed": num_range(0, 5),
    },
    "mantoI": {
        "group": "Equipamentos [100]",
        "label": "Manto do Éden I",
        "desc": "Permite o personagem fazer troca de moedas pelo Manto do Éden I.\nCusto: 20 Moedas.\n\nOpções:\n0 = Desativado (padrão) \n1-5 = Ativado (Maior prioridade-Menor prioridade)",
        "default": "0",
        "allowed": num_range(0, 5),
    },
    "boinaI": {
        "group": "Equipamentos [100]",
        "label": "Boina do Éden I",
        "desc": "Permite o personagem fazer troca de moedas pela Boina do Éden I.\nCusto: 70 Moedas.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "equips115": {
        "group": "Equipamentos [115]",
        "label": "Ativar Equipamentos [115]",
        "desc": "Permite o personagem fazer troca de moedas por equipamentos do éden de nível 115.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "anelII": {
        "group": "Equipamentos [115]",
        "label": "Anel do Éden II",
        "desc": "Permite o personagem fazer troca de moedas pelo Anel do Éden II.\nCusto: 60 Moedas.\n\nOpções:\n0 = Desativado (padrão) \n1-5 = Ativado (Maior prioridade-Menor prioridade)",
        "default": "0",
        "allowed": num_range(0, 5),
    },
    "colarII": {
        "group": "Equipamentos [115]",
        "label": "Colar do Éden II",
        "desc": "Permite o personagem fazer troca de moedas pelo Colar do Éden II.\nCusto: 60 Moedas.\n\nOpções:\n0 = Desativado (padrão) \n1-5 = Ativado (Maior prioridade-Menor prioridade)",
        "default": "0",
        "allowed": num_range(0, 5),
    },
    "fardaII": {
        "group": "Equipamentos [115]",
        "label": "Farda do Éden II",
        "desc": "Permite o personagem fazer troca de moedas pela Farda do Éden II.\nCusto: 60 Moedas.\n\nOpções:\n0 = Desativado (padrão) \n1-5 = Ativado (Maior prioridade-Menor prioridade)",
        "default": "0",
        "allowed": num_range(0, 5),
    },
    "coturII": {
        "group": "Equipamentos [115]",
        "label": "Coturno do Éden II",
        "desc": "Permite o personagem fazer troca de moedas pelo Coturno do Éden II.\nCusto: 60 Moedas.\n\nOpções:\n0 = Desativado (padrão) \n1-5 = Ativado (Maior prioridade-Menor prioridade)",
        "default": "0",
        "allowed": num_range(0, 5),
    },
    "equips130": {
        "group": "Equipamentos [130]",
        "label": "Ativar Equipamentos [130]",
        "desc": "Permite o personagem fazer troca de moedas por equipamentos do éden de nível 130.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "anelIII": {
        "group": "Equipamentos [130]",
        "label": "Anel do Éden III",
        "desc": "Permite o personagem fazer troca de moedas pelo Anel do Éden III.\nCusto: 80 Moedas.\n\nOpções:\n0 = Desativado (padrão) \n1-5 = Ativado (Maior prioridade-Menor prioridade)",
        "default": "0",
        "allowed": num_range(0, 5),
    },
    "colarIII": {
        "group": "Equipamentos [130]",
        "label": "Colar do Éden III",
        "desc": "Permite o personagem fazer troca de moedas pelo Colar do Éden III.\nCusto: 80 Moedas.\n\nOpções:\n0 = Desativado (padrão) \n1-5 = Ativado (Maior prioridade-Menor prioridade)",
        "default": "0",
        "allowed": num_range(0, 5),
    },
    "fardaIII": {
        "group": "Equipamentos [130]",
        "label": "Farda do Éden III",
        "desc": "Permite o personagem fazer troca de moedas pela Farda do Éden III.\nCusto: 80 Moedas.\n\nOpções:\n0 = Desativado (padrão) \n1-5 = Ativado (Maior prioridade-Menor prioridade)",
        "default": "0",
        "allowed": num_range(0, 5),
    },
    "coturIII": {
        "group": "Equipamentos [130]",
        "label": "Coturno do Éden III",
        "desc": "Permite o personagem fazer troca de moedas pelo Coturno do Éden III.\nCusto: 80 Moedas.\n\nOpções:\n0 = Desativado (padrão) \n1-5 = Ativado (Maior prioridade-Menor prioridade)",
        "default": "0",
        "allowed": num_range(0, 5),
    },
    "mantoII": {
        "group": "Equipamentos [130]",
        "label": "Manto do Éden III",
        "desc": "Permite o personagem fazer troca de moedas pelo Manto do Éden III.\nCusto: 80 Moedas.\n\nOpções:\n0 = Desativado (padrão) \n1-5 = Ativado (Maior prioridade-Menor prioridade)",
        "default": "0",
        "allowed": num_range(0, 5),
    },
    "equips145": {
        "group": "Equipamentos [145]",
        "label": "Ativar Equipamentos [145]",
        "desc": "Permite o personagem fazer troca de moedas por equipamentos do éden de nível 145.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "anelIV": {
        "group": "Equipamentos [145]",
        "label": "Anel do Éden IV",
        "desc": "Permite o personagem fazer troca de moedas pelo Anel do Éden IV.\nCusto: 110 Moedas.\n\nOpções:\n0 = Desativado (padrão) \n1-5 = Ativado (Maior prioridade-Menor prioridade)",
        "default": "0",
        "allowed": num_range(0, 5),
    },
    "colarIV": {
        "group": "Equipamentos [145]",
        "label": "Colar do Éden IV",
        "desc": "Permite o personagem fazer troca de moedas pelo Colar do Éden IV.\nCusto: 110 Moedas.\n\nOpções:\n0 = Desativado (padrão) \n1-5 = Ativado (Maior prioridade-Menor prioridade)",
        "default": "0",
        "allowed": num_range(0, 5),
    },
    "fardaIV": {
        "group": "Equipamentos [145]",
        "label": "Farda do Éden IV",
        "desc": "Permite o personagem fazer troca de moedas pela Farda do Éden IV.\nCusto: 110 Moedas.\n\nOpções:\n0 = Desativado (padrão) \n1-5 = Ativado (Maior prioridade-Menor prioridade)",
        "default": "0",
        "allowed": num_range(0, 5),
    },
    "coturIV": {
        "group": "Equipamentos [145]",
        "label": "Coturno do Éden IV",
        "desc": "Permite o personagem fazer troca de moedas pelo Coturno do Éden IV.\nCusto: 110 Moedas.\n\nOpções:\n0 = Desativado (padrão) \n1-5 = Ativado (Maior prioridade-Menor prioridade)",
        "default": "0",
        "allowed": num_range(0, 5),
    },
    "equips160": {
        "group": "Equipamentos [160]",
        "label": "Ativar Equipamentos [160]",
        "desc": "Permite o personagem fazer troca de moedas por equipamentos do éden de nível 160.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "anelV": {
        "group": "Equipamentos [160]",
        "label": "Anel do Éden V",
        "desc": "Permite o personagem fazer troca de moedas pelo Anel do Éden V.\nCusto: 150 Moedas.\n\nOpções:\n0 = Desativado (padrão) \n1-5 = Ativado (Maior prioridade-Menor prioridade)",
        "default": "0",
        "allowed": num_range(0, 5),
    },
    "colarV": {
        "group": "Equipamentos [160]",
        "label": "Colar do Éden V",
        "desc": "Permite o personagem fazer troca de moedas pelo Colar do Éden V.\nCusto: 150 Moedas.\n\nOpções:\n0 = Desativado (padrão) \n1-5 = Ativado (Maior prioridade-Menor prioridade)",
        "default": "0",
        "allowed": num_range(0, 5),
    },
    "fardaV": {
        "group": "Equipamentos [160]",
        "label": "Farda do Éden V",
        "desc": "Permite o personagem fazer troca de moedas pela Farda do Éden V.\nCusto: 150 Moedas.\n\nOpções:\n0 = Desativado (padrão) \n1-5 = Ativado (Maior prioridade-Menor prioridade)",
        "default": "0",
        "allowed": num_range(0, 5),
    },
    "coturV": {
        "group": "Equipamentos [160]",
        "label": "Coturno do Éden V",
        "desc": "Permite o personagem fazer troca de moedas pelo Coturno do Éden V.\nCusto: 150 Moedas.\n\nOpções:\n0 = Desativado (padrão) \n1-5 = Ativado (Maior prioridade-Menor prioridade)",
        "default": "0",
        "allowed": num_range(0, 5),
    },
    "mantoIII": {
        "group": "Equipamentos [160]",
        "label": "Manto do Éden V",
        "desc": "Permite o personagem fazer troca de moedas pelo Manto do Éden V.\nCusto: 150 Moedas.\n\nOpções:\n0 = Desativado (padrão) \n1-5 = Ativado (Maior prioridade-Menor prioridade)",
        "default": "0",
        "allowed": num_range(0, 5),
    },
    "boinaII": {
        "group": "Equipamentos [160]",
        "label": "Boina do Éden II",
        "desc": "Permite o personagem fazer troca de moedas pela Boina do Éden II.\nCusto: 600 Moedas.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "classe1": {
        "group": "1ª Classe",
        "label": "Troca de Classe 1",
        "desc": "Escolha a 1ª classe do seu personagem. (Academia Criatura)\n\nClasses:\n1 = Espadachim\t\t\t\t2 = Mago\n3 = Arqueiro\t\t\t\t4 = Noviço\n5 = Mercador\t\t\t\t6 = Gatuno\n\nOpções:\n0 = Desativado (padrão) \n1-6 = Ativado",
        "default": "0",
        "allowed": num_range(0, 6),
    },
    "classe2": {
        "group": "2ª Classe",
        "label": "Troca de Classe 2",
        "desc": "Escolha a 2ª classe do seu personagem.\nEssa opção habilita todas as evoluções de classe subsequentes. Disponíveis apenas (e evoluções até transclasse) Cavaleiro, Monge e Arruaceiro. \n\nClasses:\n1 = Cavaleiro\t\t\t\t2 = Templário\n1 = Bruxo\t\t\t\t2 = Sábio\n1 = Caçador\t\t\t\t2 = Bardo/Odalisca\n1 = Sacerdote\t\t\t\t2 = Monge\n1 = Ferreiro\t\t\t\t2 = Alquimista\n1 = Mercenário\t\t\t\t2 = Arruaceiro\n\nOpções:\n0 = Desativado (padrão) \n1 = Classe 2-1\t\t\t\t2 = Classe 2-2",
        "default": "0",
        "allowed": num_range(0, 2),
    },
    "lvlClasse2": {
        "group": "2ª Classe",
        "label": "Nível da Classe 2",
        "desc": "Escolha o nível mínimo em que quer que seu personagem faça a quest da 2ª classe.\nEssa configuração vale apenas para 2ª classe.\n\nOpções:\n40 = (padrão)",
        "default": "40",
        "allowed": num_range(40, 50),
    },
    "reborn": {
        "group": "Quest de Renascimento",
        "label": "Renascimento",
        "desc": "Ativar quest 'Renascimento'.\n\nRequisitos:\nNível: 99\n2ª Classe\n1.285.000 Zenys ou 1 Livro Capturado\n\nOpções:\n0 = Desativado (padrão) \n1 = Livro Capturado\n2 = 1.285.000 Zenys",
        "default": "0",
        "allowed": num_range(0, 2),
    },
    "1sPassos": {
        "group": "Quest de Tutorial",
        "label": "Primeiros Passos",
        "desc": "Ativar quest 'Primeiros Passos'.\n\nRecompensas:\n5x Lupa de Iniciante\t\t\t\t5x Suco de Banana\n60x Poção de Aprendiz\t\t\t\t20x Asa de Mosca de Iniciante\n10x Asa de Borboleta de Iniciante\t\t\t\t5x Maçã Dura\n1x Livro de Culinária Iniciante\t\t\t\t1x Erva Vermelha\n1x Maçã\t\t\t\t20x Kit de Culinária Iniciante\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "aulaDeConsu": {
        "group": "Quest de Tutorial",
        "label": "Aula de Consumíveis",
        "desc": "Ativar quest 'Aula de Consumíveis'.\n\nRecompensas:\n30x Poção de Aprendiz\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "aulaDeLoc": {
        "group": "Quest de Tutorial",
        "label": "Aula de Localização",
        "desc": "Ativar quest 'Aula de Localização'.\n\nRecompensas:\n20x Asa de Mosca de Iniciante\n10x Asa de Borboleta de Iniciante\n20x Poção de Aprendiz\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "aulaDeVenda": {
        "group": "Quest de Tutorial",
        "label": "Aula de Venda",
        "desc": "Ativar quest 'Aula de Venda'.\n\nRecompensas:\n10x Asa de Borboleta de Iniciante\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "rota": {
        "group": "Rotas de UP",
        "label": "0-99",
        "desc": "Rota 1:\nprt_fild08 > pay_fild08 > pay_fild07 > pay_fild09 > iz_dun01 > iz_dun02 > moc_fild17 > yuno_fild08 > yuno_fild11 > ve_fild07\n\nRota 2:\nprt_fild08 > pay_fild08 > pay_fild07 > pay_fild09 > gef_fild10 > orcsdun01 > mjolnir_08 > mjolnir_04 > gef_fild08 > gef_fild06\n\nOpções:\n0 = Desativado (padrão) \n1 = Rota 1\n2 = Rota 2",
        "default": "0",
        "allowed": num_range(0, 2),
    },
    "novoMundo": {
        "group": "Quests Misc.",
        "label": "Quest Novo Mundo",
        "desc": "A Agência Pata de Gato está oferecendo um método mais rápido para acessar o Novo Mundo, mas com um pequeno custo inicial, é claro!\n\nRequisitos:\nNível: 80+\nZeny: 50.000\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "trocarPot": {
        "group": "Máquina de Venda",
        "label": "Trocar Eq. Aprendiz por Pots",
        "desc": "Troca equipamentos de Aprendiz por Vale-Armazém, e Vale-Armazém por Poções de Aprendiz na máquina de venda automática para iniciantes no Grupo do Éden, depois de virar 1ª classe.\n\n4x Vale-Armazém = 30x Poção de Aprendiz\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "semAsas": {
        "group": "Consumíveis",
        "label": "Sem Asas de Mosquito",
        "desc": "Desativar compra de Asas de Mosquito nas Quests do Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
    "semPot": {
        "group": "Consumíveis",
        "label": "Sem Poção Laranja",
        "desc": "Desativar compra de Poção Laranja nas Quests do Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "desc": "Desativar compra de Poção Laranja nas Quests do Éden.\n\nOpções:\n0 = Desativado (padrão) \n1 = Ativado",
        "default": "0",
        "allowed": {"0", "1"},
    },
}

# Definição das abas
TAB_DEFS = [
    ("Instrutora Boya", [
        "lvlQuest03", "lvlQuest04", "armaI",
        "lvlQuest05", "lvlQuest07", "armaII",
    ]),
    ("Instrutor Ur", [
        "lvlQuest08", "armaIII",
        "lvlQuest09", "encant",
        "lvlQuest10", "carta",
        "lvlQuest11",
    ]),
    ("Quests 100 - 110", [
        "quests100",
        "magma100_0", "magma100_1", "magma100_2",
        "gl100_0", "gl100_1", "gl100_2", "gl100_3", "gl100_4", "gl110_5", "gl110_6", "gl110_7", "gl110_8",
        "ash100_0", "ash100_1", "ash100_2", "ash110_3", "ash110_4", "ash110_5", "ash110_6", "ash110_7", "ash110_8",
        "aruna100_0", "aruna100_1", "aruna100_2", "aruna100_3", "aruna100_4",
        "aruna100_5", "aruna100_6", "aruna100_7", "aruna100_8",
        "thana110_0", "thana110_1", "thana110_2", "thana110_3", "thana110_4", "thana110_5",
        "jupe110_0", "jupe110_1", "jupe110_2", "jupe110_3",
    ]),
    ("Quests 120 - 140", [
        "quests100",
        "odin120_0", "odin120_1", "odin120_2",
        "abyss120_0", "abyss120_1", "abyss120_2",
    ]),
    ("Equipamentos 100+", [
        "tipoAcc",
        "equips100", "anelI", "colarI", "fardaI", "coturI", "mantoI", "boinaI",
        "equips115", "anelII", "colarII", "fardaII", "coturII",
        "equips130", "anelIII", "colarIII", "fardaIII", "coturIII", "mantoII",
        "equips145", "anelIV", "colarIV", "fardaIV", "coturIV",
        "equips160", "anelV", "colarV", "fardaV", "coturV", "mantoIII", "boinaII",
    ]),
    ("Quests de Classe", [ 
        "1sPassos", "aulaDeConsu", "aulaDeLoc", "aulaDeVenda", "classe1", "classe2", "lvlClasse2", "reborn",
    ]),
    ("Misc.", [ 
        "rota", "novoMundo", "trocarPot",
        "semAsas", "semPot",
    ]),
]

BLOCK_BEGIN = "# --- Configurações do edenQuests --- BEGIN\n"
BLOCK_END   = "\n# --- Configurações do edenQuests --- END"

# ==============================
# Utilidades de arquivo config
# ==============================
def load_existing_values(config_file=CONFIG_FILE):
    """Chaves ausentes aparecem como (vazio)."""
    vals = {k: EMPTY_LABEL for k in options}
    if not os.path.isfile(config_file):
        return vals
    try:
        with open(config_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                s = line.strip()
                if not s or s.startswith("#"):
                    continue
                m = re.match(r"^(\w+)\s+(\S+)$", s)
                if m:
                    k, v = m.group(1), m.group(2)
                    if k in options:
                        vals[k] = v
    except Exception:
        pass
    return vals

def allowed_with_empty(key):
    """(vazio) + valores permitidos para a opção."""
    raw = options[key]["allowed"]
    allowed = [str(v) for v in sorted(raw)]
    return [EMPTY_LABEL] + allowed

def write_block_to_config(lines_to_write, config_file=CONFIG_FILE):
    """Escreve/substitui o bloco no config.txt, ignorando (vazio) e 0."""
    filtered = []
    for k, v in lines_to_write:
        if v not in (EMPTY_LABEL, "0", "", None):
            filtered.append(f"{k} {v}")

    if os.path.isfile(config_file):
        with open(config_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    else:
        content = ""

    pattern = re.compile(re.escape(BLOCK_BEGIN) + r".*?" + re.escape(BLOCK_END), flags=re.DOTALL)
    content_without_block = re.sub(pattern, "", content).strip()
    content_without_block += ("\n" if content_without_block and not content_without_block.endswith("\n") else "")

    if filtered:
        block = [BLOCK_BEGIN, *filtered, BLOCK_END]
        new_content = content_without_block + "\n" + "\n".join(block) + "\n"
    else:
        new_content = content_without_block + ("\n" if content_without_block and not content_without_block.endswith("\n") else "")

    with open(config_file, "w", encoding="utf-8") as f:
        f.write(new_content)


def discover_config_targets():
    """Retorna lista de (nome, caminho) para cada config.txt detectado."""
    targets = [("control", os.path.join(CONTROL_DIR, "config.txt"))]

    if os.path.isdir(PROFILES_DIR):
        for name in sorted(os.listdir(PROFILES_DIR)):
            profile_dir = os.path.join(PROFILES_DIR, name)
            cfg = os.path.join(profile_dir, "config.txt")
            if os.path.isdir(profile_dir) and os.path.isfile(cfg):
                targets.append((name, cfg))

    return targets

# ==============================
# GUI (Tkinter)
# ==============================
class ConfigApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Janela
        self.title("[edenQuests] Configurador ")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(MIN_WIDTH, MIN_HEIGHT)

        # Fundo geral
        self.configure(bg="#e6e6e6")

        self.config_targets = discover_config_targets()
        self.config_files = {name: path for name, path in self.config_targets}
        self.current_config_name = self.config_targets[0][0]
        self.current_config_file = self.config_files[self.current_config_name]

        # Valores atuais lidos do config.txt
        self.current_values = load_existing_values(self.current_config_file)

        # Estruturas internas
        self.inputs = {}          # key -> Combobox (todas as abas)
        self.current_focus_key = None
        self.tab_frames = {}      # título da aba -> infos (left, canvas, desc, etc.)
        self._active_canvas = None

        # Monta a interface e popula as linhas
        self._build_widgets()
        self._populate_rows()

    # --------- UI
    def _build_widgets(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        base_bg  = "#e6e6e6"
        panel_bg = "#f5f5f5"

        # Frames e notebook
        style.configure("App.TFrame",   background=base_bg)
        style.configure("Panel.TFrame", background=panel_bg)
        style.configure("TNotebook",    background=base_bg, borderwidth=0)
        style.configure("TNotebook.Tab", padding=(10, 4), font=("Segoe UI", 9))

        # Labels
        style.configure(
            "Header.TLabel",
            font=("Segoe UI", 11, "bold"),
            background=base_bg,
            foreground="#222",
        )
        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 9, "bold"),
            background=panel_bg,
            foreground="#333",
        )
        style.configure(
            "Key.TLabel",
            font=("Segoe UI", 9),
            background=panel_bg,
            foreground="#222",
        )
        style.configure(
            "Group.TLabel",
            font=("Segoe UI", 9, "bold"),
            background=panel_bg,
            foreground="#555",
        )

        # Combobox estilos
        style.configure("Placeholder.TCombobox", foreground="#888")
        style.configure("Normal.TCombobox",      foreground="#111")

        # Botões
        style.configure("Danger.TButton", foreground="#fff", background="#d9534f")
        style.map("Danger.TButton", background=[("active", "#c9302c")])

        self.option_add("*TCombobox*Listbox.font", ("Segoe UI", 9))

        lbl = ttk.Label(
            self,
            text="[edenQuests] CONFIGURADOR \nInsira/Escolha os valores nos campos. *use (vazio) para limpar configurações*",
            anchor="w",
            style="Header.TLabel",
        )
        lbl.pack(fill="x", padx=16, pady=(12, 8))

        main = ttk.Frame(self, style="App.TFrame")
        main.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        # Notebook ocupando toda a largura (esquerda + descrição)
        self.nb = ttk.Notebook(main)
        self.nb.pack(fill="both", expand=True)
        self.nb.bind("<<NotebookTabChanged>>", self._on_tab_changed)

        first_tab = True

        # ---------- TABS ----------
        for tab_title, key_list in TAB_DEFS:
            tab = ttk.Frame(self.nb, style="Panel.TFrame")
            self.nb.add(tab, text=tab_title)

            # grid dentro da aba: esquerda (lista) e direita (descrição)
            tab.columnconfigure(0, weight=3, minsize=LEFT_W)
            tab.columnconfigure(1, weight=2, minsize=RIGHT_W)
            tab.rowconfigure(0, weight=1)

            # ------- LADO ESQUERDO (lista + scroll) -------
            left_container = ttk.Frame(tab, style="Panel.TFrame")
            left_container.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)

            canvas = tk.Canvas(
                left_container,
                highlightthickness=0,
                bg=panel_bg,
                borderwidth=0,
            )
            vsb = ttk.Scrollbar(left_container, orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=vsb.set)

            canvas.grid(row=0, column=0, sticky="nsew")
            vsb.grid(row=0, column=1, sticky="ns", padx=(3, 0))

            left_container.rowconfigure(0, weight=1)
            left_container.columnconfigure(0, weight=1)

            left = ttk.Frame(canvas, style="Panel.TFrame")
            win_id = canvas.create_window((0, 0), window=left, anchor="nw")

            # coluna 0 preenche, coluna 1 ("Valor") fica à direita
            left.grid_columnconfigure(0, weight=1)
            left.grid_columnconfigure(1, weight=0, minsize=80)

            ttk.Label(left, text="Configuração", style="Title.TLabel").grid(
                row=0, column=0, sticky="w", padx=(2, 6), pady=(2, 6)
            )
            ttk.Label(left, text="Valor", style="Title.TLabel").grid(
                row=0, column=1, sticky="e", padx=(6, 2), pady=(2, 6)
            )

            # --- callback de resize/scrollregion ---
            def _on_left_config(event, c, sb, wid):
                # Reserva SEMPRE um espaço para a barra de rolagem,
                # mesmo se não tiver conteúdo rolável.
                inner_width = max(c.winfo_width() - 20, 50)
                c.itemconfigure(wid, width=inner_width)

                c.configure(scrollregion=c.bbox("all"))
                bbox = c.bbox("all")
                height = (bbox[3] - bbox[1]) if bbox else 0

                if height <= c.winfo_height():
                    # Sem conteúdo rolável: desabilita a barra, mas ela continua ocupando espaço.
                    sb.state(["disabled"])
                    c.yview_moveto(0)
                else:
                    # Conteúdo maior: barra habilitada.
                    sb.state(["!disabled"])

            left.bind(
                "<Configure>",
                lambda event, c=canvas, sb=vsb, wid=win_id: _on_left_config(event, c, sb, wid)
            )

            # Scroll com o mouse
            left.bind("<Enter>", lambda e, c=canvas: self._bind_mousewheel(c))
            left.bind("<Leave>", lambda e: self._unbind_mousewheel())

            # ------- LADO DIREITO (descrição) -------
            right = ttk.Frame(tab, style="Panel.TFrame")
            right.grid(row=0, column=1, sticky="nsew", padx=(4, 4), pady=4)

            ttk.Label(right, text="Descrição da opção selecionada:", style="Title.TLabel").pack(
                anchor="w", padx=8, pady=(6, 2)
            )
            desc = tk.Text(
                right,
                height=10,
                wrap="word",
                font=("Segoe UI", 9),
                bg="white",
                relief="solid",
                borderwidth=1,
            )
            desc.configure(state="disabled", padx=8, pady=6)
            desc.pack(fill="both", expand=True, padx=8, pady=(0, 8))

            # tags de formatação
            desc.tag_configure("h1",   font=("Segoe UI", 10, "bold"))
            desc.tag_configure("bold", font=("Segoe UI", 9,  "bold"))
            desc.tag_configure("mono", font=("Consolas",  9))
            desc.tag_configure("note", foreground="#666")
            desc.tag_configure("link", foreground="#0066cc", underline=True)
            desc.tag_bind("link", "<Enter>", lambda e, d=desc: d.config(cursor="hand2"))
            desc.tag_bind("link", "<Leave>", lambda e, d=desc: d.config(cursor=""))
            desc.tag_bind("link", "<Button-1>", self._on_link_click)


            # guarda referência desta aba
            self.tab_frames[tab_title] = {
                "keys": key_list,
                "tab": tab,
                "left_container": left_container,
                "canvas": canvas,
                "scrollbar": vsb,
                "left": left,
                "win_id": win_id,
                "desc": desc,
            }

            # o primeiro desc vira o "desc atual"
            if first_tab:
                self.desc = desc
                first_tab = False

        # ---------- BOTÕES INFERIORES ----------
        btns = ttk.Frame(self, style="App.TFrame")
        btns.pack(fill="x", padx=16, pady=(0, 12))
        selector = ttk.Frame(btns, style="App.TFrame")
        selector.pack(side="left", padx=(0, 10))

        ttk.Label(selector, text="Perfil:").pack(side="left", padx=(0, 6))
        self.profile_var = tk.StringVar(value=self.current_config_name)
        self.profile_select = ttk.Combobox(
            selector,
            values=[name for name, _ in self.config_targets],
            textvariable=self.profile_var,
            state="readonly",
            width=14,
        )
        self.profile_select.bind("<<ComboboxSelected>>", self._on_profile_change)
        self.profile_select.pack(side="left")

        ttk.Button(btns, text="Restaurar para (vazio)", command=self.restore_default).pack(side="left")
        ttk.Button(btns, text="Salvar e Fechar", command=self.save_and_close).pack(side="right")
        ttk.Button(btns, text="Cancelar", command=self.destroy).pack(side="right", padx=(0, 8))

        self.bind("<Control-s>", lambda e: self.save_and_close())
        self.bind("<Escape>",    lambda e: self.destroy())

    # --------- Scroll
    def _bind_mousewheel(self, canvas):
        bbox = canvas.bbox("all")
        if bbox:
            height = bbox[3] - bbox[1]
        else:
            height = 0
        if height > canvas.winfo_height():
            self._active_canvas = canvas
            self.bind_all("<MouseWheel>", self._on_mousewheel)
        else:
            self._active_canvas = None
            self.unbind_all("<MouseWheel>")

    def _unbind_mousewheel(self):
        self._active_canvas = None
        self.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        if self._active_canvas is not None:
            self._active_canvas.yview_scroll(int(-1 * (event.delta / 20)), "units")

    # --------- Troca de perfil/config.txt
    def _on_profile_change(self, event=None):
        name = self.profile_var.get()
        if name not in self.config_files:
            return

        self.current_config_name = name
        self.current_config_file = self.config_files[name]
        self.current_values = load_existing_values(self.current_config_file)
        self._populate_rows()

    # --------- Troca de aba
    def _on_tab_changed(self, event):
        """Atualiza o Text de descrição para o da aba ativa e mostra a 1ª opção."""
        idx = self.nb.index(self.nb.select())
        tab_title, keys = TAB_DEFS[idx]

        info = self.tab_frames[tab_title]
        self.desc = info["desc"]  # passa a escrever na descrição da aba atual

        if keys:
            self._focus_row(keys[0])

    # --------- Montagem das linhas (todas as abas)
    def _populate_rows(self):
        # limpa tudo abaixo do cabeçalho (linha 0) em TODAS as abas
        for tab_info in self.tab_frames.values():
            left = tab_info["left"]
            for child in left.grid_slaves():
                info = child.grid_info()
                if int(info.get("row", 0)) > 0:
                    child.destroy()

        self.inputs.clear()

        # recria as linhas de cada aba
        for tab_title, tab_info in self.tab_frames.items():
            left = tab_info["left"]
            keys = tab_info["keys"]

            r = 1
            current_group = None

            for key in keys:
                opt = options[key]
                group = opt.get("group")
                label = opt.get("label", key)

                if group and group != current_group:
                    current_group = group
                    lbl_group = ttk.Label(left, text=group, style="Group.TLabel")
                    lbl_group.grid(row=r, column=0, columnspan=2, sticky="w", padx=2, pady=(8, 2))
                    r += 1

                lbl = ttk.Label(
                    left,
                    text=label,
                    style="Key.TLabel",
                    wraplength=LABEL_WRAP,
                    justify="left"
                )
                lbl.grid(row=r, column=0, sticky="w", padx=(4, 6), pady=2)
                lbl.bind("<Button-1>", lambda e, k=key: self._focus_row(k))

                allowed = allowed_with_empty(key)
                cb = ttk.Combobox(left, values=allowed, state="normal", width=COMBO_WIDTH)
                cur = self.current_values.get(key, EMPTY_LABEL)
                cb.set(cur if cur in allowed else EMPTY_LABEL)
                cb.grid(row=r, column=1, sticky="e", padx=(0, 6), pady=2)

                self.inputs[key] = cb
                self._apply_cb_style(key)

                cb.bind("<<ComboboxSelected>>", lambda e, k=key: self._on_value_change(k))
                cb.bind("<FocusIn>",           lambda e, k=key: self._focus_row(k))
                cb.bind("<FocusOut>",          lambda e, k=key: self._validate_field(k))
                cb.bind("<KeyRelease>",        lambda e, k=key: self._on_typing(k))

                r += 1

        # foco inicial na primeira opção da primeira aba
        if TAB_DEFS and TAB_DEFS[0][1]:
            self._focus_row(TAB_DEFS[0][1][0])

    # --------- Interações / Estilos dinâmicos
    def _apply_cb_style(self, key):
        cb = self.inputs[key]
        val = cb.get().strip()
        if val == EMPTY_LABEL:
            cb.configure(style="Placeholder.TCombobox")
        else:
            cb.configure(style="Normal.TCombobox")

    def _on_typing(self, key):
        self._apply_cb_style(key)

    def _focus_row(self, key):
        self.current_focus_key = key
        text = options[key]["desc"]
        self._set_desc(text, allowed_with_empty(key), key)

    def _on_value_change(self, key):
        self._validate_field(key)
        self._focus_row(key)
        self._apply_cb_style(key)

    def _validate_field(self, key):
        cb = self.inputs[key]
        val = cb.get().strip()
        allowed = set(allowed_with_empty(key))
        if val not in allowed:
            messagebox.showerror(
                "Valor inválido",
                f"Valor '{val}' não é permitido para '{key}'.\nPermitidos: {sorted(allowed)}"
            )
            cb.set(EMPTY_LABEL)
            val = EMPTY_LABEL
        self.current_values[key] = val
        self._apply_cb_style(key)

    # ---- LINKS NA DESCRIÇÃO ----
    def _insert_with_links(self, text):
        """Insere o texto na caixa de descrição, detectando URLs."""
        pattern = re.compile(r"(https?://[^\s)]+)")
        pos = 0

        for m in pattern.finditer(text):
            if m.start() > pos:
                self.desc.insert("end", text[pos:m.start()])

            url = m.group(1)
            self.desc.insert("end", url, ("link",))
            pos = m.end()

        if pos < len(text):
            self.desc.insert("end", text[pos:])

    def _on_link_click(self, event):
        """Abre no navegador o link clicado dentro do Text da aba atual."""
        d = self.desc
        index = d.index("@%d,%d" % (event.x, event.y))
        ranges = list(d.tag_ranges("link"))
        for i in range(0, len(ranges), 2):
            start = ranges[i]
            end = ranges[i + 1]
            if d.compare(index, ">=", start) and d.compare(index, "<", end):
                url = d.get(start, end)
                webbrowser.open_new(url)
                break

    def _set_desc(self, description, allowed_list=None, var_name=None):
        """
        Atualiza a área de descrição com:
        - título "Descrição"
        - texto da descrição (com URLs clicáveis)
        - linha de valores permitidos
        - linha 'Variável: <nome>'
        - bloco de observação
        """
        self.desc.configure(state="normal")
        self.desc.delete("1.0", "end")

        self.desc.insert("1.0", "Descrição\n", "h1")
        self.desc.mark_set("insert", "end")
        self._insert_with_links(description)
        self.desc.insert("end", "\n\n")

        if allowed_list is not None:
            self.desc.insert("end", "Valores permitidos: ", "bold")
            self.desc.insert("end", ", ".join(allowed_list) + "\n\n", "mono")

            if var_name is not None:
                self.desc.insert("end", "Variável: ", "bold")
                self.desc.insert("end", var_name + " \n")

            self.desc.insert("end", "\n\nObservação:\n", "note")
            self.desc.insert("end", "{vazio} limpa o valor da variável no config.txt.\n", "note")
            self.desc.insert("end", "{0} não será salvo no config.txt, por ser um valor padrão.\n", "note")
            self.desc.insert("end", "A opção padrão será usada para variáveis não configuradas.", "note")

        self.desc.configure(state="disabled")

    def restore_default(self):
        k = self.current_focus_key
        if not k or k not in self.inputs:
            return
        self.inputs[k].set(EMPTY_LABEL)
        self.current_values[k] = EMPTY_LABEL
        self._apply_cb_style(k)
        self._focus_row(k)

    def save_and_close(self):
        lines = []
        for key in options:
            if key in self.inputs:
                self._validate_field(key)
                val = self.inputs[key].get().strip()
            else:
                val = self.current_values.get(key, EMPTY_LABEL)
            lines.append((key, val))
        try:
            write_block_to_config(lines, self.current_config_file)
        except Exception as e:
            messagebox.showerror(
                "Erro ao salvar",
                f"Falha ao escrever no arquivo:\n{self.current_config_file}\n\n{e}",
            )
            return
        messagebox.showinfo("Sucesso", f"Configurações salvas em:\n{self.current_config_file}")
        self.destroy()

# ==============================
# Run
# ==============================
def main():
    app = ConfigApp()
    app.mainloop()

if __name__ == "__main__":
    main()
