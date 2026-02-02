---
name: remix-lingui
description: "Integrate Lingui.js i18n into a Remix v2 / React Router v7 app with full SSR support, locale detection, and the macro system. Use when the user asks to: (1) add i18n or internationalization to a Remix app, (2) integrate Lingui with Remix, (3) set up translations in a Remix/React Router v7 project, (4) add multi-language support to a Remix app. Triggers on phrases like 'add lingui', 'add i18n', 'internationalization', 'translations', 'multi-language' in the context of Remix or React Router v7."
---

# Remix + Lingui Integration

Integrate Lingui.js v5+ into a Remix v2 / React Router v7 Vite-based app with SSR, cookie-based locale detection, and the macro system.

## Quick Reference

- **Packages (runtime):** `@lingui/core`, `@lingui/react`
- **Packages (dev):** `@lingui/cli`, `@lingui/vite-plugin`, `@lingui/babel-plugin-lingui-macro`, `@babel/preset-typescript`, `vite-plugin-babel`
- **Config files:** `lingui.config.ts`, `vite.config.ts`
- **Catalog format:** PO (`.po` files)

## Integration Workflow

1. Install dependencies
2. Create `lingui.config.ts`
3. Update `vite.config.ts` with Babel + Lingui plugins
4. Create `app/lib/i18n.ts` (locale utilities + catalog loader)
5. Create `app/locales/lingui.d.ts` (PO type declaration)
6. Update `app/entry.client.tsx` (load catalog before hydration)
7. Update `app/root.tsx` (loader detects locale, Layout wraps with `I18nProvider`)
8. Add locale switching route (`app/routes/set-locale.ts`)
9. Update `app/routes.ts` to include the set-locale route
10. Run `lingui extract` to generate initial catalog files
11. Add build scripts to `package.json`

For detailed file contents and patterns, read [references/setup.md](references/setup.md).

## Translation Patterns

Two main approaches — choose based on context:

### `Trans` component — for JSX content

```tsx
import { Trans } from "@lingui/react/macro";

<h1><Trans>Hello, World</Trans></h1>
<p><Trans>Welcome, <strong>{name}</strong>!</Trans></p>
```

### `msg` macro + `i18n._()` — for data structures and non-JSX

```tsx
import { msg } from "@lingui/core/macro";
import { useLingui } from "@lingui/react";

const navLinks = [
  { href: "/about", label: msg`About` },
  { href: "/contact", label: msg`Contact` },
];

function Nav() {
  const { i18n } = useLingui();
  return navLinks.map(link => (
    <a key={link.href} href={link.href}>{i18n._(link.label)}</a>
  ));
}
```

### Plurals

```tsx
import { Plural } from "@lingui/react/macro";

<Plural value={count} one="# item" other="# items" />
```

For the complete macro reference and advanced patterns, read [references/patterns.md](references/patterns.md).

## Extraction & Build

```bash
# Extract messages from source code into .po files
npx lingui extract

# Compile .po files (done automatically by vite plugin, but needed before production build)
npx lingui compile

# Recommended package.json scripts
# "build": "lingui compile && react-router build"
# "extract": "lingui extract"
```

## Key Architecture Decisions

- **Cookie-based locale detection** with `Accept-Language` header fallback (no URL prefix needed)
- **`window.__LOCALE__`** injected via inline script to prevent flash of untranslated content during hydration
- **Catalog loaded before hydration** on client, and before render on server
- **PO format** for catalogs (rich translator tooling ecosystem)
- **Babel plugin** (not SWC) for macro transformation — more reliable with Remix/React Router v7
