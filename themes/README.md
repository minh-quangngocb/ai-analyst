# Themes

The `themes/` directory controls the visual identity of all AI Analyst outputs: charts, slide decks, and exports.

- **`_base.yaml`** defines the default theme (colors, typography, chart settings, presentation defaults). All brand themes inherit from this file and override only what they need.
- **`coolblue.css`** is the Marp CSS theme for slide decks (Coolblue brand).

To create a brand theme, copy `_base.yaml` to `{org-name}.yaml` and override the values you want to change. Unspecified values fall back to `_base.yaml` defaults.

See `docs/theming.md` for the full customization guide.
