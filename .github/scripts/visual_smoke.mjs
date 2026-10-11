import { chromium } from "playwright";
import fs from "node:fs";
import path from "node:path";

const baseURL = process.env.PREVIEW_BASE_URL || "http://127.0.0.1:4173";
const outDir = process.argv[2] || "artifacts/preview";
fs.mkdirSync(outDir, { recursive: true });

const cases = [
  { name: "home-zh-desktop", route: "/", viewport: { width: 1440, height: 1000 }, lang: "zh", mode: "desktop" },
  { name: "home-zh-tablet", route: "/", viewport: { width: 820, height: 1180 }, lang: "zh", mode: "mobile-menu" },
  { name: "home-zh-mobile", route: "/", viewport: { width: 390, height: 844 }, lang: "zh", mode: "mobile-menu" },
  { name: "home-en-desktop", route: "/en/", viewport: { width: 1440, height: 1000 }, lang: "en", mode: "desktop" },
  { name: "project-detail-mobile", route: "/projects/wafer-scheduling/", viewport: { width: 390, height: 844 }, lang: "zh", mode: "mobile-menu" },
  { name: "writing-search-mobile", route: "/writing/", viewport: { width: 390, height: 844 }, lang: "zh", mode: "search" },
];

const browser = await chromium.launch({ headless: true });
const failures = [];
try {
  for (const test of cases) {
    const page = await browser.newPage({ viewport: test.viewport, deviceScaleFactor: 1 });
    const pageErrors = [];
    page.on("pageerror", error => pageErrors.push(error.message));

    const response = await page.goto(baseURL + test.route, { waitUntil: "networkidle", timeout: 30000 });
    if (!response || !response.ok()) {
      failures.push(test.name + ": route returned " + (response ? response.status() : "no response"));
      await page.close();
      continue;
    }

    const actualLang = await page.locator("html").getAttribute("lang");
    if (actualLang !== test.lang) failures.push(test.name + ": expected lang=" + test.lang + ", got " + actualLang);

    if (test.mode === "desktop") {
      if (!(await page.locator("nav.desktop").isVisible())) failures.push(test.name + ": desktop navigation is hidden");
      if (await page.locator(".mobile summary").isVisible()) failures.push(test.name + ": mobile menu appears on desktop");
    } else {
      if (!(await page.locator(".mobile summary").isVisible())) failures.push(test.name + ": mobile menu trigger is hidden");
      if (!(await page.locator(".lang-switch").isVisible())) failures.push(test.name + ": language switch is hidden");
    }

    await page.evaluate(async () => {
      document.documentElement.style.scrollBehavior = "auto";
      const step = Math.max(window.innerHeight, 500);
      for (let y = 0; y < document.body.scrollHeight; y += step) {
        window.scrollTo(0, y);
        await new Promise(resolve => setTimeout(resolve, 35));
      }
      window.scrollTo(0, 0);
      await new Promise(resolve => requestAnimationFrame(() => resolve()));
    });

    const dimensions = await page.evaluate(() => ({
      viewport: document.documentElement.clientWidth,
      document: document.documentElement.scrollWidth,
      body: document.body.scrollWidth
    }));
    if (dimensions.document > dimensions.viewport + 1 || dimensions.body > dimensions.viewport + 1) {
      const offenders = await page.evaluate(() => Array.from(document.querySelectorAll("body *")).map(el => {
        const rect = el.getBoundingClientRect();
        return {
          tag: el.tagName.toLowerCase(),
          id: el.id || "",
          className: typeof el.className === "string" ? el.className : "",
          text: (el.innerText || "").trim().slice(0, 70),
          left: Math.round(rect.left),
          right: Math.round(rect.right),
          width: Math.round(rect.width),
          scrollWidth: el.scrollWidth,
          clientWidth: el.clientWidth
        };
      }).filter(el => el.right > window.innerWidth + 1 || el.left < -1)
        .sort((a, b) => b.right - a.right)
        .slice(0, 8));
      failures.push(test.name + ": horizontal overflow " + JSON.stringify({ ...dimensions, offenders }));
    }

    const brokenImages = await page.locator("img").evaluateAll(images =>
      images.filter(img => img.complete && img.naturalWidth === 0).map(img => img.currentSrc || img.src)
    );
    if (brokenImages.length) failures.push(test.name + ": broken images " + brokenImages.join(", "));

    await page.screenshot({ path: path.join(outDir, test.name + ".png"), fullPage: true });

    if (test.mode === "mobile-menu") {
      await page.locator(".mobile summary").click();
      if (!(await page.locator(".mobile nav").isVisible())) failures.push(test.name + ": mobile menu did not open");
      const navLabels = await page.locator(".mobile nav a").allTextContents();
      if (navLabels.length < 6) failures.push(test.name + ": expected at least six mobile navigation links");
      const openMenuDimensions = await page.evaluate(() => ({
        viewport: document.documentElement.clientWidth,
        document: document.documentElement.scrollWidth
      }));
      if (openMenuDimensions.document > openMenuDimensions.viewport + 1) {
        failures.push(test.name + ": opening mobile menu causes horizontal overflow");
      }
    }

    if (test.mode === "search") {
      const search = page.locator("#article-search");
      if (!(await search.isVisible())) {
        failures.push(test.name + ": article search input is missing");
      } else {
        await search.fill("模型预测控制");
        const visibleResults = await page.locator("[data-article]:visible").count();
        if (visibleResults < 1) failures.push(test.name + ": article search returned no matching results");
        const countText = await page.locator("#search-count").textContent();
        if (!countText || !countText.includes(String(visibleResults))) {
          failures.push(test.name + ": search result counter did not update (" + countText + ")");
        }
      }
    }

    if (pageErrors.length) failures.push(test.name + ": browser errors " + pageErrors.join(" | "));
    await page.close();
    console.log("PASS " + test.name + " (" + test.viewport.width + "x" + test.viewport.height + ")");
  }
} finally {
  await browser.close();
}

if (failures.length) {
  console.error("\nBrowser QA failures:\n- " + failures.join("\n- "));
  process.exitCode = 1;
} else {
  console.log("Browser QA passed for " + cases.length + " pages/viewports. Screenshots: " + outDir);
}
