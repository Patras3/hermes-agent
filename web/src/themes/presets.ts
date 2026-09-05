import type { DashboardTheme, ThemeTypography, ThemeLayout } from "./types";

/**
 * Built-in dashboard themes.
 *
 * Each theme defines its own palette, typography, and layout so switching
 * themes produces visible changes beyond just color — fonts, density, and
 * corner-radius all shift to match the theme's personality.
 *
 * Theme names must stay in sync with the backend's
 * `_BUILTIN_DASHBOARD_THEMES` list in `hermes_cli/web_server.py`.
 */

// ---------------------------------------------------------------------------
// Shared typography / layout presets
// ---------------------------------------------------------------------------

/** Default system stack — neutral, safe fallback for every platform. */
const SYSTEM_SANS =
  'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif';
const SYSTEM_MONO =
  'ui-monospace, "SF Mono", "Cascadia Mono", Menlo, Consolas, monospace';

const DEFAULT_TYPOGRAPHY: ThemeTypography = {
  fontSans: SYSTEM_SANS,
  fontMono: SYSTEM_MONO,
  baseSize: "15px",
  lineHeight: "1.55",
  letterSpacing: "0",
};

const DEFAULT_LAYOUT: ThemeLayout = {
  radius: "0.5rem",
  density: "comfortable",
};

// ---------------------------------------------------------------------------
// Themes
// ---------------------------------------------------------------------------

export const defaultTheme: DashboardTheme = {
  name: "default",
  label: "Hermes Teal",
  description: "Classic dark teal — the canonical Hermes look",
  palette: {
    background: { hex: "#041c1c", alpha: 1 },
    midground: { hex: "#ffe6cb", alpha: 1 },
    foreground: { hex: "#ffffff", alpha: 0 },
    warmGlow: "rgba(255, 189, 56, 0.35)",
    noiseOpacity: 1,
  },
  typography: DEFAULT_TYPOGRAPHY,
  layout: DEFAULT_LAYOUT,
};

export const midnightTheme: DashboardTheme = {
  name: "midnight",
  label: "Midnight",
  description: "Deep blue-violet with cool accents",
  palette: {
    background: { hex: "#0a0a1f", alpha: 1 },
    midground: { hex: "#d4c8ff", alpha: 1 },
    foreground: { hex: "#ffffff", alpha: 0 },
    warmGlow: "rgba(167, 139, 250, 0.32)",
    noiseOpacity: 0.8,
  },
  typography: {
    ...DEFAULT_TYPOGRAPHY,
    fontSans: `"Inter", ${SYSTEM_SANS}`,
    fontMono: `"JetBrains Mono", ${SYSTEM_MONO}`,
    fontUrl:
      "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap",
    letterSpacing: "-0.005em",
  },
  layout: {
    ...DEFAULT_LAYOUT,
    radius: "0.75rem",
  },
};

export const emberTheme: DashboardTheme = {
  name: "ember",
  label: "Ember",
  description: "Warm crimson and bronze — forge vibes",
  palette: {
    background: { hex: "#1a0a06", alpha: 1 },
    midground: { hex: "#ffd8b0", alpha: 1 },
    foreground: { hex: "#ffffff", alpha: 0 },
    warmGlow: "rgba(249, 115, 22, 0.38)",
    noiseOpacity: 1,
  },
  typography: {
    ...DEFAULT_TYPOGRAPHY,
    fontSans: `"Spectral", Georgia, "Times New Roman", serif`,
    fontMono: `"IBM Plex Mono", ${SYSTEM_MONO}`,
    fontUrl:
      "https://fonts.googleapis.com/css2?family=Spectral:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;700&display=swap",
  },
  layout: {
    ...DEFAULT_LAYOUT,
    radius: "0.25rem",
  },
  colorOverrides: {
    destructive: "#c92d0f",
    warning: "#f97316",
  },
};

export const monoTheme: DashboardTheme = {
  name: "mono",
  label: "Mono",
  description: "Clean grayscale — minimal and focused",
  palette: {
    background: { hex: "#0e0e0e", alpha: 1 },
    midground: { hex: "#eaeaea", alpha: 1 },
    foreground: { hex: "#ffffff", alpha: 0 },
    warmGlow: "rgba(255, 255, 255, 0.1)",
    noiseOpacity: 0.6,
  },
  typography: {
    ...DEFAULT_TYPOGRAPHY,
    fontSans: `"IBM Plex Sans", ${SYSTEM_SANS}`,
    fontMono: `"IBM Plex Mono", ${SYSTEM_MONO}`,
    fontUrl:
      "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap",
  },
  layout: {
    ...DEFAULT_LAYOUT,
    radius: "0",
  },
};

export const cyberpunkTheme: DashboardTheme = {
  name: "cyberpunk",
  label: "Cyberpunk",
  description: "Neon green on black — matrix terminal",
  palette: {
    background: { hex: "#040608", alpha: 1 },
    midground: { hex: "#9bffcf", alpha: 1 },
    foreground: { hex: "#ffffff", alpha: 0 },
    warmGlow: "rgba(0, 255, 136, 0.22)",
    noiseOpacity: 1.2,
  },
  typography: {
    ...DEFAULT_TYPOGRAPHY,
    fontSans: `"Share Tech Mono", "JetBrains Mono", ${SYSTEM_MONO}`,
    fontMono: `"Share Tech Mono", "JetBrains Mono", ${SYSTEM_MONO}`,
    fontUrl:
      "https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=JetBrains+Mono:wght@400;700&display=swap",
  },
  layout: {
    ...DEFAULT_LAYOUT,
    radius: "0",
  },
  colorOverrides: {
    success: "#00ff88",
    warning: "#ffd700",
    destructive: "#ff0055",
  },
};

export const roseTheme: DashboardTheme = {
  name: "rose",
  label: "Rosé",
  description: "Soft pink and warm ivory — easy on the eyes",
  palette: {
    background: { hex: "#1a0f15", alpha: 1 },
    midground: { hex: "#ffd4e1", alpha: 1 },
    foreground: { hex: "#ffffff", alpha: 0 },
    warmGlow: "rgba(249, 168, 212, 0.3)",
    noiseOpacity: 0.9,
  },
  typography: {
    ...DEFAULT_TYPOGRAPHY,
    fontSans: `"Fraunces", Georgia, serif`,
    fontMono: `"DM Mono", ${SYSTEM_MONO}`,
    fontUrl:
      "https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=DM+Mono:wght@400;500&display=swap",
  },
  layout: {
    ...DEFAULT_LAYOUT,
    radius: "1rem",
  },
};

export const auroraTheme: DashboardTheme = {
  name: "aurora",
  label: "Aurora",
  description: "Premium glassmorphic dark theme with purple, pink, and cyan glow",
  palette: {
    background: { hex: "#0a0a0b", alpha: 1 },
    midground: { hex: "#f6f7ff", alpha: 1 },
    foreground: { hex: "#64c8ff", alpha: 0.35 },
    warmGlow: "rgba(255, 119, 169, 0.36)",
    noiseOpacity: 0.55,
  },
  typography: {
    ...DEFAULT_TYPOGRAPHY,
    fontSans: `"Inter", ${SYSTEM_SANS}`,
    fontMono: `"JetBrains Mono", ${SYSTEM_MONO}`,
    fontUrl:
      "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap",
    baseSize: "14px",
    lineHeight: "1.5",
    letterSpacing: "-0.005em",
  },
  layout: {
    ...DEFAULT_LAYOUT,
    radius: "1rem",
    density: "comfortable",
  },
  assets: {
    bg:
      "radial-gradient(ellipse at top left, rgba(120, 119, 198, 0.32), transparent 50%), radial-gradient(ellipse at bottom right, rgba(255, 119, 168, 0.32), transparent 50%), radial-gradient(ellipse at center, rgba(100, 200, 255, 0.22), transparent 50%)",
  },
  componentStyles: {
    card: {
      background:
        "linear-gradient(135deg, rgba(255,255,255,0.075), rgba(255,255,255,0.035))",
      boxShadow:
        "0 8px 32px rgba(0,0,0,0.30), 0 0 0 1px rgba(255,255,255,0.10) inset",
    },
    header: {
      background: "rgba(10,10,11,0.78)",
    },
    sidebar: {
      background: "rgba(10,10,11,0.82)",
    },
    backdrop: {
      fillerBlendMode: "screen",
      fillerOpacity: "0.78",
      backgroundSize: "200% 200%",
      backgroundPosition: "center",
    },
  },
  colorOverrides: {
    card: "#15151a",
    cardForeground: "#ffffff",
    popover: "#111116",
    popoverForeground: "#ffffff",
    primary: "#667eea",
    primaryForeground: "#ffffff",
    secondary: "#ff77a9",
    secondaryForeground: "#ffffff",
    muted: "#1f2028",
    mutedForeground: "#b8b8c8",
    accent: "#232437",
    accentForeground: "#ffffff",
    destructive: "#ff7675",
    destructiveForeground: "#ffffff",
    success: "#00b894",
    warning: "#fdcb6e",
    border: "#2a2c3a",
    input: "#3a3d52",
    ring: "#667eea",
  },
  customCSS: `
@keyframes hermes-aurora-drift {
  0%, 100% { transform: rotate(0deg) scale(1); opacity: 0.72; }
  33% { transform: rotate(60deg) scale(1.08); opacity: 0.92; }
  66% { transform: rotate(-60deg) scale(0.95); opacity: 0.58; }
}

:root {
  --selection-bg: rgba(102, 126, 234, 0.45);
  --aurora-select-trigger-bg: rgba(255, 255, 255, 0.06);
  --aurora-select-trigger-bg-hover: rgba(255, 255, 255, 0.09);
  --aurora-select-trigger-border: rgba(255, 255, 255, 0.16);
  --aurora-select-trigger-border-hover: rgba(102, 126, 234, 0.45);
  --aurora-select-text: rgba(255, 255, 255, 0.92);
  --aurora-select-placeholder: rgba(255, 255, 255, 0.46);
  --aurora-select-list-bg: rgba(17, 17, 22, 0.98);
  --aurora-select-list-border: rgba(102, 126, 234, 0.35);
  --aurora-select-option-text: rgba(255, 255, 255, 0.76);
  --aurora-select-option-active-bg: linear-gradient(135deg, rgba(102, 126, 234, 0.20), rgba(255, 119, 169, 0.16));
  --aurora-select-option-active-text: #ffffff;
  --aurora-select-shadow: 0 16px 40px rgba(0, 0, 0, 0.42), 0 0 0 1px rgba(255, 255, 255, 0.08) inset;
}

::selection {
  background: var(--selection-bg);
  color: #ffffff;
}

body::before {
  content: "";
  position: fixed;
  inset: -50%;
  z-index: 1;
  pointer-events: none;
  background:
    radial-gradient(ellipse at top left, rgba(120, 119, 198, 0.28), transparent 50%),
    radial-gradient(ellipse at bottom right, rgba(255, 119, 168, 0.28), transparent 50%),
    radial-gradient(ellipse at center, rgba(100, 200, 255, 0.18), transparent 50%);
  mix-blend-mode: screen;
  animation: hermes-aurora-drift 30s ease infinite;
}

#root [role="combobox"] {
  background: var(--aurora-select-trigger-bg) !important;
  border-color: var(--aurora-select-trigger-border) !important;
  color: var(--aurora-select-text) !important;
  box-shadow: 0 0 0 1px rgba(102, 126, 234, 0.08) inset;
}

#root [role="combobox"] span,
#root [role="combobox"] svg {
  color: var(--aurora-select-text) !important;
}

#root [role="combobox"] span[class*="text-midground/50"] {
  color: var(--aurora-select-placeholder) !important;
}

#root [role="combobox"]:hover,
#root [role="combobox"][aria-expanded="true"] {
  background: var(--aurora-select-trigger-bg-hover) !important;
  border-color: var(--aurora-select-trigger-border-hover) !important;
}

#root [role="listbox"] {
  background: var(--aurora-select-list-bg) !important;
  color: var(--aurora-select-option-text) !important;
  border-color: var(--aurora-select-list-border) !important;
  box-shadow: var(--aurora-select-shadow) !important;
  backdrop-filter: blur(18px);
}

#root [role="option"] {
  color: var(--aurora-select-option-text) !important;
}

#root [role="option"]:hover,
#root [role="option"][aria-selected="true"] {
  background: var(--aurora-select-option-active-bg) !important;
  color: var(--aurora-select-option-active-text) !important;
}

#root input:not([type="checkbox"]),
#root textarea {
  background: rgba(255, 255, 255, 0.055) !important;
  border-color: rgba(255, 255, 255, 0.14) !important;
  color: #ffffff !important;
}

#root input:not([type="checkbox"])::placeholder,
#root textarea::placeholder {
  color: rgba(255, 255, 255, 0.34) !important;
}

#root input:not([type="checkbox"]):focus,
#root textarea:focus {
  border-color: rgba(102, 126, 234, 0.55) !important;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.12) !important;
}
`,
};

/** Light mode — vivid Nous-blue accents on a cream canvas. */
export const nousBlueTheme: DashboardTheme = {
  name: "nous-blue",
  label: "Nous Blue",
  description: "Light mode — vivid Nous-blue accents on cream canvas",
  palette: {
    background: { hex: "#E8F2FD", alpha: 1 },
    midground: { hex: "#0053FD", alpha: 1 },
    foreground: { hex: "#170d02", alpha: 0 },
    warmGlow: "rgba(0, 83, 253, 0.12)",
    noiseOpacity: 0,
  },
  typography: DEFAULT_TYPOGRAPHY,
  layout: DEFAULT_LAYOUT,
  terminalBackground: "#f5f8fc",
  terminalForeground: "#170d02",
  seriesColors: {
    inputTokenAccent: "#001934",
    outputTokenAccent: "#0053fd",
  },
  swatchColors: ["#170d02", "#0053FD", "#E8F2FD"],
};

/**
 * Same look as ``defaultTheme`` but with a larger root font size, looser
 * line-height, and ``spacious`` density so every rem-based size in the
 * dashboard scales up. For users who find the default 15px UI too dense.
 */
export const defaultLargeTheme: DashboardTheme = {
  name: "default-large",
  label: "Hermes Teal (Large)",
  description: "Hermes Teal with bigger fonts and roomier spacing",
  palette: defaultTheme.palette,
  typography: {
    ...DEFAULT_TYPOGRAPHY,
    baseSize: "18px",
    lineHeight: "1.65",
  },
  layout: {
    ...DEFAULT_LAYOUT,
    density: "spacious",
  },
};

export const BUILTIN_THEMES: Record<string, DashboardTheme> = {
  default: defaultTheme,
  "default-large": defaultLargeTheme,
  "nous-blue": nousBlueTheme,
  midnight: midnightTheme,
  ember: emberTheme,
  mono: monoTheme,
  cyberpunk: cyberpunkTheme,
  rose: roseTheme,
  aurora: auroraTheme,
};
