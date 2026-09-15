# -*- coding: utf-8 -*-
"""
Gera o guia da Yunara (guia_yunara.md).

ATENÇÃO: a Yunara não existe na base do projeto — não está em hero_dict.json
(158 campeões), nem em campeoes_counters.md (134), nem no ranking de
tencent_data.json (126). Então, diferente dos guias da Miss Fortune e do
Smolder, aqui não há counters, duo nem taxa de vitória para citar.

O que é calculado continua valendo: preços, atributos e passivas dos itens
saem de metadata.json, e o modelo de dano é o mesmo de analise_atirador.py.
A rota abaixo é a do arquétipo "atirador de ataque básico com crítico" — o
ótimo que o próprio relatório aponta para quem tira dano de ataque básico.
"""
import analise_atirador as base
import guia_miss_fortune as mf

SAIDA = 'guia_yunara.md'

NOTA_DPS = ('e é a métrica certa para um atirador de ataque básico; se a '
            'Yunara tirar dano de habilidade, esta coluna subestima a build '
            'de aceleração')

ROTA_FRAGIL = [
    ('Início', 500, ['Espada Longa'], 'Espada Longa'),
    ('1ª volta', 1350, ['Alijava Vespertina'], 'Alijava Vespertina'),
    ('2ª volta', 900, ['Alijava Vespertina', 'Grevas do Berserker'],
     'Grevas do Berserker (base)'),
    ('3ª volta', 1450, ['Mata-Cráquens', 'Grevas do Berserker'],
     'completa Mata-Cráquens'),
    ('4ª volta', 1300, ['Mata-Cráquens', 'Grevas do Berserker (Reformuladas)'],
     'evolui as botas'),
    ('5ª volta', 3100, ['Mata-Cráquens', 'Grevas do Berserker (Reformuladas)',
                        '[NEW]Forca do Vendaval'], 'Força do Vendaval'),
    ('6ª volta', 3400, ['Mata-Cráquens', 'Grevas do Berserker (Reformuladas)',
                        '[NEW]Forca do Vendaval', 'Gume do Infinito'],
     'Gume do Infinito'),
    ('7ª volta', 2900, ['Mata-Cráquens', 'Grevas do Berserker (Reformuladas)',
                        '[NEW]Forca do Vendaval', 'Gume do Infinito',
                        'Furacão de Runaan'], 'Furacão de Runaan'),
    ('Build fechada', 3300, ['Mata-Cráquens',
                             'Grevas do Berserker (Reformuladas)',
                             '[NEW]Forca do Vendaval', 'Gume do Infinito',
                             'Furacão de Runaan', 'Lembrete Mortal'],
     'Lembrete Mortal'),
]

ROTA_TANQUE = [
    ('Início', 500, ['Espada Longa'], 'Espada Longa'),
    ('1ª volta', 1200, ['Cetro Vampírico'], 'Cetro Vampírico'),
    ('2ª volta', 900, ['Cetro Vampírico', 'Grevas do Berserker'],
     'Grevas do Berserker (base)'),
    ('3ª volta', 1500, ['Espada do Rei Destruído', 'Grevas do Berserker'],
     'completa Espada do Rei Destruído'),
    ('4ª volta', 1300, ['Espada do Rei Destruído',
                        'Grevas do Berserker (Reformuladas)'],
     'evolui as botas + Encantamento de Estase'),
    ('5ª volta', 2800, ['Espada do Rei Destruído',
                        'Grevas do Berserker (Reformuladas)',
                        'Mata-Cráquens'], 'Mata-Cráquens'),
    ('6ª volta', 3100, ['Espada do Rei Destruído',
                        'Grevas do Berserker (Reformuladas)', 'Mata-Cráquens',
                        '[NEW]Forca do Vendaval'], 'Força do Vendaval'),
    ('7ª volta', 3300, ['Espada do Rei Destruído',
                        'Grevas do Berserker (Reformuladas)', 'Mata-Cráquens',
                        '[NEW]Forca do Vendaval', 'Lembrete Mortal'],
     'Lembrete Mortal'),
    ('Build fechada', 3400, ['Espada do Rei Destruído',
                             'Grevas do Berserker (Reformuladas)',
                             'Mata-Cráquens', '[NEW]Forca do Vendaval',
                             'Lembrete Mortal', 'Gume do Infinito'],
     'Gume do Infinito'),
]

BUILD_RUNAS = ['Mata-Cráquens', 'Grevas do Berserker (Reformuladas)',
               '[NEW]Forca do Vendaval', 'Gume do Infinito']


def main():
    itens = base.carregar_itens()
    mf.BUILD_COMPARACAO = BUILD_RUNAS      # runas avaliadas nesta build
    linhas = []
    w = linhas.append

    w('# Yunara — rota de build e de partida')
    w('')
    w('> **Leia isto antes.** A Yunara **não está na base do projeto**: não '
      'aparece em `hero_dict.json` (158 campeões), nem em '
      '`campeoes_counters.md` (134), nem no ranking de `tencent_data.json` '
      '(126). Diferente dos guias da Miss Fortune e do Smolder, aqui **não há '
      'counters, duo recomendado nem taxa de vitória** para citar, e o acesso '
      'ao site de origem (`wildlegends.net`) está bloqueado nesta sessão, '
      'então também não deu para conferir por fora.')
    w('>')
    w('> O que continua valendo: preços, atributos e passivas dos itens saem '
      'de `metadata.json`, e as contas são as mesmas dos outros guias. A rota '
      'abaixo é a do **arquétipo de atirador de ataque básico com crítico** — '
      'que é o ótimo apontado pelo próprio relatório para quem tira dano de '
      'ataque básico. Se a Yunara for de dano por habilidade, a rota certa é '
      'a do Smolder, não esta.')
    w('')

    w('## 1. Qual rota serve a ela')
    w('')
    w('Os dois guias anteriores cobriram os extremos, e a Yunara cai em um '
      'deles:')
    w('')
    w('| Padrão de dano | Exemplo | Rota |')
    w('|---|---|---|')
    w('| Explosão curta, dano vindo de habilidade e ult | Miss Fortune | AD + '
      'crítico desde cedo (`guia_miss_fortune.md`) |')
    w('| Dano por habilidade repetida, escalonamento | Smolder | AD + '
      'aceleração + mana (`guia_smolder.md`) |')
    w('| **Ataque básico contínuo, crítico** | **esta rota** | dano fixo por '
      'ataque primeiro, crítico depois |')
    w('')
    w('Esta terceira rota é a que o relatório de custo-benefício mais premia: '
      'Mata-Cráquens (29,2 de DPS por 1000g como 1º item), Espada do Rei '
      'Destruído (27,9) e Terminus (26,4) lideram justamente porque o dano '
      'deles não depende de crítico acumulado. Crítico como 1º item é o pior '
      'investimento da lista — Gume do Infinito rende 13,8 no 1º slot e 39,3 '
      'no 4º.')
    w('')

    w('## 2. Contra suporte FRÁGIL (Lux, Morgana, Nami, Sona, Seraphine)')
    w('')
    w('**Postura: agressiva a partir do nível 3**, e não do 1. Atirador de '
      'ataque básico depende de ter tempo parado batendo; no nível 1-2, sem '
      'velocidade de ataque nenhuma, a troca é fraca. Farme até o 3, e a '
      'partir daí force troca sempre que o suporte inimigo pisar à frente da '
      'onda.')
    w('')
    w('- **Empurre**: rota frágil não contesta torre e você ganha tempo de '
      'bater na estrutura — o Mata-Cráquens acelera isso.')
    w('- **Nível 5**: a ultimate é o pico de todo campeão no Wild Rift; use '
      'para fechar a luta 2v2 que você já estava ganhando, não para começar '
      'uma perdida.')
    w('- **Não persiga** depois da troca vencida: sem dash, o recuo do '
      'inimigo é o gancho do caçador dele.')
    w('')
    mf.tabela(itens, ROTA_FRAGIL, 'Rota de compras', linhas, NOTA_DPS)
    w('> **Penetração é escolha única**: Lembrete Mortal, Lembranças do Lorde '
      'Dominik e Rancor de Serylda saem todos do Último Sussurro. E crítico '
      'tem teto de 100% — Força do Vendaval, Gume do Infinito, Runaan e '
      'Lembrete Mortal somam exatamente 100%, sem desperdício.')
    w('')

    w('## 3. Contra suporte TANQUE/ENGATE (Leona, Nautilus, Blitzcrank, '
      'Alistar, Thresh)')
    w('')
    w('**Postura: passiva até as botas evoluídas.** O problema não é a troca '
      'de dano, é o engate: um acerto de CC com você sem Estase é morte '
      'garantida.')
    w('')
    w('- **Fique atrás da onda** e farme; conte a recarga do CC principal do '
      'suporte inimigo — é a informação que define quando você pode avançar.')
    w('- **Espada do Rei Destruído como 1º lendário**: contra alvo de 250 de '
      'armadura ela rende 40,7 de DPS por 1000g, o melhor da lista inteira, '
      'porque tira porcentagem da vida atual em vez de depender de crítico.')
    w('- **Encantamento de Estase** nas botas vale mais que 1.000g de dano '
      'nessa rota.')
    w('- **Só avance depois do 2º lendário**, e sempre com o CC deles gasto.')
    w('')
    mf.tabela(itens, ROTA_TANQUE, 'Rota de compras', linhas, NOTA_DPS)

    w('## 4. Picos de poder')
    w('')
    w('Sem os dados de habilidade dela, os picos abaixo são os de **item**, '
      'que valem para qualquer atirador de ataque básico, mais o nível 5, que '
      'é a ultimate de todo campeão no Wild Rift.')
    w('')
    perfis = [('1º lendário + botas base', ['Mata-Cráquens',
                                            'Grevas do Berserker']),
              ('botas evoluídas', ['Mata-Cráquens',
                                   'Grevas do Berserker (Reformuladas)']),
              ('2º lendário', ['Mata-Cráquens',
                               'Grevas do Berserker (Reformuladas)',
                               '[NEW]Forca do Vendaval']),
              ('3º lendário (Gume)', BUILD_RUNAS)]
    w('| Momento | DPS no frágil | Salto |')
    w('|---|---|---|')
    anterior = None
    for rotulo, nomes in perfis:
        p, _ = mf.perfil_da_build(itens, nomes, base.ALVOS['frágil'])
        d = base.dps(p, base.ALVOS['frágil'])
        salto = '—' if anterior is None else '+%.0f%%' % ((d / anterior - 1) * 100)
        w('| %s | %.0f | %s |' % (rotulo, d, salto))
        anterior = d
    w('')
    w('O maior salto da partida é o **das botas evoluídas**: 50% de velocidade '
      'de ataque de uma vez só, por 1.300g. É o momento de forçar torre e '
      'Dragão.')
    w('')

    w('## 5. Runas')
    w('')
    w('Aqui a conta muda em relação à Miss Fortune, e a diferença é o ponto '
      'inteiro deste guia: para quem fica batendo, **Ritmo Fatal ganha**.')
    w('')
    w('| Runa de Chave | Luta longa (DPS) | Troca de 3 ataques | Alcance |')
    w('|---|---|---|---|')
    dados = []
    for nome, (nota, _) in mf.RUNAS_CHAVE.items():
        dados.append((mf.dps_com_runa(itens, nome, base.ALVOS['frágil']),
                      mf.troca_de_3_ataques(itens, nome, base.ALVOS['frágil']),
                      nome, nota))
    for longa, troca, nome, nota in sorted(dados, reverse=True):
        w('| **%s** | %.0f | %.0f | %s |' % (nome, longa, troca, nota))
    w('')
    w('**Escolha: Ritmo Fatal**, se ela for de ataque básico contínuo — '
      '%.0f de DPS contra %.0f do Fortalecimento, e ainda ultrapassa o limite '
      'de velocidade de ataque no máximo de acúmulos. É a runa que a Miss '
      'Fortune não aproveita e este arquétipo aproveita inteira.'
      % (mf.dps_com_runa(itens, 'Ritmo Fatal', base.ALVOS['frágil']),
         mf.dps_com_runa(itens, 'Fortalecimento', base.ALVOS['frágil'])))
    w('')
    w('- **Contra suporte tanque**: Fortalecimento, pela amplificação de 9% '
      'que funciona contra qualquer armadura.')
    w('- **Se ela tiver explosão curta em vez de dano contínuo**: Eletrocutar '
      '(%.0f de dano numa troca de 3 ataques, o melhor da tabela).'
      % mf.troca_de_3_ataques(itens, 'Eletrocutar', base.ALVOS['frágil']))
    w('')
    w('**Outros três espaços** — Brutal (dano por ataque), Lenda: '
      'Espontaneidade (até 20% de velocidade de ataque, que este arquétipo '
      'converte direto em dano), Golpe de Misericórdia ou Dilacerar, e '
      'Perserverança no lugar de um deles contra rota de engate. O banco não '
      'guarda a qual espaço cada runa pertence — confirme na tela do jogo.')
    w('')
    w('**Feitiços:** Flash + Curar contra rota frágil; Flash + Barreira '
      'contra engate.')
    w('')

    w('## 6. O que falta para este guia ficar no nível dos outros')
    w('')
    w('| Falta | Efeito | Como resolver |')
    w('|---|---|---|')
    w('| Yunara em `hero_dict.json` | ela não aparece em nenhuma tela do site '
      '| rodar o sync de campeões, se ela já estiver no Wild Rift |')
    w('| Linha em `campeoes_counters.md` | sem "forte contra / fraco contra" '
      '| `generate_counters_list.py`, depois do sync |')
    w('| Entrada no Duo Bot (`app.js`) | sem suporte recomendado | adicionar '
      'junto dos outros atiradores |')
    w('| Dados de habilidade (nenhum campeão tem) | picos e combos ficam '
      'genéricos | precisaria de uma fonte nova; hoje o banco só tem itens, '
      'runas e feitiços |')
    w('')
    w('Me diga se ela é de **ataque básico** ou de **habilidade**, e eu ajusto '
      'a rota — a estrutura de cálculo já está pronta para as duas.')
    w('')

    conteudo = '\n'.join(linhas) + '\n'
    with open(SAIDA, 'w', encoding='utf-8') as fh:
        fh.write(conteudo)
    print(conteudo)


if __name__ == '__main__':
    main()
