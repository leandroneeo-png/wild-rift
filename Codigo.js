// Código.js - Google Apps Script

// =========================================================================
// CONFIGURAÇÃO DO FIREBASE
// =========================================================================
const FIREBASE_CONFIG = {
  apiKey: "AIzaSyAJfutv_N-tD4d5I4jvFBBaE4oMO3OoQ2Y",
  authDomain: "wild-rift-533bd.firebaseapp.com",
  projectId: "wild-rift-533bd",
  storageBucket: "wild-rift-533bd.firebasestorage.app",
  messagingSenderId: "298535587482",
  appId: "1:298535587482:web:47d7351762f2230ce9d923",
  measurementId: "G-4CD4Z7NX0L"
};

// Escolha qual banco de dados você deseja usar setando true/false abaixo:
const USAR_FIRESTORE = true; // Se true, envia para o Firestore. Se false, envia para o Realtime Database.

// URLs REST derivadas do Config
const FIREBASE_REALTIME_DB_URL = "https://" + FIREBASE_CONFIG.projectId + "-default-rtdb.firebaseio.com/";

// URLs das Fontes de Dados (APIs da Tencent)
const TENCENT_HERO_LIST_URL = "https://apps.game.qq.com/lolm/raider/GetHeroListData.php";
const TENCENT_HERO_EQUIP_URL = "https://apps.game.qq.com/lolm/raider/GetItemEquipData.php";

// =========================================================================
// CONFIGURAÇÃO DE PROXY (Para contornar o bloqueio de Referer do Apps Script)
// =========================================================================
// Como o Google Apps Script impede que alteremos o cabeçalho 'Referer' nativamente,
// você pode hospedar um Cloudflare Worker (100% gratuito) que atua como proxy.
// Insira a URL do seu Worker aqui (ex: "https://meu-proxy.seu-usuario.workers.dev")
// Se deixar vazio "", o script tentará fazer a chamada direta (pode retornar erro 404 da Tencent).
const PROXY_URL = "https://lolm-proxy.leandroneeo.workers.dev"; 

function monitorarSiteChines() {
  try {
    Logger.log("Iniciando coleta e tradução de dados do Wild Rift...");

    // 1. Coleta a lista geral de campeões (Contém Win Rate, Pick Rate, Ban Rate)
    const dadosHeroList = fetchJsonp(TENCENT_HERO_LIST_URL + "?callback=jsonpCallback");
    if (!dadosHeroList || dadosHeroList.status !== 0 || !dadosHeroList.data) {
      throw new Error("Falha ao obter dados da lista de campeões da Tencent.");
    }
    const listaCampeoesChineses = dadosHeroList.data;

    // 2. Carrega o dicionário de tradução do Sheets
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Dicionario_Campeoes");
    if (!sheet) {
      throw new Error("Planilha 'Dicionario_Campeoes' não encontrada. Crie a aba correspondente.");
    }
    const dicionario = obterDicionario(sheet);

    // 3. Processa e monta os dados
    let dadosParaRealtime = {};

    listaCampeoesChineses.forEach(campeaoChines => {
      const id = String(campeaoChines.heroId);
      const infoTraduzida = dicionario[id];
      
      if (infoTraduzida) {
        Logger.log("Processando: " + infoTraduzida.nomePTBR);

        // Busca build recomendada
        let buildRecomendada = [];
        let runasRecomendadas = [];
        let spellsRecomendados = [];
        
        try {
          const dadosEquip = fetchJsonp(TENCENT_HERO_EQUIP_URL + "?heroId=" + id + "&callback=jsonpCallback");
          if (dadosEquip && dadosEquip.status === 0 && dadosEquip.data && dadosEquip.data.equipList) {
            const primeiraBuild = dadosEquip.data.equipList[0];
            if (primeiraBuild) {
              buildRecomendada = primeiraBuild.equipItem || [];
              runasRecomendadas = primeiraBuild.runeId || [];
              spellsRecomendados = primeiraBuild.spellId || [];
            }
          }
        } catch (errEquip) {
          Logger.log("Aviso de build para " + infoTraduzida.nomePTBR + ": " + errEquip.message);
        }

        // Calcula a tier dinamicamente
        const winRateVal = parseFloat(campeaoChines.winRate.replace("%", ""));
        const pickRateVal = parseFloat(campeaoChines.appearanceRate.replace("%", ""));
        const tier = calcularTier(winRateVal, pickRateVal);

        const payloadCampeao = {
          id: id,
          nome: infoTraduzida.nomePTBR,
          slug: infoTraduzida.slug,
          winRate: campeaoChines.winRate,
          pickRate: campeaoChines.appearanceRate,
          banRate: campeaoChines.banRate,
          tier: tier,
          buildRecomendada: buildRecomendada,
          runasRecomendadas: runasRecomendadas,
          spellsRecomendados: spellsRecomendados,
          atualizadoEm: new Date().toISOString()
        };

        if (USAR_FIRESTORE) {
          // Salva campeão por campeão diretamente no Firestore via REST
          atualizarFirestoreRest(id, payloadCampeao);
        } else {
          // Prepara objeto completo para salvar de uma vez no Realtime Database
          dadosParaRealtime[id] = payloadCampeao;
        }
        
        Utilities.sleep(100); // Evita rate limiting
      }
    });

    // 4. Envio final caso use Realtime Database
    if (!USAR_FIRESTORE) {
      atualizarRealtimeDatabaseRest(dadosParaRealtime);
    }
    
    Logger.log("Sincronização concluída com sucesso no Firebase!");

  } catch (error) {
    Logger.log("Erro durante a execução: " + error.toString());
  }
}

/**
 * Converte o retorno JSONP em JSON Limpo, opcionalmente roteando pelo proxy
 */
function fetchJsonp(url) {
  let targetUrl = url;
  if (PROXY_URL) {
    targetUrl = PROXY_URL + "?url=" + encodeURIComponent(url);
  }

  const options = {
    method: "get",
    headers: {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
      "Referer": "https://lolm.qq.com/"
    },
    muteHttpExceptions: true
  };
  
  const response = UrlFetchApp.fetch(targetUrl, options);
  const text = response.getContentText("UTF-8");
  const jsonStart = text.indexOf("(");
  const jsonEnd = text.lastIndexOf(")");
  
  if (jsonStart !== -1 && jsonEnd !== -1) {
    const jsonStr = text.substring(jsonStart + 1, jsonEnd);
    return JSON.parse(jsonStr);
  }
  return JSON.parse(text);
}

/**
 * Lê o dicionário mapeado da planilha ativa
 */
function obterDicionario(sheet) {
  const data = sheet.getDataRange().getValues();
  const dicionario = {};
  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    const id = String(row[0]).trim();
    if (id) {
      dicionario[id] = {
        nomeChines: row[1],
        nomePTBR: row[2],
        slug: row[3]
      };
    }
  }
  return dicionario;
}

/**
 * Classificação matemática de Tiers
 */
function calcularTier(winRate, pickRate) {
  if (winRate >= 52.5 && pickRate >= 8.0) return "S+";
  if (winRate >= 51.5 && pickRate >= 5.0) return "S";
  if (winRate >= 50.0 && pickRate >= 3.0) return "A";
  if (winRate >= 48.0) return "B";
  return "C";
}

/**
 * Envia um documento para o Firestore via API REST com chave de acesso
 */
function atualizarFirestoreRest(heroId, docData) {
  const url = "https://firestore.googleapis.com/v1/projects/" + FIREBASE_CONFIG.projectId + "/databases/(default)/documents/campeoes/" + heroId + "?key=" + FIREBASE_CONFIG.apiKey;
  
  // Transforma objeto simples no formato de campos esperado pela API REST do Firestore
  const firestoreDoc = {
    fields: {}
  };
  
  for (const key in docData) {
    firestoreDoc.fields[key] = formatarCampoFirestore(docData[key]);
  }

  const options = {
    method: "patch", // Patch substitui ou cria se não existir
    contentType: "application/json",
    payload: JSON.stringify(firestoreDoc),
    muteHttpExceptions: true
  };

  const response = UrlFetchApp.fetch(url, options);
  const code = response.getResponseCode();
  
  if (code !== 200) {
    Logger.log("Erro ao salvar no Firestore (HeroID: " + heroId + ") - Status " + code + ": " + response.getContentText());
  }
}

/**
 * Auxiliar para tipagem de dados da API REST do Firestore
 */
function formatarCampoFirestore(val) {
  if (typeof val === 'string') return { stringValue: val };
  if (typeof val === 'number') return { doubleValue: val };
  if (typeof val === 'boolean') return { booleanValue: val };
  if (Array.isArray(val)) {
    return {
      arrayValue: {
        values: val.map(item => formatarCampoFirestore(item))
      }
    };
  }
  return { stringValue: String(val) };
}

/**
 * Salva a árvore inteira de campeões no Firebase Realtime Database
 */
function atualizarRealtimeDatabaseRest(dados) {
  const url = FIREBASE_REALTIME_DB_URL + "campeoes.json?key=" + FIREBASE_CONFIG.apiKey;
  const options = {
    method: "put",
    contentType: "application/json",
    payload: JSON.stringify(dados),
    muteHttpExceptions: true
  };
  
  const response = UrlFetchApp.fetch(url, options);
  const code = response.getResponseCode();
  
  if (code !== 200) {
    throw new Error("Erro ao salvar no Realtime DB (" + code + "): " + response.getContentText());
  }
  Logger.log("Realtime Database sincronizado com sucesso!");
}
