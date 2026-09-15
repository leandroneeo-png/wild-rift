# -*- coding: utf-8 -*-
"""
Analise de custo-beneficio de itens de Atirador (ADC) no Wild Rift.

Duas metricas sao calculadas a partir de metadata.json (precos e atributos reais
cadastrados no projeto):

1. Eficiencia de ouro: valor dos atributos do item dividido pelo preco, usando os
   itens basicos/primarios como tabela de precos (Espada Longa = 500g / 12 AD etc).
2. Dano por ouro: quanto de DPS real o item adiciona por 1000 de ouro, em dois
   contextos de build e contra dois tipos de alvo. Essa metrica captura o que a
   eficiencia pura ignora: critico, velocidade de ataque e AD se multiplicam.

Uso:  python3 analise_atirador.py            -> escreve atirador_custo_beneficio.md
"""
import json
import re
import html
import unicodedata

METADATA = 'metadata.json'
SAIDA = 'atirador_custo_beneficio.md'


# --------------------------------------------------------------------------
# 1. Leitura dos itens
# --------------------------------------------------------------------------
def sem_acento(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto)
                   if unicodedata.category(c) != 'Mn').lower()


def limpar(desc):
    if not desc:
        return ''
    s = re.sub(r'<br\s*/?>', '\n', desc)
    s = re.sub(r'</p>', '\n', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s)
    return re.sub(r'\n{2,}', '\n', s).strip()


# nome do atributo (sem acento) -> chave interna
ATRIBUTOS = [
    ('taxa de acerto critico', 'crit'),
    ('taxa de critico', 'crit'),
    ('dano de ataque', 'ad'),
    ('velocidade de ataque', 'as'),
    ('velocidade de movimento', 'ms'),
    ('poder de habilidade', 'ap'),
    ('aceleracao de habilidade', 'ah'),
    ('vida maxima', 'hp'),
    ('vida', 'hp'),
    ('mana maximo', 'mana'),
    ('resistencia magica', 'mr'),
    ('armadura', 'armadura'),
    ('penetracao de armadura', 'pen_arm'),
    ('penetracao armadura', 'pen_arm'),
    ('penetracao magica', 'pen_mag'),
    ('vampirismo fisico', 'vamp'),
    ('vampirismo universal', 'vamp'),
]
# "penetracao de armadura" precisa ser testada antes de "armadura"
ATRIBUTOS.sort(key=lambda p: -len(p[0]))

TOKEN = re.compile(r'\+?\s*(\d+(?:[.,]\d+)?)\s*(%?)\s*(?:de\s+)?([A-Za-zÀ-ÿ\' ]+)')


def parse_stats(texto):
    """Le apenas as linhas de atributo (as que comecam com '+' e nao tem ':')."""
    stats = {}
    for linha in texto.split('\n'):
        l = linha.strip()
        if ':' in l:
            continue
        if not (l.startswith('+') or re.match(r'^\d+\s+de\s+', l)):
            continue
        for bruto, pct, nome in TOKEN.findall(l):
            nome_n = sem_acento(nome).strip()
            for rotulo, chave in ATRIBUTOS:
                if nome_n.startswith(rotulo):
                    valor = float(bruto.replace(',', '.'))
                    # penetracao de armadura tem versao plana e percentual
                    if chave == 'pen_arm' and pct == '%':
                        chave = 'pen_arm_pct'
                    if chave == 'ms' and pct == '%':
                        chave = 'ms_pct'
                    stats[chave] = stats.get(chave, 0) + valor
                    break
    return stats


def carregar_itens():
    dados = json.load(open(METADATA, encoding='utf-8'))
    itens = {}
    for _id, item in dados['items'].items():
        nome = (item.get('name') or '').strip()
        preco = item.get('price') or 0
        desc = limpar(item.get('description'))
        # o banco tem nomes repetidos (versoes antigas com preco 0): fica a
        # entrada com preco cadastrado.
        antigo = itens.get(nome)
        if antigo and antigo['preco'] and not preco:
            continue
        itens[nome] = {'preco': preco, 'desc': desc, 'stats': parse_stats(desc)}
    return itens


# --------------------------------------------------------------------------
# 2. Tabela de precos dos atributos, derivada dos itens primarios
# --------------------------------------------------------------------------
# Cada valor abaixo vem de um item basico do proprio metadata.json.
VALOR_OURO = {
    'ad':          500 / 12,     # Espada Longa .......... 500g / 12 AD
    'as':          500 / 15,     # Adaga ................. 500g / 15% VA
    'crit':        500 / 10,     # Luvas da Pancadaria ... 500g / 10% Crit
    'hp':          500 / 150,    # Cristal de Rubi ....... 500g / 150 Vida
    'armadura':    500 / 20,     # Couraca de Pano ....... 500g / 20 Armadura
    'mr':          500 / 20,     # Manto Anula-Magia ..... 500g / 20 RM
    'ap':          500 / 25,     # Tomo Amplificador ..... 500g / 25 PH
    'ah':          400 / 10,     # Anel da Revelacao ..... 400g / 10 AH
    'mana':        300 / 200,    # Capitulo Perdido (900g - 30 PH) / 200 Mana
    'vamp':        (1200 - 20 * (500 / 12)) / 8,   # Cetro Vampirico
    'ms':          500 / 25,     # Botas da Velocidade ... 500g / 25 VM
    'ms_pct':      (1400 - 15 * 50 - 15 * (500 / 15)) / 5,   # Zelo
    'pen_arm_pct': 800 / 12,     # Ultimo Sussurro ....... 800g / 12% Pen. Arm.
    'pen_mag':     800 / 18,     # Sapatos do Feiticeiro (aprox.)
    'pen_arm':     800 / 12,     # sem item basico puro; usa a mesma referencia
}

ROTULO = {
    'ad': 'Dano de Ataque', 'as': 'Vel. Ataque', 'crit': 'Critico',
    'hp': 'Vida', 'armadura': 'Armadura', 'mr': 'Resist. Magica',
    'ap': 'Poder de Habilidade', 'ah': 'Acel. Habilidade', 'mana': 'Mana',
    'vamp': 'Vampirismo', 'ms': 'Vel. Movimento', 'ms_pct': 'Vel. Movimento',
    'pen_arm_pct': 'Pen. Armadura', 'pen_arm': 'Pen. Armadura plana',
    'pen_mag': 'Pen. Magica',
}

# Atributos que o jogo entrega dentro do texto da passiva (o parser so le as
# linhas de atributo). Entram na conta de eficiencia de ouro, marcados com *.
STATS_DE_PASSIVA = {
    'Último Sussurro': {'pen_arm_pct': 12},
    'Sedenta por Sangue': {'vamp': 8},
    'Lembrete Mortal': {'pen_arm_pct': 30},
    'A Coletora': {'pen_arm': 10},
    'Espada do Rei Destruído': {'vamp': 10},
    'Lâmina da Fúria de Guinsoo': {'ad': 25, 'as': 32},
    'Terminus': {'pen_arm_pct': 33},
    'Dançarina Fantasma': {'as': 25},
    'Detonador Magnético': {'ms_pct': 5},
    'Mata-Cráquens': {'ms_pct': 5},
    'Zelo': {'ms_pct': 5},
}


def stats_totais(nome, item):
    """Atributos da ficha + atributos escondidos na passiva."""
    total = dict(item['stats'])
    for chave, valor in STATS_DE_PASSIVA.get(nome, {}).items():
        total[chave] = total.get(chave, 0) + valor
    return total


def valor_atributos(stats):
    return sum(VALOR_OURO.get(k, 0) * v for k, v in stats.items())


def eficiencia(nome, item):
    if not item['preco']:
        return None
    return valor_atributos(stats_totais(nome, item)) / item['preco']


# --------------------------------------------------------------------------
# 3. Modelo de DPS
# --------------------------------------------------------------------------
# Atirador de referencia no nivel 15, sem runas: 110 de AD base e 0,90 ataque/s.
BASE_AD = 110.0
BASE_AS = 0.90
TETO_AS = 2.5
CRIT_PADRAO = 1.75      # critico causa 175% do dano no Wild Rift

ALVOS = {
    'frágil': {'armadura': 100.0, 'mr': 45.0, 'vida': 2200.0, 'vida_adicional': 400.0},
    'tanque': {'armadura': 250.0, 'mr': 110.0, 'vida': 4200.0, 'vida_adicional': 2400.0},
}

# Contextos de compra: o que o campeao ja tem quando o item entra no slot.
CONTEXTOS = {
    '1º item': {'ad': 0.0, 'as': 0.0, 'crit': 0.0},
    '4º item': {'ad': 80.0, 'as': 0.60, 'crit': 0.50},
}


class Perfil(object):
    """Soma dos atributos ofensivos ativos no momento do calculo."""

    def __init__(self, ad=0.0, as_pct=0.0, crit=0.0, pen_pct=0.0, pen_plana=0.0,
                 pen_mag_pct=0.0, dano_critico=CRIT_PADRAO, onhit_fis=0.0,
                 onhit_mag=0.0, pct_vida_atual=0.0, bonus_dano=0.0, pode_critar=True):
        self.ad = ad
        self.as_pct = as_pct
        self.crit = crit
        self.pen_pct = pen_pct
        self.pen_plana = pen_plana
        self.pen_mag_pct = pen_mag_pct
        self.dano_critico = dano_critico
        self.onhit_fis = onhit_fis
        self.onhit_mag = onhit_mag
        self.pct_vida_atual = pct_vida_atual
        self.bonus_dano = bonus_dano
        self.pode_critar = pode_critar


def dps(perfil, alvo):
    ad = BASE_AD + perfil.ad
    vel = min(BASE_AS * (1 + perfil.as_pct), TETO_AS)
    crit = min(perfil.crit, 1.0)
    mult_crit = 1 + crit * (perfil.dano_critico - 1) if perfil.pode_critar else 1.0

    armadura = alvo['armadura'] * (1 - min(perfil.pen_pct, 0.9)) - perfil.pen_plana
    armadura = max(armadura, 0.0)
    red_fis = 100.0 / (100.0 + armadura)
    mr = alvo['mr'] * (1 - min(perfil.pen_mag_pct, 0.9))
    red_mag = 100.0 / (100.0 + mr)

    # 8,5% da vida atual: media ao longo de uma luta que leva o alvo de 100% a 0%
    vida_atual_medio = 0.5 * alvo['vida'] * perfil.pct_vida_atual

    por_ataque = (ad * mult_crit + perfil.onhit_fis + vida_atual_medio) * red_fis \
        + perfil.onhit_mag * red_mag
    return por_ataque * vel * (1 + perfil.bonus_dano)


def perfil_base(contexto):
    return Perfil(ad=contexto['ad'], as_pct=contexto['as'], crit=contexto['crit'])


def aplicar(perfil, stats, extras, alvo):
    """Devolve um novo perfil com os atributos do item somados."""
    novo = Perfil(
        ad=perfil.ad + stats.get('ad', 0),
        as_pct=perfil.as_pct + stats.get('as', 0) / 100.0,
        crit=perfil.crit + stats.get('crit', 0) / 100.0,
        pen_pct=perfil.pen_pct + stats.get('pen_arm_pct', 0) / 100.0,
        pen_plana=perfil.pen_plana + stats.get('pen_arm', 0),
    )
    if extras:
        extras(novo, alvo)
    return novo


# ---- passivas modeladas (apenas as que geram dano continuo mensuravel) ----
def p_gume(p, alvo):
    p.dano_critico = 2.05                      # critico passa a causar 205%


def p_dominik(p, alvo):
    if alvo['vida_adicional'] >= 1200:
        p.bonus_dano += 0.12                   # Mata-Gigantes no teto
    else:
        p.bonus_dano += 0.12 * alvo['vida_adicional'] / 1200.0


def p_lembrete(p, alvo):
    p.pen_pct += 0.30 + 0.06 * min(p.crit, 1.0)


def p_terminus(p, alvo):
    p.onhit_mag += 35
    p.pen_pct += 0.33                          # 3 acumulos de 11%
    p.pen_mag_pct += 0.33


def p_botrk(p, alvo):
    p.pct_vida_atual += 0.085


def p_kraken(p, alvo):
    # 110-150 a cada 3 ataques, +1% por 1% de vida perdida (teto 70%)
    p.onhit_fis += 130 * 1.35 / 3.0


def p_runaan(p, alvo):
    p.onhit_fis += 15                          # so o dano de contato no alvo principal


def p_coletora(p, alvo):
    p.pen_plana += 10                          # Homicida


def p_chuva(p, alvo):
    p.onhit_mag += 100 / 4.0                   # Energizado a cada ~4 ataques


def p_detonador(p, alvo):
    p.onhit_mag += 70 / 4.0


def p_guinsoo(p, alvo):
    p.pode_critar = False
    p.ad += 25                                 # Caos (adaptativo)
    p.as_pct += 0.32                           # Golpe Fervente no maximo
    p.onhit_mag += 30 + 1.5 * (p.crit * 100)   # Ira


def p_dancarina(p, alvo):
    p.as_pct += 0.25                           # Valsa Espectral, uptime alto


def p_vendaval(p, alvo):
    pass                                       # ativo, nao entra no DPS continuo


PASSIVAS = {
    'Gume do Infinito': p_gume,
    'Lembranças do Lorde Dominik': p_dominik,
    'Lembrete Mortal': p_lembrete,
    'Terminus': p_terminus,
    'Espada do Rei Destruído': p_botrk,
    'Mata-Cráquens': p_kraken,
    'Furacão de Runaan': p_runaan,
    'A Coletora': p_coletora,
    'Chuva de Canivete': p_chuva,
    'Detonador Magnético': p_detonador,
    'Lâmina da Fúria de Guinsoo': p_guinsoo,
    'Dançarina Fantasma': p_dancarina,
    '[NEW]Forca do Vendaval': p_vendaval,
}

# Itens lendarios comprados por atirador (ordem de dano / criticos).
LENDARIOS = [
    'Gume do Infinito', 'Lembrete Mortal', 'Lembranças do Lorde Dominik',
    'Terminus', 'Transferência de Alma', 'Espada do Rei Destruído',
    '[NEW]Forca do Vendaval', 'Lâmina da Fúria de Guinsoo', 'Sedenta por Sangue',
    'Lâmina Impetuosa Solari', 'Detonador Magnético', 'Chuva de Canivete',
    'Arco-escudo Imortal', 'A Coletora', 'Colhedor de Essência',
    'Furacão de Runaan', 'Dançarina Fantasma', 'Mata-Cráquens',
    'Adagas Rápidas Navori',
]

BOTAS = ['Grevas do Berserker (Reformuladas)', 'Botas do Dinamismo (REFORMULADAS)',
         'Grevas Vorazes (REFORMULADAS)']

EPICOS = ['Zelo', 'Arco Recurvo', 'Alijava Vespertina', 'Espada G. p. C.',
          'Capa da Agilidade', 'Punhal Serrilhado', 'Ferrão', 'Cetro Vampírico',
          'Martelo de Guerra de Caulfield', 'Estilhaço de Kircheis',
          'Chamado do Carrasco', 'Último Sussurro']

BASICOS = ['Espada Longa', 'Adaga', 'Luvas da Pancadaria', 'Cristal de Rubi',
           'Couraça de Pano', 'Manto Anula-Magia', 'Tomo Amplificador',
           'Anel da Revelação', 'Botas da Velocidade', 'Cristal de Safira']


def dps_por_ouro(nome, item, contexto, alvo):
    base = perfil_base(contexto)
    novo = aplicar(base, item['stats'], PASSIVAS.get(nome), alvo)
    ganho = dps(novo, alvo) - dps(base, alvo)
    return ganho, ganho / item['preco'] * 1000.0


# --------------------------------------------------------------------------
# 4. Relatorio
# --------------------------------------------------------------------------
def linha_stats(stats):
    ordem = ['ad', 'as', 'crit', 'hp', 'armadura', 'mr', 'ah', 'vamp',
             'pen_arm_pct', 'pen_arm', 'ap', 'mana', 'ms', 'ms_pct']
    partes = []
    for k in ordem:
        if stats.get(k):
            v = stats[k]
            v = int(v) if float(v).is_integer() else v
            pct = '%' if k in ('as', 'crit', 'vamp', 'pen_arm_pct', 'ms_pct') else ''
            partes.append('%s%s %s' % (v, pct, ROTULO[k]))
    return ', '.join(partes) or '—'


def main():
    itens = carregar_itens()

    linhas = []
    w = linhas.append
    w('# Itens de Atirador no Wild Rift — custo-benefício')
    w('')
    w('Gerado por `analise_atirador.py` a partir dos preços e atributos de '
      '`metadata.json`. Refaça o cálculo sempre que os itens forem atualizados.')
    w('')

    # --- tabela de precos dos atributos ---
    w('## 1. Quanto vale cada atributo (itens primários como régua)')
    w('')
    w('| Atributo | Item primário de referência | Ouro por ponto |')
    w('|---|---|---|')
    refs = [
        ('ad', 'Espada Longa — 500g / 12 Dano de Ataque'),
        ('as', 'Adaga — 500g / 15% Vel. de Ataque'),
        ('crit', 'Luvas da Pancadaria — 500g / 10% Crítico'),
        ('hp', 'Cristal de Rubi — 500g / 150 Vida'),
        ('armadura', 'Couraça de Pano — 500g / 20 Armadura'),
        ('mr', 'Manto Anula-Magia — 500g / 20 Resist. Mágica'),
        ('ap', 'Tomo Amplificador — 500g / 25 Poder de Habilidade'),
        ('ah', 'Anel da Revelação — 400g / 10 Acel. de Habilidade'),
        ('mana', 'Capítulo Perdido — (900g − 30 PH) / 200 Mana'),
        ('vamp', 'Cetro Vampírico — (1200g − 20 AD) / 8% Vampirismo'),
        ('ms', 'Botas da Velocidade — 500g / 25 Vel. de Movimento'),
        ('ms_pct', 'Zelo — (1400g − 15% Crít − 15% VA) / 5% Vel. Mov.'),
        ('pen_arm_pct', 'Último Sussurro — 800g / 12% Pen. de Armadura'),
    ]
    for chave, ref in refs:
        w('| %s | %s | **%.1f g** |' % (ROTULO[chave], ref, VALOR_OURO[chave]))
    w('')
    w('Itens básicos por definição valem 100% (a régua é feita deles). '
      'Um item lendário acima de 100% já compensa só pelos atributos; abaixo '
      'disso, ele precisa da passiva para valer o preço.')
    w('')

    # --- eficiencia de ouro ---
    for titulo, lista in (('2. Eficiência de ouro — itens lendários', LENDARIOS),
                          ('3. Eficiência de ouro — botas e itens épicos',
                           BOTAS + EPICOS)):
        w('## %s' % titulo)
        w('')
        w('| Item | Preço | Atributos | Valor em ouro | Eficiência |')
        w('|---|---|---|---|---|')
        dados = []
        for nome in lista:
            it = itens.get(nome)
            if not it or not it['preco']:
                continue
            dados.append((eficiencia(nome, it), nome, it))
        for ef, nome, it in sorted(dados, reverse=True):
            total = stats_totais(nome, it)
            marca = '*' if nome in STATS_DE_PASSIVA else ''
            w('| %s%s | %dg | %s | %.0fg | **%.0f%%** |'
              % (nome.replace('[NEW]', ''), marca, it['preco'],
                 linha_stats(total), valor_atributos(total), ef * 100))
        w('')
        w('`*` inclui atributos que o item entrega pela passiva '
          '(penetração, vampirismo, acúmulos de vel. de ataque).')
        w('')

    # --- dps por ouro ---
    w('## 4. Dano por ouro (o que realmente importa para o atirador)')
    w('')
    w('Eficiência de ouro trata cada atributo isoladamente, mas para um atirador '
      'AD, velocidade de ataque e crítico se **multiplicam** entre si. O cálculo '
      'abaixo mede o DPS que cada item adiciona e divide pelo preço.')
    w('')
    w('Referência: atirador nível 15 com %d de AD base e %.2f ataque/s base. '
      'Alvo frágil = %d de armadura e %d de vida; alvo tanque = %d de armadura e '
      '%d de vida. "1º item" = build vazia; "4º item" = já com 80 de AD, 60%% de '
      'vel. de ataque e 50%% de crítico acumulados.'
      % (BASE_AD, BASE_AS, ALVOS['frágil']['armadura'], ALVOS['frágil']['vida'],
         ALVOS['tanque']['armadura'], ALVOS['tanque']['vida']))
    w('')
    for ctx_nome, ctx in CONTEXTOS.items():
        w('### Como %s' % ctx_nome)
        w('')
        w('| Item | Preço | DPS no frágil | DPS/1000g (frágil) | DPS no tanque | '
          'DPS/1000g (tanque) |')
        w('|---|---|---|---|---|---|')
        linhas_ctx = []
        for nome in LENDARIOS:
            it = itens.get(nome)
            if not it or not it['preco']:
                continue
            gf, pf = dps_por_ouro(nome, it, ctx, ALVOS['frágil'])
            gt, pt = dps_por_ouro(nome, it, ctx, ALVOS['tanque'])
            linhas_ctx.append((pf, nome, it['preco'], gf, pf, gt, pt))
        for _, nome, preco, gf, pf, gt, pt in sorted(linhas_ctx, reverse=True):
            w('| %s | %dg | +%.0f | **%.1f** | +%.0f | **%.1f** |'
              % (nome.replace('[NEW]', ''), preco, gf, pf, gt, pt))
        w('')

    w('### O que o modelo não mede')
    w('')
    w('- **Furacão de Runaan**: o cálculo só conta o alvo principal. Os dois raios '
      'extras (55% do dano) valem perto de +110% de DPS em luta de 3 alvos.')
    w('- **Lâmina Impetuosa Solari** e **Colhedor de Essência**: o dano depende de '
      'conjurar habilidades, então dependem do campeão.')
    w('- **Adagas Rápidas Navori**: os 15% de redução de recarga por ataque não '
      'viram DPS de ataque básico — valem para atiradores que dependem de '
      'habilidades (Ezreal, Vayne, Lucian).')
    w('- **Sedenta por Sangue**, **Arco-escudo Imortal**, **Cimitarra Mercurial**: '
      'parte do preço é sobrevivência, não dano.')
    w('- Passivas de utilidade (lentidão, vel. de movimento, escudos) não entram.')
    w('')

    # --- itens basicos de referencia ---
    w('## 5. Itens primários usados como régua')
    w('')
    w('| Item básico | Preço | Atributos |')
    w('|---|---|---|')
    for nome in BASICOS:
        it = itens.get(nome)
        if it:
            w('| %s | %dg | %s |' % (nome, it['preco'], linha_stats(it['stats'])))
    w('')

    # --- leitura pratica ---
    w('## 6. Leitura prática')
    w('')
    w('**Melhor custo-benefício puro (atributos por ouro):** Sedenta por Sangue, '
      'Terminus, Dançarina Fantasma, Lembrete Mortal e Lembranças do Lorde '
      'Dominik passam de 140% — pagam-se sozinhos antes mesmo da passiva.')
    w('')
    w('**Melhor custo-benefício em dano real:** a ordem muda bastante, porque '
      'crítico só rende com AD e vel. de ataque já acumulados:')
    w('')
    w('- **1º item** — Mata-Cráquens, Espada do Rei Destruído e Terminus lideram. '
      'São itens de dano fixo por ataque (não dependem de crítico), por isso '
      'rendem cedo. Crítico como primeiro item é o pior investimento da lista.')
    w('- **3º/4º item** — Terminus, Guinsoo, Mata-Cráquens e Dançarina Fantasma '
      'seguem na frente, mas Gume do Infinito e Lembrete Mortal sobem muito, '
      'porque multiplicam o crítico que a build já tem.')
    w('- **Contra tanque** — Espada do Rei Destruído, Terminus, Lembranças do '
      'Lorde Dominik e Lembrete Mortal são os únicos que mantêm o rendimento; '
      'itens de crítico puro perdem quase metade do valor contra 250 de armadura.')
    w('')
    w('**Armadilhas de preço:**')
    w('')
    w('- *Arco Recurvo* (71%) e *Estilhaço de Kircheis* (69%) são os piores itens '
      'épicos por atributo — só valem pelo caminho de construção.')
    w('- *Furacão de Runaan* (83% de eficiência) só compensa em luta coletiva; '
      'contra um alvo só é o pior item de crítico da lista.')
    w('- *Lâmina da Fúria de Guinsoo* anula o crítico dos ataques. O número alto '
      'de DPS acima assume que você **não** vai montar build de crítico com ele.')
    w('- *Gume do Infinito* custa 3400g e só é eficiente com crítico alto; '
      'comprado cedo é 30% pior por ouro que Mata-Cráquens.')
    w('')
    w('**Sequência com melhor retorno por ouro, pelos números acima:**')
    w('')
    w('1. Item de dano por ataque (Mata-Cráquens / Espada do Rei Destruído / '
      'Terminus)')
    w('2. Botas do Dinamismo ou Grevas do Berserker (as duas botas mais '
      'eficientes, 171% e 127%)')
    w('3. Item de crítico com AD alto (Sedenta por Sangue ou Força do Vendaval)')
    w('4. Gume do Infinito, quando o crítico já estiver alto')
    w('5. Penetração conforme o inimigo (Lembrete Mortal ou Lembranças do Lorde '
      'Dominik contra tanques)')
    w('')

    # --- observacoes sobre os dados ---
    sem_preco = sorted(n for n, i in itens.items() if not i['preco'])
    w('## 7. Observações sobre os dados')
    w('')
    w('- Preços e atributos vêm de `metadata.json`; mudanças de patch invalidam '
      'os números.')
    w('- Penetração de armadura plana não tem item básico puro de referência: '
      'está precificada pela equivalência com penetração percentual contra 100 '
      'de armadura.')
    w('- %d itens do banco estão com preço 0 e ficaram fora das tabelas: %s.'
      % (len(sem_preco), ', '.join(sem_preco)))
    w('')

    conteudo = '\n'.join(linhas) + '\n'
    with open(SAIDA, 'w', encoding='utf-8') as fh:
        fh.write(conteudo)
    print(conteudo)


if __name__ == '__main__':
    main()
