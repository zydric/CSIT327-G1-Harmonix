# Harmonix UI Design System & Style Guide

**Version:** 1.0  
**Last Updated:** December 2, 2025

## Table of Contents

1. [Color Palette](#1-color-palette)
2. [Typography](#2-typography)
3. [Spacing System](#3-spacing-system)
4. [Border Radius](#4-border-radius)
5. [Shadows & Effects](#5-shadows--effects)
6. [Icons](#6-icons)
7. [Avatar System](#7-avatar-system)
8. [Buttons & Interactive Elements](#8-buttons--interactive-elements)
9. [Form Elements](#9-form-elements)
10. [Cards & Containers](#10-cards--containers)
11. [Layout Patterns](#11-layout-patterns)
12. [Transitions & Animations](#12-transitions--animations)
13. [Responsive Breakpoints](#13-responsive-breakpoints)
14. [Component Patterns](#14-component-patterns)
15. [Accessibility Guidelines](#15-accessibility-guidelines)

---

## 1. Color Palette

Harmonix uses a carefully selected dark-themed color palette focused on purples and grays. **Light theme is not supported.**

### Primary Colors

| Token               | Hex Code  | Usage                                       |
| ------------------- | --------- | ------------------------------------------- |
| **Primary Purple**  | `#4F2FC0` | Primary actions, links, active states, logo |
| **Primary Hover**   | `#3f24a0` | Hover state for primary purple elements     |
| **Light Purple BG** | `#F3EFF8` | Light backgrounds, subtle highlights (rare) |

### Neutral Colors (Tailwind Grays)

| Token      | Example Use                          |
| ---------- | ------------------------------------ |
| `gray-50`  | Page background (light contexts)     |
| `gray-100` | Badge backgrounds, subtle containers |
| `gray-200` | Borders, dividers                    |
| `gray-300` | Input borders, disabled states       |
| `gray-400` | Icon colors, secondary text          |
| `gray-500` | Muted text, placeholders             |
| `gray-600` | Secondary text                       |
| `gray-700` | Body text                            |
| `gray-800` | Headings, emphasis text              |
| `gray-900` | Primary text, strong emphasis        |
| `white`    | Card backgrounds, navbar background  |

### Semantic Colors

| Token       | Hex/Tailwind | Usage                                |
| ----------- | ------------ | ------------------------------------ |
| **Success** | `green-*`    | Success messages, positive states    |
| **Error**   | `red-*`      | Error messages, destructive actions  |
| **Warning** | `yellow-*`   | Warning messages, caution states     |
| **Info**    | `blue-*`     | Information messages, neutral alerts |

#### Message Color Classes

```html
<!-- Success -->
<div class="bg-green-50 border border-green-200 text-green-800">
  Success message
</div>

<!-- Error -->
<div class="bg-red-50 border border-red-200 text-red-800">Error message</div>

<!-- Warning -->
<div class="bg-yellow-50 border border-yellow-200 text-yellow-800">
  Warning message
</div>

<!-- Info -->
<div class="bg-blue-50 border border-blue-200 text-blue-800">Info message</div>
```

---

## 2. Typography

### Font Family

**Primary Font:** Inter  
**Fallback:** Sans-serif (system fonts)

#### Font Loading Strategy

Inter is loaded via Google Fonts for reliable delivery and performance:

```html
<!-- In base.html <head> -->
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link
  href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
  rel="stylesheet"
/>

<style>
  body {
    font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  }
</style>
```

**Note:** Inter provides excellent readability and is optimized for UI design. The font weights 300, 400, 500, 600, and 700 cover all our design needs.

### Font Sizes

| Tailwind Class | Size | Usage                                   |
| -------------- | ---- | --------------------------------------- |
| `text-xs`      | 12px | Small badges, helper text               |
| `text-sm`      | 14px | Labels, secondary info, table text      |
| `text-base`    | 16px | Body text, descriptions, paragraph text |
| `text-lg`      | 18px | Section headers, sidebar titles         |
| `text-xl`      | 20px | Card titles, navbar links               |
| `text-2xl`     | 24px | Logo, modal titles, page subtitles      |
| `text-3xl`     | 30px | Page headings                           |
| `text-4xl`     | 36px | Major section headers                   |
| `text-5xl`     | 48px | Landing page elements                   |
| `text-6xl`     | 60px | Hero headlines                          |
| `text-7xl`     | 72px | Large hero text (e.g., "HARMONIX")      |

### Font Weights

| Tailwind Class  | Weight | Usage                              |
| --------------- | ------ | ---------------------------------- |
| `font-light`    | 300    | Hero subtitles, decorative text    |
| Regular (none)  | 400    | Body text, paragraphs              |
| `font-medium`   | 500    | Labels, navigation links, emphasis |
| `font-semibold` | 600    | Section headers, card titles       |
| `font-bold`     | 700    | Main headings, logo, CTAs          |

### Text Colors

```html
<!-- Primary text -->
<p class="text-gray-900">Primary heading</p>
<p class="text-gray-700">Body text</p>
<p class="text-gray-600">Secondary text</p>
<p class="text-gray-500">Muted text</p>

<!-- Brand colors -->
<p class="text-[#4F2FC0]">Purple text (links, emphasis)</p>
<p class="text-purple-900">Alternative purple (landing)</p>

<!-- Semantic -->
<p class="text-red-600">Error text</p>
<p class="text-green-700">Success text</p>
```

### Typography Examples

```html
<!-- Page Header -->
<h1 class="text-3xl font-bold text-gray-900">Page Title</h1>
<p class="text-gray-600">Subtitle or description</p>

<!-- Section Header -->
<h2 class="text-lg font-semibold text-gray-900">Section Title</h2>

<!-- Card Title -->
<h3 class="text-xl font-semibold text-gray-900">Card Title</h3>

<!-- Body Text -->
<p class="text-base text-gray-700">Regular paragraph text</p>

<!-- Label -->
<label class="text-sm font-medium text-gray-700">Form Label</label>

<!-- Helper Text -->
<span class="text-xs text-gray-500">Helper text</span>
```

---

## 3. Spacing System

Harmonix follows Tailwind's default spacing scale (1 unit = 0.25rem = 4px).

### Common Spacing Values

| Tailwind | Value | Usage                               |
| -------- | ----- | ----------------------------------- |
| `1`      | 4px   | Tight gaps (icon spacing)           |
| `2`      | 8px   | Small gaps (badges, chips)          |
| `3`      | 12px  | Form element gaps                   |
| `4`      | 16px  | Standard gaps (card content, lists) |
| `6`      | 24px  | Section spacing, navbar padding     |
| `8`      | 32px  | Page content padding, large gaps    |
| `12`     | 48px  | Major section spacing               |
| `16`     | 64px  | Hero sections                       |

### Layout Spacing Patterns

```html
<!-- Page Container -->
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
  <!-- Navbar -->
  <nav class="px-4 sm:px-6 lg:px-8 py-6">
    <!-- Card Content -->
    <div class="p-6">
      <!-- Form Stack -->
      <div class="space-y-4">
        <!-- Horizontal Button Group -->
        <div class="flex gap-4">
          <!-- Grid Gap -->
          <div class="grid grid-cols-3 gap-4"></div>
        </div>
      </div>
    </div>
  </nav>
</div>
```

### Margin & Padding Guidelines

**Use margin for:**

- Creating space between distinct sections
- Separating components vertically (`mb-6`, `mt-8`)

**Use padding for:**

- Internal spacing within components (`p-6`, `px-4 py-3`)

**Use gap for:**

- Flex and grid layouts (`gap-4`, `gap-8`)

**Use space-y/space-x for:**

- Consistent spacing in lists/stacks (`space-y-4`, `space-x-2`)

---

## 4. Border Radius

Harmonix uses consistent border radius values throughout the design.

| Tailwind Class | Value | Usage                                |
| -------------- | ----- | ------------------------------------ |
| `rounded`      | 4px   | Small elements (badges)              |
| `rounded-md`   | 6px   | Inputs, buttons, small cards         |
| `rounded-lg`   | 8px   | Cards, containers, modals            |
| `rounded-full` | 100%  | Pills, circular avatars, CTA buttons |

### Examples

```html
<!-- Card -->
<div class="bg-white rounded-lg shadow-sm">
  <!-- Button -->
  <button class="rounded-md px-4 py-2">
    <!-- Badge -->
    <span class="rounded-full px-2 py-1">
      <!-- Input -->
      <input class="rounded-md border border-gray-300" />

      <!-- Avatar -->
      <div class="rounded-full w-12 h-12"></div
    ></span>
  </button>
</div>
```

---

## 5. Shadows & Effects

### Shadow Scale

| Tailwind Class | Usage                         |
| -------------- | ----------------------------- |
| `shadow-sm`    | Subtle cards, inputs, navbar  |
| `shadow`       | Standard cards, dropdowns     |
| `shadow-md`    | Elevated cards, modals        |
| `shadow-lg`    | Important modals, overlays    |
| `shadow-none`  | Remove shadow on hover/active |

### Common Shadow Patterns

```html
<!-- Default Card -->
<div class="bg-white rounded-lg shadow-sm">
  <!-- Elevated Card (hover state) -->
  <div class="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow">
    <!-- Modal -->
    <div class="bg-white rounded-lg shadow-lg"></div>
  </div>
</div>
```

### Border Styles

```html
<!-- Standard border -->
<div class="border border-gray-200">
  <!-- Bottom border only (navigation active state) -->
  <a class="border-b-2 border-[#4F2FC0]">
    <!-- No border -->
    <div class="border-0"></div
  ></a>
</div>
```

---

## 6. Icons

### Icon System

**Recommended Icon Library:** [Heroicons](https://heroicons.com/)

Heroicons is the recommended icon library for Django templates as it provides inline SVG icons that are:

- Free and open-source
- Consistent with Tailwind CSS design
- Easy to copy/paste into Django templates
- No JavaScript dependencies

#### Icon Styles

Heroicons offers two styles:

- **Outline** (stroke-based) - Use for most UI elements
- **Solid** (fill-based) - Use for filled states, badges, emphasis

#### Installation & Usage

No installation required - copy SVG code directly into templates:

```html
<!-- Outline icon (most common) -->
<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
  <path
    stroke-linecap="round"
    stroke-linejoin="round"
    stroke-width="2"
    d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
  ></path>
</svg>

<!-- Solid icon -->
<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
  <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"></path>
  <path
    fill-rule="evenodd"
    d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z"
    clip-rule="evenodd"
  ></path>
</svg>
```

### Icon Sizes

| Tailwind Class | Size | Usage                                   |
| -------------- | ---- | --------------------------------------- |
| `w-3 h-3`      | 12px | Very small inline icons                 |
| `w-4 h-4`      | 16px | Standard UI icons (buttons, cards, nav) |
| `w-5 h-5`      | 20px | Navigation, filters, section headers    |
| `w-6 h-6`      | 24px | Back buttons, page actions              |
| `w-8 h-8`      | 32px | Logo, large action buttons              |
| `w-12 h-12`    | 48px | Empty states, placeholders              |
| `w-20 h-20`    | 80px | Modal icons, large illustrations        |

### Icon Colors

Icons inherit text color using `currentColor`:

```html
<!-- Gray icon -->
<svg
  class="w-4 h-4 text-gray-400"
  fill="none"
  stroke="currentColor"
  viewBox="0 0 24 24"
>
  <!-- Purple icon -->
  <svg
    class="w-4 h-4 text-[#4F2FC0]"
    fill="none"
    stroke="currentColor"
    viewBox="0 0 24 24"
  >
    <!-- Icon that changes on hover -->
    <a class="text-gray-500 hover:text-[#4F2FC0] transition-colors">
      <svg
        class="w-5 h-5"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      ></svg>
    </a>
  </svg>
</svg>
```

### Common Icon Usage

```html
<!-- Navigation icon -->
<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
  <path
    stroke-linecap="round"
    stroke-linejoin="round"
    stroke-width="2"
    d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
  ></path>
</svg>

<!-- Filter icon -->
<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
  <path
    stroke-linecap="round"
    stroke-linejoin="round"
    stroke-width="2"
    d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.207A1 1 0 013 6.5V4z"
  ></path>
</svg>

<!-- Loading spinner -->
<svg class="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
  <circle
    class="opacity-25"
    cx="12"
    cy="12"
    r="10"
    stroke="currentColor"
    stroke-width="4"
  ></circle>
  <path
    class="opacity-75"
    fill="currentColor"
    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
  ></path>
</svg>

<!-- Dropdown arrow -->
<svg
  class="h-4 w-4 text-gray-400"
  fill="none"
  stroke="currentColor"
  viewBox="0 0 24 24"
>
  <path
    stroke-linecap="round"
    stroke-linejoin="round"
    stroke-width="2"
    d="M19 9l-7 7-7-7"
  ></path>
</svg>

<!-- Back arrow -->
<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
  <path
    stroke-linecap="round"
    stroke-linejoin="round"
    stroke-width="2"
    d="M10 19l-7-7m0 0l7-7m-7 7h18"
  ></path>
</svg>
```

### Icon Resources

- **Browse icons:** [heroicons.com](https://heroicons.com/)
- **Search icons:** Use the search feature on heroicons.com
- **Alternative:** [Tabler Icons](https://tabler-icons.io/) (similar inline SVG approach)

---

## 7. Avatar System

Harmonix uses a simple, colorful initial-based avatar system for user profiles.

### Implementation

Each user gets a single-letter avatar with a unique, randomly assigned background color.

#### Backend Implementation (Python)

```python
# In accounts/models.py or utils
import hashlib

AVATAR_COLORS = [
    '#EF4444',  # red-500
    '#F59E0B',  # amber-500
    '#10B981',  # emerald-500
    '#3B82F6',  # blue-500
    '#8B5CF6',  # violet-500
    '#EC4899',  # pink-500
    '#14B8A6',  # teal-500
    '#F97316',  # orange-500
]

def get_avatar_color(user_id):
    """Generate consistent color based on user ID"""
    hash_value = int(hashlib.md5(str(user_id).encode()).hexdigest(), 16)
    return AVATAR_COLORS[hash_value % len(AVATAR_COLORS)]

def get_avatar_initial(username):
    """Get first letter of username in uppercase"""
    return username[0].upper() if username else '?'

# Add methods to User model
class User(AbstractUser):
    # ... existing fields ...

    def get_avatar_color(self):
        return get_avatar_color(self.id)

    def get_avatar_initial(self):
        return get_avatar_initial(self.username)
```

#### Template Usage

```html
<!-- Small avatar (card) -->
<div
  class="w-12 h-12 rounded-full flex items-center justify-center text-white font-bold text-lg"
  style="background-color: {{ user.get_avatar_color }};"
>
  {{ user.get_avatar_initial }}
</div>

<!-- Large avatar (profile) -->
<div
  class="w-20 h-20 rounded-full flex items-center justify-center text-white font-bold text-3xl"
  style="background-color: {{ user.get_avatar_color }};"
>
  {{ user.get_avatar_initial }}
</div>

<!-- Extra large avatar (modal) -->
<div
  class="w-32 h-32 rounded-full flex items-center justify-center text-white font-bold text-5xl"
  style="background-color: {{ user.get_avatar_color }};"
>
  {{ user.get_avatar_initial }}
</div>
```

### Avatar Sizes

| Size Class  | Dimensions | Usage                             |
| ----------- | ---------- | --------------------------------- |
| `w-8 h-8`   | 32px       | Tiny avatar (comments, mentions)  |
| `w-10 h-10` | 40px       | Small avatar (compact lists)      |
| `w-12 h-12` | 48px       | Standard avatar (cards, listings) |
| `w-16 h-16` | 64px       | Medium avatar (sidebar)           |
| `w-20 h-20` | 80px       | Large avatar (modals, profiles)   |
| `w-32 h-32` | 128px      | Extra large avatar (profile page) |

### Text Size Pairing

| Avatar Size | Text Class | Font Size |
| ----------- | ---------- | --------- |
| `w-8 h-8`   | `text-xs`  | 12px      |
| `w-10 h-10` | `text-sm`  | 14px      |
| `w-12 h-12` | `text-lg`  | 18px      |
| `w-16 h-16` | `text-xl`  | 20px      |
| `w-20 h-20` | `text-3xl` | 30px      |
| `w-32 h-32` | `text-5xl` | 48px      |

---

## 8. Buttons & Interactive Elements

### Button Variants

#### Primary Button

```html
<button
  class="px-6 py-2.5 bg-[#4F2FC0] text-white rounded-md font-medium hover:bg-[#3f24a0] transition-colors"
>
  Primary Action
</button>
```

#### Secondary Button (Outline)

```html
<button
  class="px-6 py-2.5 border-2 border-[#4F2FC0] text-[#4F2FC0] rounded-md font-medium hover:bg-[#4F2FC0] hover:text-white transition-colors"
>
  Secondary Action
</button>
```

#### Outline Button (Light)

```html
<button
  class="px-6 py-2.5 border-2 border-white text-white rounded-full font-semibold hover:bg-white/10 transition"
>
  Outline Button
</button>
```

#### Danger Button

```html
<button
  class="px-4 py-2 bg-red-600 text-white rounded-md font-medium hover:bg-red-700 transition-colors"
>
  Delete
</button>
```

#### Ghost Button

```html
<button
  class="px-4 py-2 text-gray-700 hover:text-[#4F2FC0] hover:bg-gray-100 rounded-md transition-colors"
>
  Ghost Button
</button>
```

#### Disabled Button

```html
<button
  disabled
  class="px-6 py-2.5 bg-gray-300 text-gray-500 rounded-md font-medium cursor-not-allowed"
>
  Disabled
</button>
```

### Button Sizes

```html
<!-- Small -->
<button class="px-3 py-1.5 text-sm">Small</button>

<!-- Medium (default) -->
<button class="px-4 py-2 text-base">Medium</button>

<!-- Large -->
<button class="px-6 py-2.5 text-lg">Large</button>

<!-- Full width -->
<button class="w-full px-6 py-2.5">Full Width</button>
```

### Button with Icon

```html
<!-- Icon left -->
<button
  class="px-4 py-2 bg-[#4F2FC0] text-white rounded-md flex items-center gap-2"
>
  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path
      stroke-linecap="round"
      stroke-linejoin="round"
      stroke-width="2"
      d="M12 4v16m8-8H4"
    ></path>
  </svg>
  Add Item
</button>

<!-- Icon right -->
<button
  class="px-4 py-2 bg-[#4F2FC0] text-white rounded-md flex items-center gap-2"
>
  Next
  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path
      stroke-linecap="round"
      stroke-linejoin="round"
      stroke-width="2"
      d="M9 5l7 7-7 7"
    ></path>
  </svg>
</button>

<!-- Loading state -->
<button
  class="px-4 py-2 bg-[#4F2FC0] text-white rounded-md flex items-center gap-2"
  disabled
>
  <svg class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
    <circle
      class="opacity-25"
      cx="12"
      cy="12"
      r="10"
      stroke="currentColor"
      stroke-width="4"
    ></circle>
    <path
      class="opacity-75"
      fill="currentColor"
      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
    ></path>
  </svg>
  Processing...
</button>
```

### Links

```html
<!-- Standard link -->
<a href="#" class="text-[#4F2FC0] hover:text-[#3f24a0] transition-colors">
  Standard Link
</a>

<!-- Underlined link -->
<a href="#" class="text-[#4F2FC0] underline hover:text-[#3f24a0]">
  Underlined Link
</a>

<!-- External link with icon -->
<a href="#" class="text-[#4F2FC0] hover:text-[#3f24a0] flex items-center gap-1">
  External Link
  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path
      stroke-linecap="round"
      stroke-linejoin="round"
      stroke-width="2"
      d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
    ></path>
  </svg>
</a>
```

---

## 9. Form Elements

### Text Input

```html
<!-- Standard input -->
<div>
  <label for="name" class="block text-sm font-medium text-gray-700 mb-1">
    Name
  </label>
  <input
    type="text"
    id="name"
    name="name"
    placeholder="Enter your name"
    class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-[#4F2FC0] focus:border-transparent"
  />
</div>

<!-- Input with error -->
<div>
  <label for="email" class="block text-sm font-medium text-gray-700 mb-1">
    Email
  </label>
  <input
    type="email"
    id="email"
    name="email"
    class="w-full px-3 py-2 border border-red-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent"
  />
  <p class="mt-1 text-sm text-red-600">Please enter a valid email address</p>
</div>

<!-- Disabled input -->
<input
  type="text"
  disabled
  class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm bg-gray-100 text-gray-500 cursor-not-allowed"
/>
```

### Textarea

```html
<div>
  <label for="description" class="block text-sm font-medium text-gray-700 mb-1">
    Description
  </label>
  <textarea
    id="description"
    name="description"
    rows="4"
    placeholder="Enter description..."
    class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-[#4F2FC0] focus:border-transparent"
  ></textarea>
</div>
```

### Select Dropdown

```html
<div>
  <label for="genre" class="block text-sm font-medium text-gray-700 mb-1">
    Genre
  </label>
  <div class="relative">
    <select
      id="genre"
      name="genre"
      class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-[#4F2FC0] focus:border-transparent appearance-none bg-white pr-8"
    >
      <option value="">Select a genre</option>
      <option value="rock">Rock</option>
      <option value="jazz">Jazz</option>
      <option value="pop">Pop</option>
    </select>
    <!-- Custom dropdown arrow -->
    <div
      class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none"
    >
      <svg
        class="h-4 w-4 text-gray-400"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M19 9l-7 7-7-7"
        ></path>
      </svg>
    </div>
  </div>
</div>
```

### Checkbox

```html
<div class="flex items-center">
  <input
    type="checkbox"
    id="terms"
    name="terms"
    class="w-4 h-4 text-[#4F2FC0] border-gray-300 rounded focus:ring-[#4F2FC0]"
  />
  <label for="terms" class="ml-2 text-sm text-gray-700">
    I agree to the terms and conditions
  </label>
</div>
```

### Radio Buttons

```html
<div class="space-y-2">
  <div class="flex items-center">
    <input
      type="radio"
      id="option1"
      name="option"
      value="1"
      class="w-4 h-4 text-[#4F2FC0] border-gray-300 focus:ring-[#4F2FC0]"
    />
    <label for="option1" class="ml-2 text-sm text-gray-700"> Option 1 </label>
  </div>
  <div class="flex items-center">
    <input
      type="radio"
      id="option2"
      name="option"
      value="2"
      class="w-4 h-4 text-[#4F2FC0] border-gray-300 focus:ring-[#4F2FC0]"
    />
    <label for="option2" class="ml-2 text-sm text-gray-700"> Option 2 </label>
  </div>
</div>
```

### Form Layout

```html
<!-- Standard form -->
<form class="space-y-4">
  <!-- Form fields -->
</form>

<!-- Form with sections -->
<form class="space-y-8">
  <div class="bg-gray-50 p-6 rounded-lg border border-gray-200">
    <h3 class="text-base font-semibold text-gray-900 mb-3">Section Title</h3>
    <div class="space-y-4">
      <!-- Section fields -->
    </div>
  </div>
</form>
```

---

## 10. Cards & Containers

### Basic Card

```html
<div class="bg-white rounded-lg shadow-sm p-6">
  <h3 class="text-xl font-semibold text-gray-900 mb-2">Card Title</h3>
  <p class="text-gray-600">Card content goes here.</p>
</div>
```

### Card with Border

```html
<div class="bg-white rounded-lg border border-gray-200 p-6">
  <h3 class="text-xl font-semibold text-gray-900 mb-2">Card Title</h3>
  <p class="text-gray-600">Card content goes here.</p>
</div>
```

### Hoverable Card

```html
<div
  class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow cursor-pointer"
>
  <h3 class="text-xl font-semibold text-gray-900 mb-2">Card Title</h3>
  <p class="text-gray-600">Card content goes here.</p>
</div>
```

### Card with Header and Footer

```html
<div
  class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden"
>
  <!-- Header -->
  <div class="px-6 py-4 border-b border-gray-200 bg-gray-50">
    <h3 class="text-lg font-semibold text-gray-900">Card Header</h3>
  </div>

  <!-- Body -->
  <div class="p-6">
    <p class="text-gray-600">Card content goes here.</p>
  </div>

  <!-- Footer -->
  <div class="px-6 py-4 border-t border-gray-200 bg-gray-50">
    <button class="text-sm text-[#4F2FC0] hover:text-[#3f24a0]">Action</button>
  </div>
</div>
```

### User Card (Listing Card)

```html
<div
  class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
>
  <!-- Header with avatar -->
  <div class="flex items-center mb-4">
    <div
      class="w-12 h-12 rounded-full flex items-center justify-center text-white font-bold text-lg mr-3"
      style="background-color: #3B82F6;"
    >
      J
    </div>
    <div>
      <h3 class="text-lg font-semibold text-gray-900">John Doe</h3>
      <p class="text-sm text-gray-600">@johndoe</p>
    </div>
  </div>

  <!-- Content -->
  <p class="text-gray-700 mb-4">Looking for a guitarist for jazz band...</p>

  <!-- Tags -->
  <div class="flex flex-wrap gap-2 mb-4">
    <span class="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full"
      >Jazz</span
    >
    <span class="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full"
      >Guitar</span
    >
  </div>

  <!-- Footer -->
  <div class="flex items-center justify-between text-sm text-gray-500">
    <span>2 days ago</span>
    <button class="text-[#4F2FC0] hover:text-[#3f24a0] font-medium">
      View Details
    </button>
  </div>
</div>
```

---

## 11. Layout Patterns

### Max Width Container

```html
<!-- Standard page container -->
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
  <!-- Page content -->
</div>

<!-- Narrow container (forms, articles) -->
<div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
  <!-- Narrow content -->
</div>
```

### Two-Column Layout (Sidebar + Main)

```html
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
  <div class="flex flex-col lg:flex-row gap-8">
    <!-- Sidebar -->
    <aside class="lg:w-80 space-y-6">
      <!-- Sidebar content -->
    </aside>

    <!-- Main content -->
    <main class="flex-1">
      <!-- Main content -->
    </main>
  </div>
</div>
```

### Grid Layouts

```html
<!-- 3-column grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <!-- Grid items -->
</div>

<!-- 2-column grid -->
<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
  <!-- Grid items -->
</div>

<!-- 4-column grid -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
  <!-- Grid items -->
</div>
```

### Full Height Layout

```html
<div class="min-h-screen bg-gray-50">
  <!-- Full height content -->
</div>
```

### Centered Content

```html
<!-- Vertically and horizontally centered -->
<div class="min-h-screen flex items-center justify-center">
  <div class="max-w-md w-full">
    <!-- Centered content -->
  </div>
</div>
```

---

## 12. Transitions & Animations

### Transition Classes

```html
<!-- Color transitions (default for interactive elements) -->
<button class="transition-colors hover:bg-[#3f24a0]">
  <!-- All properties -->
  <div class="transition-all duration-300 hover:scale-105">
    <!-- Shadow transitions -->
    <div class="transition-shadow hover:shadow-lg">
      <!-- Opacity transitions -->
      <div class="transition-opacity hover:opacity-75">
        <!-- Transform transitions -->
        <div class="transition-transform hover:-translate-y-1"></div>
      </div>
    </div>
  </div>
</button>
```

### Duration

| Class          | Duration | Usage                        |
| -------------- | -------- | ---------------------------- |
| `duration-150` | 150ms    | Fast interactions (hover)    |
| `duration-200` | 200ms    | Standard transitions         |
| `duration-300` | 300ms    | Smooth transitions (default) |
| `duration-500` | 500ms    | Slow, deliberate transitions |

### Animations

```html
<!-- Spin (loading) -->
<svg class="animate-spin h-5 w-5">
  <!-- Pulse (notification) -->
  <div class="animate-pulse">
    <!-- Bounce (attention) -->
    <div class="animate-bounce"></div>
  </div>
</svg>
```

### Common Hover Effects

```html
<!-- Card hover -->
<div class="hover:shadow-md hover:-translate-y-1 transition-all duration-300">
  <!-- Button hover -->
  <button class="hover:bg-[#3f24a0] transition-colors duration-200">
    <!-- Link hover -->
    <a class="hover:text-[#3f24a0] transition-colors">
      <!-- Icon hover -->
      <svg class="text-gray-500 hover:text-[#4F2FC0] transition-colors"></svg
    ></a>
  </button>
</div>
```

---

## 13. Responsive Breakpoints

Harmonix follows Tailwind's default breakpoint system:

| Breakpoint | Min Width | Device Target       |
| ---------- | --------- | ------------------- |
| `sm:`      | 640px     | Small tablets       |
| `md:`      | 768px     | Tablets             |
| `lg:`      | 1024px    | Desktops            |
| `xl:`      | 1280px    | Large desktops      |
| `2xl:`     | 1536px    | Extra large screens |

### Responsive Patterns

```html
<!-- Responsive padding -->
<div class="px-4 sm:px-6 lg:px-8">
  <!-- Responsive grid -->
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    <!-- Responsive flex direction -->
    <div class="flex flex-col lg:flex-row gap-8">
      <!-- Responsive text size -->
      <h1 class="text-4xl md:text-5xl lg:text-6xl">
        <!-- Hide on mobile -->
        <div class="hidden md:block">
          <!-- Show on mobile only -->
          <div class="block md:hidden">
            <!-- Responsive width -->
            <div class="w-full lg:w-80"></div>
          </div>
        </div>
      </h1>
    </div>
  </div>
</div>
```

---

## 14. Component Patterns

### Navigation Bar

```html
<nav class="bg-white shadow-sm border-b border-gray-200">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex justify-between items-center h-16">
      <!-- Logo -->
      <a href="/" class="flex items-center group">
        <div class="w-8 h-8 mr-3">
          <img src="logo.png" alt="Harmonix Logo" class="w-full h-full" />
        </div>
        <h1
          class="text-[#4F2FC0] text-xl font-bold group-hover:text-[#3f24a0] transition-colors"
        >
          Harmonix
        </h1>
      </a>

      <!-- Navigation Links -->
      <div class="flex space-x-8 text-sm font-medium text-gray-700">
        <a
          href="/listings"
          class="hover:text-[#4F2FC0] transition-colors pb-4 -mb-px"
        >
          Listings
        </a>
        <a
          href="/profile"
          class="text-[#4F2FC0] border-b-2 border-[#4F2FC0] pb-4 -mb-px"
        >
          Profile
        </a>
      </div>
    </div>
  </div>
</nav>
```

### Badge

```html
<!-- Default badge -->
<span class="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">
  Badge
</span>

<!-- Purple badge -->
<span class="px-2 py-1 bg-purple-100 text-purple-700 text-xs rounded-full">
  Featured
</span>

<!-- Status badges -->
<span class="px-2 py-1 bg-green-100 text-green-700 text-xs rounded-full">
  Active
</span>
<span class="px-2 py-1 bg-yellow-100 text-yellow-700 text-xs rounded-full">
  Pending
</span>
<span class="px-2 py-1 bg-red-100 text-red-700 text-xs rounded-full">
  Closed
</span>

<!-- Badge with dot -->
<span
  class="inline-flex items-center px-2 py-1 bg-green-100 text-green-700 text-xs rounded-full"
>
  <svg
    class="mr-1.5 h-2 w-2 text-green-400"
    fill="currentColor"
    viewBox="0 0 8 8"
  >
    <circle cx="4" cy="4" r="3"></circle>
  </svg>
  Online
</span>
```

### Empty State

```html
<div class="text-center py-12">
  <svg
    class="mx-auto h-12 w-12 text-gray-400"
    fill="none"
    stroke="currentColor"
    viewBox="0 0 24 24"
  >
    <path
      stroke-linecap="round"
      stroke-linejoin="round"
      stroke-width="2"
      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
    ></path>
  </svg>
  <h3 class="mt-4 text-lg font-medium text-gray-900">No listings found</h3>
  <p class="mt-2 text-sm text-gray-500">
    Get started by creating a new listing.
  </p>
  <div class="mt-6">
    <button
      class="px-4 py-2 bg-[#4F2FC0] text-white rounded-md font-medium hover:bg-[#3f24a0]"
    >
      Create Listing
    </button>
  </div>
</div>
```

### Alert/Message Banner

```html
<!-- Success -->
<div
  class="bg-green-50 border border-green-200 text-green-800 px-4 py-3 rounded-lg"
>
  Your profile has been updated successfully!
</div>

<!-- Error -->
<div class="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg">
  An error occurred. Please try again.
</div>

<!-- Warning -->
<div
  class="bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 py-3 rounded-lg"
>
  Your session is about to expire.
</div>

<!-- Info -->
<div
  class="bg-blue-50 border border-blue-200 text-blue-800 px-4 py-3 rounded-lg"
>
  New features are available!
</div>
```

### Modal

```html
<!-- Modal backdrop -->
<div
  class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
>
  <!-- Modal container -->
  <div
    class="bg-white rounded-lg shadow-lg max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto"
  >
    <!-- Modal header -->
    <div
      class="px-6 py-4 border-b border-gray-200 flex items-center justify-between"
    >
      <h2 class="text-2xl font-semibold text-gray-900">Modal Title</h2>
      <button class="text-gray-400 hover:text-gray-600 transition-colors">
        <svg
          class="w-6 h-6"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M6 18L18 6M6 6l12 12"
          ></path>
        </svg>
      </button>
    </div>

    <!-- Modal body -->
    <div class="p-6">
      <p class="text-gray-700">Modal content goes here...</p>
    </div>

    <!-- Modal footer -->
    <div class="px-6 py-4 border-t border-gray-200 flex justify-end gap-3">
      <button
        class="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md transition-colors"
      >
        Cancel
      </button>
      <button
        class="px-4 py-2 bg-[#4F2FC0] text-white rounded-md hover:bg-[#3f24a0] transition-colors"
      >
        Confirm
      </button>
    </div>
  </div>
</div>
```

### Pagination

```html
<div
  class="flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 sm:px-6"
>
  <!-- Mobile view -->
  <div class="flex flex-1 justify-between sm:hidden">
    <a
      href="?page=1"
      class="relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
    >
      Previous
    </a>
    <a
      href="?page=3"
      class="relative ml-3 inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
    >
      Next
    </a>
  </div>

  <!-- Desktop view -->
  <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
    <div>
      <p class="text-sm text-gray-700">
        Showing <span class="font-medium">1</span> to
        <span class="font-medium">10</span> of
        <span class="font-medium">97</span> results
      </p>
    </div>
    <div>
      <nav class="isolate inline-flex -space-x-px rounded-md shadow-sm">
        <a
          href="?page=1"
          class="relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 hover:bg-gray-50"
        >
          <svg
            class="h-5 w-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M15 19l-7-7 7-7"
            ></path>
          </svg>
        </a>
        <a
          href="?page=1"
          class="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-900 hover:bg-gray-50"
          >1</a
        >
        <a
          href="?page=2"
          class="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-[#4F2FC0] bg-purple-50"
          >2</a
        >
        <a
          href="?page=3"
          class="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-900 hover:bg-gray-50"
          >3</a
        >
        <a
          href="?page=3"
          class="relative inline-flex items-center rounded-r-md px-2 py-2 text-gray-400 hover:bg-gray-50"
        >
          <svg
            class="h-5 w-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 5l7 7-7 7"
            ></path>
          </svg>
        </a>
      </nav>
    </div>
  </div>
</div>
```

---

## 15. Accessibility Guidelines

### General Principles

1. **Semantic HTML**: Use proper HTML elements (`<button>`, `<nav>`, `<main>`, `<article>`)
2. **Color Contrast**: Ensure text meets WCAG AA standards (4.5:1 for normal text)
3. **Focus States**: Always provide visible focus indicators
4. **Alt Text**: Provide descriptive alt text for images
5. **ARIA Labels**: Use ARIA labels for icon-only buttons
6. **Keyboard Navigation**: Ensure all interactive elements are keyboard accessible

### Focus Styles

```html
<!-- Input focus -->
<input
  class="focus:outline-none focus:ring-2 focus:ring-[#4F2FC0] focus:border-transparent"
/>

<!-- Button focus -->
<button
  class="focus:outline-none focus:ring-2 focus:ring-[#4F2FC0] focus:ring-offset-2"
>
  <!-- Link focus -->
  <a class="focus:outline-none focus:ring-2 focus:ring-[#4F2FC0] rounded"></a>
</button>
```

### ARIA Labels

```html
<!-- Icon-only button -->
<button aria-label="Close modal" class="text-gray-400 hover:text-gray-600">
  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path
      stroke-linecap="round"
      stroke-linejoin="round"
      stroke-width="2"
      d="M6 18L18 6M6 6l12 12"
    ></path>
  </svg>
</button>

<!-- Search input -->
<label for="search" class="sr-only">Search listings</label>
<input type="text" id="search" name="search" placeholder="Search..." />
```

### Screen Reader Text

```html
<!-- Hidden but accessible to screen readers -->
<span class="sr-only">Current page: </span>
<span class="text-[#4F2FC0]">Dashboard</span>
```

---

## Implementation Checklist

### Setup Tasks

- [ ] Verify Inter font is loaded in `base.html` via Google Fonts
- [ ] Implement avatar color system in `User` model
- [ ] Create template tag for avatar generation (optional)
- [ ] Document Heroicons usage for team
- [ ] Update `tailwind.config.js` with custom colors if needed
- [ ] Run `python manage.py collectstatic` before deployment

### Design Consistency

- [ ] Audit all templates for inconsistent colors (replace with `#4F2FC0`)
- [ ] Replace all icon implementations with Heroicons
- [ ] Update all buttons to match style guide patterns
- [ ] Ensure all forms use consistent input styles
- [ ] Verify all cards use standard shadow and border patterns
- [ ] Check responsive breakpoints across all pages

### Testing

- [ ] Test font loading in development and production
- [ ] Verify avatar colors are unique and consistent per user
- [ ] Test all interactive states (hover, focus, active)
- [ ] Verify keyboard navigation works throughout app
- [ ] Test responsive layouts on multiple screen sizes
- [ ] Check color contrast for accessibility

---

## Resources

- **Tailwind CSS Documentation**: [tailwindcss.com](https://tailwindcss.com/)
- **Heroicons**: [heroicons.com](https://heroicons.com/)
- **Inter Font**: [Google Fonts - Inter](https://fonts.google.com/specimen/Inter)
- **Color Contrast Checker**: [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- **Tailwind Color Palette**: [Tailwind Colors](https://tailwindcss.com/docs/customizing-colors)

---

## Questions & Support

For questions about this style guide or design decisions, contact the development team or refer to the `CONTRIBUTING.md` file.

**Maintained by:** Harmonix Development Team  
**Last Review:** December 2, 2025
