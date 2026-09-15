# Smolder — passo a passo de build e de rota

Gerado por `guia_smolder.py`, em cima do modelo de `analise_atirador.py` (preços e atributos de `metadata.json`).

O que o projeto já diz sobre ele:

- **Duo Bot** (`app.js`): tier **S**, nota **9,4**, melhor parceira **Janna**. A descrição do próprio projeto: *"dragãozinho focado em escalonamento tardio que precisa de farm seguro para atingir os 225 acúmulos da passiva"*, e a dica: *"Joguem de forma totalmente defensiva na fase de rotas. O foco exclusivo deve ser farmar e acumular cargas da passiva com o Q."*
- **Counters** (`campeoes_counters.md`): **vence** KaiSa, Kalista e Jinx; **perde** para Corki, Varus e Ezreal.
- Ele **não** aparece no ranking de `tencent_data.json`, então não há taxa de vitória no banco para citar.

## 1. A build dele é o oposto da build da Miss Fortune

No relatório de custo-benefício, três itens levaram a ressalva *"o dano depende de conjurar habilidades"* e por isso ficaram mal colocados no ranking de DPS: Colhedor de Essência, Lâmina Impetuosa Solari e Adagas Rápidas Navori. O Smolder é exatamente o campeão para quem essa ressalva vira vantagem — o dano dele sai do **Q**, não do ataque básico.

Então a métrica muda: em vez de DPS por ouro, o que conta é **Dano de Ataque + Aceleração de Habilidade + mana**.

| Item | Preço | AD | Acel. Hab. | Eficiência | Por que serve a ele |
|---|---|---|---|---|---|
| Colhedor de Essência | 3000g | +35 | 20 | 117% | Lâmina Arcana: cada habilidade vira dano no próximo ataque + devolve mana |
| Adagas Rápidas Navori | 2800g | +0 | 0 | 104% | ataques cortam 15% da recarga restante — mais Q por luta |
| Manamune | 2700g | +25 | 20 | 85% | vira Muramana: AD vindo do mana e dano extra ao usar habilidade |
| Serrespada Quimiopunk | 2800g | +45 | 15 | 118% | 45 de AD com Feridas Dolorosas, contra time com cura |
| Cutelo Negro | 3000g | +40 | 20 | 127% | AD, vida e 20 de aceleração — opção mais durável |
| Lâmina Impetuosa Solari | 3000g | +0 | 20 | 113% | habilidade carrega dano mágico no ataque seguinte |
| Martelo de Guerra de Caulfield | 1200g | +25 | 10 | 120% | melhor peça épica de AD+aceleração para a 1ª volta |
| Botas da Lucidez de Ionia (REFORMULADAS) | 2000g | +0 | 25 | 95% | 25 de aceleração — as botas dele, sem discussão |

> **A dúvida que muda a build:** se o Q dele aceitar crítico e efeitos de contato, Gume do Infinito, Navori e Colhedor de Essência são obrigatórios (é o que as rotas abaixo assumem). Se **não** aceitar, troque Gume do Infinito e Navori por **Cutelo Negro** e **Serrespada Quimiopunk** — mesmo ouro, todo em AD e aceleração. O banco do projeto não guarda dados de habilidade, então essa é a única coisa aqui que você precisa confirmar em jogo.

## 2. Contra suporte FRÁGIL (Lux, Morgana, Nami, Sona, Seraphine)

**Postura: neutra, farmando com prioridade.** Diferente da Miss Fortune, o Smolder não ganha a rota no nível 1 — ele ganha no minuto 15. Contra suporte frágil você não precisa ter medo de se posicionar, então use isso para **empurrar e farmar mais**, não para caçar abate.

- **Nível 1-4**: use o Q em tropa para acumular. Cada acúmulo perdido é dano permanente que você não vai ter na luta de Dragão.
- **Troque só com o Q**, de longe. Entrar em troca de ataque básico contra rota frágil é o único jeito de você perder uma rota que ganharia sozinho farmando.
- **Empurre**: rota frágil não contesta torre, e onda empurrada = mais tropas = mais acúmulos.
- **Contra Corki, Varus ou Ezreal** (os counters dele): recue a linha e farme sob a torre. São rotas de poke que vencem você antes do pico.

### Rota de compras — 18.000 de ouro até fechar a build

| Etapa | Ouro da volta | Compra | Total investido | AD | Acel. Hab. | Habilidades a mais | Crítico |
|---|---|---|---|---|---|---|---|
| Início | 500g | Espada Longa | 500g | +12 | 0 | **+0%** | 0% |
| 1ª volta | 1200g | Martelo de Guerra de Caulfield | 1700g | +25 | 10 | **+10%** | 0% |
| 2ª volta | 900g | Botas Ionianas (base) | 2600g | +25 | 25 | **+25%** | 0% |
| 3ª volta | 1800g | completa Colhedor de Essência | 4400g | +35 | 35 | **+35%** | 25% |
| 4ª volta | 1100g | evolui as botas | 5500g | +35 | 45 | **+45%** | 25% |
| 5ª volta | 2800g | Adagas Rápidas Navori | 8300g | +35 | 45 | **+45%** | 50% |
| 6ª volta | 3400g | Gume do Infinito | 11700g | +95 | 45 | **+45%** | 75% |
| 7ª volta | 3300g | Lembrete Mortal | 15000g | +120 | 45 | **+45%** | 100% |
| Build fechada | 3000g | Cutelo Negro | 18000g | +160 | 65 | **+65%** | 100% |

O crítico é limitado a 100%: quatro itens de 25% já fecham o limite, e o quinto seria ouro jogado fora — por isso a build termina com um item sem crítico.

"Habilidades a mais" é matemática direta da Aceleração de Habilidade: 65 de aceleração = 65% mais conjurações no mesmo tempo. Para um campeão que vive de Q, essa é a coluna que importa.

> **Penetração é escolha única.** Lembrete Mortal, Lembranças do Lorde Dominik e Rancor de Serylda saem todos do Último Sussurro: só um por build.

## 3. Contra suporte TANQUE/ENGATE (Leona, Nautilus, Blitzcrank, Alistar, Thresh)

**Postura: totalmente defensiva** — é literalmente a dica que o projeto já dá para ele. Você não tem escape confiável e é o campeão mais fraco do mapa até acumular; qualquer morte cedo atrasa o pico duas vezes (perde ouro e perde acúmulos).

- **Fique atrás da onda** e farme com o Q à distância máxima. Tropa morta sob a torre ainda conta.
- **Mana é o recurso da rota**, não vida: por isso a Manamune na 3ª volta. Sem mana você para de acumular, e parar de acumular é perder o jogo em câmera lenta.
- **Encantamento de Estase** nas botas: contra Leona ou Nautilus, os 1.000g de estase valem mais que qualquer item de dano — você sobrevive ao combo inteiro e a luta vira 5v4 a seu favor.
- **Peça Janna, Lulu, Soraka ou Braum** (as parceiras que o próprio projeto lista). O suporte não é detalhe nessa rota: é a condição para a build funcionar.
- **Só jogue para frente depois do 2º lendário.** Antes disso, morrer custa mais que qualquer abate que você consiga.

### Rota de compras — 18.100 de ouro até fechar a build

| Etapa | Ouro da volta | Compra | Total investido | AD | Acel. Hab. | Habilidades a mais | Crítico |
|---|---|---|---|---|---|---|---|
| Início | 500g | Espada Longa | 500g | +12 | 0 | **+0%** | 0% |
| 1ª volta | 1200g | Martelo de Guerra de Caulfield | 1700g | +25 | 10 | **+10%** | 0% |
| 2ª volta | 900g | Botas Ionianas (base) | 2600g | +25 | 25 | **+25%** | 0% |
| 3ª volta | 1500g | completa Manamune | 4100g | +25 | 35 | **+35%** | 0% |
| 4ª volta | 1100g | evolui as botas + Encantamento de Estase | 5200g | +25 | 45 | **+45%** | 0% |
| 5ª volta | 3000g | Colhedor de Essência | 8200g | +60 | 65 | **+65%** | 25% |
| 6ª volta | 3200g | Espada do Rei Destruído | 11400g | +85 | 65 | **+65%** | 25% |
| 7ª volta | 3300g | Lembrete Mortal | 14700g | +110 | 65 | **+65%** | 50% |
| Build fechada | 3400g | Gume do Infinito | 18100g | +170 | 65 | **+65%** | 75% |

"Habilidades a mais" é matemática direta da Aceleração de Habilidade: 65 de aceleração = 65% mais conjurações no mesmo tempo. Para um campeão que vive de Q, essa é a coluna que importa.

> Contra tanque, **Espada do Rei Destruído** entra na 6ª volta pelo motivo que o relatório mostrou: 40,7 de DPS por 1000g contra alvo de 250 de armadura, o melhor da lista. Ela tira porcentagem da vida atual, que é o que atravessa armadura alta.

## 4. Picos de poder

| Momento | O que muda | Como aproveitar |
|---|---|---|
| **Nível 1-4** | Nenhum. É o campeão mais fraco do mapa | Só farmar; não force nada |
| **Nível 5 (ultimate)** | Primeiro recurso de luta coletiva | Usar para segurar Dragão, não para caçar abate |
| **1º lendário + botas evoluídas** | +45 de aceleração = **45% mais Q** | Começar a empurrar e disputar objetivo |
| **Acúmulos intermediários** | O Q começa a limpar onda sozinho | Empurrar e rotacionar; cada onda é acúmulo |
| **225 acúmulos** | O pico que a build inteira serve | A partir daí a luta coletiva é sua; jogue de trás e acerte o Q |
| **3º lendário** | Dano de item alcança o dano de acúmulo | Forçar Barão/Dragão enquanto o inimigo ainda não fechou build |

A diferença dele para a Miss Fortune é essa: ela tem pico no **nível 5** e cai no fim; ele **não tem pico nenhum antes dos acúmulos** e depois não tem teto. Jogar Smolder como se fosse Miss Fortune é o erro clássico.

## 5. Runas

O banco tem o texto das 58 runas, e a lista de Chave está em `RUNES_KEYSTONES` (`app.js`). Ele **não** tem a qual dos outros três espaços cada runa pertence — confirme na tela do jogo.

### Chave

| Runa | O que o texto do banco diz | Para o Smolder |
|---|---|---|
| **Conquistador** | *"acúmulos ao atingir um Campeão com ataques **ou habilidades** diferentes... 3-7 de AD por acúmulo... vampirismo universal no máximo"* | **Escolha padrão.** É a única Chave que acumula com habilidade, e o AD adaptativo alimenta direto o Q |
| **Primeiro Ataque** | *"concede ouro... recebe ouro extra de acordo com o dano adicional causado"* | **Escolha para escalar.** Ouro é exatamente o recurso que ele precisa acelerar |
| **Cometa Arcano** | *"causar dano a um Campeão com uma habilidade lançará um cometa... 35% do AD adicional"* | Para rota de poke com o Q à distância |
| Fortalecimento | *"3 ataques consecutivos... amplifica o dano em 9%"* | Amplificação boa, mas exige encostar com ataque básico — não é o padrão dele |
| Ritmo Fatal / Agilidade nos Pés | velocidade de ataque e cura | Desperdício: o dano dele não é ataque básico |

### Os outros três espaços

| Função | Runa | Por quê |
|---|---|---|
| Dano de habilidade | **Ataque em Sequência** | marca ao acertar habilidade e os 2 golpes seguintes causam dano adaptativo extra — feito para quem abre com Q |
| Mais Q | **Transcendência** | aceleração nos níveis 1 e 5, e no 9 reduz recarga ao acertar habilidade |
| Escala | **Tempestade Crescente** | AD adaptativo crescente a partir dos 6 min — a runa do campeão de escalonamento |
| Escala com farm | **Crescimento Excessivo** | 3 de vida por 2 tropas, sem teto; ele farma mais que qualquer um |
| Contra CC | **Perserverança** | tenacidade + resistências ao ser imobilizado |
| Sustentação | **Ventos Revigorantes** | regenera 6 + 2% da vida perdida, segura rota de poke |

**Contra suporte frágil:** Conquistador + Ataque em Sequência + Transcendência + Tempestade Crescente.

**Contra suporte tanque:** Conquistador + Transcendência + Perserverança + Crescimento Excessivo.

**Feitiços:** Flash + Barreira contra engate (absorve o combo enquanto o CC ainda está em você); Flash + Curar contra rota de poke.

## 6. Regras rápidas de postura

| Situação | Jogar |
|---|---|
| Antes do nível 5, qualquer rota | **Passivo, farmar** |
| Suporte inimigo tanque, antes do 2º lendário | **Passivo** |
| Suporte inimigo frágil | **Neutro**: empurrar e farmar, trocar só com o Q |
| Rota contra KaiSa, Kalista ou Jinx (você é o counter) | **Neutro a agressivo** |
| Rota contra Corki, Varus ou Ezreal (eles te counteram) | **Passivo, farmar sob a torre** |
| Depois dos acúmulos altos + 3 itens | **Agressivo em luta coletiva, sempre de trás** |
| Escolher entre uma tropa e um abate arriscado | **Sempre a tropa** |

A regra que resume o campeão: **morrer custa duas vezes** — o ouro e os acúmulos que você não fez. É por isso que a dica do próprio projeto é jogar "totalmente defensivo" na rota.

