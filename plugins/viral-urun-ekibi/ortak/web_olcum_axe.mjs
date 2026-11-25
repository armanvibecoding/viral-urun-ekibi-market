// axe-core ile erişilebilirlik ölçümü (web_olcum.py çağırır). Yalnız okur: sayfayı açar, axe çalıştırır, JSON basar.
//   node web_olcum_axe.mjs <web-olcum-dizini> <chrome-yolu> <url> [genislik]
// Modüller <web-olcum-dizini>/node_modules'tan çözülür (axe-core, puppeteer-core: sürüm sabit, ayrı klasör; global kurulum yok).
import { createRequire } from "node:module";
import { readFileSync } from "node:fs";
import { join } from "node:path";

const [dizin, chrome, url, genislikArg] = process.argv.slice(2);
if (!dizin || !chrome || !url) {
  console.error("kullanım: node web_olcum_axe.mjs <dizin> <chrome> <url> [genislik]");
  process.exit(2);
}
const genislik = Number(genislikArg || 390);
const require = createRequire(join(dizin, "package.json"));
const puppeteer = require("puppeteer-core");
const axeKaynak = readFileSync(require.resolve("axe-core/axe.min.js"), "utf8");
const axeSurum = require("axe-core/package.json").version;
// WCAG 2.2 AA = 2.0 A/AA + 2.1 A/AA + 2.2 AA (en-iyi-uygulama kuralları dahil değil: yalnız standart ihlali sayılır)
const ETIKETLER = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"];

const tarayici = await puppeteer.launch({ executablePath: chrome, headless: true, args: ["--no-first-run", "--disable-gpu"] });
try {
  const sayfa = await tarayici.newPage();
  await sayfa.setViewport({ width: genislik, height: genislik < 700 ? 844 : 900, deviceScaleFactor: 1, isMobile: genislik < 700 });
  await sayfa.goto(url, { waitUntil: "load", timeout: 60000 });
  await sayfa.evaluate(axeKaynak);
  const sonuc = await sayfa.evaluate(async (etiketler) => {
    const r = await window.axe.run(document, { runOnly: { type: "tag", values: etiketler }, resultTypes: ["violations", "incomplete"] });
    const ozet = (l) => l.map((v) => ({
      kural: v.id, etki: v.impact, aciklama: v.help, adet: v.nodes.length,
      ornek: v.nodes.slice(0, 2).map((n) => ({ secici: (n.target || []).join(" "), ozet: (n.failureSummary || "").split("\n").slice(0, 3).join(" ") })),
    }));
    return { ihlaller: ozet(r.violations), incomplete: ozet(r.incomplete) };
  }, ETIKETLER);
  console.log(JSON.stringify({ axe: axeSurum, genislik, url, ...sonuc }));
} finally {
  await tarayici.close();
}
