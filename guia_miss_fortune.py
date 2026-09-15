# -*- coding: utf-8 -*-
"""
Gera o guia passo a passo de Miss Fortune (guia_miss_fortune.md).

Reaproveita o modelo de dano de analise_atirador.py: os numeros de cada etapa
da build saem dos mesmos precos e atributos de metadata.json.
"""
import analise_atirador as base

SAIDA = 'guia_miss_fortune.md'

# Cada etapa lista os itens que a Miss Fortune TEM ao final da volta a base.
# 'gasto' e o ouro da loja naquela volta (o jogo abate os componentes que voce
# ja carrega, entao o valor mostrado em jogo pode ser menor).
ROTA_FRAGIL = [
    ('Início', 500, ['Espada Longa'], 'Espada Longa'),
    ('1ª volta', 1000, ['Punhal Serrilhado'], 'Punhal Serrilhado'),
    ('2ª volta', 1400, ['Punhal Serrilhado', 'Capa da Agilidade'],
     'Capa da Agilidade + Botas da Velocidade'),
    ('3ª volta', 1700, ['[NEW]Forca do Vendaval'], 'completa Força do Vendaval'),
    ('4ª volta', 1300, ['[NEW]Forca do Vendaval',
                        'Grevas do Berserker (Reformuladas)'],
     'evolui as botas + encantamento'),
    ('5ª volta', 3000, ['[NEW]Forca do Vendaval',
                        'Grevas do Berserker (Reformuladas)', 'A Coletora'],
     'A Coletora'),
    ('6ª volta', 3400, ['[NEW]Forca do Vendaval',
                        'Grevas do Berserker (Reformuladas)', 'A Coletora',
                        'Gume do Infinito'], 'Gume do Infinito'),
    ('7ª volta', 3300, ['[NEW]Forca do Vendaval',
                        'Grevas do Berserker (Reformuladas)', 'A Coletora',
                        'Gume do Infinito', 'Lembrete Mortal'], 'Lembrete Mortal'),
    ('Build fechada', 3000, ['[NEW]Forca do Vendaval',
                             'Grevas do Berserker (Reformuladas)', 'A Coletora',
                             'Gume do Infinito', 'Lembrete Mortal',
                             'Sedenta por Sangue'], 'Sedenta por Sangue'),
]

ROTA_TANQUE = [
    ('Início', 500, ['Espada Longa'], 'Espada Longa'),
    ('1ª volta', 1200, ['Cetro Vampírico'], 'Cetro Vampírico'),
    ('2ª volta', 900, ['Cetro Vampírico'], 'Botas do Dinamismo (base)'),
    ('3ª volta', 1800, ['Sedenta por Sangue'], 'completa Sedenta por Sangue'),
    ('4ª volta', 1300, ['Sedenta por Sangue',
                        'Botas do Dinamismo (REFORMULADAS)'],
     'evolui as botas + Encantamento de Estase'),
    ('5ª volta', 3200, ['Sedenta por Sangue',
                        'Botas do Dinamismo (REFORMULADAS)',
                        'Espada do Rei Destruído'], 'Espada do Rei Destruído'),
    ('6ª volta', 3300, ['Sedenta por Sangue',
                        'Botas do Dinamismo (REFORMULADAS)',
                        'Espada do Rei Destruído', 'Lembrete Mortal'],
     'Lembrete Mortal'),
    ('7ª volta', 3400, ['Sedenta por Sangue',
                        'Botas do Dinamismo (REFORMULADAS)',
                        'Espada do Rei Destruído', 'Lembrete Mortal',
                        'Gume do Infinito'], 'Gume do Infinito'),
    ('Build fechada', 3100, ['Sedenta por Sangue',
                             'Botas do Dinamismo (REFORMULADAS)',
                             'Espada do Rei Destruído', 'Lembrete Mortal',
                             'Gume do Infinito', '[NEW]Cimitarra Mercurial'],
     'Cimitarra Mercurial'),
]


# Runas modeladas a partir do texto de metadata.json['runes'] (nível 15,
# campeã de ataque à distância). Cada função recebe o perfil já montado com os
# itens e devolve o dano por segundo extra que a runa adiciona fora do ataque.
RUNAS_CHAVE = {
    'Fortalecimento': (
        'Amplifica também o Tiro Duplo e o Tiroteio',
        lambda p: setattr(p, 'bonus_dano', p.bonus_dano + 0.09) or 200 / 4.0),
    'Ritmo Fatal': (
        'Só ataque básico; ultrapassa o limite de vel. de ataque',
        lambda p: setattr(p, 'as_pct', p.as_pct + 0.60) or 0.0),
    'Conquistador': (
        'AD adaptativo, então soma no Tiro Duplo e no Tiroteio',
        lambda p: setattr(p, 'ad', p.ad + 42) or 0.0),
    'Eletrocutar': (
        'Explosão a cada 13s; bom para pegar alvo isolado',
        lambda p: (194 + 0.35 * p.ad) / 13.0),
    'Primeiro Ataque': (
        'Dano verdadeiro nos 3s iniciais + ouro extra',
        lambda p: setattr(p, 'bonus_dano', p.bonus_dano + 0.07 * 0.3) or 0.0),
    'Colheita Sombria': (
        'Só contra alvo abaixo de 50% de vida',
        lambda p: (40 + 10 * 20 + 0.25 * p.ad) / 20.0),
    'Agilidade nos Pés': (
        'Cura e velocidade; dano quase nulo',
        lambda p: 0.0),
}

BUILD_COMPARACAO = ['[NEW]Forca do Vendaval', 'Grevas do Berserker (Reformuladas)',
                    'A Coletora', 'Gume do Infinito']


# Dano extra de cada runa numa troca de 3 ataques (o padrao da Miss Fortune na
# rota), em vez de luta longa. Ritmo Fatal nao aparece aqui de proposito: ele
# da mais ataques por segundo, nao mais dano por ataque.
TROCA_CURTA = {
    'Fortalecimento': ('plano', 200.0),      # gatilho no 3º ataque
    'Eletrocutar': ('ad', (194.0, 0.35)),    # 194 + 35% do AD adicional
    'Conquistador': ('ad_medio', 14.0),      # 3 acumulos, subindo
    'Primeiro Ataque': ('amp', 0.07),        # dano verdadeiro nos 3s
    'Ritmo Fatal': ('plano', 0.0),
    'Colheita Sombria': ('plano', 0.0),      # alvo ainda acima de 50%
    'Agilidade nos Pés': ('plano', 0.0),
}


def troca_de_3_ataques(itens, runa, alvo):
    p, _ = perfil_da_build(itens, BUILD_COMPARACAO, alvo)
    reducao = 100.0 / (100.0 + alvo['armadura'] * (1 - min(p.pen_pct, 0.9))
                       - p.pen_plana)
    mult_crit = 1 + min(p.crit, 1.0) * (p.dano_critico - 1)
    ad = base.BASE_AD + p.ad
    extra_ad, plano, amp = 0.0, 0.0, 0.0
    if runa:
        tipo, valor = TROCA_CURTA[runa]
        if tipo == 'plano':
            plano = valor
        elif tipo == 'ad':
            plano = valor[0] + valor[1] * p.ad
        elif tipo == 'ad_medio':
            extra_ad = valor
        elif tipo == 'amp':
            amp = valor
    por_ataque = (ad + extra_ad) * mult_crit + p.onhit_fis
    return (3 * por_ataque * (1 + amp) + plano) * reducao


def dps_com_runa(itens, runa, alvo):
    p, _ = perfil_da_build(itens, BUILD_COMPARACAO, alvo)
    extra = 0.0
    if runa:
        extra = RUNAS_CHAVE[runa][1](p) or 0.0
    reducao = 100.0 / (100.0 + alvo['armadura'] * (1 - min(p.pen_pct, 0.9))
                       - p.pen_plana)
    return base.dps(p, alvo) + extra * reducao


def perfil_da_build(itens, nomes, alvo):
    """Soma os atributos de todos os itens da build e aplica as passivas."""
    total = {}
    for nome in nomes:
        for chave, valor in itens[nome]['stats'].items():
            total[chave] = total.get(chave, 0) + valor
    p = base.Perfil(
        ad=total.get('ad', 0),
        as_pct=total.get('as', 0) / 100.0,
        crit=total.get('crit', 0) / 100.0,
        pen_pct=total.get('pen_arm_pct', 0) / 100.0,
        pen_plana=total.get('pen_arm', 0),
    )
    for nome in nomes:
        passiva = base.PASSIVAS.get(nome)
        if passiva:
            passiva(p, alvo)
    return p, total


def tabela(itens, rota, titulo, linhas):
    w = linhas.append
    w('### %s — %s de ouro até fechar a build'
      % (titulo, '{:,}'.format(sum(e[1] for e in rota)).replace(',', '.')))
    w('')
    w('| Etapa | Ouro da volta | Compra | Total investido | AD | Crítico | '
      'DPS no frágil | DPS no tanque |')
    w('|---|---|---|---|---|---|---|---|')
    acumulado = 0
    for etapa, gasto, nomes, compra in rota:
        acumulado += gasto
        pf, total = perfil_da_build(itens, nomes, base.ALVOS['frágil'])
        pt, _ = perfil_da_build(itens, nomes, base.ALVOS['tanque'])
        w('| %s | %dg | %s | %dg | +%d | %d%% | %.0f | %.0f |'
          % (etapa, gasto, compra.replace('[NEW]', ''), acumulado,
             total.get('ad', 0), min(total.get('crit', 0), 100),
             base.dps(pf, base.ALVOS['frágil']),
             base.dps(pt, base.ALVOS['tanque'])))
    w('')
    w('"Ouro da volta" é o preço de loja do que você compra naquela ida à '
      'base e "total investido" soma tudo que já passou pela build, '
      'componentes inclusos — em jogo a loja abate o valor das peças que você '
      'já carrega, então o número na tela costuma ser menor.')
    w('')
    w('DPS = ataques básicos do atirador de referência do relatório '
      '(nível 15, %d de AD base, %.2f ataque/s). Serve para comparar as etapas '
      'entre si, não é a simulação exata da Miss Fortune — Amor Duplo, o Tiro '
      'Duplo e o Tiroteio somam por cima disso e escalam com AD e crítico.'
      % (base.BASE_AD, base.BASE_AS))
    w('')


def main():
    itens = base.carregar_itens()
    linhas = []
    w = linhas.append

    w('# Miss Fortune — passo a passo de build e de rota')
    w('')
    w('Gerado por `guia_miss_fortune.py`, em cima do modelo de '
      '`analise_atirador.py` (preços e atributos de `metadata.json`).')
    w('')
    w('Dados do próprio projeto (`tencent_data.json`): Miss Fortune está com '
      '**52,18% de vitórias**, 23,28% de presença e 2,42% de banimentos — é a '
      'atiradora mais jogada do banco. Pelos counters de '
      '`campeoes_counters.md` (coluna "Forte Contra"): ela **vence** Draven, '
      'Kalista e Jinx, e **perde** para Jhin, Sivir e Varus.')
    w('')

    w('## 1. Por que a build dela foge do ranking geral de atirador')
    w('')
    w('No relatório de custo-benefício, os melhores itens por ouro no 1º slot '
      'são Mata-Cráquens, Espada do Rei Destruído e Terminus — itens de dano '
      'fixo por ataque, feitos para quem fica batendo. A Miss Fortune não é '
      'isso: o dano dela sai de **Amor Duplo** (dano extra ao trocar de alvo), '
      'do **Tiro Duplo** (que quica e pode crítico) e do **Tiroteio**. Tudo '
      'isso escala com **AD e crítico**, não com tempo em combate.')
    w('')
    w('Por isso a régua que vale para ela é a da eficiência de ouro pura, onde '
      'os itens de AD+crítico lideram:')
    w('')
    w('| Item | Preço | AD | Crítico | Eficiência |')
    w('|---|---|---|---|---|')
    nucleo = ['Sedenta por Sangue', '[NEW]Forca do Vendaval', 'A Coletora',
              'Gume do Infinito', 'Lembrete Mortal',
              'Lembranças do Lorde Dominik']
    for ef, nome in sorted(((base.eficiencia(n, itens[n]), n) for n in nucleo),
                           reverse=True):
        it = itens[nome]
        st = base.stats_totais(nome, it)
        w('| %s | %dg | +%d | %d%% | **%.0f%%** |'
          % (nome.replace('[NEW]', ''), it['preco'], st.get('ad', 0),
             st.get('crit', 0), ef * 100))
    w('')

    w('## 2. Contra suporte FRÁGIL (Lux, Morgana, Nami, Sona, Seraphine, Zyra)')
    w('')
    w('**Postura: agressiva desde o nível 1.** Nessa rota você tem o melhor '
      'dano de troca do jogo no nível 1-2, porque Amor Duplo dá dano extra '
      'sempre que você troca de alvo: bata numa tropa, bata no suporte, volte '
      'para a tropa. Contra suporte sem escudo forte e sem engate, cada troca '
      'é lucro.')
    w('')
    w('- **Nível 1-2**: force a troca antes de o suporte inimigo chegar ao '
      'nível 3. Use o Tiro Duplo na tropa da frente para quicar no campeão.')
    w('- **Nível 5 (Tiroteio)**: primeiro grande pico. Com o suporte frágil '
      'sem mobilidade, o ult fecha a luta 2v2 — chame o caçador.')
    w('- **Empurre a rota**: rota frágil não consegue contestar torre. Empurrar '
      'acelera as voltas à base e o seu 1º lendário.')
    w('- **Cuidado**: Morgana (escudo bloqueia o ult) e Lux com escudo no aliado '
      'seguram a troca. Contra elas, jogue o E no chão para forçar recuo antes '
      'de entrar.')
    w('')
    tabela(itens, ROTA_FRAGIL, 'Rota de compras', linhas)
    w('> **Penetração é escolha única.** Lembrete Mortal, Lembranças do Lorde '
      'Dominik e Rancor de Serylda nascem todos do Último Sussurro: a loja não '
      'deixa levar dois. Escolha pelo inimigo — Dominik contra vida alta, '
      'Lembrete Mortal contra cura, Serylda contra mobilidade.')
    w('')
    w('**Ordem de habilidades:** maximize o **Tiro Duplo** primeiro (dano de '
      'rota e limpeza de onda), depois **Golpes Fatais**, deixando **Fazer '
      'Chover** por último. Ultimate sempre que disponível (nível 5, 9, 13).')
    w('')

    w('## 3. Contra suporte TANQUE/ENGATE (Leona, Nautilus, Blitzcrank, '
      'Alistar, Thresh, Braum, Rell)')
    w('')
    w('**Postura: passiva até o nível 5 e até ter botas.** Aqui a troca de dano '
      'não é o problema — o problema é uma única pegada. Você não tem dash '
      'nem escudo: qualquer acerto de Blitzcrank, Nautilus ou Leona vira morte.')
    w('')
    w('- **Nível 1-4**: fique **atrás da sua onda**, nunca na lateral livre. '
      'Farme com ataque básico e com o Tiro Duplo quicando; não conteste a '
      'troca, você perde a corrida de dano contra um tanque com cura do '
      'suporte.')
    w('- **Segure o Fazer Chover para defesa**, não para dano: a lentidão é o '
      'que cancela o engate depois que o CC deles acerta.')
    w('- **Nível 5**: primeiro momento de jogar para frente — mas só com o CC '
      'principal do suporte inimigo em recarga (Q do Blitz, E do Naut, E da '
      'Leona). Conte a recarga, é a informação mais valiosa da rota.')
    w('- **Encantamento de Estase (1.000g) ou de Mercúrio (800g)** nas botas é '
      'obrigatório nessa rota, e vale mais que 1.000g de dano.')
    w('- **Contra tanque de linha de frente**, os números do relatório são '
      'claros: Espada do Rei Destruído (40,7 DPS/1000g contra tanque) e '
      'Lembrete Mortal são os itens que mantêm rendimento; crítico puro perde '
      'quase metade do valor contra 250 de armadura.')
    w('')
    tabela(itens, ROTA_TANQUE, 'Rota de compras', linhas)
    w('> **Um item de penetração só.** Aqui a escolha é Lembrete Mortal (as '
      'Feridas Dolorosas cortam a cura do suporte tanque). Se o time inimigo '
      'for de vida alta sem cura, troque por Lembranças do Lorde Dominik no '
      'mesmo slot — nunca os dois.')
    w('')
    w('> A **Cimitarra Mercurial** fecha a build porque o ativo dela limpa o '
      'CC que te mata nessa rota. Se levar ela, o encantamento das botas deve '
      'ser **Estase**, não Mercúrio — são o mesmo efeito.')
    w('')
    w('**Ordem de habilidades:** ainda Tiro Duplo primeiro, mas suba o **Fazer '
      'Chover** um ponto cedo (nível 3) pelo desengate. Se o suporte inimigo é '
      'Blitzcrank, o ponto em Fazer Chover no nível 2 já se paga.')
    w('')

    w('## 4. Picos de poder — quando você é mais forte que o inimigo')
    w('')
    w('| Momento | O que muda | Como aproveitar |')
    w('|---|---|---|')
    w('| **Nível 1-2** | Amor Duplo dá o melhor dano de troca da rota | '
      'Trocar alvo a cada ataque; só contra suporte frágil |')
    w('| **Nível 5 — Tiroteio** | Maior pico da fase de rota | Lutar 2v2 e '
      'chamar o caçador; pedir o primeiro Arauto |')
    w('| **1º lendário (~4.000g investidos)** | Sai de ~%d para ~%d de DPS de '
      'ataque, e o Tiroteio passa a matar suporte frágil sozinho | Forçar a '
      'torre da rota inferior |' % (
        base.dps(perfil_da_build(itens, ['Espada Longa'],
                                 base.ALVOS['frágil'])[0], base.ALVOS['frágil']),
        base.dps(perfil_da_build(itens, ['[NEW]Forca do Vendaval'],
                                 base.ALVOS['frágil'])[0], base.ALVOS['frágil'])))
    w('| **Nível 9-10 + 2º lendário** | Habilidades no máximo e crítico em 50% '
      '| Rotacionar para Dragão; é a janela mais forte da partida |')
    w('| **Gume do Infinito com crítico alto** | Crítico passa de 175% para '
      '205% de dano — vale 39,3 DPS/1000g no 4º slot contra 13,8 no 1º | '
      'Só comprar depois de 50% de crítico |')
    w('| **Build fechada (6 itens)** | Sem novos picos: a partir daí é '
      'posicionamento | Ficar no fundo, ult só com o CC inimigo gasto |')
    w('')

    w('## 5. Runas')
    w('')
    w('O `metadata.json` tem 58 runas com o texto completo, e o `app.js` '
      '(`RUNES_KEYSTONES`, linha 107) diz quais são de **Chave**. O que o banco '
      '**não** tem é a qual dos outros três espaços cada runa pertence — então '
      'só a escolha de Chave abaixo é calculada; as demais vão por função, e '
      'você confirma o espaço na tela do jogo.')
    w('')
    w('### Chave — comparação calculada')
    w('')
    w('Build de referência: Força do Vendaval + Grevas do Berserker + A '
      'Coletora + Gume do Infinito (155 de AD, 75% de crítico). Duas colunas '
      'porque as duas situações premiam runas diferentes: **luta longa** é DPS '
      'com você batendo sem parar; **troca de 3 ataques** é o que realmente '
      'acontece na rota.')
    w('')
    w('| Runa de Chave | Luta longa (DPS) | Troca de 3 ataques (dano) | '
      'Alcance do efeito |')
    w('|---|---|---|---|')
    linhas_runa = []
    for nome, (nota, _) in RUNAS_CHAVE.items():
        linhas_runa.append((troca_de_3_ataques(itens, nome,
                                               base.ALVOS['frágil']),
                            dps_com_runa(itens, nome, base.ALVOS['frágil']),
                            nome, nota))
    for troca, dps_longa, nome, nota in sorted(linhas_runa, reverse=True):
        w('| **%s** | %.0f | %.0f | %s |' % (nome, dps_longa, troca, nota))
    w('| _(sem runa de Chave)_ | %.0f | %.0f | referência |'
      % (dps_com_runa(itens, None, base.ALVOS['frágil']),
         troca_de_3_ataques(itens, None, base.ALVOS['frágil'])))
    w('')
    w('**Leitura honesta da tabela:** em luta longa, **Ritmo Fatal** ganha '
      '(%.0f contra %.0f de DPS), porque 60%% de velocidade de ataque rende '
      'muito quando você fica batendo. Na troca de 3 ataques ele rende '
      '**zero** — mais ataques por segundo não é mais dano por ataque, e a '
      'Miss Fortune não fica 6 ataques em cima de ninguém.'
      % (dps_com_runa(itens, 'Ritmo Fatal', base.ALVOS['frágil']),
         dps_com_runa(itens, 'Fortalecimento', base.ALVOS['frágil'])))
    w('')
    w('**Escolha padrão: Fortalecimento.** É a segunda melhor em luta longa, a '
      'segunda melhor na troca curta, e é a única cuja amplificação de 9% '
      'também vale para o Tiro Duplo e o Tiroteio — que a tabela nem conta, '
      'porque ela só mede ataque básico.')
    w('')
    w('- **Contra suporte frágil, jogando para matar cedo**: **Eletrocutar** — '
      '%.0f de dano na troca de 3 ataques contra %.0f do Fortalecimento. É a '
      'runa que transforma uma troca no nível 3 em abate.'
      % (troca_de_3_ataques(itens, 'Eletrocutar', base.ALVOS['frágil']),
         troca_de_3_ataques(itens, 'Fortalecimento', base.ALVOS['frágil'])))
    w('- **Contra suporte tanque**: Fortalecimento. A amplificação de 9% '
      'funciona contra qualquer armadura; crítico, não.')
    w('- **Ritmo Fatal** só se você for de segurar ataque básico em luta '
      'coletiva longa — não é o padrão dela.')
    w('- **Primeiro Ataque** se você joga para economia: o ouro extra adianta '
      'o primeiro lendário, que é o pico que mais importa.')
    w('')
    w('### Os outros três espaços')
    w('')
    w('| Função | Runa | Por quê |')
    w('|---|---|---|')
    w('| Dano contínuo | **Brutal** | 6 + 8% do AD adicional por ataque, '
      'adaptativo; escala com a build inteira |')
    w('| Execução | **Golpe de Misericórdia** | +8% de dano em alvo abaixo de '
      '40% de vida — casa com a passiva de execução de A Coletora |')
    w('| Abertura de luta | **Dilacerar** | +8% de dano em alvo acima de 60% '
      'de vida; melhor que Golpe de Misericórdia em rota de poke |')
    w('| Sobrevivência na rota | **Ventos Revigorantes** | regenera 6 + 2% da '
      'vida perdida; segura rota contra poke |')
    w('| Contra CC pesado | **Perserverança** | 10% de tenacidade + armadura e '
      'RM ao ser imobilizada — direto contra Leona, Naut e Blitz |')
    w('| Escala tardia | **Tempestade Crescente** | AD adaptativo que cresce a '
      'cada 3 min a partir dos 6 min |')
    w('| Vampirismo | **Lenda: Linhagem** | até 8% de vampirismo universal |')
    w('')
    w('**Contra suporte frágil:** Brutal + Dilacerar + Tempestade Crescente. '
      'Rota de troca de dano, você quer dano puro em cima do Amor Duplo.')
    w('')
    w('**Contra suporte tanque:** Brutal + Perserverança + Ventos Revigorantes. '
      'Aqui sobreviver ao engate vale mais do que 8% de dano — sem escape, '
      'tenacidade é o que te dá a chance de usar o Flash depois do CC.')
    w('')
    w('> Se duas dessas caírem no mesmo espaço na tela do jogo, fique com a de '
      'cima da lista e pegue a próxima da mesma coluna.')
    w('')
    w('### Feitiços')
    w('')
    w('Feitiços disponíveis no projeto (`SPELLS_MAPPING`, `app.js`): Flash, '
      'Curar, Barreira, Exaustão, Incendiar, Purificar, Fantasma e Golpear.')
    w('')
    w('**Flash + Curar** contra suporte frágil (a cura salva da troca e do '
      'Incendiar). **Flash + Barreira** contra suporte de engate: a barreira '
      'absorve a explosão do combo enquanto o CC ainda está em cima de você.')
    w('')

    w('## 6. Regras rápidas de postura')
    w('')
    w('| Situação | Jogar |')
    w('|---|---|')
    w('| Suporte inimigo frágil, os dois no nível 1-2 | **Agressivo** |')
    w('| Suporte inimigo tanque, antes do seu nível 5 | **Passivo, farmar** |')
    w('| CC principal do suporte inimigo em recarga | **Agressivo** |')
    w('| Você sem o Tiroteio, eles com o ult pronto | **Passivo** |')
    w('| Rota contra Draven, Kalista ou Jinx (você é o counter) | '
      '**Agressivo desde o nível 1** |')
    w('| Rota contra Jhin, Sivir ou Varus (eles te counteram) | **Passivo até '
      'o 1º lendário** |')
    w('| Luta coletiva com 3+ inimigos agrupados | Ult de trás, nunca de frente |')
    w('')
    w('> **Confira a árvore na loja.** O `metadata.json` guarda preço, '
      'atributos e passiva, mas não a receita nem a exclusividade dos itens. '
      'Nenhum número deste guia detecta sozinho que dois itens não podem ser '
      'combinados — os conflitos conhecidos estão listados em '
      '`atirador_custo_beneficio.md`, seção 5.')
    w('')
    w('A Miss Fortune não tem escape: toda decisão agressiva depende de o '
      'inimigo ter gastado o CC dele antes. Essa é a única regra que não muda '
      'com o item.')
    w('')

    conteudo = '\n'.join(linhas) + '\n'
    with open(SAIDA, 'w', encoding='utf-8') as fh:
        fh.write(conteudo)
    print(conteudo)


if __name__ == '__main__':
    main()
