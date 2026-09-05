import { contrastRatio, THEME_PRESET_PALETTES, type ThemePresetPalette } from "@hermes/shared";
import { describe, expect, it } from "vitest";

import { auroraTheme, BUILTIN_THEMES, webPresetFromShared } from "./presets";

// Every preset the dashboard shares with the desktop must render the shared
// table's palette and keep its accent legible against the canvas.
describe("dashboard presets derive from the shared palette table", () => {
  const shared = Object.keys(BUILTIN_THEMES).filter(
    (name): name is keyof typeof THEME_PRESET_PALETTES => name in THEME_PRESET_PALETTES,
  );

  it("covers the presets both surfaces ship", () => {
    expect(shared).toEqual(expect.arrayContaining(["cyberpunk", "ember", "midnight", "mono"]));
  });

  it.each(shared)("%s: canvas equals the shared background and the accent reads on it", (name) => {
    const preset: ThemePresetPalette = THEME_PRESET_PALETTES[name];
    const derived = webPresetFromShared(preset);
    const palette = BUILTIN_THEMES[name].palette;

    expect(palette.background.hex).toBe((preset.darkColors ?? preset.colors).background);
    expect(palette.midground.hex).toBe(derived.midground.hex);
    expect(contrastRatio(palette.midground.hex, palette.background.hex)).toBeGreaterThanOrEqual(3);
  });
});

describe("Aurora dashboard theme", () => {
  it("is available as a built-in glassmorphic theme", () => {
    expect(BUILTIN_THEMES.aurora).toBe(auroraTheme);
    expect(auroraTheme.name).toBe("aurora");
    expect(auroraTheme.assets?.bg).toContain("radial-gradient");
    expect(auroraTheme.customCSS).toContain("hermes-aurora-drift");
  });
});
