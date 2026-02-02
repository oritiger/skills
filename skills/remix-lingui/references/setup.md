# Remix + Lingui Setup Reference

Complete file-by-file setup guide. Apply these to the user's existing Remix project, adapting to their specific locales and structure.

## Table of Contents

- [1. Install Dependencies](#1-install-dependencies)
- [2. lingui.config.ts](#2-linguiconfigts)
- [3. vite.config.ts](#3-viteconfigts)
- [4. app/lib/i18n.ts](#4-applibi18nts)
- [5. app/locales/lingui.d.ts](#5-applocaleslinguidts)
- [6. app/entry.client.tsx](#6-appentryclienttsx)
- [7. app/root.tsx](#7-approottsx)
- [8. Locale Switching Route](#8-locale-switching-route)
- [9. Language Selector Component](#9-language-selector-component)
- [10. package.json Scripts](#10-packagejson-scripts)

## 1. Install Dependencies

```bash
# Runtime
npm install @lingui/core @lingui/react

# Dev
npm install -D @lingui/cli @lingui/vite-plugin @lingui/babel-plugin-lingui-macro @babel/preset-typescript vite-plugin-babel
```

## 2. lingui.config.ts

Create at project root. Adjust `locales` to match the user's needs.

```ts
import { defineConfig } from "@lingui/cli";

export default defineConfig({
  sourceLocale: "en",
  locales: ["en", "vi"],
  catalogs: [
    {
      path: "<rootDir>/app/locales/{locale}/messages",
      include: ["app"],
    },
  ],
});
```

## 3. vite.config.ts

Add `vite-plugin-babel` and `@lingui/vite-plugin`. The babel plugin MUST have a `filter` that matches the app source files. Order matters: babel and lingui should be placed alongside other plugins.

```ts
import { lingui } from "@lingui/vite-plugin";
import babel from "vite-plugin-babel";

// Add these to the plugins array in vite.config.ts:
babel({
  filter: /app\/.*\.[jt]sx?$/,
  babelConfig: {
    presets: ["@babel/preset-typescript"],
    plugins: ["@lingui/babel-plugin-lingui-macro"],
    babelrc: false,
    configFile: false,
  },
}),
lingui(),
```

**Important:** Keep existing plugins (reactRouter/remix, tailwind, tsconfigPaths, etc.). Just add `babel()` and `lingui()` to the array.

## 4. app/lib/i18n.ts

Core i18n utilities. Adjust `Locale` type and `locales` map for the user's languages.

```ts
import { i18n } from "@lingui/core";

export type Locale = "en" | "vi";

export const locales: Record<Locale, string> = {
  en: "English",
  vi: "Tiếng Việt",
};

export const defaultLocale: Locale = "en";

export function getLocaleFromCookie(cookieHeader: string | null): Locale | null {
  if (!cookieHeader) return null;
  const cookies = cookieHeader.split(";").reduce(
    (acc, cookie) => {
      const [key, value] = cookie.trim().split("=");
      if (key && value) acc[key] = value;
      return acc;
    },
    {} as Record<string, string>
  );
  const locale = cookies["locale"];
  if (locale && locale in locales) return locale as Locale;
  return null;
}

export function getLocaleFromHeaders(acceptLanguage: string | null): Locale {
  if (!acceptLanguage) return defaultLocale;
  const languages = acceptLanguage
    .split(",")
    .map((lang) => {
      const [locale, priority = "q=1"] = lang.trim().split(";");
      const q = parseFloat(priority.replace("q=", "")) || 1;
      return { locale: locale.split("-")[0].toLowerCase(), q };
    })
    .sort((a, b) => b.q - a.q);
  for (const { locale } of languages) {
    if (locale in locales) return locale as Locale;
  }
  return defaultLocale;
}

export async function loadCatalog(locale: string) {
  const { messages } = await import(`../locales/${locale}/messages.po`);
  i18n.loadAndActivate({ locale, messages });
}

export { i18n };
```

## 5. app/locales/lingui.d.ts

TypeScript declaration for `.po` file imports:

```ts
declare module "*.po" {
  import type { Messages } from "@lingui/core";
  export const messages: Messages;
}
```

## 6. app/entry.client.tsx

Load the correct catalog BEFORE hydration to prevent flash of untranslated content:

```tsx
import { startTransition, StrictMode } from "react";
import { hydrateRoot } from "react-dom/client";
import { HydratedRouter } from "react-router/dom";
import { loadCatalog, defaultLocale } from "~/lib/i18n";

declare global {
  interface Window {
    __LOCALE__?: string;
  }
}

const locale = window.__LOCALE__ || defaultLocale;

loadCatalog(locale).then(() => {
  startTransition(() => {
    hydrateRoot(
      document,
      <StrictMode>
        <HydratedRouter />
      </StrictMode>
    );
  });
});
```

**Note:** If the project already has an `entry.client.tsx`, wrap the existing hydration logic inside the `loadCatalog(...).then()` callback.

## 7. app/root.tsx

Three changes needed:

### a. Import i18n modules

```ts
import { I18nProvider } from "@lingui/react";
import {
  i18n,
  loadCatalog,
  getLocaleFromHeaders,
  getLocaleFromCookie,
  defaultLocale,
  type Locale,
} from "~/lib/i18n";
```

### b. Add/update the root loader

```ts
// Load default catalog on server at module init
if (typeof window === "undefined") {
  await loadCatalog(defaultLocale);
}

export async function loader({ request }: Route.LoaderArgs) {
  const cookieHeader = request.headers.get("Cookie");
  const acceptLanguage = request.headers.get("Accept-Language");

  let locale = getLocaleFromCookie(cookieHeader);
  if (!locale) {
    locale = getLocaleFromHeaders(acceptLanguage);
  }

  await loadCatalog(locale);
  return { locale };
}
```

### c. Update the Layout component

Wrap children with `I18nProvider` and inject `window.__LOCALE__`:

```tsx
export function Layout({ children }: { children: React.ReactNode }) {
  const locale = i18n.locale || defaultLocale;

  return (
    <html lang={locale}>
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <Meta />
        <Links />
      </head>
      <body>
        <script
          dangerouslySetInnerHTML={{
            __html: `window.__LOCALE__="${locale}"`,
          }}
        />
        <I18nProvider i18n={i18n}>{children}</I18nProvider>
        <ScrollRestoration />
        <Scripts />
      </body>
    </html>
  );
}
```

## 8. Locale Switching Route

Create `app/routes/set-locale.ts`:

```ts
import { redirect } from "react-router";
import type { Route } from "./+types/set-locale";
import { locales, type Locale } from "~/lib/i18n";

export async function action({ request }: Route.ActionArgs) {
  const formData = await request.formData();
  const locale = formData.get("locale") as string;

  if (!locale || !(locale in locales)) {
    return redirect("/");
  }

  const referer = request.headers.get("Referer") || "/";

  return redirect(referer, {
    headers: {
      "Set-Cookie": `locale=${locale}; Path=/; Max-Age=${60 * 60 * 24 * 365}; SameSite=Lax`,
    },
  });
}

export function loader() {
  return redirect("/");
}
```

Add to `app/routes.ts`:

```ts
import { route } from "@react-router/dev/routes";

// Add to the routes array:
route("set-locale", "routes/set-locale.ts"),
```

## 9. Language Selector Component

Example component for switching languages. Adapt styling to the user's UI framework:

```tsx
import { useLingui } from "@lingui/react";
import { locales, type Locale } from "~/lib/i18n";

function setCookie(name: string, value: string, days: number) {
  const maxAge = days * 24 * 60 * 60;
  document.cookie = `${name}=${value}; Path=/; Max-Age=${maxAge}; SameSite=Lax`;
}

export function LanguageSelector() {
  const { i18n } = useLingui();
  const currentLocale = (i18n.locale as Locale) || "en";

  const handleLocaleChange = (locale: Locale) => {
    if (locale === currentLocale) return;
    setCookie("locale", locale, 365);
    window.location.reload();
  };

  return (
    <div>
      {(Object.keys(locales) as Locale[]).map((locale) => (
        <button
          key={locale}
          onClick={() => handleLocaleChange(locale)}
          disabled={locale === currentLocale}
        >
          {locales[locale]}
        </button>
      ))}
    </div>
  );
}
```

## 10. package.json Scripts

Add these scripts:

```json
{
  "scripts": {
    "extract": "lingui extract",
    "compile": "lingui compile",
    "build": "lingui compile && react-router build"
  }
}
```

After setup, run `npx lingui extract` to generate initial `.po` catalog files in `app/locales/{locale}/messages.po`.
