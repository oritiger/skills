# Lingui Translation Patterns Reference

## Table of Contents

- [Import Paths](#import-paths)
- [Trans Component](#trans-component)
- [msg Macro + i18n._()](#msg-macro--i18n_)
- [useLingui Hook](#uselingui-hook)
- [Plurals](#plurals)
- [Select](#select)
- [Nested ICU](#nested-icu)
- [Common Patterns](#common-patterns)

## Import Paths

```ts
// JSX macros (components)
import { Trans, Plural, Select, SelectOrdinal } from "@lingui/react/macro";

// JS macros (non-JSX)
import { msg } from "@lingui/core/macro";

// Runtime hook
import { useLingui } from "@lingui/react";
```

**Do NOT import from `@lingui/macro`** — use the specific `/react/macro` and `/core/macro` paths.

## Trans Component

For inline JSX translations:

```tsx
// Simple text
<Trans>Welcome to our app</Trans>

// With variables
<Trans>Hello, {userName}!</Trans>

// With JSX elements (elements become indexed placeholders in the catalog)
<Trans>Read the <a href="/tos">Terms of Service</a></Trans>

// With rich formatting
<Trans>
  Your order of <strong>{itemName}</strong> will arrive in{" "}
  <em>{days} days</em>.
</Trans>
```

## msg Macro + i18n._()

For translatable strings defined outside JSX — constants, arrays, objects, config:

```tsx
import { msg } from "@lingui/core/macro";
import { useLingui } from "@lingui/react";

// Define translatable messages (extracted at build time, translated at runtime)
const menuItems = [
  { label: msg`Home`, href: "/" },
  { label: msg`About`, href: "/about" },
  { label: msg`Contact`, href: "/contact" },
];

function Menu() {
  const { i18n } = useLingui();
  return (
    <nav>
      {menuItems.map((item) => (
        <a key={item.href} href={item.href}>
          {i18n._(item.label)}
        </a>
      ))}
    </nav>
  );
}
```

**When to use `msg` vs `Trans`:**
- `msg` — data structures, constants, arrays, objects defined outside render
- `Trans` — inline JSX content, especially with embedded markup

## useLingui Hook

Access the i18n instance in components. Always use this instead of importing `i18n` directly in components to ensure re-render on locale change:

```tsx
import { useLingui } from "@lingui/react";

function MyComponent() {
  const { i18n } = useLingui();

  return <span>{i18n._(msg`Hello`)}</span>;
}
```

## Plurals

```tsx
import { Plural } from "@lingui/react/macro";

// Basic
<Plural value={count} one="# item" other="# items" />

// With zero
<Plural value={count} zero="No items" one="# item" other="# items" />

// With surrounding text
<Trans>You have <Plural value={count} one="# new message" other="# new messages" /></Trans>
```

JS context:

```ts
import { plural } from "@lingui/core/macro";

const message = plural(count, {
  zero: "No items",
  one: "# item",
  other: "# items",
});
```

## Select

For gender, status, or other categorical values:

```tsx
import { Select } from "@lingui/react/macro";

<Select
  value={gender}
  male="He liked your post"
  female="She liked your post"
  other="They liked your post"
/>
```

## Nested ICU

Combine plural + select:

```tsx
<Select
  value={gender}
  male={<Plural value={count} one="He has # book" other="He has # books" />}
  female={<Plural value={count} one="She has # book" other="She has # books" />}
  other={<Plural value={count} one="They have # book" other="They have # books" />}
/>
```

## Common Patterns

### Page titles / meta

```tsx
import { msg } from "@lingui/core/macro";
import { useLingui } from "@lingui/react";

const pageTitle = msg`About Us`;

export function meta() {
  // Note: meta runs outside React context, so server-side translation
  // is needed here. Use the i18n instance from the loader instead.
  return [{ title: "About Us" }]; // fallback to source locale
}

function AboutPage() {
  const { i18n } = useLingui();
  return <h1>{i18n._(pageTitle)}</h1>;
}
```

### Form validation messages

```tsx
const validationMessages = {
  required: msg`This field is required`,
  minLength: msg`Must be at least ${min} characters`,
  email: msg`Please enter a valid email address`,
};
```

### Conditional text

```tsx
<Trans>
  {isLoggedIn ? "Welcome back!" : "Please sign in"}
</Trans>
```

### Date and number formatting

Use `i18n.date()` and `i18n.number()` for locale-aware formatting:

```tsx
const { i18n } = useLingui();

i18n.date(new Date(), { dateStyle: "long" });
// "January 15, 2025" (en) / "15 tháng 1, 2025" (vi)

i18n.number(1234.56, { style: "currency", currency: "USD" });
// "$1,234.56" (en) / "1.234,56 US$" (vi)
```
