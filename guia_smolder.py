# -*- coding: utf-8 -*-
"""
Gera o guia passo a passo do Smolder (guia_smolder.md).

Mesma base do guia da Miss Fortune, mas a métrica muda: o Smolder é um
atirador de habilidade, então o que conta não é DPS de ataque básico e sim
Dano de Ataque, Aceleração de Habilidade e mana — quantas vezes ele consegue
lançar o Q por minuto.
"""
import analise_atirador as base

SAIDA = 'guia_smolder.md'

# Rotas de compra. Cada etapa lista o que ele TEM ao final da volta à base.
ROTA_FRAGIL = [
    ('Início', 500, ['Espada Longa'], 'Espada Longa'),
    ('1ª volta', 1200, ['Martelo de Guerra de Caulfield'],
     'Martelo de Guerra de Caulfield'),
    ('2ª volta', 900, ['Martelo de Guerra de Caulfield',
                       'Botas Ionianas da Lucidez'], 'Botas Ionianas (base)'),
    ('3ª volta', 1800, ['Colhedor de Essência', 'Botas Ionianas da Lucidez'],
     'completa Colhedor de Essência'),
    ('4ª volta', 1100, ['Colhedor de Essência',
                        'Botas da Lucidez de Ionia (REFORMULADAS)'],
     'evolui as botas'),
    ('5ª volta', 2800, ['Colhedor de Essência',
                        'Botas da Lucidez de Ionia (REFORMULADAS)',
                        'Adagas Rápidas Navori'], 'Adagas Rápidas Navori'),
    ('6ª volta', 3400, ['Colhedor de Essência',
                        'Botas da Lucidez de Ionia (REFORMULADAS)',
                        'Adagas Rápidas Navori', 'Gume do Infinito'],
     'Gume do Infinito'),
    ('7ª volta', 3300, ['Colhedor de Essência',
                        'Botas da Lucidez de Ionia (REFORMULADAS)',
                        'Adagas Rápidas Navori', 'Gume do Infinito',
                        'Lembrete Mortal'], 'Lembrete Mortal'),
    ('Build fechada', 3000, ['Colhedor de Essência',
                             'Botas da Lucidez de Ionia (REFORMULADAS)',
                             'Adagas Rápidas Navori', 'Gume do Infinito',
                             'Lembrete Mortal', 'Cutelo Negro'],
     'Cutelo Negro'),
]

ROTA_TANQUE = [
    ('Início', 500, ['Espada Longa'], 'Espada Longa'),
    ('1ª volta', 1200, ['Martelo de Guerra de Caulfield'],
     'Martelo de Guerra de Caulfield'),
    ('2ª volta', 900, ['Martelo de Guerra de Caulfield',
                       'Botas Ionianas da Lucidez'], 'Botas Ionianas (base)'),
    ('3ª volta', 1500, ['Manamune', 'Botas Ionianas da Lucidez'],
     'completa Manamune'),
    ('4ª volta', 1100, ['Manamune',
                        'Botas da Lucidez de Ionia (REFORMULADAS)'],
     'evolui as botas + Encantamento de Estase'),
    ('5ª volta', 3000, ['Manamune',
                        'Botas da Lucidez de Ionia (REFORMULADAS)',
                        'Colhedor de Essência'], 'Colhedor de Essência'),
    ('6ª volta', 3200, ['Manamune',
                        'Botas da Lucidez de Ionia (REFORMULADAS)',
                        'Colhedor de Essência', 'Espada do Rei Destruído'],
     'Espada do Rei Destruído'),
    ('7ª volta', 3300, ['Manamune',
                        'Botas da Lucidez de Ionia (REFORMULADAS)',
                        'Colhedor de Essência', 'Espada do Rei Destruído',
                        'Lembrete Mortal'], 'Lembrete Mortal'),
    ('Build fechada', 3400, ['Manamune',
                             'Botas da Lucidez de Ionia (REFORMULADAS)',
                             'Colhedor de Essência', 'Espada do Rei Destruído',
                             'Lembrete Mortal', 'Gume do Infinito'],
     'Gume do Infinito'),
]

NUCLEO = ['Colhedor de Essência', 'Adagas Rápidas Navori', 'Manamune',
          'Serrespada Quimiopunk', 'Cutelo Negro', 'Lâmina Impetuosa Solari',
          'Martelo de Guerra de Caulfield',
          'Botas da Lucidez de Ionia (REFORMULADAS)']


def soma_stats(itens, nomes):
    total = {}
    for nome in nomes:
        for chave, valor in itens[nome]['stats'].items():
            total[chave] = total.get(chave, 0) + valor
    return total


def tabela_rota(itens, rota, linhas):
    w = linhas.append
    w('| Etapa | Ouro da volta | Compra | Total investido | AD | Acel. Hab. | '
      'Habilidades a mais | Crítico |')
    w('|---|---|---|---|---|---|---|---|')
    acumulado = 0
    for etapa, gasto, nomes, compra in rota:
        acumulado += gasto
        t = soma_stats(itens, nomes)
        ah = t.get('ah', 0)
        crit = t.get('crit', 0)
        aviso = ' ⚠' if crit > 100 else ''
        w('| %s | %dg | %s | %dg | +%d | %d | **+%d%%** | %d%%%s |'
          % (etapa, gasto, compra, acumulado, t.get('ad', 0), ah, ah,
             min(crit, 100), aviso))
    w('')
    if max(soma_stats(itens, e[2]).get('crit', 0) for e in rota) >= 100:
        w('O crítico é limitado a 100%: quatro itens de 25% já fecham o '
          'limite, e o quinto seria ouro jogado fora — por isso a build '
          'termina com um item sem crítico.')
        w('')
    w('"Habilidades a mais" é matemática direta da Aceleração de Habilidade: '
      '%d de aceleração = %d%% mais conjurações no mesmo tempo. Para um '
      'campeão que vive de Q, essa é a coluna que importa.'
      % (soma_stats(itens, rota[-1][2]).get('ah', 0),
         soma_stats(itens, rota[-1][2]).get('ah', 0)))
    w('')


def main():
    itens = base.carregar_itens()
    linhas = []
    w = linhas.append

    w('# Smolder — passo a passo de build e de rota')
    w('')
    w('Gerado por `guia_smolder.py`, em cima do modelo de '
      '`analise_atirador.py` (preços e atributos de `metadata.json`).')
    w('')
    w('O que o projeto já diz sobre ele:')
    w('')
    w('- **Duo Bot** (`app.js`): tier **S**, nota **9,4**, melhor parceira '
      '**Janna**. A descrição do próprio projeto: *"dragãozinho focado em '
      'escalonamento tardio que precisa de farm seguro para atingir os 225 '
      'acúmulos da passiva"*, e a dica: *"Joguem de forma totalmente '
      'defensiva na fase de rotas. O foco exclusivo deve ser farmar e acumular '
      'cargas da passiva com o Q."*')
    w('- **Counters** (`campeoes_counters.md`): **vence** KaiSa, Kalista e '
      'Jinx; **perde** para Corki, Varus e Ezreal.')
    w('- Ele **não** aparece no ranking de `tencent_data.json`, então não há '
      'taxa de vitória no banco para citar.')
    w('')

    w('## 1. A build dele é o oposto da build da Miss Fortune')
    w('')
    w('No relatório de custo-benefício, três itens levaram a ressalva *"o dano '
      'depende de conjurar habilidades"* e por isso ficaram mal colocados no '
      'ranking de DPS: Colhedor de Essência, Lâmina Impetuosa Solari e Adagas '
      'Rápidas Navori. O Smolder é exatamente o campeão para quem essa '
      'ressalva vira vantagem — o dano dele sai do **Q**, não do ataque '
      'básico.')
    w('')
    w('Então a métrica muda: em vez de DPS por ouro, o que conta é **Dano de '
      'Ataque + Aceleração de Habilidade + mana**.')
    w('')
    w('| Item | Preço | AD | Acel. Hab. | Eficiência | Por que serve a ele |')
    w('|---|---|---|---|---|---|')
    razoes = {
        'Colhedor de Essência': 'Lâmina Arcana: cada habilidade vira dano no '
                                'próximo ataque + devolve mana',
        'Adagas Rápidas Navori': 'ataques cortam 15% da recarga restante — '
                                 'mais Q por luta',
        'Manamune': 'vira Muramana: AD vindo do mana e dano extra ao usar '
                    'habilidade',
        'Serrespada Quimiopunk': '45 de AD com Feridas Dolorosas, contra time '
                                 'com cura',
        'Cutelo Negro': 'AD, vida e 20 de aceleração — opção mais durável',
        'Lâmina Impetuosa Solari': 'habilidade carrega dano mágico no ataque '
                                   'seguinte',
        'Martelo de Guerra de Caulfield': 'melhor peça épica de AD+aceleração '
                                          'para a 1ª volta',
        'Botas da Lucidez de Ionia (REFORMULADAS)': '25 de aceleração — as '
                                                    'botas dele, sem discussão',
    }
    for nome in NUCLEO:
        it = itens[nome]
        st = base.stats_totais(nome, it)
        w('| %s | %dg | +%d | %d | %.0f%% | %s |'
          % (nome, it['preco'], st.get('ad', 0), st.get('ah', 0),
             base.eficiencia(nome, it) * 100, razoes[nome]))
    w('')
    w('> **A dúvida que muda a build:** se o Q dele aceitar crítico e efeitos '
      'de contato, Gume do Infinito, Navori e Colhedor de Essência são '
      'obrigatórios (é o que as rotas abaixo assumem). Se **não** aceitar, '
      'troque Gume do Infinito e Navori por **Cutelo Negro** e **Serrespada '
      'Quimiopunk** — mesmo ouro, todo em AD e aceleração. O banco do projeto '
      'não guarda dados de habilidade, então essa é a única coisa aqui que '
      'você precisa confirmar em jogo.')
    w('')

    w('## 2. Contra suporte FRÁGIL (Lux, Morgana, Nami, Sona, Seraphine)')
    w('')
    w('**Postura: neutra, farmando com prioridade.** Diferente da Miss '
      'Fortune, o Smolder não ganha a rota no nível 1 — ele ganha no minuto '
      '15. Contra suporte frágil você não precisa ter medo de se posicionar, '
      'então use isso para **empurrar e farmar mais**, não para caçar abate.')
    w('')
    w('- **Nível 1-4**: use o Q em tropa para acumular. Cada acúmulo perdido '
      'é dano permanente que você não vai ter na luta de Dragão.')
    w('- **Troque só com o Q**, de longe. Entrar em troca de ataque básico '
      'contra rota frágil é o único jeito de você perder uma rota que ganharia '
      'sozinho farmando.')
    w('- **Empurre**: rota frágil não contesta torre, e onda empurrada = mais '
      'tropas = mais acúmulos.')
    w('- **Contra Corki, Varus ou Ezreal** (os counters dele): recue a linha e '
      'farme sob a torre. São rotas de poke que vencem você antes do pico.')
    w('')
    w('### Rota de compras — %s de ouro até fechar a build'
      % '{:,}'.format(sum(e[1] for e in ROTA_FRAGIL)).replace(',', '.'))
    w('')
    tabela_rota(itens, ROTA_FRAGIL, linhas)
    w('> **Penetração é escolha única.** Lembrete Mortal, Lembranças do Lorde '
      'Dominik e Rancor de Serylda saem todos do Último Sussurro: só um por '
      'build.')
    w('')

    w('## 3. Contra suporte TANQUE/ENGATE (Leona, Nautilus, Blitzcrank, '
      'Alistar, Thresh)')
    w('')
    w('**Postura: totalmente defensiva** — é literalmente a dica que o projeto '
      'já dá para ele. Você não tem escape confiável e é o campeão mais fraco '
      'do mapa até acumular; qualquer morte cedo atrasa o pico duas vezes '
      '(perde ouro e perde acúmulos).')
    w('')
    w('- **Fique atrás da onda** e farme com o Q à distância máxima. Tropa '
      'morta sob a torre ainda conta.')
    w('- **Mana é o recurso da rota**, não vida: por isso a Manamune na 3ª '
      'volta. Sem mana você para de acumular, e parar de acumular é perder o '
      'jogo em câmera lenta.')
    w('- **Encantamento de Estase** nas botas: contra Leona ou Nautilus, os '
      '1.000g de estase valem mais que qualquer item de dano — você sobrevive '
      'ao combo inteiro e a luta vira 5v4 a seu favor.')
    w('- **Peça Janna, Lulu, Soraka ou Braum** (as parceiras que o próprio '
      'projeto lista). O suporte não é detalhe nessa rota: é a condição para '
      'a build funcionar.')
    w('- **Só jogue para frente depois do 2º lendário.** Antes disso, morrer '
      'custa mais que qualquer abate que você consiga.')
    w('')
    w('### Rota de compras — %s de ouro até fechar a build'
      % '{:,}'.format(sum(e[1] for e in ROTA_TANQUE)).replace(',', '.'))
    w('')
    tabela_rota(itens, ROTA_TANQUE, linhas)
    w('> Contra tanque, **Espada do Rei Destruído** entra na 6ª volta pelo '
      'motivo que o relatório mostrou: 40,7 de DPS por 1000g contra alvo de '
      '250 de armadura, o melhor da lista. Ela tira porcentagem da vida atual, '
      'que é o que atravessa armadura alta.')
    w('')

    w('## 4. Picos de poder')
    w('')
    w('| Momento | O que muda | Como aproveitar |')
    w('|---|---|---|')
    w('| **Nível 1-4** | Nenhum. É o campeão mais fraco do mapa | Só farmar; '
      'não force nada |')
    w('| **Nível 5 (ultimate)** | Primeiro recurso de luta coletiva | Usar '
      'para segurar Dragão, não para caçar abate |')
    w('| **1º lendário + botas evoluídas** | +45 de aceleração = **45% mais '
      'Q** | Começar a empurrar e disputar objetivo |')
    w('| **Acúmulos intermediários** | O Q começa a limpar onda sozinho | '
      'Empurrar e rotacionar; cada onda é acúmulo |')
    w('| **225 acúmulos** | O pico que a build inteira serve | A partir daí a '
      'luta coletiva é sua; jogue de trás e acerte o Q |')
    w('| **3º lendário** | Dano de item alcança o dano de acúmulo | Forçar '
      'Barão/Dragão enquanto o inimigo ainda não fechou build |')
    w('')
    w('A diferença dele para a Miss Fortune é essa: ela tem pico no **nível '
      '5** e cai no fim; ele **não tem pico nenhum antes dos acúmulos** e '
      'depois não tem teto. Jogar Smolder como se fosse Miss Fortune é o erro '
      'clássico.')
    w('')

    w('## 5. Runas')
    w('')
    w('O banco tem o texto das 58 runas, e a lista de Chave está em '
      '`RUNES_KEYSTONES` (`app.js`). Ele **não** tem a qual dos outros três '
      'espaços cada runa pertence — confirme na tela do jogo.')
    w('')
    w('### Chave')
    w('')
    w('| Runa | O que o texto do banco diz | Para o Smolder |')
    w('|---|---|---|')
    w('| **Conquistador** | *"acúmulos ao atingir um Campeão com ataques **ou '
      'habilidades** diferentes... 3-7 de AD por acúmulo... vampirismo '
      'universal no máximo"* | **Escolha padrão.** É a única Chave que acumula '
      'com habilidade, e o AD adaptativo alimenta direto o Q |')
    w('| **Primeiro Ataque** | *"concede ouro... recebe ouro extra de acordo '
      'com o dano adicional causado"* | **Escolha para escalar.** Ouro é '
      'exatamente o recurso que ele precisa acelerar |')
    w('| **Cometa Arcano** | *"causar dano a um Campeão com uma habilidade '
      'lançará um cometa... 35% do AD adicional"* | Para rota de poke com o Q '
      'à distância |')
    w('| Fortalecimento | *"3 ataques consecutivos... amplifica o dano em 9%"* '
      '| Amplificação boa, mas exige encostar com ataque básico — não é o '
      'padrão dele |')
    w('| Ritmo Fatal / Agilidade nos Pés | velocidade de ataque e cura | '
      'Desperdício: o dano dele não é ataque básico |')
    w('')
    w('### Os outros três espaços')
    w('')
    w('| Função | Runa | Por quê |')
    w('|---|---|---|')
    w('| Dano de habilidade | **Ataque em Sequência** | marca ao acertar '
      'habilidade e os 2 golpes seguintes causam dano adaptativo extra — feito '
      'para quem abre com Q |')
    w('| Mais Q | **Transcendência** | aceleração nos níveis 1 e 5, e no 9 '
      'reduz recarga ao acertar habilidade |')
    w('| Escala | **Tempestade Crescente** | AD adaptativo crescente a partir '
      'dos 6 min — a runa do campeão de escalonamento |')
    w('| Escala com farm | **Crescimento Excessivo** | 3 de vida por 2 tropas, '
      'sem teto; ele farma mais que qualquer um |')
    w('| Contra CC | **Perserverança** | tenacidade + resistências ao ser '
      'imobilizado |')
    w('| Sustentação | **Ventos Revigorantes** | regenera 6 + 2% da vida '
      'perdida, segura rota de poke |')
    w('')
    w('**Contra suporte frágil:** Conquistador + Ataque em Sequência + '
      'Transcendência + Tempestade Crescente.')
    w('')
    w('**Contra suporte tanque:** Conquistador + Transcendência + '
      'Perserverança + Crescimento Excessivo.')
    w('')
    w('**Feitiços:** Flash + Barreira contra engate (absorve o combo enquanto '
      'o CC ainda está em você); Flash + Curar contra rota de poke.')
    w('')

    w('## 6. Regras rápidas de postura')
    w('')
    w('| Situação | Jogar |')
    w('|---|---|')
    w('| Antes do nível 5, qualquer rota | **Passivo, farmar** |')
    w('| Suporte inimigo tanque, antes do 2º lendário | **Passivo** |')
    w('| Suporte inimigo frágil | **Neutro**: empurrar e farmar, trocar só '
      'com o Q |')
    w('| Rota contra KaiSa, Kalista ou Jinx (você é o counter) | **Neutro a '
      'agressivo** |')
    w('| Rota contra Corki, Varus ou Ezreal (eles te counteram) | **Passivo, '
      'farmar sob a torre** |')
    w('| Depois dos acúmulos altos + 3 itens | **Agressivo em luta coletiva, '
      'sempre de trás** |')
    w('| Escolher entre uma tropa e um abate arriscado | **Sempre a tropa** |')
    w('')
    w('A regra que resume o campeão: **morrer custa duas vezes** — o ouro e os '
      'acúmulos que você não fez. É por isso que a dica do próprio projeto é '
      'jogar "totalmente defensivo" na rota.')
    w('')

    conteudo = '\n'.join(linhas) + '\n'
    with open(SAIDA, 'w', encoding='utf-8') as fh:
        fh.write(conteudo)
    print(conteudo)


if __name__ == '__main__':
    main()
