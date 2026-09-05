import { describe, expect, it } from "vitest";

import { auroraTheme, BUILTIN_THEMES } from "./presets";

describe("Aurora dashboard theme", () => {
  it("is available as a built-in glassmorphic theme", () => {
    expect(BUILTIN_THEMES.aurora).toBe(auroraTheme);
    expect(auroraTheme.name).toBe("aurora");
    expect(auroraTheme.assets?.bg).toContain("radial-gradient");
    expect(auroraTheme.customCSS).toContain("hermes-aurora-drift");
  });
});
