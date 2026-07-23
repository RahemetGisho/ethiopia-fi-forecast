const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, ImageRun, Table, TableRow,
  TableCell, WidthType, ShadingType, BorderStyle, AlignmentType, PageBreak,
  Header, Footer, PageNumber, NumberFormat, VerticalAlign, convertInchesToTwip,
  ExternalHyperlink, TabStopType, TabStopPosition, LevelFormat,
} = require("docx");

const FIG = path.join(__dirname, "figures");
const img = (name) => fs.readFileSync(path.join(FIG, name));

// ---------- palette ----------
const NAVY = "1E293B";
const BLUE = "2563EB";
const GREEN = "16A34A";
const PINK = "DB2777";
const SLATE = "475569";
const LIGHT = "EFF6FF";
const LIGHTGREY = "F1F5F9";
const WHITE = "FFFFFF";
const GOLD = "D97706";

const FONT = "Calibri";

// ---------- small helpers ----------
const h1 = (text, num) => new Paragraph({
  heading: HeadingLevel.HEADING_1,
  spacing: { before: 480, after: 200 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: BLUE, space: 6 } },
  children: [
    ...(num ? [new TextRun({ text: `${num}  `, color: BLUE, bold: true, font: FONT })] : []),
    new TextRun({ text, color: NAVY, bold: true, font: FONT }),
  ],
});

const h2 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_2,
  spacing: { before: 300, after: 140 },
  children: [new TextRun({ text, color: BLUE, bold: true, font: FONT })],
});

const body = (text, opts = {}) => new Paragraph({
  spacing: { after: 160, line: 276 },
  children: (Array.isArray(text) ? text : [new TextRun({ text, font: FONT, size: 22, color: "1F2937" })]),
  ...opts,
});

const bullet = (text, level = 0) => new Paragraph({
  numbering: { reference: "main-bullets", level },
  spacing: { after: 90, line: 268 },
  children: Array.isArray(text) ? text : [new TextRun({ text, font: FONT, size: 22, color: "1F2937" })],
});

const bold = (text, color = NAVY) => new TextRun({ text, bold: true, font: FONT, size: 22, color });
const italic = (text, color = SLATE) => new TextRun({ text, italics: true, font: FONT, size: 22, color });
const plain = (text, color = "1F2937") => new TextRun({ text, font: FONT, size: 22, color });

const caption = (text) => new Paragraph({
  spacing: { before: 100, after: 260 },
  alignment: AlignmentType.CENTER,
  children: [new TextRun({ text, italics: true, font: FONT, size: 18, color: SLATE })],
});

function figure(name, widthPx, heightPx, captionText) {
  return [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 160, after: 0 },
      children: [
        new ImageRun({
          data: img(name),
          transformation: { width: widthPx, height: heightPx },
          type: "png",
        }),
      ],
    }),
    caption(captionText),
  ];
}

// Pull-quote / stat callout box (shaded table used as a card, not a rule)
function statCard(bigText, bigColor, label) {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 4, color: "E2E8F0" },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: "E2E8F0" },
      left: { style: BorderStyle.SINGLE, size: 4, color: "E2E8F0" },
      right: { style: BorderStyle.SINGLE, size: 4, color: "E2E8F0" },
      insideHorizontal: { style: BorderStyle.NONE, size: 0, color: WHITE },
      insideVertical: { style: BorderStyle.NONE, size: 0, color: WHITE },
    },
    rows: [
      new TableRow({
        children: [
          new TableCell({
            shading: { type: ShadingType.CLEAR, fill: LIGHTGREY },
            margins: { top: 200, bottom: 200, left: 260, right: 260 },
            verticalAlign: VerticalAlign.CENTER,
            children: [
              new Paragraph({
                alignment: AlignmentType.LEFT,
                children: [new TextRun({ text: bigText, bold: true, font: FONT, size: 40, color: bigColor })],
              }),
              new Paragraph({
                alignment: AlignmentType.LEFT,
                spacing: { before: 40 },
                children: [new TextRun({ text: label, font: FONT, size: 19, color: SLATE })],
              }),
            ],
          }),
        ],
      }),
    ],
  });
}

function statRow(cards) {
  // cards: array of {big, color, label}
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: {
      top: { style: BorderStyle.NONE, size: 0, color: WHITE },
      bottom: { style: BorderStyle.NONE, size: 0, color: WHITE },
      left: { style: BorderStyle.NONE, size: 0, color: WHITE },
      right: { style: BorderStyle.NONE, size: 0, color: WHITE },
      insideHorizontal: { style: BorderStyle.NONE, size: 0, color: WHITE },
      insideVertical: { style: BorderStyle.NONE, size: 0, color: WHITE },
    },
    rows: [
      new TableRow({
        children: cards.map((c, i) => new TableCell({
          width: { size: 100 / cards.length, type: WidthType.PERCENTAGE },
          margins: { right: i < cards.length - 1 ? 160 : 0 },
          children: [statCardInner(c.big, c.color, c.label)],
        })),
      }),
    ],
  });
}

function statCardInner(bigText, bigColor, label) {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 4, color: "E2E8F0" },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: "E2E8F0" },
      left: { style: BorderStyle.SINGLE, size: 4, color: "E2E8F0" },
      right: { style: BorderStyle.SINGLE, size: 4, color: "E2E8F0" },
      insideHorizontal: { style: BorderStyle.NONE, size: 0, color: WHITE },
      insideVertical: { style: BorderStyle.NONE, size: 0, color: WHITE },
    },
    rows: [new TableRow({ children: [new TableCell({
      shading: { type: ShadingType.CLEAR, fill: LIGHTGREY },
      margins: { top: 180, bottom: 180, left: 200, right: 200 },
      children: [
        new Paragraph({ children: [new TextRun({ text: bigText, bold: true, font: FONT, size: 34, color: bigColor })] }),
        new Paragraph({ spacing: { before: 40 }, children: [new TextRun({ text: label, font: FONT, size: 17, color: SLATE })] }),
      ],
    })] })],
  });
}

// Insight card: colored left bar + number badge, via a 2-col table
function insightHeader(number, title, accent) {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    columnWidths: [700, 8800],
    borders: {
      top: { style: BorderStyle.NONE, size: 0, color: WHITE }, bottom: { style: BorderStyle.NONE, size: 0, color: WHITE },
      left: { style: BorderStyle.NONE, size: 0, color: WHITE }, right: { style: BorderStyle.NONE, size: 0, color: WHITE },
      insideHorizontal: { style: BorderStyle.NONE, size: 0, color: WHITE }, insideVertical: { style: BorderStyle.NONE, size: 0, color: WHITE },
    },
    rows: [new TableRow({ children: [
      new TableCell({
        width: { size: 700, type: WidthType.DXA },
        shading: { type: ShadingType.CLEAR, fill: accent },
        verticalAlign: VerticalAlign.CENTER,
        children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: String(number), bold: true, color: WHITE, font: FONT, size: 24 })] })],
      }),
      new TableCell({
        width: { size: 8800, type: WidthType.DXA },
        margins: { left: 200 },
        verticalAlign: VerticalAlign.CENTER,
        children: [new Paragraph({ children: [new TextRun({ text: title, bold: true, color: NAVY, font: FONT, size: 26 })] })],
      }),
    ] })],
  });
}

function simpleTable(headerRow, rows, widths) {
  const mkCell = (text, isHeader, w) => new TableCell({
    width: { size: w, type: WidthType.PERCENTAGE },
    shading: isHeader ? { type: ShadingType.CLEAR, fill: NAVY } : { type: ShadingType.CLEAR, fill: WHITE },
    margins: { top: 100, bottom: 100, left: 120, right: 120 },
    verticalAlign: VerticalAlign.CENTER,
    children: [new Paragraph({ children: [new TextRun({ text, font: FONT, size: 19, bold: isHeader, color: isHeader ? WHITE : "1F2937" })] })],
  });
  const bandedRows = rows.map((r, i) => new TableRow({
    children: r.map((cellText, ci) => new TableCell({
      width: { size: widths[ci], type: WidthType.PERCENTAGE },
      shading: { type: ShadingType.CLEAR, fill: i % 2 === 0 ? WHITE : "F8FAFC" },
      margins: { top: 90, bottom: 90, left: 120, right: 120 },
      children: [new Paragraph({ children: [new TextRun({ text: cellText, font: FONT, size: 19, color: "1F2937" })] })],
    })),
  }));
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 2, color: "CBD5E1" },
      bottom: { style: BorderStyle.SINGLE, size: 2, color: "CBD5E1" },
      left: { style: BorderStyle.SINGLE, size: 2, color: "CBD5E1" },
      right: { style: BorderStyle.SINGLE, size: 2, color: "CBD5E1" },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: "E2E8F0" },
      insideVertical: { style: BorderStyle.SINGLE, size: 2, color: "E2E8F0" },
    },
    rows: [
      new TableRow({ children: headerRow.map((t, i) => mkCell(t, true, widths[i])) }),
      ...bandedRows,
    ],
  });
}

// ---------- COVER PAGE ----------
const coverChildren = [
  new Paragraph({ spacing: { before: 1400 }, children: [] }),
  new Paragraph({
    alignment: AlignmentType.LEFT,
    children: [new TextRun({ text: "SELAM ANALYTICS  ·  10 ACADEMY WEEK 11", font: FONT, size: 20, bold: true, color: BLUE, characterSpacing: 20 })],
  }),
  new Paragraph({ spacing: { before: 260 }, children: [
    new TextRun({ text: "Ethiopia Financial Inclusion", font: FONT, size: 60, bold: true, color: NAVY }),
  ]}),
  new Paragraph({ spacing: { after: 200 }, children: [
    new TextRun({ text: "Forecasting Project", font: FONT, size: 60, bold: true, color: BLUE }),
  ]}),
  new Paragraph({
    spacing: { before: 200, after: 700 },
    children: [new TextRun({ text: "Interim Report — Data Enrichment & Exploratory Data Analysis", font: FONT, size: 28, color: SLATE, italics: true })],
  }),
  new Paragraph({
    border: { top: { style: BorderStyle.SINGLE, size: 8, color: BLUE, space: 12 } },
    spacing: { before: 200 },
    children: [],
  }),
  new Paragraph({ spacing: { before: 260 }, children: [bold("Prepared by:  ", SLATE), plain("Rahmi", NAVY)] }),
  new Paragraph({ spacing: { before: 80 }, children: [bold("Date:  ", SLATE), plain("19 July 2026", NAVY)] }),
  new Paragraph({ spacing: { before: 80 }, children: [bold("Covers:  ", SLATE), plain("Task 1 (Data Exploration & Enrichment) and Task 2 (Exploratory Data Analysis)", NAVY)] }),
  new Paragraph({ spacing: { before: 80, after: 700 }, children: [bold("Submission:  ", SLATE), plain("Interim Submission — 19 July 2026, 20:00 UTC", NAVY)] }),
  statRow([
    { big: "58", color: BLUE, label: "Main dataset records\n(43 starter + 15 new)" },
    { big: "18", color: GREEN, label: "Modeled event→indicator\nimpact links" },
    { big: "49%", color: PINK, label: "Ethiopians with a financial\naccount, 2024 (Findex)" },
  ]),
  new Paragraph({ children: [new PageBreak()] }),
];

// ---------- EXEC SUMMARY ----------
const execSummary = [
  h1("Executive Summary"),
  body([
    plain("Ethiopia's mobile money boom tells one story — "),
    bold("Telebirr alone has more than 54 million registered users"),
    plain(". The World Bank's Global Findex survey tells another: only "),
    bold("49% of Ethiopian adults have a financial account", PINK),
    plain(", barely up from 46% three years earlier. This report reconciles the two stories."),
  ]),
  body([
    plain("Working from Selam Analytics' starter dataset, we "),
    bold("enriched it with 15 new, independently-sourced records"),
    plain(" — pulling from the IMF, World Bank, UNESCO, GSMA, and the National Bank of Ethiopia — and ran a full exploratory analysis to surface what's really driving (and stalling) financial inclusion. The headline finding: "),
    bold("Ethiopia has a usage problem hiding inside an access story", BLUE),
    plain(". Sign-ups are exploding; genuine, active use is not keeping pace — and neither is the infrastructure that first-time users need to get onboarded at all."),
  ]),
  new Paragraph({ spacing: { before: 120, after: 300 }, children: [
    new TextRun({ text: "This document walks through what we added to the dataset and why, five key insights from the analysis, how cataloged policy/product events line up against the data, and the limitations we're carrying into the forecasting phase.", font: FONT, size: 22, italics: true, color: SLATE }),
  ]}),
  new Paragraph({ children: [new PageBreak()] }),
];

// ---------- SECTION 1: ENRICHMENT ----------
const enrichmentSection = [
  h1("Data Enrichment Summary", "1"),
  body([
    plain("Task 1 grew the dataset from 43 to "),
    bold("58 main records"),
    plain(" and from 14 to "),
    bold("18 impact links"),
    plain(", with every addition traceable to a real, cited source — no figure was estimated or invented. Nothing in the original 43 records needed correction."),
  ]),
  statRow([
    { big: "+12", color: BLUE, label: "New observations\n(real, sourced data points)" },
    { big: "+2", color: GOLD, label: "New events\n(policy & regulatory)" },
    { big: "+4", color: GREEN, label: "New impact links\n(event → indicator)" },
  ]),
  new Paragraph({ spacing: { before: 300 }, children: [] }),
  h2("What we added, and why"),
  simpleTable(
    ["Category", "What we added", "Why it matters"],
    [
      ["Supply-side access", "Bank branch density, ATM density, active-account & active-agent shares", "Real Access/Usage predictors beyond survey-only data points"],
      ["Enabling infrastructure", "Electricity access, adult literacy, internet penetration", "Explains why Access can stall even as telecom products launch"],
      ["Gender & digital skill", "Usage-side gender gap, mobile-money skill gap (male & female)", "Deepens the existing Access-only gender gap with a usage and capability lens"],
      ["Market-nuance evidence", "Sector-wide registered-vs-active mobile money figures", "Tests the guide's warning that headline sign-up numbers overstate real usage"],
      ["New events", "NBE Proclamation 1282/2023 (opened market to foreign providers); Directive NPS/10/2025 (interoperability mandate)", "Fills in legal preconditions for two already-catalogued events"],
      ["New impact links", "4 links, incl. proclamation → M-Pesa entry, and existing NFIS-II event → new skill-gap indicator", "Makes an implicit causal chain explicit and traceable"],
    ],
    [22, 40, 38]
  ),
  new Paragraph({ spacing: { before: 260, after: 160 }, children: [
    new TextRun({ text: "All additions came from the IMF Financial Access Survey, World Bank/ESMAP, UNESCO, DataReportal (GSMA Intelligence), and the National Bank of Ethiopia's own NDPS 2.0 strategy page. Two candidate additions — a newer unsourced literacy estimate and a GSMA Mobile Connectivity Index score — were deliberately ", font: FONT, size: 21, color: SLATE }),
    new TextRun({ text: "rejected", font: FONT, size: 21, color: PINK, bold: true }),
    new TextRun({ text: " for lack of a traceable primary source. Full citations, exact quotes, and confidence ratings for every record live in data_enrichment_log.md.", font: FONT, size: 21, color: SLATE }),
  ]}),
  new Paragraph({ children: [new PageBreak()] }),
];

// ---------- SECTION 2: KEY INSIGHTS ----------
const insightsIntro = [
  h1("Key Insights from the Exploratory Analysis", "2"),
  body("Five insights stood out from the enriched dataset — each backed by a supporting visualization built directly from the data."),
];

const insight1 = [
  insightHeader(1, "Account ownership growth slammed the brakes after 2021", BLUE),
  new Paragraph({ spacing: { before: 160 }, children: [
    plain("Growth of "), bold("+13pp"), plain(" (2014-17) and "), bold("+11pp"), plain(" (2017-21) collapsed to just "),
    bold("+3pp over 2021-24", PINK), plain(" (46% → 49%) — despite Telebirr, Safaricom, and the NFIS‑II strategy all launching in that exact window."),
  ]}),
  ...figure("03_access_trajectory.png", 460, 279, "Figure 1. Account ownership rate, 2014-2024, with the NFIS-II 2025 target overlaid."),
  ...figure("04_growth_rates.png", 400, 248, "Figure 2. Growth between Findex survey waves — the 2021-24 bar tells the story."),
  body([
    bold("Why: "), plain("mobile-money adoption mostly deepened engagement among people who could "),
    italic("already"), plain(" access formal services — it didn't reach the harder-to-onboard rural, illiterate, or off-grid population nearly as fast."),
  ]),
];

const insight2 = [
  insightHeader(2, "139.5 million sign-ups, but only 15% are actually active", GREEN),
  new Paragraph({ spacing: { before: 160 }, children: [
    plain("Sector-wide, Ethiopia has "), bold("~139.5 million registered mobile money accounts", GREEN),
    plain(" (NBE) — more than the entire adult population. But the regulator reports only "),
    bold("~15% of accounts and ~25% of agents are active", PINK), plain(". Compare that to Safaricom's own "),
    bold("self-reported 66% active rate"), plain(" for M-Pesa alone — the two numbers are measuring different things, and conflating them would badly distort any usage forecast."),
  ]}),
  ...figure("07_registered_vs_active.png", 420, 288, "Figure 3. Registered vs. active mobile money accounts — sector-wide (NBE) vs. one operator's self-report."),
];

const insight3 = [
  insightHeader(3, "The gender gap is wider at the door than it is once inside", PINK),
  new Paragraph({ spacing: { before: 160 }, children: [
    plain("The "), bold("Access gender gap sits at 18-20 percentage points"), plain(", roughly "), bold("double the Usage gender gap of 10pp"),
    plain(". In other words: once a woman has an account, her usage looks close to parity with men — the bigger barrier is getting the account in the first place."),
  ]}),
  ...figure("05_gender_analysis.png", 560, 178, "Figure 4. Account ownership by gender, the access-vs-usage gap, and mobile-money digital-skill gaps."),
  body([
    plain("Notably, the digital-skill data shows a "), bold("majority of both genders"), plain(" — not just women — lack mobile-money skills (66% female, 60% male), suggesting general digital literacy is a bigger lever than gender-targeted programs alone."),
  ]),
];

const insight4 = [
  insightHeader(4, "Networks got faster; the ground underneath them didn't", GOLD),
  new Paragraph({ spacing: { before: 160 }, children: [
    plain("4G coverage nearly "), bold("doubled in two years"), plain(" (37.5% → 70.8%) — comfortably outpacing account-ownership growth over the same window. Meanwhile "),
    bold("electricity access sits at just 55.4%"), plain(" and "), bold("adult literacy at roughly 52%"),
    plain(". Connectivity is no longer the binding constraint on Access; power and literacy plausibly are."),
  ]}),
  ...figure("08_infrastructure.png", 560, 213, "Figure 5. 4G coverage growth alongside the slower-moving enabling indicators."),
];

const insight5 = [
  insightHeader(5, "This is a genuinely sparse dataset — and that shapes everything downstream", NAVY),
  new Paragraph({ spacing: { before: 160 }, children: [
    plain("Roughly "), bold("85% of indicators have only 1-2 observed years"), plain(". That rules out conventional trend/seasonality forecasting and points toward the "),
    bold("event-driven, intervention-style regression"), plain(" approach the challenge brief itself suggests, rather than naive extrapolation."),
  ]}),
  ...figure("02_temporal_coverage.png", 420, 331, "Figure 6. Temporal coverage heatmap — most indicator rows are mostly empty."),
  new Paragraph({ children: [new PageBreak()] }),
];

// ---------- SECTION 3: EVENT-INDICATOR RELATIONSHIPS ----------
const eventSection = [
  h1("Preliminary Observations on Event-Indicator Relationships", "3"),
  body("Overlaying the cataloged events onto the trend lines lets us sanity-check the dataset's modeled impact_link relationships against what the raw numbers actually show."),
  ...figure("09_event_timeline.png", 560, 213, "Figure 7. Timeline of all cataloged events, 2021-2025, colored by category."),
  ...figure("10_events_overlay.png", 460, 249, "Figure 8. Telebirr users and Mobile Money Account Rate with event dates overlaid."),
  h2("What lines up, and what doesn't"),
  bullet([bold("Telebirr (May 2021) → Usage, fast: "), plain("registered users grew explosively right after launch — consistent with the dataset's existing impact_link (direct, high magnitude, 3-month lag).")]),
  bullet([bold("Telebirr → Access, weak: "), plain("the Findex-measured Mobile Money Account rate only reached 9.45% by 2024 — usage-product growth did not translate proportionally into Findex account ownership.")]),
  bullet([bold("Safaricom entry (Aug 2022) → 4G coverage: "), plain("timing lines up with the acceleration in 4G population coverage, matching the starter dataset's own impact_link.")]),
  bullet([bold("New: Proclamation 1282/2023 (Feb 2023) → M-Pesa launch (Aug 2023): "), plain("a clean ~6-month lag between the legal market-opening and the actual product launch, now made explicit in our enrichment.")]),
  bullet([bold("M-Pesa entry (Aug 2023) → too recent for the 2024 Findex wave: "), plain("its effect likely hasn't \"landed\" in survey data yet — a lag the forecasting model will need to handle explicitly.")]),
  new Paragraph({
    spacing: { before: 260, after: 160 },
    shading: { type: ShadingType.CLEAR, fill: LIGHT },
    border: { left: { style: BorderStyle.SINGLE, size: 24, color: BLUE, space: 8 } },
    children: [new TextRun({ text: "  A caveat worth stating plainly: statistical correlation on this dataset is unreliable — most indicator pairs share only 1-2 overlapping years, so any correlation coefficient is close to definitionally ±1. The literature/expert-based impact_link table (18 records) is a more trustworthy signal at this stage than raw statistical correlation.", font: FONT, size: 21, italics: true, color: NAVY })],
  }),
  new Paragraph({ children: [new PageBreak()] }),
];

// ---------- SECTION 4: LIMITATIONS ----------
const limitationsSection = [
  h1("Data Limitations Identified", "4"),
  body("Being upfront about what this dataset can't yet tell us — so the forecasting phase carries appropriately wide uncertainty bounds, not false precision."),
  bullet([bold("Sparse time series: "), plain("nearly all indicators have only 1-2 observed years, ruling out conventional trend decomposition.")]),
  bullet([bold("Zero coverage on three pillars: "), plain("QUALITY, TRUST, and DEPTH have no observations at all, even after enrichment.")]),
  bullet([bold("Stale literacy figure: "), plain("the only verifiable adult literacy rate (51.8%) dates to 2017; newer unsourced estimates exist but couldn't be traced to a primary release.")]),
  bullet([bold("No urban/rural Access split: "), plain("only Usage has a published rural-urban gap (from NBE); the equivalent Access breakdown would require gated Findex microdata.")]),
  bullet([bold("Definitional inconsistency in \"active user\": "), plain("operator self-reports and regulator sector-wide figures don't measure the same thing, and this wasn't flagged anywhere in the original dataset.")]),
  new Paragraph({ spacing: { before: 300 }, children: [] }),
  h2("Hypotheses carried into impact modeling"),
  bullet("H1 — Enabling infrastructure (electricity, literacy) will out-predict telecom-launch events for Access; telecom-launch events will out-predict infrastructure for Usage."),
  bullet("H2 — A consistent, regulator-sourced \"active account\" definition will produce a materially lower, more realistic Usage forecast than naive extrapolation of registered-account growth."),
  bullet("H3 — The Access gender gap will close more slowly than the Usage gender gap over 2025-2027, since it's tied to slower-moving structural enablers rather than product adoption."),
];

// ---------- FOOTER / closing ----------
const closing = [
  new Paragraph({ children: [new PageBreak()] }),
  h1("Deliverables in This Submission"),
  bullet("ethiopia_fi_unified_data_enriched.xlsx (+ .csv) — the enriched dataset"),
  bullet("data_enrichment_log.md — full documentation of every addition, with citations"),
  bullet("01_eda.ipynb — the executed EDA notebook, all outputs embedded"),
  bullet("reports/figures/ — 11 exported chart images"),
  bullet("This report (interim_report.docx)"),
  bullet("Git history: main branch with task-1 and task-2 merged in, ready to push and open as PRs"),
];

const doc = new Document({
  styles: {
    default: {
      document: { run: { font: FONT, size: 22, color: "1F2937" } },
    },
  },
  numbering: {
    config: [{
      reference: "main-bullets",
      levels: [
        { level: 0, format: LevelFormat.BULLET, text: "●", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 260 } } }, },
        { level: 1, format: LevelFormat.BULLET, text: "○", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 260 } } }, },
      ],
    }],
  },
  sections: [
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1000, bottom: 1000, left: 1100, right: 1100 },
        },
        titlePage: true,
      },
      headers: {
        default: new Header({ children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "E2E8F0", space: 4 } },
          children: [new TextRun({ text: "Ethiopia Financial Inclusion Forecasting  ·  Interim Report", font: FONT, size: 16, color: SLATE })],
        })] }),
        first: new Header({ children: [new Paragraph({ children: [] })] }),
      },
      footers: {
        default: new Footer({ children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "Selam Analytics  ·  10 Academy Week 11  ·  Page ", font: FONT, size: 16, color: SLATE }),
            new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: SLATE }),
            new TextRun({ text: " of ", font: FONT, size: 16, color: SLATE }),
            new TextRun({ children: [PageNumber.TOTAL_PAGES], font: FONT, size: 16, color: SLATE }),
          ],
        })] }),
        first: new Footer({ children: [new Paragraph({ children: [] })] }),
      },
      children: [
        ...coverChildren,
        ...execSummary,
        ...enrichmentSection,
        ...insightsIntro,
        ...insight1,
        ...insight2,
        ...insight3,
        ...insight4,
        ...insight5,
        ...eventSection,
        ...limitationsSection,
        ...closing,
      ],
    },
  ],
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(path.join(__dirname, "interim_report.docx"), buffer);
  console.log("Wrote interim_report.docx");
});
