# Mail Parser Dashboard Redesign

## Table of Contents
1. [Design Philosophy](#design-philosophy)
2. [User Personas](#user-personas)
3. [User Flows](#user-flows)
4. [Wireframes](#wireframes)
5. [Component Specifications](#component-specifications)
6. [Accessibility](#accessibility)
7. [Responsive Design](#responsive-design)
8. [Implementation Plan](#implementation-plan)

---

## Design Philosophy

### Core Principles

**1. Progressive Disclosure**
- Show essential information first
- Reveal complexity only when needed
- Layer advanced features behind simple interfaces

**2. Immediate Clarity**
- Users should understand purpose within 3 seconds
- Every action should have clear outcomes
- No mystery meat navigation

**3. Forgiving Interactions**
- Easy to undo or retry
- Clear error recovery paths
- No dead ends

**4. Accessibility First**
- Keyboard navigation throughout
- Screen reader optimized
- High contrast, readable fonts
- No color-only information

**5. Performance Perception**
- Optimistic UI updates
- Skeleton screens during loading
- Instant feedback for all actions
- Smart caching and prefetching

---

## User Personas

### Persona 1: Sarah the Office Manager
**Background:** Non-technical, manages team communications
**Goals:** Find specific emails quickly, organize by sender
**Pain Points:** Overwhelmed by technical interfaces, needs guidance
**Frequency:** Daily user

**Design Implications:**
- Clear, simple language (no jargon)
- Visual date pickers (no text entry)
- Helpful tooltips and examples
- Guided search suggestions

### Persona 2: Mike the Analyst
**Background:** Moderately technical, analyzes email patterns
**Goals:** Advanced filtering, export data, find trends
**Pain Points:** Current interface too simple, needs power features
**Frequency:** Weekly user

**Design Implications:**
- Advanced search mode option
- Multi-select filters
- Export functionality
- Keyboard shortcuts

### Persona 3: Lisa the Executive
**Background:** Non-technical, time-constrained
**Goals:** Quick access to important emails, dashboard overview
**Pain Points:** Too many clicks, information overload
**Frequency:** Occasional user

**Design Implications:**
- High-level statistics first
- Saved searches/filters
- Mobile-optimized
- One-click actions

---

## User Flows

### Flow 1: First-Time User Landing

```
┌─────────────────────────────────────────────────────────────┐
│                    LANDING PAGE                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  Welcome Overlay (First Visit Only)                    │ │
│  │  ┌─────────────────────────────────────────────────┐  │ │
│  │  │  👋 Welcome to Your Email Archive!              │  │ │
│  │  │                                                   │  │ │
│  │  │  [✓] Browse 39,768 emails                        │  │ │
│  │  │  [✓] Search by date, sender, or content          │  │ │
│  │  │  [✓] Filter by domain or label                   │  │ │
│  │  │                                                   │  │ │
│  │  │  [Skip Tour]  [Take Quick Tour] ←───────────────────┐│ │
│  │  └─────────────────────────────────────────────────┘  │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  Dashboard Statistics (Contextual Help)               │ │
│  │  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐                │ │
│  │  │39.7K│  │1,234│  │  42 │  │3,456│                │ │
│  │  │Email│  │Thread│  │Domain│  │Files│                │ │
│  │  └──i──┘  └──i──┘  └──i──┘  └──i──┘                │ │
│  │      └ Tooltip: "Total emails in your archive"       │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                          ↓
                    (User clicks "Take Quick Tour")
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Interactive Tutorial (4 Steps)                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  Step 1/4: Search                                      │ │
│  │  ┌─────────────────────────────────────┐              │ │
│  │  │ 🔍 Type here to search emails...    │ ← Highlight  │ │
│  │  └─────────────────────────────────────┘              │ │
│  │  Try searching for a sender's name or email subject   │ │
│  │  [Next →]                                              │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                          ↓
                     (After tour)
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Dashboard Ready to Use                                     │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  🔍 Search: "github notifications"   [Help?]          │ │
│  │  ↓ Results: 234 emails found                          │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Flow 2: Common Task - Find Email from Last Week

```
USER GOAL: Find email from specific sender last week

Step 1: User arrives at dashboard
  ↓
Step 2: Click "Filters" button (visible, prominent)
  ↓
┌─────────────────────────────────────────────────────────────┐
│  Filter Panel Opens (Slide from right)                      │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  📅 Date Range                                         │ │
│  │  ┌─────────────────────────────────────┐              │ │
│  │  │ [This Week ▼]                       │ Quick Preset │ │
│  │  │ ○ Today     ○ This Week             │              │ │
│  │  │ ○ This Month ○ Custom...            │              │ │
│  │  └─────────────────────────────────────┘              │ │
│  │                                                         │ │
│  │  👤 From (Sender)                                      │ │
│  │  ┌─────────────────────────────────────┐              │ │
│  │  │ 🔍 Type to search senders...        │              │ │
│  │  │ Suggestions:                        │              │ │
│  │  │  • github.com (234 emails)          │              │ │
│  │  │  • jameco.com (12 emails)           │              │ │
│  │  └─────────────────────────────────────┘              │ │
│  │                                                         │ │
│  │  [Clear All]              [Apply Filters]              │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
  ↓
Step 3: Select "This Week" preset (single click)
  ↓
Step 4: Type "github" in sender search (auto-suggests)
  ↓
Step 5: Click "Apply Filters" or press Enter
  ↓
┌─────────────────────────────────────────────────────────────┐
│  Results View                                               │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  Active Filters:                                       │ │
│  │  [This Week ×] [github.com ×]  ← Removable chips      │ │
│  │                                                         │ │
│  │  📊 234 emails found                                   │ │
│  │  ┌─────────────────────────────────────────────┐      │ │
│  │  │ Oct 28 | GitHub | Run failed...              │      │ │
│  │  │ Oct 27 | GitHub | PR merged...               │      │ │
│  │  │ Oct 26 | GitHub | New issue...               │      │ │
│  │  └─────────────────────────────────────────────┘      │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

TOTAL CLICKS: 4 (Filter → Preset → Sender → Apply)
ALTERNATIVE: 2 clicks if using search instead
```

### Flow 3: View Email Details

```
USER GOAL: Read an email and see attachments

Current State: User sees email in results table
  ↓
Step 1: Click email subject OR "View" button
  ↓
┌─────────────────────────────────────────────────────────────┐
│  Modal Overlay (Email Viewer)                     [× Close] │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  ┌─────────────────────────────────────────────────┐  │ │
│  │  │  Subject: GitHub Run Failed                     │  │ │
│  │  │  From: GitHub <noreply@github.com>              │  │ │
│  │  │  Date: October 28, 2025 at 8:19 PM              │  │ │
│  │  │  Labels: [INBOX] [IMPORTANT]                    │  │ │
│  │  └─────────────────────────────────────────────────┘  │ │
│  │                                                         │ │
│  │  ┌─────────────────────────────────────────────────┐  │ │
│  │  │  Email Content (scrollable)                     │  │ │
│  │  │  ...                                             │  │ │
│  │  └─────────────────────────────────────────────────┘  │ │
│  │                                                         │ │
│  │  📎 Attachments (2)                                    │ │
│  │  ┌─────────────────────────────────────────────────┐  │ │
│  │  │ 📄 workflow.yml (2.4 KB) [Download]             │  │ │
│  │  │ 📊 report.pdf (156 KB) [Download] [Preview]     │  │ │
│  │  └─────────────────────────────────────────────────┘  │ │
│  │                                                         │ │
│  │  [← Previous Email]  [Next Email →]  [⭐ Star]         │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

KEYBOARD SHORTCUTS:
- ESC: Close modal
- ← / →: Navigate between emails
- S: Star email
- D: Download all attachments

MOBILE VARIATION: Full-screen view with swipe gestures
```

---

## Wireframes

### 1. Landing Page (Desktop)

```
┌────────────────────────────────────────────────────────────────────────┐
│  📧 Email Archive                    [? Help] [⚙️ Settings] [Profile]  │
├────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │  📊 STATISTICS                                [Last updated: Now] │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │ │
│  │  │  39,768  │  │  1,234   │  │    42    │  │  3,456   │         │ │
│  │  │  Emails  │  │  Threads │  │  Domains │  │  Files   │         │ │
│  │  │    ℹ️    │  │    ℹ️     │  │    ℹ️     │  │    ℹ️     │         │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │  SEARCH & FILTERS                                                 │ │
│  │  ┌────────────────────────────────────────────────────────────┐  │ │
│  │  │  🔍 Search emails...                    [Advanced Search]  │  │ │
│  │  └────────────────────────────────────────────────────────────┘  │ │
│  │                                                                    │ │
│  │  Quick Filters:                                                   │ │
│  │  [📅 This Week]  [⭐ Starred]  [📎 With Attachments]  [More...]  │ │
│  │                                                                    │ │
│  │  Active Filters: (None)                           [Clear All]    │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │  EMAILS                                       [Export] [Settings] │ │
│  │  ┌────────────────────────────────────────────────────────────┐  │ │
│  │  │  Views: [📅 By Date] [👤 By Sender] [💬 By Thread]        │  │ │
│  │  │  Sort: [Most Recent ▼]              Display: [50 per page]  │  │ │
│  │  └────────────────────────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────────────────┐   │ │
│  │  │ Date      │ From              │ Subject           │ Actions│  │ │
│  │  ├──────────────────────────────────────────────────────────┤   │ │
│  │  │ Oct 28    │ GitHub            │ Run failed...     │ [View]│  │ │
│  │  │ 8:19 PM   │ noreply@github... │ 📎               │ [⭐]  │  │ │
│  │  ├──────────────────────────────────────────────────────────┤   │ │
│  │  │ Oct 28    │ John Doe          │ Meeting notes     │ [View]│  │ │
│  │  │ 2:15 PM   │ john@company...   │                   │ [⭐]  │  │ │
│  │  ├──────────────────────────────────────────────────────────┤   │ │
│  │  │ Oct 27    │ Adobe Creative... │ See what's new... │ [View]│  │ │
│  │  │ 3:00 PM   │ mail.adobe.com    │ 📎               │ [⭐]  │  │ │
│  │  └──────────────────────────────────────────────────────────┘   │ │
│  │                                                                    │ │
│  │  [← Previous]  Page 1 of 796  [Next →]                           │ │
│  └──────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────┘
```

### 2. Advanced Search Panel

```
┌────────────────────────────────────────────────────────────────┐
│  ADVANCED SEARCH                                     [× Close] │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📅 DATE RANGE                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Quick Presets:                                           │ │
│  │  [Today] [This Week] [This Month] [Last 3 Months]        │ │
│  │                                                            │ │
│  │  Custom Range:                                            │ │
│  │  From: [Oct 1, 2025 ▼]  To: [Oct 28, 2025 ▼]           │ │
│  │  ┌──────────────────────────────────────────────────┐    │ │
│  │  │  S  M  T  W  T  F  S    ← Calendar Picker       │    │ │
│  │  │        1  2  3  4  5                             │    │ │
│  │  │  6  7  8  9 10 11 12                             │    │ │
│  │  │ 13 14 15 16 17 18 19                             │    │ │
│  │  │ 20 21 22 23 24 25 26                             │    │ │
│  │  │ 27 28 29 30 31                                   │    │ │
│  │  └──────────────────────────────────────────────────┘    │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
│  👤 SENDER                                                     │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  🔍 Type to search...                                     │ │
│  │  Recent:                                                  │ │
│  │  ☑️ github.com (234 emails)                               │ │
│  │  ☐ adobe.com (45 emails)                                 │ │
│  │  ☐ in2being.com (12 emails)                              │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
│  🏷️ LABELS                                                     │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  ☑️ INBOX                                                 │ │
│  │  ☐ IMPORTANT                                              │ │
│  │  ☐ UNREAD                                                 │ │
│  │  [+ Show all labels...]                                   │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
│  📎 ATTACHMENTS                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  ○ All emails                                             │ │
│  │  ○ With attachments only                                  │ │
│  │  ○ Without attachments                                    │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
│  🔤 CONTENT SEARCH                                             │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Subject contains: [________________]                     │ │
│  │  Body contains:    [________________]                     │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  💾 Save this search as: [________________]  [Save]      │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
│  [Clear All]                            [Apply Search]         │
└────────────────────────────────────────────────────────────────┘
```

### 3. Email Viewer Modal

```
┌────────────────────────────────────────────────────────────────────┐
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  [← Back to List]                           [× Close]  [ESC] │ │
│  ├──────────────────────────────────────────────────────────────┤ │
│  │  📧 EMAIL DETAILS                                            │ │
│  │  ┌────────────────────────────────────────────────────────┐ │ │
│  │  │  Subject: GitHub Actions - Run Failed: Release Build  │ │ │
│  │  │                                                         │ │ │
│  │  │  From:    GitHub <noreply@github.com>                 │ │ │
│  │  │  To:      David Martel <david@auricleinc.com>         │ │ │
│  │  │  Date:    October 28, 2025 at 8:19 PM                 │ │ │
│  │  │  Labels:  [INBOX] [IMPORTANT] [GITHUB]                │ │ │
│  │  │                                                         │ │ │
│  │  │  Actions: [⭐ Star] [🗂️ Archive] [🏷️ Tag] [↗️ Share]   │ │ │
│  │  └────────────────────────────────────────────────────────┘ │ │
│  │                                                              │ │
│  │  ┌────────────────────────────────────────────────────────┐ │ │
│  │  │  EMAIL CONTENT                                          │ │ │
│  │  │  ┌────────────────────────────────────────────────┐    │ │ │
│  │  │  │                                                 │    │ │ │
│  │  │  │  Your workflow run failed:                     │    │ │ │
│  │  │  │                                                 │    │ │ │
│  │  │  │  Repository: auricle-inc/project               │    │ │ │
│  │  │  │  Workflow: Release Build                       │    │ │ │
│  │  │  │  Branch: main                                   │    │ │ │
│  │  │  │                                                 │    │ │ │
│  │  │  │  Error: Build failed at step 3                 │    │ │ │
│  │  │  │  [View Logs →]                                 │    │ │ │
│  │  │  │                                                 │    │ │ │
│  │  │  │  (Scrollable content area)                     │    │ │ │
│  │  │  │                                                 │    │ │ │
│  │  │  └────────────────────────────────────────────────┘    │ │ │
│  │  └────────────────────────────────────────────────────────┘ │ │
│  │                                                              │ │
│  │  📎 ATTACHMENTS (2)                                         │ │
│  │  ┌────────────────────────────────────────────────────────┐ │ │
│  │  │  📄 workflow.yml           2.4 KB  [Download] [View]   │ │ │
│  │  │  📊 error-report.pdf     156.0 KB  [Download] [View]   │ │ │
│  │  │                                                         │ │ │
│  │  │  [Download All Attachments]                            │ │ │
│  │  └────────────────────────────────────────────────────────┘ │ │
│  │                                                              │ │
│  │  💬 THREAD (3 messages)                                     │ │
│  │  ┌────────────────────────────────────────────────────────┐ │ │
│  │  │  ▼ Oct 28, 8:00 PM - Initial notification             │ │ │
│  │  │  ▼ Oct 28, 8:15 PM - Follow-up                        │ │ │
│  │  │  ▶ Oct 28, 8:19 PM - You are here                     │ │ │
│  │  └────────────────────────────────────────────────────────┘ │ │
│  │                                                              │ │
│  │  [← Previous Email]  [Next Email →]    [🖨️ Print]  [📤 Export]│ │
│  └──────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────┘

KEYBOARD SHORTCUTS:
  ← / →  : Navigate emails     S : Star          A : Archive
  ESC    : Close viewer        P : Print         T : Add tag
```

### 4. Mobile View (375px width)

```
┌─────────────────────────────┐
│  ☰  Email Archive  [?] [⚙️] │
├─────────────────────────────┤
│                              │
│  ┌────────┐  ┌────────┐     │
│  │ 39.7K  │  │ 1,234  │     │
│  │ Emails │  │Threads │     │
│  └────────┘  └────────┘     │
│  [View All Stats →]          │
│                              │
│  ┌─────────────────────────┐│
│  │🔍 Search...             ││
│  └─────────────────────────┘│
│                              │
│  Filters: [None]  [Edit +]  │
│                              │
│  ┌─────────────────────────┐│
│  │ Views:                  ││
│  │ [📅 Date] [👤] [💬]     ││
│  └─────────────────────────┘│
│                              │
│  ┌─────────────────────────┐│
│  │ Oct 28, 8:19 PM         ││
│  │ GitHub                  ││
│  │ Run failed...      📎   ││
│  │ [Tap to view]           ││
│  └─────────────────────────┘│
│                              │
│  ┌─────────────────────────┐│
│  │ Oct 28, 2:15 PM         ││
│  │ John Doe                ││
│  │ Meeting notes           ││
│  │ [Tap to view]           ││
│  └─────────────────────────┘│
│                              │
│  ┌─────────────────────────┐│
│  │ Oct 27, 3:00 PM         ││
│  │ Adobe Creative Cloud    ││
│  │ See what's new...  📎   ││
│  │ [Tap to view]           ││
│  └─────────────────────────┘│
│                              │
│  [← Prev] Page 1/796 [Next→]│
│                              │
└─────────────────────────────┘

MOBILE FILTERS (Bottom Sheet):
┌─────────────────────────────┐
│  Filters          [× Close] │
├─────────────────────────────┤
│                              │
│  📅 Date                     │
│  [This Week ▼]              │
│                              │
│  👤 Sender                   │
│  [All Senders ▼]            │
│                              │
│  🏷️ Labels                   │
│  [All Labels ▼]             │
│                              │
│  📎 Attachments              │
│  [All ▼]                     │
│                              │
│  [Clear]    [Apply Filters] │
└─────────────────────────────┘
```

---

## Component Specifications

### 1. Search Input Component

**States:**
- Default: Gray border, placeholder text
- Focus: Blue border, no placeholder
- Active Search: Show clear button (×)
- With Results: Show result count below
- Error: Red border, error message

**Features:**
- Autocomplete dropdown
- Recent searches
- Search suggestions
- Keyboard navigation (↑↓ Enter)
- Clear button appears on input
- Loading spinner during search

**HTML Structure:**
```html
<div class="search-container">
  <div class="search-input-wrapper">
    <input type="text" placeholder="Search emails..." />
    <button class="search-clear" aria-label="Clear search">×</button>
    <span class="search-icon">🔍</span>
  </div>
  <div class="search-suggestions" role="listbox">
    <!-- Autocomplete suggestions -->
  </div>
  <div class="search-results-count">
    234 emails found
  </div>
</div>
```

**Accessibility:**
- role="combobox" on input
- aria-autocomplete="list"
- aria-expanded for dropdown
- aria-activedescendant for selected suggestion

### 2. Filter Chip Component

**Visual Design:**
- Rounded rectangle
- Light background
- Dark text
- Remove icon (×) on hover
- Hover state: Slightly darker
- Animation: Fade in/out

**HTML Structure:**
```html
<div class="filter-chip" role="button" tabindex="0">
  <span class="chip-label">This Week</span>
  <button class="chip-remove" aria-label="Remove filter">×</button>
</div>
```

**Accessibility:**
- role="button" for keyboard access
- tabindex="0" for focus
- Enter/Space to remove
- Screen reader announces filter

### 3. Date Picker Component

**Features:**
- Calendar popup
- Quick presets (Today, This Week, etc.)
- Month/year navigation
- Date range selection
- Keyboard navigation
- Highlighted today

**States:**
- Closed: Show selected range or "Select dates"
- Open: Calendar visible with navigation
- Selecting: First date selected, awaiting second
- Selected: Range highlighted in calendar

**Accessibility:**
- role="dialog" for calendar
- Arrow keys navigate dates
- Tab navigates controls
- Enter selects date
- ESC closes calendar

### 4. Email Table/List Component

**Desktop Table:**
- Fixed header on scroll
- Sortable columns (click header)
- Row hover highlights
- Click anywhere on row to open
- Checkbox for bulk actions (future)

**Mobile List:**
- Card-based layout
- Swipe for actions
- Tap to expand preview
- Pull to refresh

**Accessibility:**
- role="table" with proper headers
- scope attributes on th elements
- aria-sort on sortable columns
- Keyboard navigation with Tab

### 5. Modal Component

**Features:**
- Overlay background (semi-transparent)
- Centered content
- Close on ESC, overlay click, or × button
- Trap focus within modal
- Restore focus on close
- Smooth fade animation

**Accessibility:**
- role="dialog"
- aria-modal="true"
- aria-labelledby pointing to title
- Focus trap
- ESC key handler

---

## Accessibility (WCAG 2.1 AA Compliance)

### Color Contrast

**Text:**
- Normal text: 4.5:1 minimum
- Large text (18pt+): 3:1 minimum
- Link text: 4.5:1 against background

**Interactive Elements:**
- Buttons: 4.5:1 minimum
- Focus indicators: 3:1 minimum
- Icons: 3:1 minimum (or text alternative)

**Current Colors (to audit):**
- Primary blue: #667eea
- Purple accent: #764ba2
- Text: #333
- Background: #f5f7fa

### Keyboard Navigation

**Global:**
- Tab: Move forward through interactive elements
- Shift+Tab: Move backward
- Enter/Space: Activate buttons/links
- ESC: Close modals/dialogs
- Arrow keys: Navigate lists/calendars

**Search:**
- Tab to search input
- Type to search
- Down arrow: Open suggestions
- Up/Down: Navigate suggestions
- Enter: Select suggestion
- ESC: Close suggestions

**Table:**
- Tab: Enter table
- Arrow keys: Navigate cells
- Enter: Open email
- S: Star email
- A: Archive (future)

**Modal:**
- Tab: Cycle through modal elements only
- ESC: Close modal
- Arrow keys: Navigate to next/previous email

### Screen Reader Support

**Required ARIA Labels:**
- Main navigation: `<nav aria-label="Main navigation">`
- Search: `<form role="search" aria-label="Email search">`
- Stats: `<div role="region" aria-label="Email statistics">`
- Email list: `<table aria-label="Email list">`
- Filters: `<aside aria-label="Filters">`

**Dynamic Content:**
- Search results: `aria-live="polite"` for count updates
- Loading states: `aria-busy="true"` during load
- Errors: `role="alert"` for errors
- Success: Toast with `role="status"`

**Link Purpose:**
- Descriptive link text (not "click here")
- Email subjects as link text
- "View email: [subject]" for screen readers

### Focus Management

**Visible Focus:**
- 2px solid outline
- High contrast color
- Never remove outline
- Ensure visibility on all backgrounds

**Focus Order:**
- Logical tab order (top to bottom, left to right)
- Skip links for main content
- Focus trap in modals
- Return focus after modal close

---

## Responsive Design

### Breakpoints

```css
/* Small phones */
@media (max-width: 374px) {
  /* Minimal layout, single column */
}

/* Phones */
@media (min-width: 375px) and (max-width: 767px) {
  /* Mobile-optimized, bottom sheets */
}

/* Tablets */
@media (min-width: 768px) and (max-width: 1023px) {
  /* 2-column layout where appropriate */
}

/* Desktop */
@media (min-width: 1024px) {
  /* Full multi-column layout */
}

/* Large desktop */
@media (min-width: 1440px) {
  /* Max-width container, more whitespace */
}
```

### Mobile Optimizations

**Touch Targets:**
- Minimum 44x44px (Apple HIG)
- 48x48px preferred (Material Design)
- Adequate spacing between targets

**Navigation:**
- Hamburger menu for secondary actions
- Bottom navigation for primary actions
- Sticky header with search
- Pull-to-refresh for email list

**Interactions:**
- Swipe left/right for next/previous email
- Swipe on email row for quick actions
- Long press for context menu
- Tap to expand, tap again to open

**Layout:**
- Single column for email list
- Full-screen email viewer
- Bottom sheet for filters
- Collapsible statistics

**Typography:**
- Minimum 16px font (avoid zoom on iOS)
- 1.5 line height for readability
- Adequate paragraph spacing

---

## Implementation Plan

### Phase 1: Foundation (Week 1)
- [ ] Create design system components
- [ ] Set up CSS variables for theming
- [ ] Build reusable component library
- [ ] Implement base layouts (desktop/mobile)

### Phase 2: Core Features (Weeks 2-3)
- [ ] Enhanced search with autocomplete
- [ ] Advanced filter panel
- [ ] Date picker component
- [ ] Filter chips
- [ ] Improved email table

### Phase 3: Email Viewer (Week 4)
- [ ] Modal email viewer
- [ ] Next/previous navigation
- [ ] Attachment handling
- [ ] Thread visualization
- [ ] Quick actions

### Phase 4: Help & Onboarding (Week 5)
- [ ] Welcome overlay
- [ ] Interactive tour
- [ ] Contextual help system
- [ ] Tooltips
- [ ] FAQ panel

### Phase 5: Polish (Week 6)
- [ ] Animations and transitions
- [ ] Loading states
- [ ] Error handling
- [ ] Empty states
- [ ] Success messages

### Phase 6: Testing (Week 7)
- [ ] Accessibility audit
- [ ] Keyboard navigation testing
- [ ] Screen reader testing
- [ ] Cross-browser testing
- [ ] Mobile device testing
- [ ] User acceptance testing

### Phase 7: Optimization (Week 8)
- [ ] Performance optimization
- [ ] Code splitting
- [ ] Image optimization
- [ ] Caching strategy
- [ ] Analytics implementation

---

## Success Metrics

### Performance
- First Contentful Paint: <1.5s
- Time to Interactive: <3s
- Search response: <300ms
- Filter application: <200ms
- Modal open: <100ms

### Usability
- Task completion rate: >95%
- Time to first search: <30s
- Filter usage: >60%
- Help usage: <20%
- Error recovery: >90%

### Accessibility
- WCAG 2.1 AA: 100% compliance
- Keyboard navigation: All features accessible
- Screen reader: All content accessible
- Color contrast: All text passes

---

## Next Steps

1. **Prototype:** Build interactive prototype for user testing
2. **Test:** Conduct usability testing with 5-10 users
3. **Iterate:** Refine based on feedback
4. **Develop:** Implement in phases
5. **Monitor:** Track metrics and continuously improve
