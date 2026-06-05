// Configuração do Firebase (REST API)
const FIREBASE_CONFIG = {
  apiKey: "AIzaSyAJfutv_N-tD4d5I4jvFBBaE4oMO3OoQ2Y",
  projectId: "wild-rift-533bd"
};

const FIRESTORE_URL = `https://firestore.googleapis.com/v1/projects/${FIREBASE_CONFIG.projectId}/databases/(default)/documents/campeoes?key=${FIREBASE_CONFIG.apiKey}&pageSize=300`;

// Dicionários Locais de Dados
let champions = [];
let itemData = {};
let spellData = {};
let runeData = {};
let metadata = { items: {}, runes: {}, spells: {} };

// Estado da Aplicação
let selectedLane = "all";
let searchQuery = "";
let sortOption = "tier-desc";
let selectedStatsFilter = "all"; // Opções: "all", "s", "high-wr", "high-ban"

// Mapeamento CORRETO de lanes do WildLegends
// 1=Mid, 2=Solo/Barão, 3=ADC, 4=Suporte, 5=Jungle
const LANE_NAMES = {
  "1": "Mid",
  "2": "Solo",
  "3": "ADC",
  "4": "Suporte",
  "5": "Selva"
};

const LANE_ICONS = {
  "1": "fa-wand-magic-sparkles",
  "2": "fa-shield-halved",
  "3": "fa-crosshairs",
  "4": "fa-hands-holding-circle",
  "5": "fa-tree"
};

// Mapeamentos Customizados de Fallback (Caso DDragon falhe ou para itens específicos de Wild Rift)
const WILD_RIFT_ITEMS = {
  // Wild Rift exclusive item IDs (127xxx) — use WildLegends CDN or DDragon equivalent
  "127009": { name: "Botas de Mana", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3158.png" },
  "127010": { name: "Orbe do Infinito", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3285.png" },
  "127011": { name: "Coroa da Rainha Despedaçada", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3040.png" },
  "127014": { name: "Duplaguarda de Amaranto", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3105.png" },
  "127016": { name: "Tempestade Colossal", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3031.png" },
  "127017": { name: "Tá Fudido", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3142.png" },
  "127021": { name: "Ladrão de Almas Desperto", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/4645.png" },
  "127022": { name: "Tempestade Imortal", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3053.png" },
  "127023": { name: "Tridente da Oceânide", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3119.png" },
  "127026": { name: "Placa Gargolítica", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3193.png" },
  "127032": { name: "Eclipse", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/6630.png" },
  "127035": { name: "Véu de Banshee", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3102.png" },
  "127036": { name: "Armadilha de Yordle", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3110.png" },
  "127040": { name: "Eco de Luden", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3285.png" },
  "127051": { name: "Perseverança de Navori", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/6672.png" },
  "127052": { name: "Fúria de Navori", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/6672.png" },
  "127053": { name: "Orbe do Infinito", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3285.png" },
  "127055": { name: "Fantasia de Bandopolis", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3135.png" },
  "127057": { name: "Colosso do Frostfire", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3068.png" },
  "127062": { name: "Rancor de Serylda", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/6694.png" },
  "127072": { name: "Frenesi Kraken", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/6653.png" },
  "127083": { name: "Desespero Eterno", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3065.png" },
  // Standard LoL item IDs with local name mapping
  "6610": { name: "Céu Dividido", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/6610.png" },
  "3026": { name: "Anjo Guardião", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3026.png" },
  "3078": { name: "Força da Trindade", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3078.png" },
  "3071": { name: "Cutelo Negro", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3071.png" },
  "3156": { name: "Fauce de Malmortius", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3156.png" },
  "3161": { name: "Lança de Shojin", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3161.png" },
  "3158": { name: "Botas Ionianas da Lucidez", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3158.png" },
  "3111": { name: "Passos de Mercúrio", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3111.png" },
  "3123": { name: "Chamado do Algoz", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3123.png" },
  "3142": { name: "Fantasma de Youmuu", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3142.png" },
  "3153": { name: "Espada do Rei Destruído", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3153.png" },
  "3031": { name: "Borda do Infinito", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3031.png" },
  "3033": { name: "Armamento Mortal", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3033.png" },
  "3072": { name: "Espada Ensanguentada", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3072.png" },
  "3006": { name: "Botas do Berserker", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3006.png" },
  "3075": { name: "Armadura Espinhosa", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3075.png" },
  "3050": { name: "Zan-hou Purificado", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3050.png" },
  "3084": { name: "Espírito da Força", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3084.png" },
  "3110": { name: "Congelamento de Randuin", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3110.png" },
  "6676": { name: "Lâmina da Fúria do Rei", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/6676.png" },
  "6694": { name: "Fio da Serpente", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/6694.png" },
  "6695": { name: "Profanidade de Serpente", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/6695.png" },
  "4628": { name: "Horizonte do Crepúsculo", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/4628.png" },
  "4629": { name: "Fluxo de Força", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/4629.png" },
  "4633": { name: "Criafendas", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/4633.png" },
  "7012": { name: "Tormento de Liandry", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3151.png" },
  "7018": { name: "Força da Trindade", image: "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3078.png" }
};

const RUNES_KEYSTONES = {
  "8010": { name: "Conquistador", image: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Precision/Conqueror/Conqueror.png" },
  "8005": { name: "Pressione o Ataque", image: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Precision/PressTheAttack/PressTheAttack.png" },
  "8008": { name: "Agilidade nos Pés", image: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Precision/FleetFootwork/FleetFootwork.png" },
  "8021": { name: "Agilidade nos Pés", image: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Precision/FleetFootwork/FleetFootwork.png" },
  "5012": { name: "Primeiro Golpe", image: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Inspiration/FirstStrike/FirstStrike.png" },
  "5011": { name: "Aprimoramento Glacial", image: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Inspiration/GlacialAugment/GlacialAugment.png" },
  "8437": { name: "Aperto dos Mortos-Vivos", image: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Resolve/GraspOfTheUndying/GraspOfTheUndying.png" },
  "8439": { name: "Pós-choque", image: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Resolve/VeteranAftershock/VeteranAftershock.png" },
  "8230": { name: "Ímpeto Gradual", image: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Sorcery/PhaseRush/PhaseRush.png" },
  "8223": { name: "Aery", image: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Sorcery/SummonAery/SummonAery.png" },
  "8112": { name: "Eletrocutar", image: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Domination/Electrocute/Electrocute.png" },
  "8128": { name: "Colheita Sombria", image: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Domination/DarkHarvest/DarkHarvest.png" },
  "8351": { name: "Ritmo Fatal", image: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Precision/LethalTempo/LethalTempoTemp.png" },
  "8360": { name: "Ritmo Fatal", image: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Precision/LethalTempo/LethalTempoTemp.png" }
};

const SPELLS_MAPPING = {
  "4": { name: "Flash", key: "SummonerFlash" },
  "11": { name: "Golpear", key: "SummonerSmite" },
  "14": { name: "Incendiar", key: "SummonerDot" },
  "21": { name: "Barreira", key: "SummonerBarrier" },
  "7": { name: "Curar", key: "SummonerHeal" },
  "3": { name: "Exaustão", key: "SummonerExhaust" },
  "6": { name: "Fantasma", key: "SummonerHaste" },
  "1": { name: "Purificar", key: "SummonerBoost" }
};

// ============================================================
//  INICIALIZAÇÃO E ESTADO DE NAVEGAÇÃO
// ============================================================
let activeTab = "x1"; // "x1", "ranking", "tierlist", "itens"
let activeSubtab = "itens"; // "itens", "runas", "spells"
let activeItemsSort = "all";
let activeItemCheckboxes = [];
let itemsSearchQuery = "";
let runesSearchQuery = "";
let spellsSearchQuery = "";
let activeTierListLane = "2"; // Inicia no Solo/Barão
let x1SelectedLane = "all"; // Filtro de lane na página X1

document.addEventListener("DOMContentLoaded", async () => {
  setupEventListeners();
  initParticles();
  initScrollHeader();
  initLegalModals();

  // Carrega dados em paralelo
  await loadMetadata();
  await loadDDragonData();
  await fetchChampions();

  // Define a aba padrão ativa
  switchTab("x1");
});

// ============================================================
//  EVENT LISTENERS
// ============================================================
function setupEventListeners() {
  // Controle de Abas Principais (Header Nav)
  const tabButtons = document.querySelectorAll(".tab-btn");
  tabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      tabButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      activeTab = btn.getAttribute("data-tab");
      switchTab(activeTab);
    });
  });

  // Filtros de Lane - Aba de Ranking
  const laneButtons = document.querySelectorAll("#lane-filters .lane-btn");
  laneButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      laneButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      selectedLane = btn.getAttribute("data-lane");
      renderChampions();
    });
  });

  // Filtros de Lane - Aba de Tier List
  const tierlistLaneButtons = document.querySelectorAll("#tierlist-lane-filters .lane-btn");
  tierlistLaneButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      tierlistLaneButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      activeTierListLane = btn.getAttribute("data-lane");
      renderTierList();
    });
  });

  // Filtros de Stats (Resumo do Dashboard na aba de Ranking)
  const statsItems = document.querySelectorAll(".stats-item");
  statsItems.forEach(item => {
    item.addEventListener("click", () => {
      const filter = item.getAttribute("data-filter");
      if (!filter) return;

      statsItems.forEach(b => b.classList.remove("active"));

      if (selectedStatsFilter === filter && filter !== "all") {
        selectedStatsFilter = "all";
        const allItem = document.querySelector('.stats-item[data-filter="all"]');
        if (allItem) allItem.classList.add("active");
      } else {
        selectedStatsFilter = filter;
        item.classList.add("active");
      }

      renderChampions();
    });
  });

  // Barra de Pesquisa Principal (Aba de Ranking e busca geral)
  const searchInput = document.getElementById("search-input");
  searchInput.addEventListener("input", (e) => {
    searchQuery = e.target.value;
    if (activeTab === "ranking") renderChampions();
    else if (activeTab === "tierlist") renderTierList();
  });

  // Atalho Ctrl+K para pesquisa
  window.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "k") {
      e.preventDefault();
      searchInput.focus();
    }
    if (e.key === "Escape") {
      if (document.getElementById("detail-modal").classList.contains("active")) {
        closeModal();
      } else if (document.activeElement === searchInput) {
        searchInput.blur();
        searchInput.value = "";
        searchQuery = "";
        renderChampions();
      }
    }
  });

  // Ordenação do Ranking
  const sortSelect = document.getElementById("sort-select");
  sortSelect.addEventListener("change", (e) => {
    sortOption = e.target.value;
    renderChampions();
  });

  // Sub-abas na Aba de Itens (ITENS, RUNAS, FEITIÇOS)
  const subtabButtons = document.querySelectorAll(".subtab-btn");
  subtabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      subtabButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      activeSubtab = btn.getAttribute("data-subtab");
      switchSubtab(activeSubtab);
    });
  });

  // Filtro Rápido de Itens (Sort Pills)
  const sortPills = document.querySelectorAll(".sort-pill");
  sortPills.forEach(pill => {
    pill.addEventListener("click", () => {
      sortPills.forEach(p => p.classList.remove("active"));
      pill.classList.add("active");
      activeItemsSort = pill.getAttribute("data-sort");
      renderItems();
    });
  });

  // Checkbox filtros de Itens
  const itemCheckboxes = document.querySelectorAll("#items-checkbox-filters input");
  itemCheckboxes.forEach(cb => {
    cb.addEventListener("change", () => {
      activeItemCheckboxes = Array.from(itemCheckboxes).filter(c => c.checked).map(c => c.value);
      renderItems();
    });
  });

  // Busca dedicada nas sub-abas de itens
  document.getElementById("items-search-input").addEventListener("input", (e) => {
    itemsSearchQuery = e.target.value;
    renderItems();
  });
  document.getElementById("runes-search-input").addEventListener("input", (e) => {
    runesSearchQuery = e.target.value;
    renderRunes();
  });
  document.getElementById("spells-search-input").addEventListener("input", (e) => {
    spellsSearchQuery = e.target.value;
    renderSpells();
  });

  // Fechar Modal
  document.getElementById("close-modal-btn").addEventListener("click", closeModal);
  document.getElementById("modal-overlay").addEventListener("click", closeModal);
}

// Alternar entre as abas principais
function switchTab(tab) {
  // Esconde todos os conteúdos de abas
  document.querySelectorAll(".tab-content").forEach(el => {
    el.style.display = "none";
    el.classList.remove("active");
  });

  // Mostra a aba selecionada
  const activeContent = document.getElementById(`${tab}-tab-content`);
  if (activeContent) {
    activeContent.style.display = "block";
    activeContent.classList.add("active");
  }

  // Se for a aba de Itens, X1 ou Duos, esconde a barra de pesquisa principal do cabeçalho
  const searchArea = document.querySelector(".search-area");
  if (tab === "itens" || tab === "x1" || tab === "duos") {
    if (searchArea) {
      searchArea.style.opacity = "0";
      searchArea.style.pointerEvents = "none";
    }
  } else {
    if (searchArea) {
      searchArea.style.opacity = "1";
      searchArea.style.pointerEvents = "auto";
    }
  }

  // Executa a renderização correspondente
  if (tab === "x1") {
    renderX1();
  } else if (tab === "duos") {
    renderDuos();
  } else if (tab === "ranking") {
    renderChampions();
  } else if (tab === "tierlist") {
    renderTierList();
  } else if (tab === "itens") {
    switchSubtab(activeSubtab);
  }
}

// Alternar entre sub-abas (Itens, Runas, Feitiços)
function switchSubtab(subtab) {
  document.querySelectorAll(".subtab-content").forEach(el => {
    el.style.display = "none";
    el.classList.remove("active");
  });

  const activeSubContent = document.getElementById(`subtab-${subtab}-content`);
  if (activeSubContent) {
    activeSubContent.style.display = "block";
    activeSubContent.classList.add("active");
  }

  if (subtab === "itens") {
    renderItems();
  } else if (subtab === "runas") {
    renderRunes();
  } else if (subtab === "spells") {
    renderSpells();
  }
}

// ============================================================
//  VISUAL EFFECTS
// ============================================================
function initParticles() {
  const container = document.getElementById("bg-particles");
  if (!container) return;

  // Reduce particles on mobile for performance
  const isMobile = window.innerWidth <= 768;
  const PARTICLE_COUNT = isMobile ? 10 : 25;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const particle = document.createElement("div");
    particle.className = "particle";
    particle.style.left = `${Math.random() * 100}%`;
    particle.style.animationDuration = `${8 + Math.random() * 15}s`;
    particle.style.animationDelay = `${Math.random() * 10}s`;
    particle.style.width = `${2 + Math.random() * 3}px`;
    particle.style.height = particle.style.width;
    particle.style.opacity = `${0.2 + Math.random() * 0.5}`;
    container.appendChild(particle);
  }
}

function initScrollHeader() {
  const header = document.getElementById("main-header");
  if (!header) return;

  window.addEventListener("scroll", () => {
    if (window.scrollY > 60) {
      header.classList.add("scrolled");
    } else {
      header.classList.remove("scrolled");
    }
  }, { passive: true });
}

// ============================================================
//  DATA LOADING
// ============================================================
async function loadDDragonData() {
  try {
    const [itemRes, spellRes, runeRes] = await Promise.all([
      fetch("https://ddragon.leagueoflegends.com/cdn/16.11.1/data/pt_BR/item.json").then(r => r.json()).catch(() => ({ data: {} })),
      fetch("https://ddragon.leagueoflegends.com/cdn/16.11.1/data/pt_BR/summoner.json").then(r => r.json()).catch(() => ({ data: {} })),
      fetch("https://ddragon.leagueoflegends.com/cdn/16.11.1/data/pt_BR/runesReforged.json").then(r => r.json()).catch(() => [])
    ]);

    itemData = itemRes.data || {};
    spellData = spellRes.data || {};

    if (Array.isArray(runeRes)) {
      runeRes.forEach(tree => {
        if (tree.slots) {
          tree.slots.forEach(slot => {
            if (slot.runes) {
              slot.runes.forEach(rune => {
                runeData[rune.id] = rune;
              });
            }
          });
        }
      });
    }
  } catch (e) {
    console.error("Falha ao ler Data Dragon:", e);
  }
}

async function loadMetadata() {
  try {
    const res = await fetch("metadata.json");
    if (res.ok) {
      metadata = await res.json();
    }
  } catch (e) {
    console.error("Falha ao ler metadata.json:", e);
  }
}

async function fetchChampions() {
  try {
    const res = await fetch(FIRESTORE_URL);
    if (!res.ok) throw new Error("Erro na conexão com Firestore API.");

    const body = await res.json();
    const docs = body.documents || [];

    champions = docs.map(doc => {
      const f = doc.fields;
      return {
        id: f.id?.stringValue || "",
        nome: f.nome?.stringValue || "",
        slug: f.slug?.stringValue || "",
        winRate: f.winRate?.stringValue || "50.00%",
        pickRate: f.pickRate?.stringValue || "1.00%",
        banRate: f.banRate?.stringValue || "0.00%",
        tier: f.tier?.stringValue || "A",
        lane: f.lane?.stringValue || "1",
        variacao: f.variacao?.stringValue || "0",
        buildRecomendada: f.buildRecomendada?.arrayValue?.values?.map(v => v.stringValue) || [],
        runasRecomendadas: f.runasRecomendadas?.arrayValue?.values?.map(v => v.stringValue) || [],
        spellsRecomendados: f.spellsRecomendados?.arrayValue?.values?.map(v => v.stringValue) || [],
        skills: f.skills?.arrayValue?.values?.map(v => {
          const mapVal = v.mapValue?.fields;
          return {
            id: mapVal.id?.stringValue || "",
            key: mapVal.key?.stringValue || "",
            name: mapVal.name?.stringValue || "",
            description: mapVal.description?.stringValue || "",
            imageUrl: mapVal.imageUrl?.stringValue || "",
            upgrades: mapVal.upgrades?.arrayValue?.values?.map(u => parseInt(u.integerValue || u.doubleValue || "0")) || []
          };
        }) || [],
        maxingOrder: f.maxingOrder?.arrayValue?.values?.map(v => v.stringValue) || [],
        forteContra: f.forteContra?.arrayValue?.values?.map(v => {
          const mapVal = v.mapValue?.fields;
          return {
            id: mapVal.id?.stringValue || "",
            nome: mapVal.nome?.stringValue || "",
            slug: mapVal.slug?.stringValue || ""
          };
        }) || [],
        fracoContra: f.fracoContra?.arrayValue?.values?.map(v => {
          const mapVal = v.mapValue?.fields;
          return {
            id: mapVal.id?.stringValue || "",
            nome: mapVal.nome?.stringValue || "",
            slug: mapVal.slug?.stringValue || ""
          };
        }) || [],
        atualizadoEm: f.atualizadoEm?.stringValue || ""
      };
    });

    // Atualiza data na interface do Tier List
    if (champions.length > 0 && champions[0].atualizadoEm) {
      const date = new Date(champions[0].atualizadoEm);
      document.getElementById("tierlist-update-time").textContent = date.toLocaleDateString("pt-BR") + " " + date.toLocaleTimeString("pt-BR", { hour: '2-digit', minute: '2-digit' });
    }

    updateStatsBar();
    renderChampions();
    initX1();
    initDuos();
  } catch (err) {
    console.error("Erro ao buscar campeões:", err);
    const tbody = document.getElementById("ranking-table-body");
    if (tbody) {
      tbody.innerHTML = `
        <tr>
          <td colspan="6" style="text-align: center; padding: 40px; color: var(--red);">
            <i class="fa-solid fa-triangle-exclamation" style="font-size: 2rem; margin-bottom: 12px; display: block;"></i>
            Não foi possível carregar o ranking de campeões.
          </td>
        </tr>
      `;
    }
  }
}

function getUniqueChampions(champsList) {
  const uniqueMap = new Map();
  champsList.forEach(c => {
    const existing = uniqueMap.get(c.nome);
    if (!existing || parseFloat(c.pickRate) > parseFloat(existing.pickRate)) {
      uniqueMap.set(c.nome, c);
    }
  });
  return Array.from(uniqueMap.values());
}

function updateStatsBar() {
  const uniqueChamps = getUniqueChampions(champions);
  const total = uniqueChamps.length;
  const sCount = uniqueChamps.filter(c => c.tier === "S").length;
  const highWR = uniqueChamps.filter(c => parseFloat(c.winRate) >= 52).length;
  const highBan = uniqueChamps.filter(c => parseFloat(c.banRate) >= 20).length;

  animateCounter("stat-total", total);
  animateCounter("stat-s-plus", sCount);
  animateCounter("stat-high-wr", highWR);
  animateCounter("stat-high-ban", highBan);
}


function animateCounter(elementId, targetValue) {
  const el = document.getElementById(elementId);
  if (!el) return;

  let current = 0;
  const step = Math.max(1, Math.ceil(targetValue / 30));
  const interval = setInterval(() => {
    current += step;
    if (current >= targetValue) {
      current = targetValue;
      clearInterval(interval);
    }
    el.textContent = current;
  }, 25);
}

// ============================================================
//  RENDERING - RANKING TAB (TABELA)
// ============================================================
function normalizeText(text) {
  return text.trim().toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-zA-Z0-9]/g, "");
}

const SLUG_TO_DDRAGON = {
  "aatrox": "Aatrox", "ahri": "Ahri", "akali": "Akali", "akshan": "Akshan",
  "alistar": "Alistar", "ambessa": "Ambessa", "amumu": "Amumu", "anivia": "Anivia",
  "annie": "Annie", "ashe": "Ashe", "aurelion-sol": "AurelionSol", "aurora": "Aurora",
  "azir": "Azir", "bard": "Bard", "belveth": "Belveth", "blitzcrank": "Blitzcrank",
  "braum": "Braum", "brand": "Brand", "briar": "Briar", "caitlyn": "Caitlyn",
  "camille": "Camille", "chogath": "Chogath", "corki": "Corki", "darius": "Darius",
  "diana": "Diana", "dr-mundo": "DrMundo", "draven": "Draven", "ekko": "Ekko",
  "elise": "Elise", "evelynn": "Evelynn", "ezreal": "Ezreal", "fiddlesticks": "Fiddlesticks",
  "fiora": "Fiora", "fizz": "Fizz", "galio": "Galio", "gangplank": "Gangplank",
  "garen": "Garen", "gnar": "Gnar", "gragas": "Gragas", "graves": "Graves",
  "gwen": "Gwen", "hecarim": "Hecarim", "heimerdinger": "Heimerdinger", "hwei": "Hwei",
  "illaoi": "Illaoi", "irelia": "Irelia", "ivern": "Ivern", "janna": "Janna",
  "jarvan-iv": "JarvanIV", "jax": "Jax", "jayce": "Jayce", "jhin": "Jhin",
  "jinx": "Jinx", "kaisa": "Kaisa", "kalista": "Kalista", "karma": "Karma",
  "kassadin": "Kassadin", "katarina": "Katarina", "kayle": "Kayle", "kayn": "Kayn",
  "kennen": "Kennen", "khazix": "Khazix", "kindred": "Kindred", "kled": "Kled",
  "kogmaw": "KogMaw", "ksante": "KSante", "lee-sin": "LeeSin", "leona": "Leona",
  "lillia": "Lillia", "lissandra": "Lissandra", "lucian": "Lucian", "lulu": "Lulu",
  "lux": "Lux", "malphite": "Malphite", "maokai": "Maokai", "master-yi": "MasterYi",
  "mel": "Mel", "milio": "Milio", "miss-fortune": "MissFortune", "mordekaiser": "Mordekaiser",
  "morgana": "Morgana", "naafiri": "Naafiri", "nami": "Nami", "nasus": "Nasus",
  "nautilus": "Nautilus", "neeko": "Neeko", "nidalee": "Nidalee", "nilah": "Nilah",
  "nocturne": "Nocturne", "nunu-willump": "Nunu", "olaf": "Olaf",
  "orianna": "Orianna", "ornn": "Ornn", "pantheon": "Pantheon", "poppy": "Poppy",
  "pyke": "Pyke", "qiyana": "Qiyana", "rakan": "Rakan", "rammus": "Rammus",
  "reksai": "RekSai", "rell": "Rell", "reni": "Senna", "renekton": "Renekton",
  "rengar": "Rengar", "riven": "Riven", "rumble": "Rumble", "ryze": "Ryze",
  "samira": "Samira", "seraphine": "Seraphine", "senna": "Senna", "sett": "Sett",
  "shaco": "Shaco", "shen": "Shen", "shyvana": "Shyvana", "singed": "Singed",
  "singed": "Singed", "sion": "Sion", "sivir": "Sivir", "smolder": "Smolder", "sona": "Sona",
  "soraka": "Soraka", "swain": "Swain", "sylas": "Sylas", "syndra": "Syndra",
  "tahm-kench": "TahmKench", "taliyah": "Taliyah", "talon": "Talon", "thresh": "Thresh",
  "tristana": "Tristana", "tryndamere": "Tryndamere", "twitch": "Twitch",
  "twisted-fate": "TwistedFate", "urgot": "Urgot", "varus": "Varus",
  "vayne": "Vayne", "veigar": "Veigar", "velkoz": "Velkoz", "vex": "Vex",
  "vi": "Vi", "viego": "Viego", "viktor": "Viktor", "vladimir": "Vladimir",
  "volibear": "Volibear", "warwick": "Warwick", "wukong": "MonkeyKing",
  "xayah": "Xayah", "xin-zhao": "XinZhao", "yasuo": "Yasuo", "yone": "Yone",
  "yuumi": "Yuumi", "zac": "Zac", "zed": "Zed", "zeri": "Zeri", "ziggs": "Ziggs",
  "zilean": "Zilean", "zoe": "Zoe", "zyra": "Zyra"
};

function getChampionIcon(slug, id) {
  const ddragonName = SLUG_TO_DDRAGON[slug];
  if (ddragonName) {
    return `https://ddragon.leagueoflegends.com/cdn/16.11.1/img/champion/${ddragonName}.png`;
  }
  return `https://game.gtimg.cn/images/lgamem/act/lrlib/img/HeadIcon/H_S_${id}.png`;
}

function renderChampions() {
  if (activeTab !== "ranking") return;

  const tbody = document.getElementById("ranking-table-body");
  const mobileContainer = document.getElementById("ranking-mobile-cards");
  if (tbody) tbody.innerHTML = "";
  if (mobileContainer) mobileContainer.innerHTML = "";

  // 1. Filtra por Lane, Busca e Stats
  let filtered = champions.filter(c => {
    const matchesLane = selectedLane === "all" || c.lane === selectedLane;
    const matchesSearch = normalizeText(c.nome).includes(normalizeText(searchQuery));

    let matchesStats = true;
    if (selectedStatsFilter === "s") {
      matchesStats = c.tier === "S";
    } else if (selectedStatsFilter === "high-wr") {
      matchesStats = parseFloat(c.winRate) >= 52;
    } else if (selectedStatsFilter === "high-ban") {
      matchesStats = parseFloat(c.banRate) >= 20;
    }

    return matchesLane && matchesSearch && matchesStats;
  });

  // Deduplica se a visualização for "Todos"
  if (selectedLane === "all") {
    filtered = getUniqueChampions(filtered);
  }

  // 2. Ordena
  const tierOrder = { "S+": 5, "S": 4, "A": 3, "B": 2, "C": 1, "D": 0 };

  filtered.sort((a, b) => {
    if (sortOption === "tier-desc") {
      const aVal = tierOrder[a.tier] || 0;
      const bVal = tierOrder[b.tier] || 0;
      if (bVal !== aVal) return bVal - aVal;
      return parseFloat(b.winRate) - parseFloat(a.winRate);
    }
    if (sortOption === "winRate-desc") {
      return parseFloat(b.winRate) - parseFloat(a.winRate);
    }
    if (sortOption === "pickRate-desc") {
      return parseFloat(b.pickRate) - parseFloat(a.pickRate);
    }
    if (sortOption === "banRate-desc") {
      return parseFloat(b.banRate) - parseFloat(a.banRate);
    }
    return 0;
  });

  // 3. Vazio
  if (filtered.length === 0) {
    const emptyHTML = `
      <div class="empty-state" style="padding: 40px; text-align: center;">
        <i class="fa-solid fa-magnifying-glass" style="font-size: 2rem; margin-bottom: 12px; display: block;"></i>
        Nenhum campeão encontrado para os filtros selecionados.
      </div>
    `;
    if (tbody) {
      tbody.innerHTML = `<tr><td colspan="6">${emptyHTML}</td></tr>`;
    }
    if (mobileContainer) {
      mobileContainer.innerHTML = emptyHTML;
    }
    return;
  }

  // 4. Cria as linhas da tabela de ranking (DESKTOP)
  filtered.forEach((c, idx) => {
    const tr = document.createElement("tr");

    const rankNum = idx + 1;
    let rankClass = "";
    if (rankNum === 1) rankClass = "rank-1";
    else if (rankNum === 2) rankClass = "rank-2";
    else if (rankNum === 3) rankClass = "rank-3";

    const laneIcon = LANE_ICONS[c.lane] || "fa-circle";
    const champIconUrl = getChampionIcon(c.slug, c.id);
    const tencIconUrl = `https://game.gtimg.cn/images/lgamem/act/lrlib/img/HeadIcon/H_S_${c.id}.png`;

    // Variação format
    const valVar = parseInt(c.variacao || "0");
    let varBadge = "";
    if (valVar > 0) {
      varBadge = `<span class="variation-badge variation-up"><i class="fa-solid fa-caret-up"></i> ${valVar}</span>`;
    } else if (valVar < 0) {
      varBadge = `<span class="variation-badge variation-down"><i class="fa-solid fa-caret-down"></i> ${Math.abs(valVar)}</span>`;
    } else {
      varBadge = `<span class="variation-badge variation-neutral">—</span>`;
    }

    const winPercent = parseFloat(c.winRate);

    tr.innerHTML = `
      <td class="col-rank-num ${rankClass}">${rankNum}</td>
      <td>
        <div class="col-champ-info">
          <div class="col-champ-img-wrapper">
            <img class="col-champ-img" src="${champIconUrl}" alt="${c.nome}" loading="lazy"
                 onerror="if(this.dataset.fb1!='1'){this.dataset.fb1='1';this.src='${tencIconUrl}';}else if(this.dataset.fb2!='1'){this.dataset.fb2='1';this.src='https://ddragon.leagueoflegends.com/cdn/16.11.1/img/champion/Aatrox.png';}">
            <div class="col-champ-lane-icon">
              <i class="fa-solid ${laneIcon}"></i>
            </div>
          </div>
          <div>
            <div class="col-champ-name">${c.nome}</div>
            <span class="tier-badge tier-${c.tier.toLowerCase().replace("+", "-plus")}">${c.tier}</span>
          </div>
        </div>
      </td>
      <td class="col-stat-val ${winPercent >= 50 ? 'text-green' : 'text-red'}">${c.winRate}</td>
      <td class="col-stat-val" style="color: var(--text-primary);">${c.pickRate}</td>
      <td class="col-stat-val" style="color: var(--text-secondary);">${c.banRate}</td>
      <td style="text-align: center;">${varBadge}</td>
    `;

    tr.addEventListener("click", () => showChampionDetails(c));
    if (tbody) tbody.appendChild(tr);
  });

  // 5. Cria cards mobile
  if (mobileContainer) {
    renderMobileRankingCards(filtered, mobileContainer);
  }
}

// ============================================================
//  RENDERING - MOBILE RANKING CARDS
// ============================================================
function renderMobileRankingCards(filtered, container) {
  const AD_INTERVAL = 10; // Insert ad every N cards

  filtered.forEach((c, idx) => {
    const rankNum = idx + 1;
    let rankClass = "";
    if (rankNum === 1) rankClass = "rank-1";
    else if (rankNum === 2) rankClass = "rank-2";
    else if (rankNum === 3) rankClass = "rank-3";

    const laneIcon = LANE_ICONS[c.lane] || "fa-circle";
    const laneName = LANE_NAMES[c.lane] || "";
    const champIconUrl = getChampionIcon(c.slug, c.id);
    const tencIconUrl = `https://game.gtimg.cn/images/lgamem/act/lrlib/img/HeadIcon/H_S_${c.id}.png`;
    const winPercent = parseFloat(c.winRate);

    // Variação
    const valVar = parseInt(c.variacao || "0");
    let varBadge = "";
    if (valVar > 0) {
      varBadge = `<span class="variation-badge variation-up" style="font-size:0.75rem;padding:2px 8px;min-width:auto;"><i class="fa-solid fa-caret-up"></i> ${valVar}</span>`;
    } else if (valVar < 0) {
      varBadge = `<span class="variation-badge variation-down" style="font-size:0.75rem;padding:2px 8px;min-width:auto;"><i class="fa-solid fa-caret-down"></i> ${Math.abs(valVar)}</span>`;
    } else {
      varBadge = `<span class="variation-badge variation-neutral" style="font-size:0.75rem;padding:2px 8px;min-width:auto;">—</span>`;
    }

    const card = document.createElement("div");
    card.className = "ranking-mobile-card";
    card.innerHTML = `
      <div class="ranking-mobile-card-header">
        <span class="mobile-rank-num ${rankClass}">${rankNum}</span>
        <img class="mobile-champ-portrait" src="${champIconUrl}" alt="${c.nome}" loading="lazy"
             onerror="if(this.dataset.fb1!='1'){this.dataset.fb1='1';this.src='${tencIconUrl}';}else if(this.dataset.fb2!='1'){this.dataset.fb2='1';this.src='https://ddragon.leagueoflegends.com/cdn/16.11.1/img/champion/Aatrox.png';}">
        <div class="mobile-champ-info">
          <div class="mobile-champ-name">${c.nome}</div>
          <div class="mobile-champ-meta">
            <span class="mobile-tier-badge tier-${c.tier.toLowerCase().replace('+', '-plus')}">${c.tier}</span>
            <span class="mobile-lane-label"><i class="fa-solid ${laneIcon}"></i> ${laneName}</span>
          </div>
        </div>
        <div class="mobile-variation-badge">${varBadge}</div>
      </div>
      <div class="ranking-mobile-card-stats">
        <div class="mobile-stat-item">
          <span class="mobile-stat-label">Vitórias</span>
          <span class="mobile-stat-value ${winPercent >= 50 ? 'text-green' : 'text-red'}">${c.winRate}</span>
        </div>
        <div class="mobile-stat-item">
          <span class="mobile-stat-label">Presença</span>
          <span class="mobile-stat-value">${c.pickRate}</span>
        </div>
        <div class="mobile-stat-item">
          <span class="mobile-stat-label">Ban</span>
          <span class="mobile-stat-value" style="color: var(--text-secondary);">${c.banRate}</span>
        </div>
      </div>
    `;

    card.addEventListener("click", () => showChampionDetails(c));
    container.appendChild(card);

    // Insert in-feed ad after every AD_INTERVAL cards
    if (rankNum % AD_INTERVAL === 0 && rankNum < filtered.length) {
      const adContainer = document.createElement("div");
      adContainer.className = "ad-container ad-in-feed";
      adContainer.innerHTML = `
        <div class="ad-container-inner">
          <!-- AdSense In-feed: Substituir pelo código após aprovação -->
          <!-- <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="XXXXXXXXXX" data-ad-format="fluid" data-ad-layout-key="-6t+ed+2i-1n-4w"></ins> -->
          <!-- <script>(adsbygoogle = window.adsbygoogle || []).push({});</script> -->
        </div>
      `;
      container.appendChild(adContainer);
    }
  });
}

// ============================================================
//  RENDERING - TIER LIST TAB
// ============================================================
function renderTierList() {
  const container = document.getElementById("tier-rows-container");
  if (!container) return;
  container.innerHTML = "";

  // Filtra campeões da lane selecionada para o tier list
  let laneChamps = champions.filter(c => c.lane === activeTierListLane);

  // Se houver busca no campo principal, filtra por nome
  if (searchQuery) {
    laneChamps = laneChamps.filter(c => normalizeText(c.nome).includes(normalizeText(searchQuery)));
  }

  const tiers = ["S+", "S", "A", "B", "C", "D"];
  const grouped = { "S+": [], "S": [], "A": [], "B": [], "C": [], "D": [] };

  laneChamps.forEach(c => {
    if (grouped[c.tier]) grouped[c.tier].push(c);
  });

  tiers.forEach(tier => {
    const list = grouped[tier];
    if (list.length === 0) return;

    // Ordena campeões por winrate dentro do mesmo tier
    list.sort((a, b) => parseFloat(b.winRate) - parseFloat(a.winRate));

    const row = document.createElement("div");
    row.className = `tier-row tier-${tier.toLowerCase().replace("+", "-plus")}`;

    const labelCell = document.createElement("div");
    labelCell.className = "tier-label-cell";
    labelCell.innerText = tier;
    row.appendChild(labelCell);

    const champsCell = document.createElement("div");
    champsCell.className = "tier-champs-cell";

    list.forEach(c => {
      const champCard = document.createElement("div");
      champCard.className = "tier-champ-card";

      const champIconUrl = getChampionIcon(c.slug, c.id);
      const tencIconUrl = `https://game.gtimg.cn/images/lgamem/act/lrlib/img/HeadIcon/H_S_${c.id}.png`;
      const laneIcon = LANE_ICONS[c.lane] || "fa-circle";

      // Variação icon badge
      const valVar = parseInt(c.variacao || "0");
      let varOverlay = "";
      if (valVar > 0) {
        varOverlay = `<div class="tier-champ-change change-up"><i class="fa-solid fa-caret-up"></i></div>`;
      } else if (valVar < 0) {
        varOverlay = `<div class="tier-champ-change change-down"><i class="fa-solid fa-caret-down"></i></div>`;
      }

      champCard.innerHTML = `
        <div class="tier-champ-img-wrapper">
          <img class="tier-champ-img" src="${champIconUrl}" alt="${c.nome}" loading="lazy"
               onerror="if(this.dataset.fb1!='1'){this.dataset.fb1='1';this.src='${tencIconUrl}';}else if(this.dataset.fb2!='1'){this.dataset.fb2='1';this.src='https://ddragon.leagueoflegends.com/cdn/16.11.1/img/champion/Aatrox.png';}">
          <div class="tier-champ-lane-icon">
            <i class="fa-solid ${laneIcon}"></i>
          </div>
          ${varOverlay}
        </div>
        <span class="tier-champ-name">${c.nome}</span>
      `;

      champCard.addEventListener("click", () => showChampionDetails(c));
      champsCell.appendChild(champCard);
    });

    row.appendChild(champsCell);
    container.appendChild(row);
  });

  if (laneChamps.length === 0) {
    container.innerHTML = `
      <div class="empty-state" style="padding: 40px;">
        <i class="fa-solid fa-magnifying-glass"></i>
        <p>Nenhum campeão encontrado para os filtros selecionados.</p>
      </div>
    `;
  }
}

// ============================================================
//  RENDERING - ITENS TAB
// ============================================================
let processedItems = [];

function processAllItems() {
  processedItems = [];
  if (!metadata.items) return;
  const allIds = Object.keys(metadata.items);

  allIds.forEach(id => {
    const ddItem = itemData[id];
    const metaItem = metadata.items[id];

    if (!metaItem) return;
    const name = metaItem.name || ddItem?.name || "";
    if (!name || name.startsWith("Item ") || name.includes("placeholder")) return;

    const description = metaItem.description || ddItem?.description || "";
    const image = metaItem.imageUrl || (ddItem ? `https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/${id}.png` : "");

    // Obtém o preço real de Wild Rift a partir dos metadados, ou cai no DDragon PC
    let cost = metaItem.price || ddItem?.gold?.total || 0;

    // Categorização
    let cats = [];
    const descLower = description.toLowerCase();
    const nameLower = name.toLowerCase();
    const tags = ddItem?.tags || [];

    if (tags.includes("Boots") || nameLower.includes("botas") || nameLower.includes("passos de") || nameLower.includes("grevas") || nameLower.includes("sandálias")) {
      cats.push("botas");
    } else if (tags.includes("Active") || nameLower.includes("encantamento") || nameLower.includes("placa gargolítica") || id === "127026") {
      cats.push("encantamentos");
    } else {
      let isFisico = tags.includes("Damage") || tags.includes("CriticalStrike") || tags.includes("AttackSpeed") ||
        descLower.includes("dano de ataque") || descLower.includes("acerto crítico") || descLower.includes("velocidade de ataque") ||
        descLower.includes("penetração física") || descLower.includes("letalidade");
      let isMagico = tags.includes("SpellDamage") || tags.includes("Mana") || tags.includes("ManaRegen") ||
        descLower.includes("poder de habilidade") || descLower.includes("penetração mágica") || descLower.includes("regeneração de mana") ||
        descLower.includes("aceleração de habilidade");
      let isDefesa = tags.includes("Armor") || tags.includes("SpellBlock") || tags.includes("Health") || tags.includes("HealthRegen") ||
        descLower.includes("armadura") || descLower.includes("resistência mágica") || descLower.includes("vida máxima") || descLower.includes("vida base");
      let isSuporte = nameLower.includes("foice") || nameLower.includes("gume do ladrão") || nameLower.includes("guardião") || descLower.includes("suporte") || descLower.includes("tributo") || descLower.includes("parceria");

      if (isFisico) cats.push("fisico");
      if (isMagico) cats.push("magico");
      if (isDefesa) cats.push("defesa");
      if (isSuporte) cats.push("suporte");

      if (cats.length === 0) {
        if (descLower.includes("ataque") || descLower.includes(" ad ")) cats.push("fisico");
        else if (descLower.includes("habilidade") || descLower.includes(" ap ")) cats.push("magico");
        else if (descLower.includes("vida") || descLower.includes("armadura") || descLower.includes("resistência")) cats.push("defesa");
        else cats.push("fisico");
      }
    }

    let tier = "completo";
    if (cost <= 600) {
      tier = "base";
    } else if (cost < 2000) {
      tier = "medio";
    }
    cats.push(tier);

    processedItems.push({ id, name, description, image, cost, cats });
  });

  // Remove duplicados de nomes
  const seen = new Set();
  processedItems = processedItems.filter(item => {
    const key = item.name.toLowerCase();
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function renderItems() {
  const container = document.getElementById("items-grid-container");
  if (!container) return;
  container.innerHTML = "";

  if (processedItems.length === 0) {
    processAllItems();
  }

  // 1. Filtros
  let filtered = processedItems.filter(item => {
    const matchesSearch = normalizeText(item.name).includes(normalizeText(itemsSearchQuery));

    let matchesSort = true;
    if (activeItemsSort !== "all") {
      if (activeItemsSort === "fisico") matchesSort = item.cats.includes("fisico");
      else if (activeItemsSort === "magico") matchesSort = item.cats.includes("magico");
      else if (activeItemsSort === "defesa") matchesSort = item.cats.includes("defesa");
      else if (activeItemsSort === "vida") matchesSort = item.description.toLowerCase().includes("vida");
      else if (activeItemsSort === "mana") matchesSort = item.description.toLowerCase().includes("mana");
      else if (activeItemsSort === "armadura") matchesSort = item.description.toLowerCase().includes("armadura");
      else if (activeItemsSort === "res-magica") matchesSort = item.description.toLowerCase().includes("resistência mágica");
      else if (activeItemsSort === "ouro") matchesSort = item.cost > 0;
    }

    let matchesCheckboxes = true;
    if (activeItemCheckboxes.length > 0) {
      matchesCheckboxes = activeItemCheckboxes.some(cb => item.cats.includes(cb));
    }

    return matchesSearch && matchesSort && matchesCheckboxes;
  });

  // 2. Agrupamentos
  const categories = [
    { key: "fisico", label: "Físico" },
    { key: "magico", label: "Mágico" },
    { key: "defesa", label: "Defesa" },
    { key: "suporte", label: "Suporte" },
    { key: "botas", label: "Botas" },
    { key: "encantamentos", label: "Encantamentos" }
  ];

  categories.forEach(cat => {
    const catItems = filtered.filter(item => item.cats.includes(cat.key));
    if (catItems.length === 0) return;

    catItems.sort((a, b) => b.cost - a.cost);

    const section = document.createElement("div");
    section.className = "items-cat-section";
    section.innerHTML = `
      <h3 class="items-cat-title">${cat.label}</h3>
      <div class="items-cat-grid"></div>
    `;

    const grid = section.querySelector(".items-cat-grid");

    catItems.forEach(item => {
      const itemCard = document.createElement("div");
      itemCard.className = "items-grid-item tooltip-container";

      itemCard.innerHTML = `
        <div class="items-grid-img-wrapper">
          <img class="items-grid-img" src="${item.image}" alt="${item.name}" onerror="this.src='https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3070.png'">
        </div>
        <span class="items-grid-name">${item.name}</span>
        <span class="items-grid-cost"><i class="fa-solid fa-coins"></i> ${item.cost}</span>
        <div class="rich-tooltip">
          <div class="tooltip-title">${item.name} <span style="float:right; color:#ffb347;"><i class="fa-solid fa-coins"></i> ${item.cost}</span></div>
          <div class="tooltip-desc">${formatDescription(item.description)}</div>
        </div>
      `;
      grid.appendChild(itemCard);
    });

    container.appendChild(section);
  });

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="empty-state" style="padding: 40px;">
        <i class="fa-solid fa-magnifying-glass"></i>
        <p>Nenhum item encontrado.</p>
      </div>
    `;
  }
}

// ============================================================
//  RENDERING - RUNAS TAB
// ============================================================
function renderRunes() {
  const container = document.getElementById("runes-grid");
  if (!container) return;
  container.innerHTML = "";

  const allRunes = [];
  const seenRunes = new Set();

  if (metadata.runes) {
    Object.entries(metadata.runes).forEach(([id, r]) => {
      if (!r.name) return;
      const key = r.name.toLowerCase();
      if (seenRunes.has(key)) return;
      seenRunes.add(key);

      let img = r.imageUrl;
      if (!img) {
        let rune = runeData[id];
        if (RUNES_KEYSTONES[id]) {
          img = RUNES_KEYSTONES[id].image;
        } else if (rune) {
          img = `https://ddragon.leagueoflegends.com/cdn/img/${rune.icon}`;
        }
      }
      if (!img) {
        img = "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/7200_Domination.png";
      }

      allRunes.push({
        id,
        name: r.name,
        description: r.description,
        image: img
      });
    });
  }



  let filtered = allRunes.filter(r => normalizeText(r.name).includes(normalizeText(runesSearchQuery)));

  filtered.forEach(r => {
    const card = document.createElement("div");
    card.className = "rune-grid-item tooltip-container";
    card.innerHTML = `
      <div class="rune-grid-img-wrapper">
        <img style="width: 44px; height: 44px; object-fit: contain;" src="${r.image}" alt="${r.name}" onerror="this.src='https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/7200_Domination.png'">
      </div>
      <span class="rune-grid-name">${r.name}</span>
      <div class="rich-tooltip">
        <div class="tooltip-title">${r.name}</div>
        <div class="tooltip-desc">${formatDescription(r.description)}</div>
      </div>
    `;
    container.appendChild(card);
  });

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="empty-state" style="grid-column: 1/-1; padding: 40px;">
        <i class="fa-solid fa-magnifying-glass"></i>
        <p>Nenhuma runa encontrada.</p>
      </div>
    `;
  }
}

// ============================================================
//  RENDERING - FEITIÇOS TAB
// ============================================================
function renderSpells() {
  const container = document.getElementById("spells-grid");
  if (!container) return;
  container.innerHTML = "";

  const allSpells = [];

  Object.entries(SPELLS_MAPPING).forEach(([id, s]) => {
    let desc = "Feitiço de invocador do Wild Rift.";
    let img = `https://ddragon.leagueoflegends.com/cdn/16.11.1/img/spell/${s.key}.png`;

    if (metadata.spells && metadata.spells[id]) {
      desc = metadata.spells[id].description;
      img = metadata.spells[id].imageUrl || img;
    }

    allSpells.push({ id, name: s.name, description: desc, image: img });
  });

  let filtered = allSpells.filter(s => normalizeText(s.name).includes(normalizeText(spellsSearchQuery)));

  filtered.forEach(s => {
    const card = document.createElement("div");
    card.className = "spell-grid-item tooltip-container";
    card.innerHTML = `
      <div class="spell-grid-img-wrapper">
        <img style="width: 100%; height: 100%; object-fit: cover;" src="${s.image}" alt="${s.name}">
      </div>
      <span class="spell-grid-name">${s.name}</span>
      <div class="rich-tooltip">
        <div class="tooltip-title">${s.name}</div>
        <div class="tooltip-desc">${formatDescription(s.description)}</div>
      </div>
    `;
    container.appendChild(card);
  });

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="empty-state" style="grid-column: 1/-1; padding: 40px;">
        <i class="fa-solid fa-magnifying-glass"></i>
        <p>Nenhum feitiço encontrado.</p>
      </div>
    `;
  }
}

function formatDescription(desc) {
  if (!desc) return 'Sem descrição.';
  return desc.replace(/src=["']\/icons\//g, 'src="https://wildlegends.net/icons/');
}

// ============================================================
//  DETAILS MODAL
// ============================================================
function showChampionDetails(c) {
  const modal = document.getElementById("detail-modal");

  // Reset progress bars to 0 for animation
  const wrBar = document.getElementById("modal-wr-bar");
  const prBar = document.getElementById("modal-pr-bar");
  const brBar = document.getElementById("modal-br-bar");
  if (wrBar) wrBar.style.width = "0%";
  if (prBar) prBar.style.width = "0%";
  if (brBar) brBar.style.width = "0%";

  const modalImg = document.getElementById("modal-champ-img");
  modalImg.src = getChampionIcon(c.slug, c.id);
  modalImg.onerror = function () {
    if (!this.dataset.fb1) {
      this.dataset.fb1 = '1';
      this.src = `https://game.gtimg.cn/images/lgamem/act/lrlib/img/HeadIcon/H_S_${c.id}.png`;
    } else if (!this.dataset.fb2) {
      this.dataset.fb2 = '1';
      this.src = 'https://ddragon.leagueoflegends.com/cdn/16.11.1/img/champion/Aatrox.png';
      this.onerror = null;
    }
  };

  document.getElementById("modal-champ-name").innerText = c.nome;

  const laneName = LANE_NAMES[c.lane] || "";
  document.getElementById("modal-champ-title").innerText = laneName ? `${laneName} Lane` : c.slug.replace("-", " ");

  const tierBadge = document.getElementById("modal-champ-tier");
  tierBadge.className = `modal-champ-tier tier-${c.tier.toLowerCase().replace("+", "-plus")}`;
  tierBadge.innerText = c.tier;

  const winPercent = parseFloat(c.winRate);
  const winEl = document.getElementById("modal-winrate");
  winEl.innerText = c.winRate;
  winEl.className = `stat-value ${winPercent >= 50 ? 'text-green' : 'text-red'}`;

  document.getElementById("modal-pickrate").innerText = c.pickRate;
  document.getElementById("modal-banrate").innerText = c.banRate;

  // Animate progress bars
  const pickPercent = parseFloat(c.pickRate);
  const banPercent = parseFloat(c.banRate);
  setTimeout(() => {
    const wrBar = document.getElementById("modal-wr-bar");
    const prBar = document.getElementById("modal-pr-bar");
    const brBar = document.getElementById("modal-br-bar");
    if (wrBar) wrBar.style.width = `${Math.min(winPercent, 100)}%`;
    if (prBar) prBar.style.width = `${Math.min(pickPercent * 2, 100)}%`;
    if (brBar) brBar.style.width = `${Math.min(banPercent * 2, 100)}%`;
  }, 50);

  // 1. Itens Recomendados
  const itemsGrid = document.getElementById("modal-items-grid");
  itemsGrid.innerHTML = "";

  if (c.buildRecomendada && c.buildRecomendada.length > 0) {
    c.buildRecomendada.forEach(itemId => {
      let itemName = "";
      let itemImg = "";
      let itemDesc = "Sem descrição disponível.";

      const metaItem = metadata.items && metadata.items[itemId];
      if (metaItem) {
        itemName = metaItem.name;
        itemImg = metaItem.imageUrl || `https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/${itemId}.png`;
        itemDesc = metaItem.description || itemDesc;
      }

      if (!itemName && WILD_RIFT_ITEMS[itemId]) {
        itemName = WILD_RIFT_ITEMS[itemId].name;
        itemImg = itemImg || WILD_RIFT_ITEMS[itemId].image;
      }

      if (!itemName) {
        const ddItem = itemData[itemId];
        if (ddItem) {
          itemName = ddItem.name;
          itemImg = itemImg || `https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/${itemId}.png`;
          itemDesc = ddItem.description || itemDesc;
        }
      }

      if (!itemName) itemName = `Item ${itemId}`;
      if (!itemImg) itemImg = `https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/${itemId}.png`;

      const itemSlot = document.createElement("div");
      itemSlot.className = "item-slot tooltip-container";
      const itemIndex = c.buildRecomendada.indexOf(itemId) + 1;
      itemSlot.innerHTML = `
        <span class="item-order-badge">${itemIndex}</span>
        <img class="item-img" src="${itemImg}" alt="${itemName}" onerror="this.src='https://ddragon.leagueoflegends.com/cdn/16.11.1/img/item/3070.png'">
        <span class="item-name">${itemName}</span>
        <div class="rich-tooltip">
          <div class="tooltip-title">${itemName}</div>
          <div class="tooltip-desc">${formatDescription(itemDesc)}</div>
        </div>
      `;
      itemSlot.style.animationDelay = `${itemIndex * 0.05}s`;
      itemsGrid.appendChild(itemSlot);
    });
  } else {
    itemsGrid.innerHTML = `<p class="empty-text">Sem itens recomendados.</p>`;
  }

  // 2. Runas
  const runesList = document.getElementById("modal-runes-list");
  runesList.innerHTML = "";

  if (c.runasRecomendadas && c.runasRecomendadas.length > 0) {
    c.runasRecomendadas.forEach(runeId => {
      let runeName = "Runa Auxiliar";
      let runeImg = "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/7200_Domination.png";
      let runeDesc = "Sem descrição disponível.";

      const metaRune = metadata.runes && metadata.runes[runeId];
      if (metaRune) {
        runeName = metaRune.name;
        runeDesc = metaRune.description || runeDesc;

        let foundImg = metaRune.imageUrl;
        if (!foundImg) {
          let rune = runeData[runeId];
          if (RUNES_KEYSTONES[runeId]) {
            foundImg = RUNES_KEYSTONES[runeId].image;
          } else if (rune) {
            foundImg = `https://ddragon.leagueoflegends.com/cdn/img/${rune.icon}`;
          }
        }
        runeImg = foundImg || runeImg;
      } else {
        let rune = runeData[runeId];
        if (RUNES_KEYSTONES[runeId]) {
          runeName = RUNES_KEYSTONES[runeId].name;
          runeImg = RUNES_KEYSTONES[runeId].image;
        } else if (rune) {
          runeName = rune.name;
          runeImg = `https://ddragon.leagueoflegends.com/cdn/img/${rune.icon}`;
          runeDesc = rune.description || runeDesc;
        }
      }

      const runeSlot = document.createElement("div");
      runeSlot.className = "rune-slot tooltip-container";
      runeSlot.innerHTML = `
        <img class="spell-img" style="border-radius: 50%" src="${runeImg}" alt="${runeName}" onerror="this.src='https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/7200_Domination.png'">
        <span class="rune-name">${runeName}</span>
        <div class="rich-tooltip">
          <div class="tooltip-title">${runeName}</div>
          <div class="tooltip-desc">${formatDescription(runeDesc)}</div>
        </div>
      `;
      runesList.appendChild(runeSlot);
    });
  } else {
    runesList.innerHTML = `<p class="empty-text">Sem runas recomendadas.</p>`;
  }

  // 3. Feitiços
  const spellsList = document.getElementById("modal-spells-list");
  spellsList.innerHTML = "";

  if (c.spellsRecomendados && c.spellsRecomendados.length > 0) {
    c.spellsRecomendados.forEach(spellId => {
      let spellName = "Feitiço";
      let spellImg = "https://ddragon.leagueoflegends.com/cdn/16.11.1/img/spell/SummonerFlash.png";
      let spellDesc = "Sem descrição disponível.";

      const metaSpell = metadata.spells && metadata.spells[spellId];
      if (metaSpell) {
        spellName = metaSpell.name;
        spellImg = metaSpell.imageUrl || spellImg;
        spellDesc = metaSpell.description || spellDesc;
      } else {
        const sp = SPELLS_MAPPING[spellId];
        if (sp) {
          spellName = sp.name;
          spellImg = `https://ddragon.leagueoflegends.com/cdn/16.11.1/img/spell/${sp.key}.png`;
        }
      }

      const spellSlot = document.createElement("div");
      spellSlot.className = "spell-slot tooltip-container";
      spellSlot.innerHTML = `
        <img class="spell-img" src="${spellImg}" alt="${spellName}" onerror="this.src='https://ddragon.leagueoflegends.com/cdn/16.11.1/img/spell/SummonerFlash.png'">
        <span class="spell-name">${spellName}</span>
        <div class="rich-tooltip">
          <div class="tooltip-title">${spellName}</div>
          <div class="tooltip-desc">${formatDescription(spellDesc)}</div>
        </div>
      `;
      spellsList.appendChild(spellSlot);
    });
  } else {
    spellsList.innerHTML = `<p class="empty-text">Sem feitiços recomendados.</p>`;
  }

  // 4. Ordem de Habilidades (Skills Grid)
  const skills = c.skills || [];
  const passiveSkill = skills.find(s => s.key === "passive");
  const qSkill = skills.find(s => s.key === "q");
  const wSkill = skills.find(s => s.key === "w");
  const eSkill = skills.find(s => s.key === "e");
  const rSkill = skills.find(s => s.key === "r");

  const skillsSection = document.getElementById("modal-skills-section");
  const skillsGrid = document.getElementById("modal-skills-sequence-grid");

  if (skills.length > 0) {
    let maxOrderHTML = "";
    if (c.maxingOrder && c.maxingOrder.length > 0) {
      maxOrderHTML += `<span class="max-order-title">Ordem de Max:</span>`;
      c.maxingOrder.forEach((key, index) => {
        const skill = skills.find(s => s.key === key);
        if (skill) {
          let label = "1ª";
          if (key === "q") label = "1ª";
          else if (key === "w") label = "2ª";
          else if (key === "e") label = "3ª";

          maxOrderHTML += `
            <div class="max-order-item tooltip-container">
              <div class="max-order-icon-wrapper">
                <img src="${skill.imageUrl}" alt="${skill.name}" class="max-order-icon" onerror="this.src='https://ddragon.leagueoflegends.com/cdn/16.11.1/img/spell/SummonerFlash.png'">
                <span class="max-order-badge">${label}</span>
              </div>
              <div class="rich-tooltip">
                <div class="tooltip-title">${skill.name} (${label})</div>
                <div class="tooltip-desc">${formatDescription(skill.description)}</div>
              </div>
            </div>
          `;

          if (index < c.maxingOrder.length - 1) {
            maxOrderHTML += `<i class="fa-solid fa-chevron-right max-order-arrow"></i>`;
          }
        }
      });
    }

    let gridHTML = "";
    if (passiveSkill) {
      gridHTML += `
        <div class="skill-row passive-row">
          <div class="skill-info-col tooltip-container">
            <img src="${passiveSkill.imageUrl}" alt="${passiveSkill.name}" class="skill-icon" onerror="this.src='https://ddragon.leagueoflegends.com/cdn/16.11.1/img/passive/Aatrox_Passive.png'">
            <span class="skill-badge">P</span>
            <span class="skill-name">${passiveSkill.name}</span>
            <div class="rich-tooltip">
              <div class="tooltip-title">${passiveSkill.name} (PASSIVA)</div>
              <div class="tooltip-desc">${formatDescription(passiveSkill.description)}</div>
            </div>
          </div>
          <div class="skill-max-order-col">
            ${maxOrderHTML}
          </div>
        </div>
      `;
    }

    gridHTML += `
      <div class="level-header-row">
        <div class="level-header-col">Habilidade</div>
        <div class="level-header-cells">
    `;
    for (let i = 1; i <= 15; i++) {
      gridHTML += `<div class="level-header-cell">${i}</div>`;
    }
    gridHTML += `
        </div>
      </div>
    `;

    const activeSkillsToRender = [
      { skill: qSkill, key: "q", label: "1ª" },
      { skill: wSkill, key: "w", label: "2ª" },
      { skill: eSkill, key: "e", label: "3ª" },
      { skill: rSkill, key: "r", label: "4ª" }
    ];

    activeSkillsToRender.forEach(({ skill, key, label }) => {
      if (!skill) return;

      gridHTML += `
        <div class="skill-row">
          <div class="skill-info-col tooltip-container">
            <img src="${skill.imageUrl}" alt="${skill.name}" class="skill-icon" onerror="this.src='https://ddragon.leagueoflegends.com/cdn/16.11.1/img/spell/SummonerFlash.png'">
            <span class="skill-badge">${label}</span>
            <span class="skill-name">${skill.name}</span>
            <div class="rich-tooltip">
              <div class="tooltip-title">${skill.name} (${label})</div>
              <div class="tooltip-desc">${formatDescription(skill.description)}</div>
            </div>
          </div>
          <div class="skill-levels-col">
      `;

      const upgrades = skill.upgrades || [];
      for (let i = 1; i <= 15; i++) {
        const isActive = upgrades.includes(i);
        gridHTML += `<div class="level-cell ${isActive ? 'active' : ''}">${isActive ? i : '-'}</div>`;
      }

      gridHTML += `
          </div>
        </div>
      `;
    });

    skillsGrid.innerHTML = gridHTML;
    skillsSection.style.display = "block";
  } else {
    skillsSection.style.display = "none";
  }

  // 5. Forte Contra / Fraco Contra (Counters)
  const countersSection = document.getElementById("modal-counters-section");
  const strongAgainstGrid = document.getElementById("modal-strong-against");
  const weakAgainstGrid = document.getElementById("modal-weak-against");

  if (countersSection) {
    const strongList = c.forteContra || [];
    const weakList = c.fracoContra || [];

    if (strongList.length > 0 || weakList.length > 0) {
      countersSection.style.display = "flex";

      // Render Forte Contra
      if (strongAgainstGrid) {
        strongAgainstGrid.innerHTML = "";
        if (strongList.length > 0) {
          strongList.forEach(counterChamp => {
            const slot = document.createElement("div");
            slot.className = "counter-slot strong tooltip-container";
            const iconUrl = getChampionIcon(counterChamp.slug, counterChamp.id);
            const tencIconUrl = `https://game.gtimg.cn/images/lgamem/act/lrlib/img/HeadIcon/H_S_${counterChamp.id}.png`;

            slot.innerHTML = `
              <img class="counter-champ-img" src="${iconUrl}" alt="${counterChamp.nome}" onerror="this.src='${tencIconUrl}'">
              <span class="counter-champ-name">${counterChamp.nome}</span>
              <div class="rich-tooltip">
                <div class="tooltip-title">${counterChamp.nome}</div>
                <div class="tooltip-desc">Clique para ver detalhes do campeão.</div>
              </div>
            `;

            slot.addEventListener("click", () => {
              const found = champions.find(hc => hc.id === counterChamp.id && hc.lane === c.lane) ||
                champions.find(hc => hc.id === counterChamp.id);
              if (found) {
                const modalContent = document.querySelector(".modal-content");
                if (modalContent) modalContent.scrollTop = 0;
                showChampionDetails(found);
              }
            });
            strongAgainstGrid.appendChild(slot);
          });
        } else {
          strongAgainstGrid.innerHTML = `<p class="empty-text">Sem dados.</p>`;
        }
      }

      // Render Fraco Contra
      if (weakAgainstGrid) {
        weakAgainstGrid.innerHTML = "";
        if (weakList.length > 0) {
          weakList.forEach(counterChamp => {
            const slot = document.createElement("div");
            slot.className = "counter-slot weak tooltip-container";
            const iconUrl = getChampionIcon(counterChamp.slug, counterChamp.id);
            const tencIconUrl = `https://game.gtimg.cn/images/lgamem/act/lrlib/img/HeadIcon/H_S_${counterChamp.id}.png`;

            slot.innerHTML = `
              <img class="counter-champ-img" src="${iconUrl}" alt="${counterChamp.nome}" onerror="this.src='${tencIconUrl}'">
              <span class="counter-champ-name">${counterChamp.nome}</span>
              <div class="rich-tooltip">
                <div class="tooltip-title">${counterChamp.nome}</div>
                <div class="tooltip-desc">Clique para ver detalhes do campeão.</div>
              </div>
            `;

            slot.addEventListener("click", () => {
              const found = champions.find(hc => hc.id === counterChamp.id && hc.lane === c.lane) ||
                champions.find(hc => hc.id === counterChamp.id);
              if (found) {
                const modalContent = document.querySelector(".modal-content");
                if (modalContent) modalContent.scrollTop = 0;
                showChampionDetails(found);
              }
            });
            weakAgainstGrid.appendChild(slot);
          });
        } else {
          weakAgainstGrid.innerHTML = `<p class="empty-text">Sem dados.</p>`;
        }
      }
    } else {
      countersSection.style.display = "none";
    }
  } else {
    console.warn("Counters container element not found in DOM");
  }

  modal.classList.add("active");
  document.body.style.overflow = "hidden";
}

function closeModal() {
  const modal = document.getElementById("detail-modal");
  modal.classList.remove("active");
  document.body.style.overflow = "";
}

// ============================================================
//  LEGAL MODALS (Privacy & Terms)
// ============================================================
function initLegalModals() {
  // Privacy Modal
  const openPrivacyBtn = document.getElementById("open-privacy-modal");
  const privacyModal = document.getElementById("privacy-modal");
  const closePrivacyBtn = document.getElementById("close-privacy-modal-btn");
  const privacyOverlay = document.getElementById("privacy-modal-overlay");

  if (openPrivacyBtn && privacyModal) {
    openPrivacyBtn.addEventListener("click", (e) => {
      e.preventDefault();
      privacyModal.classList.add("active");
      document.body.style.overflow = "hidden";
    });
  }
  if (closePrivacyBtn) {
    closePrivacyBtn.addEventListener("click", () => {
      privacyModal.classList.remove("active");
      document.body.style.overflow = "";
    });
  }
  if (privacyOverlay) {
    privacyOverlay.addEventListener("click", () => {
      privacyModal.classList.remove("active");
      document.body.style.overflow = "";
    });
  }

  // Terms Modal
  const openTermsBtn = document.getElementById("open-terms-modal");
  const termsModal = document.getElementById("terms-modal");
  const closeTermsBtn = document.getElementById("close-terms-modal-btn");
  const termsOverlay = document.getElementById("terms-modal-overlay");

  if (openTermsBtn && termsModal) {
    openTermsBtn.addEventListener("click", (e) => {
      e.preventDefault();
      termsModal.classList.add("active");
      document.body.style.overflow = "hidden";
    });
  }
  if (closeTermsBtn) {
    closeTermsBtn.addEventListener("click", () => {
      termsModal.classList.remove("active");
      document.body.style.overflow = "";
    });
  }
  if (termsOverlay) {
    termsOverlay.addEventListener("click", () => {
      termsModal.classList.remove("active");
      document.body.style.overflow = "";
    });
  }
}

// ============================================================
//  PÁGINA X1 — LÓGICA E INTERAÇÕES
// ============================================================
let selectedX1Champ = null;

function initX1() {
  const x1Search = document.getElementById("x1-search-input");
  const clearBtn = document.getElementById("x1-clear-btn");

  if (x1Search) {
    x1Search.addEventListener("input", (e) => {
      const query = e.target.value;
      if (clearBtn) {
        clearBtn.style.display = query ? "flex" : "none";
      }
      renderX1Selector(query);
    });
  }

  if (clearBtn) {
    clearBtn.addEventListener("click", () => {
      if (x1Search) x1Search.value = "";
      clearBtn.style.display = "none";
      renderX1Selector("");
      resetX1Arena();
    });
  }

  // X1 Lane Filters
  const x1LaneButtons = document.querySelectorAll("#x1-lane-filters .x1-lane-btn");
  x1LaneButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      x1LaneButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      x1SelectedLane = btn.getAttribute("data-lane");
      const searchVal = document.getElementById("x1-search-input")?.value || "";
      renderX1Selector(searchVal);
    });
  });

  // Escuta resize da janela para ajustar as conexões SVG
  window.addEventListener("resize", () => {
    if (activeTab === "x1" && selectedX1Champ) {
      updateX1Connections();
    }
  });

  // Abre o guia de detalhes do campeão ao clicar no card central
  const centerCard = document.getElementById("x1-selected-card");
  if (centerCard) {
    centerCard.addEventListener("click", () => {
      if (selectedX1Champ) {
        showChampionDetails(selectedX1Champ);
      }
    });
  }

  renderX1Selector();
}

function renderX1() {
  if (selectedX1Champ) {
    setTimeout(updateX1Connections, 100);
  }
}

function resetX1Arena() {
  selectedX1Champ = null;

  // Desativa portraits ativos no seletor
  const activeBtns = document.querySelectorAll(".x1-champ-portrait-btn.active");
  activeBtns.forEach(btn => btn.classList.remove("active"));

  // Mostra welcome, esconde arena
  const welcome = document.getElementById("x1-welcome-state");
  const arenaContent = document.getElementById("x1-arena-content");

  if (welcome) welcome.style.display = "flex";
  if (arenaContent) {
    arenaContent.style.display = "none";
    arenaContent.classList.remove("active");
  }

  // Limpa conexões SVG
  clearX1Connections();
}

function renderX1Selector(filterText = "") {
  const grid = document.getElementById("x1-grid-selector");
  if (!grid) return;

  grid.innerHTML = "";

  // Se filtro de lane for "all", mostra campeões únicos; senão, filtra por lane
  let champsList;
  if (x1SelectedLane === "all") {
    champsList = getUniqueChampions(champions);
  } else {
    champsList = champions.filter(c => c.lane === x1SelectedLane);
  }

  // Filtra por texto
  const filtered = champsList.filter(c => {
    return normalizeText(c.nome).includes(normalizeText(filterText));
  });

  // Ordena alfabeticamente
  filtered.sort((a, b) => a.nome.localeCompare(b.nome));

  if (filtered.length === 0) {
    grid.innerHTML = `<p class="empty-text" style="color: var(--text-muted); padding: 10px;">Nenhum campeão encontrado.</p>`;
    return;
  }

  filtered.forEach(c => {
    const btn = document.createElement("button");
    btn.className = "x1-champ-portrait-btn";
    btn.setAttribute("title", c.nome);
    btn.setAttribute("data-champ-id", c.id);

    if (selectedX1Champ && selectedX1Champ.id === c.id) {
      btn.classList.add("active");
    }

    const iconUrl = getChampionIcon(c.slug, c.id);
    const tencIconUrl = `https://game.gtimg.cn/images/lgamem/act/lrlib/img/HeadIcon/H_S_${c.id}.png`;

    btn.innerHTML = `
      <img src="${iconUrl}" alt="${c.nome}" loading="lazy"
           onerror="if(this.src!='${tencIconUrl}'){this.src='${tencIconUrl}';}">
    `;

    btn.addEventListener("click", () => {
      selectX1Champion(c);
    });

    grid.appendChild(btn);
  });
}

function findChampionInfo(counterObj) {
  // Busca na lista completa
  return champions.find(hc => hc.id === counterObj.id) ||
    champions.find(hc => normalizeText(hc.nome) === normalizeText(counterObj.nome)) ||
    null;
}

function selectX1Champion(champ) {
  if (!champ) return;
  selectedX1Champ = champ;

  // Atualiza classe active no seletor
  const btns = document.querySelectorAll(".x1-champ-portrait-btn");
  btns.forEach(btn => {
    if (btn.getAttribute("data-champ-id") === champ.id) {
      btn.classList.add("active");
    } else {
      btn.classList.remove("active");
    }
  });

  // Alterna visibilidade da Arena
  const welcome = document.getElementById("x1-welcome-state");
  const arenaContent = document.getElementById("x1-arena-content");

  if (welcome) welcome.style.display = "none";
  if (arenaContent) {
    arenaContent.style.display = "grid";
    arenaContent.classList.add("active");
  }

  // Preenche dados do campeão ativo central
  const centerCard = document.getElementById("x1-selected-card");
  const activeImg = document.getElementById("x1-selected-img");
  const activeName = document.getElementById("x1-selected-name");
  const activeTier = document.getElementById("x1-selected-tier");
  const activeLane = document.getElementById("x1-selected-lane");
  const activeWinrate = document.getElementById("x1-selected-winrate");
  const activeBanrate = document.getElementById("x1-selected-banrate");

  const iconUrl = getChampionIcon(champ.slug, champ.id);
  const tencIconUrl = `https://game.gtimg.cn/images/lgamem/act/lrlib/img/HeadIcon/H_S_${champ.id}.png`;

  if (activeImg) {
    activeImg.src = iconUrl;
    activeImg.onerror = () => { activeImg.src = tencIconUrl; };
  }
  if (activeName) activeName.textContent = champ.nome;
  if (activeTier) {
    activeTier.textContent = champ.tier;
    activeTier.className = `card-tier-badge tier-${champ.tier.toLowerCase().replace("+", "-plus")}`;
  }
  if (activeLane) {
    const laneName = LANE_NAMES[champ.lane] || "Solo";
    const laneIcon = LANE_ICONS[champ.lane] || "fa-shield-halved";
    activeLane.innerHTML = `<i class="fa-solid ${laneIcon}"></i> ${laneName}`;
  }
  if (activeWinrate) {
    activeWinrate.textContent = champ.winRate;
    const wrVal = parseFloat(champ.winRate);
    activeWinrate.className = `stat-val ${wrVal >= 50 ? 'text-green' : 'text-red'}`;
  }
  if (activeBanrate) activeBanrate.textContent = champ.banRate;

  // Add "Ver Build" badge
  let buildBadge = centerCard?.querySelector(".x1-build-badge");
  if (!buildBadge && centerCard) {
    buildBadge = document.createElement("div");
    buildBadge.className = "x1-build-badge";
    buildBadge.innerHTML = `<i class="fa-solid fa-eye"></i> VER BUILD`;
    centerCard.appendChild(buildBadge);
  }

  // Add VS indicator (only once)
  const arenaWrapper = document.querySelector(".x1-arena-wrapper");
  if (arenaWrapper && !arenaWrapper.querySelector(".x1-vs-indicator")) {
    const vsDiv = document.createElement("div");
    vsDiv.className = "x1-vs-indicator";
    vsDiv.innerHTML = `<div class="x1-vs-badge">VS</div>`;
    arenaWrapper.appendChild(vsDiv);
  }

  // Preenche counters (Forte Contra / Fraco Contra)
  const strongListContainer = document.getElementById("x1-list-strong");
  const weakListContainer = document.getElementById("x1-list-weak");

  // Limpa
  if (strongListContainer) strongListContainer.innerHTML = "";
  if (weakListContainer) weakListContainer.innerHTML = "";

  // Forte Contra
  const strongList = champ.forteContra || [];
  if (strongListContainer) {
    if (strongList.length > 0) {
      strongList.forEach(counterChamp => {
        const card = document.createElement("div");
        card.className = "x1-counter-card x1-counter-card-strong";

        const realInfo = findChampionInfo(counterChamp);
        const winrate = realInfo ? realInfo.winRate : "50.00%";
        const tier = realInfo ? realInfo.tier : "A";
        const cIcon = getChampionIcon(counterChamp.slug, counterChamp.id);
        const cTencIcon = `https://game.gtimg.cn/images/lgamem/act/lrlib/img/HeadIcon/H_S_${counterChamp.id}.png`;

        card.innerHTML = `
          <img src="${cIcon}" alt="${counterChamp.nome}" onerror="this.src='${cTencIcon}'">
          <div class="x1-counter-card-info">
            <div class="x1-counter-card-name">${counterChamp.nome}</div>
            <div class="x1-counter-card-details">
              <span class="x1-counter-card-winrate ${parseFloat(winrate) >= 50 ? 'text-green' : 'text-red'}">${winrate}</span>
              <span class="separator">•</span>
              <span>Tier ${tier}</span>
            </div>
          </div>
          <div class="x1-counter-card-action">
            <i class="fa-solid fa-bolt"></i> Duelo
          </div>
        `;

        card.addEventListener("click", () => {
          // Navegação recursiva: clica no counter e vira o novo selecionado
          const found = realInfo || champions.find(hc => hc.id === counterChamp.id);
          if (found) selectX1Champion(found);
        });

        strongListContainer.appendChild(card);
      });
    } else {
      strongListContainer.innerHTML = `<p class="empty-text" style="color: var(--text-muted); text-align: center; width: 100%;">Sem dados de counters.</p>`;
    }
  }

  // Fraco Contra
  const weakList = champ.fracoContra || [];
  if (weakListContainer) {
    if (weakList.length > 0) {
      weakList.forEach(counterChamp => {
        const card = document.createElement("div");
        card.className = "x1-counter-card x1-counter-card-weak";

        const realInfo = findChampionInfo(counterChamp);
        const winrate = realInfo ? realInfo.winRate : "50.00%";
        const tier = realInfo ? realInfo.tier : "A";
        const cIcon = getChampionIcon(counterChamp.slug, counterChamp.id);
        const cTencIcon = `https://game.gtimg.cn/images/lgamem/act/lrlib/img/HeadIcon/H_S_${counterChamp.id}.png`;

        card.innerHTML = `
          <img src="${cIcon}" alt="${counterChamp.nome}" onerror="this.src='${cTencIcon}'">
          <div class="x1-counter-card-info">
            <div class="x1-counter-card-name">${counterChamp.nome}</div>
            <div class="x1-counter-card-details">
              <span class="x1-counter-card-winrate ${parseFloat(winrate) >= 50 ? 'text-green' : 'text-red'}">${winrate}</span>
              <span class="separator">•</span>
              <span>Tier ${tier}</span>
            </div>
          </div>
          <div class="x1-counter-card-action">
            <i class="fa-solid fa-bolt"></i> Duelo
          </div>
        `;

        card.addEventListener("click", () => {
          const found = realInfo || champions.find(hc => hc.id === counterChamp.id);
          if (found) selectX1Champion(found);
        });

        weakListContainer.appendChild(card);
      });
    } else {
      weakListContainer.innerHTML = `<p class="empty-text" style="color: var(--text-muted); text-align: center; width: 100%;">Sem dados de counters.</p>`;
    }
  }

  // Dispara animações re-adicionando classes e reflow
  const colStrong = document.querySelector(".x1-column-strong");
  const colWeak = document.querySelector(".x1-column-weak");

  if (colStrong) {
    colStrong.classList.remove("animate-slide-left");
    void colStrong.offsetWidth;
    colStrong.classList.add("animate-slide-left");
  }
  if (colWeak) {
    colWeak.classList.remove("animate-slide-right");
    void colWeak.offsetWidth;
    colWeak.classList.add("animate-slide-right");
  }
  if (centerCard) {
    centerCard.classList.remove("animate-center-zoom");
    void centerCard.offsetWidth;
    centerCard.classList.add("animate-center-zoom");
  }

  // Desenha as conexões
  setTimeout(updateX1Connections, 100);
}

function clearX1Connections() {
  for (let i = 1; i <= 3; i++) {
    const pLeft = document.getElementById(`x1-line-left-${i}`);
    const pRight = document.getElementById(`x1-line-right-${i}`);
    if (pLeft) pLeft.setAttribute("d", "");
    if (pRight) pRight.setAttribute("d", "");
  }
}

function updateX1Connections() {
  const centerCard = document.getElementById("x1-selected-card");
  const svg = document.getElementById("x1-svg-connections");
  const arenaContent = document.getElementById("x1-arena-content");

  if (!centerCard || !svg || !arenaContent || arenaContent.style.display === "none") {
    clearX1Connections();
    return;
  }

  // Verifica se o SVG está invisível (ex: no mobile via css)
  if (window.innerWidth <= 1024) {
    clearX1Connections();
    return;
  }

  const svgRect = svg.getBoundingClientRect();
  const centerRect = centerCard.getBoundingClientRect();

  if (svgRect.width === 0 || svgRect.height === 0) return;

  const cx = (centerRect.left + centerRect.width / 2) - svgRect.left;
  const cy = (centerRect.top + centerRect.height / 2) - svgRect.top;

  // Lado Esquerdo (Forte Contra)
  const leftCards = document.querySelectorAll("#x1-list-strong .x1-counter-card");
  for (let i = 1; i <= 3; i++) {
    const path = document.getElementById(`x1-line-left-${i}`);
    if (path) {
      const card = leftCards[i - 1];
      if (card) {
        const cardRect = card.getBoundingClientRect();
        const startX = cardRect.right - svgRect.left;
        const startY = (cardRect.top + cardRect.height / 2) - svgRect.top;
        const endX = centerRect.left - svgRect.left;
        const endY = cy;

        const controlX = startX + (endX - startX) / 2;
        path.setAttribute("d", `M ${startX} ${startY} C ${controlX} ${startY}, ${controlX} ${endY}, ${endX} ${endY}`);
      } else {
        path.setAttribute("d", "");
      }
    }
  }

  // Lado Direito (Fraco Contra)
  const rightCards = document.querySelectorAll("#x1-list-weak .x1-counter-card");
  for (let i = 1; i <= 3; i++) {
    const path = document.getElementById(`x1-line-right-${i}`);
    if (path) {
      const card = rightCards[i - 1];
      if (card) {
        const cardRect = card.getBoundingClientRect();
        const startX = cardRect.left - svgRect.left;
        const startY = (cardRect.top + cardRect.height / 2) - svgRect.top;
        const endX = centerRect.right - svgRect.left;
        const endY = cy;

        const controlX = startX + (endX - startX) / 2;
        path.setAttribute("d", `M ${startX} ${startY} C ${controlX} ${startY}, ${controlX} ${endY}, ${endX} ${endY}`);
      } else {
        path.setAttribute("d", "");
      }
    }
  }
}

// ============================================================
//  PÁGINA DUO BOT — BANCO DE DADOS E LÓGICA DE SINERGIAS
// ============================================================

// Banco de dados curado de sinergias da Bot Lane (Wild Rift Patch 7.1F)
const BOTLANE_DUOS = {
  // === ADCs ===
  "ashe": {
    role: "adc",
    bestPartner: "braum",
    score: "9.7",
    tier: "S+",
    description: "A lentidão constante dos ataques e do W (Rajada) da Ashe facilita muito para o Braum se aproximar, acertar seu Q (Agressão Célere) e aplicar os acúmulos da passiva (Golpes Concussivos). Uma vez atordoado, a Ashe consegue caitar e eliminar o alvo sem sofrer retaliação.",
    tip: "Aproveitem a pressão inicial no nível 1 com o W da Ashe e o Q do Braum para forçar trocas curtas e desgastar a rota adversária.",
    alternatives: ["lulu", "karma", "nautilus"]
  },
  "caitlyn": {
    role: "adc",
    bestPartner: "lux",
    score: "9.8",
    tier: "S+",
    description: "O clássico combo de aprisionamento duplo de longo alcance. Quando a Lux acerta sua Ligação da Luz (Q), a Caitlyn tem tempo de sobra para posicionar uma Armadilha Mecânica (W) exatamente sob os pés do alvo, garantindo um tiro na cabeça (Headshot) com dano amplificado.",
    tip: "Mantenham a linha de visão limpa de tropas inimigas para que a Lux encaixe o Q, e abusem do alcance de ataque básico da Caitlyn para pressionar sob a torre.",
    alternatives: ["morgana", "nautilus", "karma"]
  },
  "corki": {
    role: "adc",
    bestPartner: "nautilus",
    score: "9.3",
    tier: "S",
    description: "O Corki causa alto dano híbrido explosivo, mas necessita de tempo de recarga e segurança na rota inferior. O Nautilus oferece o controle de grupo massivo necessário para mantê-los parados, além de fornecer a segurança que o Corki precisa na fase inicial de rotas.",
    tip: "Aproveitem o Pacote do Corki para iniciar combates rápidos assim que o Nautilus prender um inimigo principal com a âncora.",
    alternatives: ["leona", "yuumi", "braum"]
  },
  "draven": {
    role: "adc",
    bestPartner: "thresh",
    score: "9.8",
    tier: "S+",
    description: "O Draven precisa de rotações de abate rápidas para ativar sua passiva de Adoração. O Thresh oferece controle completo de zona com sua Sentença (Q) e Esfolar (E), além da Lanterna (W) que garante a segurança do Draven para buscar abates extremamente arriscados.",
    tip: "O Thresh deve se posicionar de forma agressiva nos arbustos para criar espaço enquanto o Draven foca em coletar seus machados com segurança.",
    alternatives: ["leona", "nautilus", "pyke"]
  },
  "ezreal": {
    role: "adc",
    bestPartner: "yuumi",
    score: "9.6",
    tier: "S+",
    description: "Um dos duos mais seguros e frustrantes de se enfrentar na botlane. A Yuumi amplifica a força de pokagem do Ezreal, concede velocidade de ataque e cura, enquanto o Ezreal usa sua Translocação Arcana (E) para escapar de qualquer engage, mantendo ambos a salvo.",
    tip: "Foquem no poke contínuo com o Q do Ezreal. Evitem lutas 2v2 diretas até acumular as cargas da Lágrima da Deusa e fechar o primeiro item.",
    alternatives: ["karma", "nami", "braum"]
  },
  "jhin": {
    role: "adc",
    bestPartner: "nautilus",
    score: "9.7",
    tier: "S+",
    description: "O Nautilus facilita incrivelmente o acerto do Florescer Mortal (W) do Jhin com qualquer controle de grupo básico. Uma vez enraizado à distância, o Jhin pode descarregar seus disparos poderosos e iniciar sua ultimate (Abertura do Cortinado) em segurança.",
    tip: "Sempre que o Nautilus aplicar sua passiva ou acertar uma âncora, o Jhin deve seguir imediatamente com seu W para prolongar o controle de grupo.",
    alternatives: ["karma", "zyra", "swain"]
  },
  "jinx": {
    role: "adc",
    bestPartner: "lulu",
    score: "9.9",
    tier: "S+",
    description: "A Lulu transforma a Jinx em uma máquina de abate imparável. O escudo (Help, Pix!) e o buff de velocidade de ataque (Capricho) cobrem a falta de mobilidade inicial da Jinx, permitindo que ela ative sua passiva de aceleração (Anime-se!) rapidamente em lutas.",
    tip: "Foquem puramente em coletar recursos e farmar até a Jinx fechar o primeiro item. A Lulu deve guardar o Capricho para desarmar assassinos adversários.",
    alternatives: ["yuumi", "thresh", "janna"]
  },
  "kaisa": {
    role: "adc",
    bestPartner: "nautilus",
    score: "9.8",
    tier: "S+",
    description: "A passiva da Kai'Sa (Segunda Pele) acumula cargas adicionais sempre que aliados aplicam efeitos de imobilização nos inimigos. Os múltiplos controles de grupo do Nautilus (Passiva, Q e R) estouram a passiva da Kai'Sa quase que instantaneamente.",
    tip: "A Kai'Sa deve esperar o Nautilus iniciar o combate e, assim que o alvo receber CC, usar seu ultimate para se reposicionar de forma agressiva.",
    alternatives: ["leona", "alistar", "rakan"]
  },
  "kalista": {
    role: "adc",
    bestPartner: "thresh",
    score: "9.9",
    tier: "S+",
    description: "Sinergia de alto nível mecânico. O Thresh pode lançar a lanterna (W) para salvar a Kalista após investidas profundas, ou a Kalista usa o Chamado do Destino (R) para puxar o Thresh e arremessá-lo no meio dos inimigos, criando uma iniciação perfeita.",
    tip: "Coordenem o uso do R da Kalista para salvar o Thresh quando ele iniciar com pouca vida ou para surpreender inimigos recuados.",
    alternatives: ["nautilus", "taric", "rell"]
  },
  "kogmaw": {
    role: "adc",
    bestPartner: "lulu",
    score: "9.9",
    tier: "S+",
    description: "A sinergia 'Kog-Lulu' é lendária. A Lulu fornece velocidade de ataque extra, escudos constantes, dano on-hit e o Crescimento Silvestre (R) para garantir a sobrevivência do Kog'Maw enquanto ele derrete a linha de frente inimiga a longa distância.",
    tip: "Joguem com extrema cautela no início. O Kog'Maw precisa acumular níveis e itens antes de tentar trocas forçadas contra duos de engage.",
    alternatives: ["yuumi", "soraka", "milio"]
  },
  "lucian": {
    role: "adc",
    bestPartner: "nami",
    score: "9.8",
    tier: "S+",
    description: "Um dos combos mais explosivos da botlane. Nami usa Bênção da Conjuradora (E) no Lucian, e quando ele ataca com sua passiva de ataque duplo, consome as cargas instantaneamente, aplicando alto dano mágico e lentidão pesada aos inimigos.",
    tip: "Busquem trocas agressivas nos níveis 2 e 3. O burst inicial desse duo pode facilmente abater um atirador inimigo com metade da vida.",
    alternatives: ["braum", "lulu", "yuumi"]
  },
  "miss-fortune": {
    role: "adc",
    bestPartner: "leona",
    score: "9.7",
    tier: "S+",
    description: "O combo supremo de controle de grupo e dano em área. Quando a Leona prende os oponentes com a Erupção Solar (R) ou Lâmina Zênite (E), a Miss Fortune pode canalizar seu Metendo Bala (R) por toda a duração sem que os inimigos escapem.",
    tip: "Aguardem a Leona prender os alvos prioritários antes de descarregar a ultimate da Miss Fortune para garantir o aproveitamento de 100% do dano.",
    alternatives: ["nautilus", "seraphine", "amumu"]
  },
  "samira": {
    role: "adc",
    bestPartner: "nautilus",
    score: "9.8",
    tier: "S+",
    description: "A Samira pode estender a duração de efeitos de arremesso (knockups) de aliados com seus ataques. O Nautilus possui múltiplos arremessos ao ar (Q e R), facilitando o acúmulo da nota de estilo da Samira até o Rank S para ativar seu R.",
    tip: "O Nautilus deve servir como escudo iniciador. A Samira deve aguardar o controle de grupo principal antes de se lançar no meio da luta.",
    alternatives: ["rell", "leona", "alistar"]
  },
  "senna": {
    role: "adc",
    bestPartner: "nautilus",
    score: "9.4",
    tier: "S",
    description: "Como ADC de suporte ou utilidade, a Senna se beneficia de parceiros parrudos. O Nautilus cria a parede de defesa ideal, absorve a pressão inimiga e imobiliza os alvos para que a Senna colete almas e bata com segurança de longe.",
    tip: "Utilizem o enraizamento da Senna para dar sequência ao controle de grupo aplicado pelo Nautilus.",
    alternatives: ["ashe", "seraphine", "braum"]
  },
  "sivir": {
    role: "adc",
    bestPartner: "karma",
    score: "9.5",
    tier: "S+",
    description: "Alta velocidade de rotação e excelente controle de ondas. O Escudo de Velocidade da Karma combinado com o Na Caça (R) da Sivir concede à equipe inteira uma mobilidade imparável para iniciações ou recuos rápidos.",
    tip: "Usem as habilidades de área de ambas para limpar as ondas de tropas instantaneamente e pressionar a torre adversária.",
    alternatives: ["yuumi", "lulu", "janna"]
  },
  "smolder": {
    role: "adc",
    bestPartner: "janna",
    score: "9.4",
    tier: "S",
    description: "O Smolder é um dragãozinho focado em escalonamento tardio que precisa de farm seguro para atingir os 225 acúmulos da passiva. A Janna é excelente para repelir engages agressivos inimigos com seu furacão (Q) e ultimate (Monção).",
    tip: "Joguem de forma totalmente defensiva na fase de rotas. O foco exclusivo deve ser farmar e acumular cargas da passiva com o Q.",
    alternatives: ["lulu", "soraka", "braum"]
  },
  "tristana": {
    role: "adc",
    bestPartner: "leona",
    score: "9.7",
    tier: "S+",
    description: "Engage e all-in implacável. Assim que a Leona aplica o atordoamento do Q, a Tristana pula à frente com o Salto de Foguete (W), coloca a Carga Explosiva (E) e explode o alvo rapidamente, resetando a recarga do seu salto para recuar ou caçar.",
    tip: "Comuniquem-se para focar o mesmo alvo. A Tristana deve usar seu salto apenas quando a Leona garantir a imobilização.",
    alternatives: ["nautilus", "lulu", "alistar"]
  },
  "twitch": {
    role: "adc",
    bestPartner: "lulu",
    score: "9.8",
    tier: "S+",
    description: "O Twitch se beneficia muito de velocidade de ataque e ampliação de vida. A Lulu bufa o Twitch com velocidade enquanto ele está camuflado (Q). Ao se revelar com a ultimate activa, o Twitch recebe o R da Lulu para sobreviver ao foco inimigo.",
    tip: "Surpreendam a rota inferior inimiga saindo da camuflagem perto de alvos sem mobilidade. A Lulu deve acompanhar a posição invisível do Twitch.",
    alternatives: ["yuumi", "pyke", "thresh"]
  },
  "varus": {
    role: "adc",
    bestPartner: "nautilus",
    score: "9.6",
    tier: "S+",
    description: "O Varus possui alta pokagem e controle com a Corrente da Corrupção (R). O Nautilus fornece a âncora inicial necessária para que o Varus encaixe sua ultimate sem chances de erro, prendendo múltiplos alvos nas lutas de equipe.",
    tip: "Use a ultimate do Varus como sequência imediata assim que o Nautilus iniciar a luta no inimigo mais frágil.",
    alternatives: ["karma", "lulu", "leona"]
  },
  "vayne": {
    role: "adc",
    bestPartner: "lulu",
    score: "9.7",
    tier: "S+",
    description: "Lulu é a parceira dos sonhos para a Vayne. O escudo absorve dano, os buffs de velocidade ajudam no reposicionamento da Vayne e o Crescimento Silvestre (R) impede que a Vayne seja eliminada rapidamente por assassinos.",
    tip: "Foque em trocas defensivas e caiting na fase de rotas. Use o Condenar (E) da Vayne em paredes aproveitando o CC da Lulu.",
    alternatives: ["yuumi", "soraka", "nami"]
  },
  "xayah": {
    role: "adc",
    bestPartner: "rakan",
    score: "9.9",
    tier: "S+",
    description: "A sinergia especial clássica do jogo. A Xayah ganha dano e velocidade extra na Plumagem Mortífera (W) quando o Rakan está por perto, e o Rakan ganha o dobro de alcance para saltar na Xayah com seu E, tornando a dupla extremamente segura e móvel.",
    tip: "Aproveitem a habilidade de retorno conjunto para a base para coordenar compras rápidas na loja e não perder experiência de tropas.",
    alternatives: ["lulu", "nautilus", "karma"]
  },
  "zeri": {
    role: "adc",
    bestPartner: "lulu",
    score: "9.8",
    tier: "S+",
    description: "A Zeri precisa de mobilidade e escudos constantes para manter sua velocidade alta nas lutas. Lulu fornece a proteção ideal que ativa a passiva da Zeri, além de dar a velocidade necessária para desviar de habilidades com facilidade.",
    tip: "Mantenha a distância caitando. Use o escudo da Lulu para absorver o poke adversário e reatar o combate.",
    alternatives: ["yuumi", "janna", "soraka"]
  },

  // === SUPORTES ===
  "alistar": {
    role: "support",
    bestPartner: "kaisa",
    score: "9.5",
    tier: "S+",
    description: "O combo do Alistar (Cabeçada + Pulverizar) arremessa inimigos ao ar, ativando stacks da passiva da Kai'Sa e dando a ela a oportunidade perfeita para entrar com dano explosivo de rajada.",
    tip: "Aguardem o Alistar fechar botas de velocidade para buscar engages inesperados na rota.",
    alternatives: ["samira", "tristana", "yasuo"]
  },
  "bard": {
    role: "support",
    bestPartner: "jhin",
    score: "9.3",
    tier: "S",
    description: "O Jhin consegue farmar seguro a longa distância e acompanhar o controle de grupo do Bardo com seu W de longo alcance. Isso permite que o Bardo colete seus sinos pelo mapa sem deixar a rota vulnerável.",
    tip: "O Bardo deve posicionar santuários de cura atrás da torre antes de sair para rotacionar no mapa.",
    alternatives: ["ezreal", "caitlyn", "ashe"]
  },
  "blitzcrank": {
    role: "support",
    bestPartner: "jhin",
    score: "9.5",
    tier: "S+",
    description: "Puxar um alvo com o Blitzcrank garante o acerto imediato do Florescer Mortal (W) do Jhin, prendendo o oponente sob as armadilhas e os projéteis de alto dano do atirador.",
    tip: "Evitem gastar o puxão do Blitzcrank aleatoriamente. Guardem a habilidade para criar pressão apenas com a sua presença.",
    alternatives: ["samira", "draven", "kaisa"]
  },
  "braum": {
    role: "support",
    bestPartner: "lucian",
    score: "9.7",
    tier: "S+",
    description: "O disparo duplo da passiva do Lucian aplica acúmulos da passiva do Braum (Golpes Concussivos) com extrema rapidez, ativando o atordoamento em menos de um segundo nas trocas agressivas.",
    tip: "O Braum deve pular no Lucian com o W e usar o escudo (E) para absorver o dano inimigo após o início das trocas.",
    alternatives: ["ashe", "ezreal", "jinx"]
  },
  "janna": {
    role: "support",
    bestPartner: "smolder",
    score: "9.4",
    tier: "S",
    description: "Excelente desengajamento com furacão (Q) e cura/afastamento no R para manter o Smolder seguro enquanto ele farma para acumular sua passiva. O escudo da Janna também concede AD para as habilidades do dragão.",
    tip: "Use o furacão da Janna de forma defensiva para cortar o avanço dos suportes de engage inimigos.",
    alternatives: ["draven", "jinx", "vayne"]
  },
  "karma": {
    role: "support",
    bestPartner: "ezreal",
    score: "9.6",
    tier: "S+",
    description: "Uma rota extremamente focada em pokagem e mobilidade constante. O poke do Ezreal alinhado ao Q fortalecido da Karma mantém os inimigos pressionados debaixo da torre.",
    tip: "Usem a velocidade do escudo da Karma para desviar de ganks do caçador inimigo e manter o Ezreal seguro.",
    alternatives: ["varus", "caitlyn", "sivir"]
  },
  "leona": {
    role: "support",
    bestPartner: "miss-fortune",
    score: "9.7",
    tier: "S+",
    description: "A iniciação pesada da Leona com a Erupção Solar (R) imobiliza múltiplos inimigos, alinhando-os perfeitamente para receber todo o dano em área da ultimate da Miss Fortune.",
    tip: "Busquem lutas em áreas estreitas ao redor dos objetivos (Dragão e Barão), onde as ultimates de ambas cobrem quase toda a área.",
    alternatives: ["tristana", "draven", "samira"]
  },
  "lulu": {
    role: "support",
    bestPartner: "jinx",
    score: "9.9",
    tier: "S+",
    description: "A Lulu potencializa a Jinx com velocidade de ataque extra, dano do Pix nos ataques rápidos e proteção de vida máxima no R para garantir que ela limpe as lutas de equipe após ativar sua passiva.",
    tip: "Use o W (Capricho) de forma ofensiva na Jinx para aumentar o dano, ou de forma defensiva para transformar o assassino inimigo em um bichinho.",
    alternatives: ["kogmaw", "twitch", "vayne"]
  },
  "lux": {
    role: "support",
    bestPartner: "caitlyn",
    score: "9.8",
    tier: "S+",
    description: "Duo focado em aprisionamento à distância. A Lux prende o inimigo com o Q, e a Caitlyn posiciona uma armadilha logo abaixo do alvo, garantindo um combo de Headshot, Pacifcador de Piltover (Q) e a centelha final da Lux.",
    tip: "Coordenem o tempo da armadilha para colocá-la exatamente na metade da duração do enraizamento da Lux.",
    alternatives: ["jhin", "varus", "ezreal"]
  },
  "maokai": {
    role: "support",
    bestPartner: "kaisa",
    score: "9.5",
    tier: "S+",
    description: "Os múltiplos efeitos de imobilização do Maokai (W, Q, R) acumulam rapidamente a passiva da Kai'Sa. Maokai também serve como uma excelente parede protetora para a Kai'Sa entrar nas lutas.",
    tip: "Maokai deve iniciar com o W garantindo que o inimigo não consiga desviar das habilidades da Kai'Sa.",
    alternatives: ["samira", "draven", "miss-fortune"]
  },
  "milio": {
    role: "support",
    bestPartner: "kogmaw",
    score: "9.8",
    tier: "S+",
    description: "Milio aumenta o alcance dos ataques básicos do Kog'Maw com seu W (Fogueira Acolhedora), permitindo que ele derreta inimigos de distâncias seguras sem se expor a perigos.",
    tip: "Usem o W do Milio no momento em que o Kog'Maw ativar sua própria habilidade de aumento de alcance para maximizar o efeito.",
    alternatives: ["jinx", "caitlyn", "ashe"]
  },
  "morgana": {
    role: "support",
    bestPartner: "caitlyn",
    score: "9.7",
    tier: "S+",
    description: "O Escudo Negro (E) da Morgana protege a Caitlyn contra controles de grupo inimigos, enquanto o Ligação Sombria (Q) de longa duração garante o acerto das armadilhas da Caitlyn sob o alvo.",
    tip: "Fiquem atentos para usar o Escudo Negro na Caitlyn assim que os adversários tentarem focar controle de grupo nela.",
    alternatives: ["jinx", "varus", "ezreal"]
  },
  "nami": {
    role: "support",
    bestPartner: "lucian",
    score: "9.8",
    tier: "S+",
    description: "A Bênção da Conjuradora (E) da Nami concede dano adicional e lentidão aos ataques básicos do Lucian, ativando instantaneamente com a passiva de disparo duplo do atirador.",
    tip: "Use o E na Nami no ar quando o Lucian iniciar o ataque para garantir o efeito surpresa.",
    alternatives: ["jhin", "ezreal", "draven"]
  },
  "nautilus": {
    role: "support",
    bestPartner: "kaisa",
    score: "9.8",
    tier: "S+",
    description: "Nautilus é o melhor aplicador de controle de grupo para a passiva da Kai'Sa, concessões stacks imediatos e permitindo que ela use seu ultimate de reposicionamento agressivo.",
    tip: "Foquem o mesmo alvo focado pela âncora do Nautilus para estourar a passiva da Kai'Sa o mais rápido possível.",
    alternatives: ["samira", "draven", "jhin"]
  },
  "pyke": {
    role: "support",
    bestPartner: "draven",
    score: "9.7",
    tier: "S+",
    description: "Duo focado em economia e snowball. A passiva do Draven dá ouro ao abater inimigos, e a ultimate do Pyke (Morte das Profundezas) compartilha ouro adicional, dobrando a vantagem financeira da dupla.",
    tip: "Deixem os abates finais para o Pyke usar a ultimate sempre que possível para maximizar a entrada de ouro na dupla.",
    alternatives: ["samira", "kaisa", "tristana"]
  },
  "rakan": {
    role: "support",
    bestPartner: "xayah",
    score: "9.9",
    tier: "S+",
    description: "Rakan pode saltar de distâncias muito maiores na Xayah usando seu E, permitindo fugas e engages rápidos. Ambos se beneficiam do W da Xayah para atacar com alta velocidade.",
    tip: "Usem o retorno compartilhado para sincronizar as compras de itens na loja sem perder tempo de rota.",
    alternatives: ["samira", "kaisa", "ezreal"]
  },
  "rell": {
    role: "support",
    bestPartner: "samira",
    score: "9.8",
    tier: "S+",
    description: "A atração em área da ultimate da Rell combinado com o atordoamento de suas habilidades mantém todos os inimigos juntos e imóveis para o Gatilho Infernal (R) da Samira.",
    tip: "Rell deve sinalizar antes de pular com o W para que a Samira esteja no alcance de ativar sua ultimate.",
    alternatives: ["kaisa", "kalista", "tristana"]
  },
  "seraphine": {
    role: "support",
    bestPartner: "miss-fortune",
    score: "9.6",
    tier: "S+",
    description: "A ultimate da Seraphine (Bis) concede charme aos inimigos, alinhando-os perfeitamente para receber todo o dano em área da ultimate da Miss Fortune.",
    tip: "A Seraphine deve usar suas habilidades através dos aliados para estender o alcance de sua ultimate.",
    alternatives: ["caitlyn", "ashe", "senna"]
  },
  "sona": {
    role: "support",
    bestPartner: "ezreal",
    score: "9.4",
    tier: "S",
    description: "Uma rota passiva que escala extremamente bem para o late game. O Ezreal consegue farmar seguro com seu Q, enquanto a Sona cura e dá velocidade para mantê-los saudáveis até as lutas de equipe.",
    tip: "Evitem lutas diretas nos primeiros níveis e foquem em desgastar os inimigos com o poke da Sona.",
    alternatives: ["sona", "seraphine", "caitlyn"]
  },
  "soraka": {
    role: "support",
    bestPartner: "vayne",
    score: "9.5",
    tier: "S+",
    description: "Soraka cura Vayne constantemente permitindo que ela faça trocas curtas e agressivas sem medo de perder vida, compensando a desvantagem natural de alcance da Vayne.",
    tip: "Soraka deve manter o posicionamento seguro atrás da Vayne e focar em acertar o Q para regenerar sua própria vida.",
    alternatives: ["ezreal", "smolder", "jinx"]
  },
  "thresh": {
    role: "support",
    bestPartner: "draven",
    score: "9.8",
    tier: "S+",
    description: "Thresh oferece o controle necessário para manter os inimigos no lugar para os machados do Draven, além da lanterna que permite ao Draven avançar sob a torre inimiga com segurança.",
    tip: "Thresh deve dominar o arbusto da rota para criar ameaça constante com a presença de seu gancho.",
    alternatives: ["kalista", "jinx", "kaisa"]
  },
  "yuumi": {
    role: "support",
    bestPartner: "ezreal",
    score: "9.6",
    tier: "S+",
    description: "Duo extremamente móvel e seguro. O Ezreal consegue desviar de habilidades com o E, carregando a Yuumi em segurança enquanto ela cura e amplifica seu poder de pokagem.",
    tip: "Yuumi deve aproveitar momentos de recarga inimiga para descer do Ezreal e bater para recuperar mana com seu escudo passivo.",
    alternatives: ["zeri", "twitch", "jinx"]
  },
  "zyra": {
    role: "support",
    bestPartner: "jhin",
    score: "9.6",
    tier: "S+",
    description: "Zyra enraiza os inimigos com suas plantas, permitindo o acerto fácil do W do Jhin e estendendo o controle de grupo com as plantas da Zyra batendo continuamente no alvo preso.",
    tip: "Posicionem as sementes da Zyra nos arbustos para dar visão e zoneamento contra engages do suporte inimigo.",
    alternatives: ["ashe", "caitlyn", "ezreal"]
  },
  "zilean": {
    role: "support",
    bestPartner: "jinx",
    score: "9.5",
    tier: "S",
    description: "Zilean concede velocidade absurda para a Jinx caçar alvos e sua ultimate de ressurreição dá a segurança necessária para ela jogar agressivamente e pegar o reset de sua passiva.",
    tip: "Zilean deve focar em colocar bombas duplas nos minions próximos aos inimigos para zoneá-los.",
    alternatives: ["twitch", "vayne", "ezreal"]
  }
};

// Estado da Aba Duo Bot
let selectedDuoChamp = null;
let selectedDuoPartner = null;
let duoSelectedRole = "all"; // Filtros: "all", "adc", "support"

// Inicialização da aba Duo Bot
function initDuos() {
  const duoSearch = document.getElementById("duo-search-input");
  const clearBtn = document.getElementById("duo-clear-btn");

  if (duoSearch) {
    duoSearch.addEventListener("input", (e) => {
      const query = e.target.value;
      if (clearBtn) {
        clearBtn.style.display = query ? "flex" : "none";
      }
      renderDuosSelector(query);
    });
  }

  if (clearBtn) {
    clearBtn.addEventListener("click", () => {
      if (duoSearch) duoSearch.value = "";
      clearBtn.style.display = "none";
      renderDuosSelector("");
      resetDuosArena();
    });
  }

  // Filtros de Categoria (Todos, ADC, Suportes)
  const duoLaneButtons = document.querySelectorAll("#duo-lane-filters .duo-lane-btn");
  duoLaneButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      duoLaneButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      duoSelectedRole = btn.getAttribute("data-role");
      const searchVal = document.getElementById("duo-search-input")?.value || "";
      renderDuosSelector(searchVal);
    });
  });

  // Escuta resize da janela para ajustar a linha SVG
  window.addEventListener("resize", () => {
    if (activeTab === "duos" && selectedDuoChamp) {
      updateDuosConnections();
    }
  });

  // Abre os detalhes ao clicar nos cards centrais da arena
  const leftCard = document.getElementById("duo-selected-card");
  if (leftCard) {
    leftCard.addEventListener("click", () => {
      if (selectedDuoChamp) showChampionDetails(selectedDuoChamp);
    });
  }

  const rightCard = document.getElementById("duo-partner-card");
  if (rightCard) {
    rightCard.addEventListener("click", () => {
      if (selectedDuoPartner) showChampionDetails(selectedDuoPartner);
    });
  }

  renderDuosSelector();
}

// Chamado ao entrar na aba
function renderDuos() {
  renderDuosSelector();
  if (selectedDuoChamp) {
    setTimeout(updateDuosConnections, 100);
  }
}

// Reseta a arena de sinergias
function resetDuosArena() {
  selectedDuoChamp = null;
  selectedDuoPartner = null;

  // Limpa seleção visual nos retratos
  document.querySelectorAll(".duo-champ-portrait-btn.active").forEach(btn => {
    btn.classList.remove("active");
  });

  // Mostra mensagem inicial e oculta a arena ativa
  const welcome = document.getElementById("duo-welcome-state");
  const arenaContent = document.getElementById("duo-arena-content");
  const detailsWrapper = document.getElementById("duo-details-wrapper");

  if (welcome) welcome.style.display = "flex";
  if (arenaContent) arenaContent.style.display = "none";
  if (detailsWrapper) detailsWrapper.style.display = "none";

  clearDuosConnections();
}

// Encontra estatísticas oficiais do campeão no banco
function findChampionBySlug(slug) {
  return champions.find(c => c.slug === slug) || null;
}

// Injeta e renderiza os retratos no seletor da botlane
function renderDuosSelector(filterText = "") {
  const grid = document.getElementById("duo-grid-selector");
  if (!grid) return;
  grid.innerHTML = "";

  // Filtra apenas campeões que existem no nosso banco de sinergias
  let botChamps = champions.filter(c => BOTLANE_DUOS[c.slug]);

  // Filtra por categoria de filtro selecionada (ADC ou Suporte)
  if (duoSelectedRole !== "all") {
    botChamps = botChamps.filter(c => {
      const duoDef = BOTLANE_DUOS[c.slug];
      return duoDef && duoDef.role === duoSelectedRole;
    });
  }

  // Filtra por busca textual
  if (filterText) {
    botChamps = botChamps.filter(c => normalizeText(c.nome).includes(normalizeText(filterText)));
  }

  // Deduplica e ordena por nome
  botChamps = getUniqueChampions(botChamps);
  botChamps.sort((a, b) => a.nome.localeCompare(b.nome));

  if (botChamps.length === 0) {
    grid.innerHTML = `<p class="empty-text" style="color: var(--text-muted); padding: 10px;">Nenhum campeão encontrado.</p>`;
    return;
  }

  botChamps.forEach(c => {
    const btn = document.createElement("button");
    btn.className = "duo-champ-portrait-btn";
    btn.setAttribute("title", c.nome);
    btn.setAttribute("data-champ-id", c.id);

    if (selectedDuoChamp && selectedDuoChamp.id === c.id) {
      btn.classList.add("active");
    }

    const iconUrl = getChampionIcon(c.slug, c.id);
    const tencIconUrl = `https://game.gtimg.cn/images/lgamem/act/lrlib/img/HeadIcon/H_S_${c.id}.png`;

    btn.innerHTML = `
      <img src="${iconUrl}" alt="${c.nome}" loading="lazy" onerror="if(this.src!='${tencIconUrl}'){this.src='${tencIconUrl}';}">
    `;

    btn.addEventListener("click", () => {
      selectDuoChampion(c);
    });

    grid.appendChild(btn);
  });
}

// Seleciona um campeão e carrega toda a sua sinergia na tela
function selectDuoChampion(champ) {
  if (!champ) return;
  selectedDuoChamp = champ;

  const duoData = BOTLANE_DUOS[champ.slug];
  if (!duoData) return;

  // Encontra ou cria dados do parceiro recomendado
  const realPartner = findChampionBySlug(duoData.bestPartner);
  const partnerChamp = realPartner || {
    id: "",
    nome: duoData.bestPartner.charAt(0).toUpperCase() + duoData.bestPartner.slice(1),
    slug: duoData.bestPartner,
    tier: duoData.tier,
    winRate: "51.0%",
    banRate: "2.0%",
    lane: champ.lane === "3" ? "4" : "3" // Oposto da lane do selecionado
  };
  selectedDuoPartner = partnerChamp;

  // Atualiza classe ativa no grid
  document.querySelectorAll(".duo-champ-portrait-btn").forEach(btn => {
    if (btn.getAttribute("data-champ-id") === champ.id) {
      btn.classList.add("active");
    } else {
      btn.classList.remove("active");
    }
  });

  // Troca estados na tela
  const welcome = document.getElementById("duo-welcome-state");
  const arenaContent = document.getElementById("duo-arena-content");
  const detailsWrapper = document.getElementById("duo-details-wrapper");

  if (welcome) welcome.style.display = "none";
  if (arenaContent) arenaContent.style.display = "grid";
  if (detailsWrapper) detailsWrapper.style.display = "block";

  // Preenche dados do selecionado (esquerda)
  const selectedImg = document.getElementById("duo-selected-img");
  const selectedName = document.getElementById("duo-selected-name");
  const selectedTier = document.getElementById("duo-selected-tier");
  const selectedLane = document.getElementById("duo-selected-lane");
  const selectedWin = document.getElementById("duo-selected-winrate");
  const selectedBan = document.getElementById("duo-selected-banrate");

  if (selectedImg) {
    const iconUrl = getChampionIcon(champ.slug, champ.id);
    const tencIconUrl = `https://game.gtimg.cn/images/lgamem/act/lrlib/img/HeadIcon/H_S_${champ.id}.png`;
    selectedImg.src = iconUrl;
    selectedImg.onerror = () => { selectedImg.src = tencIconUrl; };
  }
  if (selectedName) selectedName.textContent = champ.nome;
  if (selectedTier) {
    selectedTier.textContent = champ.tier;
    selectedTier.className = `card-tier-badge tier-${champ.tier.toLowerCase().replace("+", "-plus")}`;
  }
  if (selectedLane) {
    const lName = LANE_NAMES[champ.lane] || "ADC";
    const lIcon = LANE_ICONS[champ.lane] || "fa-crosshairs";
    selectedLane.innerHTML = `<i class="fa-solid ${lIcon}"></i> ${lName}`;
  }
  if (selectedWin) {
    selectedWin.textContent = champ.winRate;
    selectedWin.className = `stat-val ${parseFloat(champ.winRate) >= 50 ? 'text-green' : 'text-red'}`;
  }
  if (selectedBan) selectedBan.textContent = champ.banRate;

  // Preenche dados do parceiro (direita)
  const partnerImg = document.getElementById("duo-partner-img");
  const partnerName = document.getElementById("duo-partner-name");
  const partnerTier = document.getElementById("duo-partner-tier");
  const partnerLane = document.getElementById("duo-partner-lane");
  const partnerWin = document.getElementById("duo-partner-winrate");
  const partnerBan = document.getElementById("duo-partner-banrate");

  if (partnerImg) {
    const iconUrl = getChampionIcon(partnerChamp.slug, partnerChamp.id);
    const tencIconUrl = partnerChamp.id ? `https://game.gtimg.cn/images/lgamem/act/lrlib/img/HeadIcon/H_S_${partnerChamp.id}.png` : "";
    partnerImg.src = iconUrl;
    partnerImg.onerror = () => { if (tencIconUrl) partnerImg.src = tencIconUrl; };
  }
  if (partnerName) partnerName.textContent = partnerChamp.nome;
  if (partnerTier) {
    partnerTier.textContent = partnerChamp.tier;
    partnerTier.className = `card-tier-badge tier-${partnerChamp.tier.toLowerCase().replace("+", "-plus")}`;
  }
  if (partnerLane) {
    const lName = LANE_NAMES[partnerChamp.lane] || "Suporte";
    const lIcon = LANE_ICONS[partnerChamp.lane] || "fa-hands-holding-circle";
    partnerLane.innerHTML = `<i class="fa-solid ${lIcon}"></i> ${lName}`;
  }
  if (partnerWin) {
    partnerWin.textContent = partnerChamp.winRate;
    partnerWin.className = `stat-val ${parseFloat(partnerChamp.winRate) >= 50 ? 'text-green' : 'text-red'}`;
  }
  if (partnerBan) partnerBan.textContent = partnerChamp.banRate;

  // Preenche score central de sinergia
  const scoreNum = document.getElementById("duo-score-number");
  const scoreBadge = document.getElementById("duo-synergy-badge");
  if (scoreNum) scoreNum.textContent = duoData.score;
  if (scoreBadge) {
    scoreBadge.textContent = `${duoData.tier} Sinergia`;
  }

  // Preenche textos explicativos e dicas
  const descText = document.getElementById("duo-synergy-desc-text");
  const tipText = document.getElementById("duo-synergy-tip-text");
  if (descText) descText.textContent = duoData.description;
  if (tipText) tipText.textContent = duoData.tip;

  // Preenche outras boas sinergias (alternativas)
  const altList = document.getElementById("duo-alternatives-list");
  if (altList) {
    altList.innerHTML = "";
    duoData.alternatives.forEach(altSlug => {
      const realAlt = findChampionBySlug(altSlug);
      const altName = realAlt ? realAlt.nome : altSlug.charAt(0).toUpperCase() + altSlug.slice(1);
      const altRole = duoData.role === "adc" ? "Suporte" : "Atirador (ADC)";
      const altIcon = getChampionIcon(altSlug, realAlt?.id || "");
      const altTencIcon = realAlt?.id ? `https://game.gtimg.cn/images/lgamem/act/lrlib/img/HeadIcon/H_S_${realAlt.id}.png` : "";

      const card = document.createElement("div");
      card.className = "duo-alt-card";
      card.innerHTML = `
        <img src="${altIcon}" alt="${altName}" onerror="if(this.src!='${altTencIcon}'){this.src='${altTencIcon}';}">
        <div class="duo-alt-card-info">
          <span class="duo-alt-card-name">${altName}</span>
          <span class="duo-alt-card-role">${altRole}</span>
        </div>
      `;

      card.addEventListener("click", () => {
        const found = realAlt || champions.find(hc => hc.slug === altSlug);
        if (found) {
          selectDuoChampion(found);
          const activeContent = document.getElementById("duos-tab-content");
          if (activeContent) {
            window.scrollTo({ top: activeContent.offsetTop - 100, behavior: "smooth" });
          }
        }
      });

      altList.appendChild(card);
    });
  }

  // Trata animação e conexão SVG
  const selectedCol = document.querySelector(".duo-column-selected");
  const partnerCol = document.querySelector(".duo-column-partner");
  const centralCol = document.querySelector(".duo-column-score");

  if (selectedCol) {
    selectedCol.classList.remove("animate-slide-left");
    void selectedCol.offsetWidth;
    selectedCol.classList.add("animate-slide-left");
  }
  if (partnerCol) {
    partnerCol.classList.remove("animate-slide-right");
    void partnerCol.offsetWidth;
    partnerCol.classList.add("animate-slide-right");
  }
  if (centralCol) {
    centralCol.classList.remove("animate-center-zoom");
    void centralCol.offsetWidth;
    centralCol.classList.add("animate-center-zoom");
  }

  setTimeout(updateDuosConnections, 100);
}

// Reseta o desenho SVG
function clearDuosConnections() {
  const line = document.getElementById("duo-connection-line");
  if (line) line.setAttribute("d", "");
}

// Atualiza o desenho SVG dinamicamente conforme dimensões dos cards
function updateDuosConnections() {
  const leftCard = document.getElementById("duo-selected-card");
  const rightCard = document.getElementById("duo-partner-card");
  const svg = document.getElementById("duo-svg-connections");
  const arenaContent = document.getElementById("duo-arena-content");

  if (!leftCard || !rightCard || !svg || !arenaContent || arenaContent.style.display === "none") {
    clearDuosConnections();
    return;
  }

  if (window.innerWidth <= 1024) {
    clearDuosConnections();
    return;
  }

  const svgRect = svg.getBoundingClientRect();
  const leftRect = leftCard.getBoundingClientRect();
  const rightRect = rightCard.getBoundingClientRect();

  if (svgRect.width === 0 || svgRect.height === 0) return;

  const startX = leftRect.right - svgRect.left;
  const startY = (leftRect.top + leftRect.height / 2) - svgRect.top;

  const endX = rightRect.left - svgRect.left;
  const endY = (rightRect.top + rightRect.height / 2) - svgRect.top;

  const controlX1 = startX + (endX - startX) * 0.25;
  const controlY1 = startY;
  const controlX2 = startX + (endX - startX) * 0.75;
  const controlY2 = endY;

  const path = document.getElementById("duo-connection-line");
  if (path) {
    path.setAttribute("d", `M ${startX} ${startY} C ${controlX1} ${controlY1}, ${controlX2} ${controlY2}, ${endX} ${endY}`);
  }
}

