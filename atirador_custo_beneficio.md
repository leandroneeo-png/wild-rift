# Itens de Atirador no Wild Rift — custo-benefício

Gerado por `analise_atirador.py` a partir dos preços e atributos de `metadata.json`. Refaça o cálculo sempre que os itens forem atualizados.

## 1. Quanto vale cada atributo (itens primários como régua)

| Atributo | Item primário de referência | Ouro por ponto |
|---|---|---|
| Dano de Ataque | Espada Longa — 500g / 12 Dano de Ataque | **41.7 g** |
| Vel. Ataque | Adaga — 500g / 15% Vel. de Ataque | **33.3 g** |
| Critico | Luvas da Pancadaria — 500g / 10% Crítico | **50.0 g** |
| Vida | Cristal de Rubi — 500g / 150 Vida | **3.3 g** |
| Armadura | Couraça de Pano — 500g / 20 Armadura | **25.0 g** |
| Resist. Magica | Manto Anula-Magia — 500g / 20 Resist. Mágica | **25.0 g** |
| Poder de Habilidade | Tomo Amplificador — 500g / 25 Poder de Habilidade | **20.0 g** |
| Acel. Habilidade | Anel da Revelação — 400g / 10 Acel. de Habilidade | **40.0 g** |
| Mana | Capítulo Perdido — (900g − 30 PH) / 200 Mana | **1.5 g** |
| Vampirismo | Cetro Vampírico — (1200g − 20 AD) / 8% Vampirismo | **45.8 g** |
| Vel. Movimento | Botas da Velocidade — 500g / 25 Vel. de Movimento | **20.0 g** |
| Vel. Movimento | Zelo — (1400g − 15% Crít − 15% VA) / 5% Vel. Mov. | **30.0 g** |
| Pen. Armadura | Último Sussurro — 800g / 12% Pen. de Armadura | **66.7 g** |

Itens básicos por definição valem 100% (a régua é feita deles). Um item lendário acima de 100% já compensa só pelos atributos; abaixo disso, ele precisa da passiva para valer o preço.

## 2. Eficiência de ouro — itens lendários

| Item | Preço | Atributos | Valor em ouro | Eficiência |
|---|---|---|---|---|
| Sedenta por Sangue* | 3000g | 55 Dano de Ataque, 25% Critico, 250 Vida, 8% Vampirismo | 4742g | **158%** |
| Terminus* | 3300g | 40 Dano de Ataque, 30% Vel. Ataque, 33% Pen. Armadura | 4867g | **147%** |
| Dançarina Fantasma* | 2900g | 20 Dano de Ataque, 65% Vel. Ataque, 25% Critico | 4250g | **147%** |
| Lembrete Mortal* | 3300g | 25 Dano de Ataque, 15% Vel. Ataque, 25% Critico, 30% Pen. Armadura | 4792g | **145%** |
| Lembranças do Lorde Dominik | 3300g | 25 Dano de Ataque, 25% Critico, 36% Pen. Armadura | 4692g | **142%** |
| Forca do Vendaval | 3100g | 50 Dano de Ataque, 15% Vel. Ataque, 25% Critico, 5% Vel. Movimento | 3983g | **128%** |
| A Coletora* | 3000g | 45 Dano de Ataque, 25% Critico, 10 Pen. Armadura plana | 3792g | **126%** |
| Arco-escudo Imortal | 3000g | 40 Dano de Ataque, 15% Vel. Ataque, 25% Critico, 5% Vampirismo | 3646g | **122%** |
| Chuva de Canivete | 3000g | 40 Dano de Ataque, 20% Vel. Ataque, 25% Critico | 3583g | **119%** |
| Colhedor de Essência | 3000g | 35 Dano de Ataque, 25% Critico, 20 Acel. Habilidade | 3508g | **117%** |
| Lâmina Impetuosa Solari | 3000g | 40% Vel. Ataque, 25% Critico, 20 Acel. Habilidade | 3383g | **113%** |
| Mata-Cráquens* | 2800g | 40 Dano de Ataque, 40% Vel. Ataque, 5% Vel. Movimento | 3150g | **112%** |
| Gume do Infinito | 3400g | 60 Dano de Ataque, 25% Critico | 3750g | **110%** |
| Detonador Magnético* | 3000g | 25 Dano de Ataque, 25% Vel. Ataque, 25% Critico, 5% Vel. Movimento | 3275g | **109%** |
| Adagas Rápidas Navori | 2800g | 45% Vel. Ataque, 25% Critico, 5% Vel. Movimento | 2900g | **104%** |
| Transferência de Alma | 3200g | 25 Dano de Ataque, 30% Vel. Ataque, 25% Critico | 3292g | **103%** |
| Lâmina da Fúria de Guinsoo* | 3100g | 25 Dano de Ataque, 62% Vel. Ataque | 3108g | **100%** |
| Furacão de Runaan | 2900g | 35% Vel. Ataque, 25% Critico | 2417g | **83%** |
| Espada do Rei Destruído* | 3200g | 25 Dano de Ataque, 35% Vel. Ataque, 10% Vampirismo | 2667g | **83%** |

`*` inclui atributos que o item entrega pela passiva (penetração, vampirismo, acúmulos de vel. de ataque).

## 3. Eficiência de ouro — botas e itens épicos

| Item | Preço | Atributos | Valor em ouro | Eficiência |
|---|---|---|---|---|
| Botas do Dinamismo (REFORMULADAS) | 2200g | 40 Dano de Ataque, 6% Pen. Armadura, 12 Pen. Armadura plana, 45 Vel. Movimento | 3767g | **171%** |
| Grevas do Berserker (Reformuladas) | 2200g | 50% Vel. Ataque, 5% Vampirismo, 45 Vel. Movimento | 2796g | **127%** |
| Martelo de Guerra de Caulfield | 1200g | 25 Dano de Ataque, 10 Acel. Habilidade | 1442g | **120%** |
| Ferrão | 1200g | 30% Vel. Ataque, 10 Acel. Habilidade | 1400g | **117%** |
| Alijava Vespertina | 1350g | 25 Dano de Ataque, 15% Vel. Ataque | 1542g | **114%** |
| Espada G. p. C. | 1500g | 40 Dano de Ataque | 1667g | **111%** |
| Grevas Vorazes (REFORMULADAS) | 2200g | 25 Dano de Ataque, 10% Vampirismo, 45 Vel. Movimento | 2400g | **109%** |
| Último Sussurro* | 800g | 12% Pen. Armadura | 800g | **100%** |
| Zelo* | 1400g | 15% Vel. Ataque, 15% Critico, 5% Vel. Movimento | 1400g | **100%** |
| Cetro Vampírico | 1200g | 20 Dano de Ataque, 8% Vampirismo | 1200g | **100%** |
| Capa da Agilidade | 1000g | 20% Critico | 1000g | **100%** |
| Punhal Serrilhado | 1000g | 20 Dano de Ataque | 833g | **83%** |
| Chamado do Carrasco | 800g | 15 Dano de Ataque | 625g | **78%** |
| Arco Recurvo | 1400g | 30% Vel. Ataque | 1000g | **71%** |
| Estilhaço de Kircheis | 900g | 15 Dano de Ataque | 625g | **69%** |

`*` inclui atributos que o item entrega pela passiva (penetração, vampirismo, acúmulos de vel. de ataque).

## 4. Dano por ouro (o que realmente importa para o atirador)

Eficiência de ouro trata cada atributo isoladamente, mas para um atirador AD, velocidade de ataque e crítico se **multiplicam** entre si. O cálculo abaixo mede o DPS que cada item adiciona e divide pelo preço.

Referência: atirador nível 15 com 110 de AD base e 0.90 ataque/s base. Alvo frágil = 100 de armadura e 2200 de vida; alvo tanque = 250 de armadura e 4200 de vida. "1º item" = build vazia; "4º item" = já com 80 de AD, 60% de vel. de ataque e 50% de crítico acumulados.

### Como 1º item

| Item | Preço | DPS no frágil | DPS/1000g (frágil) | DPS no tanque | DPS/1000g (tanque) |
|---|---|---|---|---|---|
| Mata-Cráquens | 2800g | +82 | **29.2** | +47 | **16.7** |
| Espada do Rei Destruído | 3200g | +89 | **27.9** | +81 | **25.2** |
| Terminus | 3300g | +87 | **26.4** | +61 | **18.5** |
| Lâmina da Fúria de Guinsoo | 3100g | +79 | **25.5** | +49 | **15.7** |
| Dançarina Fantasma | 2900g | +65 | **22.5** | +37 | **12.8** |
| Chuva de Canivete | 3000g | +65 | **21.8** | +40 | **13.2** |
| Detonador Magnético | 3000g | +54 | **18.1** | +33 | **10.9** |
| Forca do Vendaval | 3100g | +49 | **15.7** | +28 | **9.0** |
| Lembrete Mortal | 3300g | +49 | **14.8** | +33 | **10.0** |
| Arco-escudo Imortal | 3000g | +43 | **14.2** | +24 | **8.1** |
| Gume do Infinito | 3400g | +47 | **13.8** | +27 | **7.9** |
| Transferência de Alma | 3200g | +44 | **13.8** | +25 | **7.9** |
| Furacão de Runaan | 2900g | +39 | **13.4** | +22 | **7.7** |
| Sedenta por Sangue | 3000g | +39 | **12.9** | +22 | **7.4** |
| Adagas Rápidas Navori | 2800g | +36 | **12.8** | +20 | **7.3** |
| Lembranças do Lorde Dominik | 3300g | +42 | **12.7** | +34 | **10.3** |
| A Coletora | 3000g | +38 | **12.6** | +20 | **6.8** |
| Lâmina Impetuosa Solari | 3000g | +33 | **10.9** | +19 | **6.2** |
| Colhedor de Essência | 3000g | +28 | **9.3** | +16 | **5.3** |

### Como 4º item

| Item | Preço | DPS no frágil | DPS/1000g (frágil) | DPS no tanque | DPS/1000g (tanque) |
|---|---|---|---|---|---|
| Lâmina da Fúria de Guinsoo | 3100g | +171 | **55.3** | +115 | **37.1** |
| Terminus | 3300g | +182 | **55.1** | +129 | **39.1** |
| Mata-Cráquens | 2800g | +149 | **53.3** | +85 | **30.4** |
| Dançarina Fantasma | 2900g | +144 | **49.7** | +82 | **28.4** |
| Espada do Rei Destruído | 3200g | +153 | **47.9** | +130 | **40.7** |
| Chuva de Canivete | 3000g | +131 | **43.6** | +78 | **26.0** |
| Lembrete Mortal | 3300g | +132 | **39.9** | +93 | **28.2** |
| Gume do Infinito | 3400g | +134 | **39.3** | +76 | **22.5** |
| Detonador Magnético | 3000g | +112 | **37.2** | +66 | **22.1** |
| Lembranças do Lorde Dominik | 3300g | +119 | **36.0** | +101 | **30.6** |
| Forca do Vendaval | 3100g | +107 | **34.6** | +61 | **19.8** |
| Arco-escudo Imortal | 3000g | +95 | **31.6** | +54 | **18.1** |
| Transferência de Alma | 3200g | +99 | **31.0** | +57 | **17.7** |
| Adagas Rápidas Navori | 2800g | +86 | **30.6** | +49 | **17.5** |
| A Coletora | 3000g | +90 | **30.1** | +48 | **16.0** |
| Furacão de Runaan | 2900g | +86 | **29.5** | +49 | **16.9** |
| Sedenta por Sangue | 3000g | +88 | **29.2** | +50 | **16.7** |
| Lâmina Impetuosa Solari | 3000g | +79 | **26.4** | +45 | **15.1** |
| Colhedor de Essência | 3000g | +65 | **21.7** | +37 | **12.4** |

### O que o modelo não mede

- **Furacão de Runaan**: o cálculo só conta o alvo principal. Os dois raios extras (55% do dano) valem perto de +110% de DPS em luta de 3 alvos.
- **Lâmina Impetuosa Solari** e **Colhedor de Essência**: o dano depende de conjurar habilidades, então dependem do campeão.
- **Adagas Rápidas Navori**: os 15% de redução de recarga por ataque não viram DPS de ataque básico — valem para atiradores que dependem de habilidades (Ezreal, Vayne, Lucian).
- **Sedenta por Sangue**, **Arco-escudo Imortal**, **Cimitarra Mercurial**: parte do preço é sobrevivência, não dano.
- Passivas de utilidade (lentidão, vel. de movimento, escudos) não entram.

## 5. Itens primários usados como régua

| Item básico | Preço | Atributos |
|---|---|---|
| Espada Longa | 500g | 12 Dano de Ataque |
| Adaga | 500g | 15% Vel. Ataque |
| Luvas da Pancadaria | 500g | 10% Critico |
| Cristal de Rubi | 500g | 150 Vida |
| Couraça de Pano | 500g | 20 Armadura |
| Manto Anula-Magia | 500g | 20 Resist. Magica |
| Tomo Amplificador | 500g | 25 Poder de Habilidade |
| Anel da Revelação | 400g | 10 Acel. Habilidade |
| Botas da Velocidade | 500g | 25 Vel. Movimento |
| Cristal de Safira | 500g | 5 Acel. Habilidade, 100 Mana |

## 6. Leitura prática

**Melhor custo-benefício puro (atributos por ouro):** Sedenta por Sangue, Terminus, Dançarina Fantasma, Lembrete Mortal e Lembranças do Lorde Dominik passam de 140% — pagam-se sozinhos antes mesmo da passiva.

**Melhor custo-benefício em dano real:** a ordem muda bastante, porque crítico só rende com AD e vel. de ataque já acumulados:

- **1º item** — Mata-Cráquens, Espada do Rei Destruído e Terminus lideram. São itens de dano fixo por ataque (não dependem de crítico), por isso rendem cedo. Crítico como primeiro item é o pior investimento da lista.
- **3º/4º item** — Terminus, Guinsoo, Mata-Cráquens e Dançarina Fantasma seguem na frente, mas Gume do Infinito e Lembrete Mortal sobem muito, porque multiplicam o crítico que a build já tem.
- **Contra tanque** — Espada do Rei Destruído, Terminus, Lembranças do Lorde Dominik e Lembrete Mortal são os únicos que mantêm o rendimento; itens de crítico puro perdem quase metade do valor contra 250 de armadura.

**Armadilhas de preço:**

- *Arco Recurvo* (71%) e *Estilhaço de Kircheis* (69%) são os piores itens épicos por atributo — só valem pelo caminho de construção.
- *Furacão de Runaan* (83% de eficiência) só compensa em luta coletiva; contra um alvo só é o pior item de crítico da lista.
- *Lâmina da Fúria de Guinsoo* anula o crítico dos ataques. O número alto de DPS acima assume que você **não** vai montar build de crítico com ele.
- *Gume do Infinito* custa 3400g e só é eficiente com crítico alto; comprado cedo é 30% pior por ouro que Mata-Cráquens.

**Sequência com melhor retorno por ouro, pelos números acima:**

1. Item de dano por ataque (Mata-Cráquens / Espada do Rei Destruído / Terminus)
2. Botas do Dinamismo ou Grevas do Berserker (as duas botas mais eficientes, 171% e 127%)
3. Item de crítico com AD alto (Sedenta por Sangue ou Força do Vendaval)
4. Gume do Infinito, quando o crítico já estiver alto
5. Penetração conforme o inimigo (Lembrete Mortal ou Lembranças do Lorde Dominik contra tanques)

## 7. Observações sobre os dados

- Preços e atributos vêm de `metadata.json`; mudanças de patch invalidam os números.
- Penetração de armadura plana não tem item básico puro de referência: está precificada pela equivalência com penetração percentual contra 100 de armadura.
- 5 itens do banco estão com preço 0 e ficaram fora das tabelas: Abraço de Seraph, Fimbulwinter, Muramana, [OFF] Força da Trindade, [OFF] Juramento do Protetor.

