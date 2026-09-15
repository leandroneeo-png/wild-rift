# Miss Fortune — passo a passo de build e de rota

Gerado por `guia_miss_fortune.py`, em cima do modelo de `analise_atirador.py` (preços e atributos de `metadata.json`).

Dados do próprio projeto (`tencent_data.json`): Miss Fortune está com **52,18% de vitórias**, 23,28% de presença e 2,42% de banimentos — é a atiradora mais jogada do banco. Pelos counters de `campeoes_counters.md` (coluna "Forte Contra"): ela **vence** Draven, Kalista e Jinx, e **perde** para Jhin, Sivir e Varus.

## 1. Por que a build dela foge do ranking geral de atirador

No relatório de custo-benefício, os melhores itens por ouro no 1º slot são Mata-Cráquens, Espada do Rei Destruído e Terminus — itens de dano fixo por ataque, feitos para quem fica batendo. A Miss Fortune não é isso: o dano dela sai de **Amor Duplo** (dano extra ao trocar de alvo), do **Tiro Duplo** (que quica e pode crítico) e do **Tiroteio**. Tudo isso escala com **AD e crítico**, não com tempo em combate.

Por isso a régua que vale para ela é a da eficiência de ouro pura, onde os itens de AD+crítico lideram:

| Item | Preço | AD | Crítico | Eficiência |
|---|---|---|---|---|
| Sedenta por Sangue | 3000g | +55 | 25% | **158%** |
| Lembrete Mortal | 3300g | +25 | 25% | **145%** |
| Lembranças do Lorde Dominik | 3300g | +25 | 25% | **142%** |
| Forca do Vendaval | 3100g | +50 | 25% | **128%** |
| A Coletora | 3000g | +45 | 25% | **126%** |
| Gume do Infinito | 3400g | +60 | 25% | **110%** |

## 2. Contra suporte FRÁGIL (Lux, Morgana, Nami, Sona, Seraphine, Zyra)

**Postura: agressiva desde o nível 1.** Nessa rota você tem o melhor dano de troca do jogo no nível 1-2, porque Amor Duplo dá dano extra sempre que você troca de alvo: bata numa tropa, bata no suporte, volte para a tropa. Contra suporte sem escudo forte e sem engate, cada troca é lucro.

- **Nível 1-2**: force a troca antes de o suporte inimigo chegar ao nível 3. Use o Tiro Duplo na tropa da frente para quicar no campeão.
- **Nível 5 (Tiroteio)**: primeiro grande pico. Com o suporte frágil sem mobilidade, o ult fecha a luta 2v2 — chame o caçador.
- **Empurre a rota**: rota frágil não consegue contestar torre. Empurrar acelera as voltas à base e o seu 1º lendário.
- **Cuidado**: Morgana (escudo bloqueia o ult) e Lux com escudo no aliado seguram a troca. Contra elas, jogue o E no chão para forçar recuo antes de entrar.

### Rota de compras — 18.600 de ouro até fechar a build

| Etapa | Ouro da volta | Compra | Total investido | AD | Crítico | DPS no frágil | DPS no tanque |
|---|---|---|---|---|---|---|---|
| Início | 500g | Espada Longa | 500g | +12 | 0% | 55 | 31 |
| 1ª volta | 1000g | Punhal Serrilhado | 1500g | +20 | 0% | 58 | 33 |
| 2ª volta | 1400g | Capa da Agilidade + Botas da Velocidade | 2900g | +20 | 20% | 67 | 38 |
| 3ª volta | 1700g | completa Força do Vendaval | 4600g | +50 | 25% | 98 | 56 |
| 4ª volta | 1300g | evolui as botas + encantamento | 5900g | +50 | 25% | 141 | 81 |
| 5ª volta | 3000g | A Coletora | 8900g | +95 | 50% | 220 | 123 |
| 6ª volta | 3400g | Gume do Infinito | 12300g | +155 | 75% | 370 | 207 |
| 7ª volta | 3300g | Lembrete Mortal | 15600g | +180 | 100% | 625 | 385 |
| Build fechada | 3000g | Sedenta por Sangue | 18600g | +235 | 100% | 744 | 458 |

"Ouro da volta" é o preço de loja do que você compra naquela ida à base e "total investido" soma tudo que já passou pela build, componentes inclusos — em jogo a loja abate o valor das peças que você já carrega, então o número na tela costuma ser menor.

DPS = ataques básicos do atirador de referência do relatório (nível 15, 110 de AD base, 0.90 ataque/s). Serve para comparar as etapas entre si, não é a simulação exata da Miss Fortune — Amor Duplo, o Tiro Duplo e o Tiroteio somam por cima disso e escalam com AD e crítico.

> **Penetração é escolha única.** Lembrete Mortal, Lembranças do Lorde Dominik e Rancor de Serylda nascem todos do Último Sussurro: a loja não deixa levar dois. Escolha pelo inimigo — Dominik contra vida alta, Lembrete Mortal contra cura, Serylda contra mobilidade.

**Ordem de habilidades:** maximize o **Tiro Duplo** primeiro (dano de rota e limpeza de onda), depois **Golpes Fatais**, deixando **Fazer Chover** por último. Ultimate sempre que disponível (nível 5, 9, 13).

## 3. Contra suporte TANQUE/ENGATE (Leona, Nautilus, Blitzcrank, Alistar, Thresh, Braum, Rell)

**Postura: passiva até o nível 5 e até ter botas.** Aqui a troca de dano não é o problema — o problema é uma única pegada. Você não tem dash nem escudo: qualquer acerto de Blitzcrank, Nautilus ou Leona vira morte.

- **Nível 1-4**: fique **atrás da sua onda**, nunca na lateral livre. Farme com ataque básico e com o Tiro Duplo quicando; não conteste a troca, você perde a corrida de dano contra um tanque com cura do suporte.
- **Segure o Fazer Chover para defesa**, não para dano: a lentidão é o que cancela o engate depois que o CC deles acerta.
- **Nível 5**: primeiro momento de jogar para frente — mas só com o CC principal do suporte inimigo em recarga (Q do Blitz, E do Naut, E da Leona). Conte a recarga, é a informação mais valiosa da rota.
- **Encantamento de Estase (1.000g) ou de Mercúrio (800g)** nas botas é obrigatório nessa rota, e vale mais que 1.000g de dano.
- **Contra tanque de linha de frente**, os números do relatório são claros: Espada do Rei Destruído (40,7 DPS/1000g contra tanque) e Lembrete Mortal são os itens que mantêm rendimento; crítico puro perde quase metade do valor contra 250 de armadura.

### Rota de compras — 18.700 de ouro até fechar a build

| Etapa | Ouro da volta | Compra | Total investido | AD | Crítico | DPS no frágil | DPS no tanque |
|---|---|---|---|---|---|---|---|
| Início | 500g | Espada Longa | 500g | +12 | 0% | 55 | 31 |
| 1ª volta | 1200g | Cetro Vampírico | 1700g | +20 | 0% | 58 | 33 |
| 2ª volta | 900g | Botas do Dinamismo (base) | 2600g | +20 | 0% | 58 | 33 |
| 3ª volta | 1800g | completa Sedenta por Sangue | 4400g | +55 | 25% | 88 | 50 |
| 4ª volta | 1300g | evolui as botas + Encantamento de Estase | 5700g | +95 | 25% | 120 | 68 |
| 5ª volta | 3200g | Espada do Rei Destruído | 8900g | +120 | 25% | 245 | 170 |
| 6ª volta | 3300g | Lembrete Mortal | 12200g | +145 | 50% | 402 | 297 |
| 7ª volta | 3400g | Gume do Infinito | 15600g | +205 | 75% | 601 | 423 |
| Build fechada | 3100g | Cimitarra Mercurial | 18700g | +245 | 75% | 666 | 464 |

"Ouro da volta" é o preço de loja do que você compra naquela ida à base e "total investido" soma tudo que já passou pela build, componentes inclusos — em jogo a loja abate o valor das peças que você já carrega, então o número na tela costuma ser menor.

DPS = ataques básicos do atirador de referência do relatório (nível 15, 110 de AD base, 0.90 ataque/s). Serve para comparar as etapas entre si, não é a simulação exata da Miss Fortune — Amor Duplo, o Tiro Duplo e o Tiroteio somam por cima disso e escalam com AD e crítico.

> **Um item de penetração só.** Aqui a escolha é Lembrete Mortal (as Feridas Dolorosas cortam a cura do suporte tanque). Se o time inimigo for de vida alta sem cura, troque por Lembranças do Lorde Dominik no mesmo slot — nunca os dois.

> A **Cimitarra Mercurial** fecha a build porque o ativo dela limpa o CC que te mata nessa rota. Se levar ela, o encantamento das botas deve ser **Estase**, não Mercúrio — são o mesmo efeito.

**Ordem de habilidades:** ainda Tiro Duplo primeiro, mas suba o **Fazer Chover** um ponto cedo (nível 3) pelo desengate. Se o suporte inimigo é Blitzcrank, o ponto em Fazer Chover no nível 2 já se paga.

## 4. Picos de poder — quando você é mais forte que o inimigo

| Momento | O que muda | Como aproveitar |
|---|---|---|
| **Nível 1-2** | Amor Duplo dá o melhor dano de troca da rota | Trocar alvo a cada ataque; só contra suporte frágil |
| **Nível 5 — Tiroteio** | Maior pico da fase de rota | Lutar 2v2 e chamar o caçador; pedir o primeiro Arauto |
| **1º lendário (~4.000g investidos)** | Sai de ~54 para ~98 de DPS de ataque, e o Tiroteio passa a matar suporte frágil sozinho | Forçar a torre da rota inferior |
| **Nível 9-10 + 2º lendário** | Habilidades no máximo e crítico em 50% | Rotacionar para Dragão; é a janela mais forte da partida |
| **Gume do Infinito com crítico alto** | Crítico passa de 175% para 205% de dano — vale 39,3 DPS/1000g no 4º slot contra 13,8 no 1º | Só comprar depois de 50% de crítico |
| **Build fechada (6 itens)** | Sem novos picos: a partir daí é posicionamento | Ficar no fundo, ult só com o CC inimigo gasto |

## 5. Runas

O `metadata.json` tem 58 runas com o texto completo, e o `app.js` (`RUNES_KEYSTONES`, linha 107) diz quais são de **Chave**. O que o banco **não** tem é a qual dos outros três espaços cada runa pertence — então só a escolha de Chave abaixo é calculada; as demais vão por função, e você confirma o espaço na tela do jogo.

### Chave — comparação calculada

Build de referência: Força do Vendaval + Grevas do Berserker + A Coletora + Gume do Infinito (155 de AD, 75% de crítico). Duas colunas porque as duas situações premiam runas diferentes: **luta longa** é DPS com você batendo sem parar; **troca de 3 ataques** é o que realmente acontece na rota.

| Runa de Chave | Luta longa (DPS) | Troca de 3 ataques (dano) | Alcance do efeito |
|---|---|---|---|
| **Eletrocutar** | 380 | 879 | Explosão a cada 13s; bom para pegar alvo isolado |
| **Fortalecimento** | 430 | 853 | Amplifica todo o dano, habilidades incluídas |
| **Primeiro Ataque** | 378 | 800 | Dano verdadeiro nos 3s iniciais + ouro extra |
| **Conquistador** | 429 | 787 | AD adaptativo: soma também nas habilidades |
| **Ritmo Fatal** | 505 | 748 | Só ataque básico; ultrapassa o limite de vel. de ataque |
| **Colheita Sombria** | 378 | 748 | Só contra alvo abaixo de 50% de vida |
| **Agilidade nos Pés** | 370 | 748 | Cura e velocidade; dano quase nulo |
| _(sem runa de Chave)_ | 370 | 748 | referência |

**Leitura honesta da tabela:** em luta longa, **Ritmo Fatal** ganha (505 contra 430 de DPS), porque 60% de velocidade de ataque rende muito quando você fica batendo. Na troca de 3 ataques ele rende **zero** — mais ataques por segundo não é mais dano por ataque, e a Miss Fortune não fica 6 ataques em cima de ninguém.

**Escolha padrão: Fortalecimento.** É a segunda melhor em luta longa, a segunda melhor na troca curta, e é a única cuja amplificação de 9% também vale para o Tiro Duplo e o Tiroteio — que a tabela nem conta, porque ela só mede ataque básico.

- **Contra suporte frágil, jogando para matar cedo**: **Eletrocutar** — 879 de dano na troca de 3 ataques contra 853 do Fortalecimento. É a runa que transforma uma troca no nível 3 em abate.
- **Contra suporte tanque**: Fortalecimento. A amplificação de 9% funciona contra qualquer armadura; crítico, não.
- **Ritmo Fatal** só se você for de segurar ataque básico em luta coletiva longa — não é o padrão dela.
- **Primeiro Ataque** se você joga para economia: o ouro extra adianta o primeiro lendário, que é o pico que mais importa.

### Os outros três espaços

| Função | Runa | Por quê |
|---|---|---|
| Dano contínuo | **Brutal** | 6 + 8% do AD adicional por ataque, adaptativo; escala com a build inteira |
| Execução | **Golpe de Misericórdia** | +8% de dano em alvo abaixo de 40% de vida — casa com a passiva de execução de A Coletora |
| Abertura de luta | **Dilacerar** | +8% de dano em alvo acima de 60% de vida; melhor que Golpe de Misericórdia em rota de poke |
| Sobrevivência na rota | **Ventos Revigorantes** | regenera 6 + 2% da vida perdida; segura rota contra poke |
| Contra CC pesado | **Perserverança** | 10% de tenacidade + armadura e RM ao ser imobilizada — direto contra Leona, Naut e Blitz |
| Escala tardia | **Tempestade Crescente** | AD adaptativo que cresce a cada 3 min a partir dos 6 min |
| Vampirismo | **Lenda: Linhagem** | até 8% de vampirismo universal |

**Contra suporte frágil:** Brutal + Dilacerar + Tempestade Crescente. Rota de troca de dano, você quer dano puro em cima do Amor Duplo.

**Contra suporte tanque:** Brutal + Perserverança + Ventos Revigorantes. Aqui sobreviver ao engate vale mais do que 8% de dano — sem escape, tenacidade é o que te dá a chance de usar o Flash depois do CC.

> Se duas dessas caírem no mesmo espaço na tela do jogo, fique com a de cima da lista e pegue a próxima da mesma coluna.

### Feitiços

Feitiços disponíveis no projeto (`SPELLS_MAPPING`, `app.js`): Flash, Curar, Barreira, Exaustão, Incendiar, Purificar, Fantasma e Golpear.

**Flash + Curar** contra suporte frágil (a cura salva da troca e do Incendiar). **Flash + Barreira** contra suporte de engate: a barreira absorve a explosão do combo enquanto o CC ainda está em cima de você.

## 6. Regras rápidas de postura

| Situação | Jogar |
|---|---|
| Suporte inimigo frágil, os dois no nível 1-2 | **Agressivo** |
| Suporte inimigo tanque, antes do seu nível 5 | **Passivo, farmar** |
| CC principal do suporte inimigo em recarga | **Agressivo** |
| Você sem o Tiroteio, eles com o ult pronto | **Passivo** |
| Rota contra Draven, Kalista ou Jinx (você é o counter) | **Agressivo desde o nível 1** |
| Rota contra Jhin, Sivir ou Varus (eles te counteram) | **Passivo até o 1º lendário** |
| Luta coletiva com 3+ inimigos agrupados | Ult de trás, nunca de frente |

> **Confira a árvore na loja.** O `metadata.json` guarda preço, atributos e passiva, mas não a receita nem a exclusividade dos itens. Nenhum número deste guia detecta sozinho que dois itens não podem ser combinados — os conflitos conhecidos estão listados em `atirador_custo_beneficio.md`, seção 5.

A Miss Fortune não tem escape: toda decisão agressiva depende de o inimigo ter gastado o CC dele antes. Essa é a única regra que não muda com o item.

