# WCAG 2.1 AA Accessibility Compliance Guide

## Overview

This document provides comprehensive guidance for ensuring the Mail Parser Dashboard meets WCAG 2.1 Level AA accessibility standards, making it usable by people with diverse abilities.

## Table of Contents

1. [Perceivable](#perceivable)
2. [Operable](#operable)
3. [Understandable](#understandable)
4. [Robust](#robust)
5. [Testing Checklist](#testing-checklist)
6. [Common Issues & Fixes](#common-issues--fixes)

---

## Perceivable

Information and user interface components must be presentable to users in ways they can perceive.

### 1.1 Text Alternatives

**Guideline:** Provide text alternatives for non-text content.

#### Implementation

```html
<!-- Images -->
<img src="icon.png" alt="Email attachment icon">

<!-- Decorative images -->
<img src="decoration.png" alt="" aria-hidden="true">

<!-- Icons in buttons -->
<button aria-label="Close">
  <span aria-hidden="true">×</span>
</button>

<!-- Complex images -->
<img src="chart.png" alt="Email volume chart showing increase over time"
     longdesc="chart-description.html">
```

**Checklist:**
- [ ] All functional images have alt text
- [ ] Decorative images have empty alt (`alt=""`)
- [ ] Icons have text alternatives
- [ ] Charts/graphs have detailed descriptions
- [ ] Form buttons have accessible names

### 1.2 Time-based Media

**Guideline:** Provide alternatives for time-based media (audio, video).

#### Implementation

```html
<!-- Video with captions -->
<video controls>
  <source src="tutorial.mp4" type="video/mp4">
  <track kind="captions" src="captions.vtt" srclang="en" label="English">
  Your browser doesn't support video.
</video>

<!-- Audio transcript -->
<audio controls>
  <source src="announcement.mp3" type="audio/mpeg">
</audio>
<p><a href="transcript.html">Read transcript</a></p>
```

**Not applicable to current dashboard** (no audio/video content)

### 1.3 Adaptable

**Guideline:** Create content that can be presented in different ways without losing information or structure.

#### Implementation

```html
<!-- Semantic HTML structure -->
<header role="banner">
  <h1>Email Archive</h1>
</header>

<nav role="navigation" aria-label="Main navigation">
  <!-- Navigation items -->
</nav>

<main role="main" id="main-content">
  <section aria-label="Search and filters">
    <!-- Search UI -->
  </section>

  <section aria-label="Email list">
    <table role="table" aria-label="Emails">
      <thead>
        <tr>
          <th scope="col">Date</th>
          <th scope="col">From</th>
          <th scope="col">Subject</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Oct 28</td>
          <td>John Doe</td>
          <td>Meeting notes</td>
        </tr>
      </tbody>
    </table>
  </section>
</main>

<aside role="complementary" aria-label="Help panel">
  <!-- Help content -->
</aside>
```

**Checklist:**
- [ ] Semantic HTML elements used correctly
- [ ] ARIA landmarks for page regions
- [ ] Heading hierarchy is logical (h1 → h2 → h3)
- [ ] Lists use `<ul>`, `<ol>`, `<dl>`
- [ ] Tables have proper headers (`<th scope="col">`)
- [ ] Reading order matches visual order
- [ ] Responsive design maintains content order

### 1.4 Distinguishable

**Guideline:** Make it easier for users to see and hear content, including separating foreground from background.

#### Color Contrast Requirements

**Normal Text:** 4.5:1 minimum
**Large Text (18pt or 14pt bold):** 3:1 minimum
**UI Components:** 3:1 minimum

#### Color Palette (WCAG AA Compliant)

```css
/* Text on white background */
--color-text: #1a1a1a;          /* 15.3:1 - Excellent */
--color-text-secondary: #555555; /* 7.4:1 - Good */
--color-text-muted: #777777;     /* 4.7:1 - Pass AA */

/* Interactive elements */
--color-primary: #667eea;        /* 4.6:1 on white - Pass AA */
--color-primary-dark: #5568d3;   /* 5.8:1 on white - Pass AA */

/* Status colors on white */
--color-success: #10b981;        /* 3.6:1 - Pass AA for large text */
--color-error: #ef4444;          /* 4.5:1 - Pass AA */
```

#### Implementation

```css
/* Good contrast */
.button {
  background-color: #667eea;
  color: #ffffff;
  /* Contrast ratio: 4.6:1 ✓ */
}

/* Focus indicator */
:focus-visible {
  outline: 2px solid #667eea;
  outline-offset: 2px;
  /* Contrast ratio vs background: 3:1 minimum ✓ */
}

/* Error message */
.error {
  color: #c92a2a;
  background-color: #fff5f5;
  border: 1px solid #ef4444;
  /* Text contrast: 7.3:1 ✓ */
}
```

**Checklist:**
- [ ] All text meets 4.5:1 contrast (or 3:1 for large text)
- [ ] UI components meet 3:1 contrast
- [ ] Focus indicators are visible (3:1 contrast)
- [ ] Color is not the only way to convey information
- [ ] Text can be resized to 200% without loss of content
- [ ] No horizontal scrolling at 320px width
- [ ] Spacing between UI elements is adequate

#### Non-color Information

```html
<!-- Bad: Color only -->
<span style="color: red;">Error</span>

<!-- Good: Color + icon + text -->
<span class="error-message" role="alert">
  <span aria-hidden="true">⚠️</span>
  Error: Email not found
</span>

<!-- Bad: Color-coded labels -->
<span class="green-label">Success</span>

<!-- Good: Explicit text -->
<span class="status-label">
  <span aria-hidden="true">✓</span>
  Status: Complete
</span>
```

---

## Operable

User interface components and navigation must be operable.

### 2.1 Keyboard Accessible

**Guideline:** Make all functionality available from a keyboard.

#### Keyboard Navigation Pattern

```
Tab          - Move to next interactive element
Shift+Tab    - Move to previous interactive element
Enter/Space  - Activate button or link
Arrow keys   - Navigate within component (list, menu, tabs)
Escape       - Close modal or cancel operation
/            - Focus search (custom shortcut)
```

#### Implementation

```html
<!-- All interactive elements must be keyboard accessible -->
<button onclick="openEmail()">View Email</button>  ✓
<div onclick="openEmail()">View Email</div>        ✗

<!-- Custom interactive elements need tabindex -->
<div role="button" tabindex="0" onclick="action()"
     onkeydown="if(event.key==='Enter')action()">
  Click me
</div>

<!-- Skip navigation -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<!-- Focus trap in modal -->
<div role="dialog" aria-modal="true">
  <button id="firstFocusable">Close</button>
  <!-- Content -->
  <button id="lastFocusable">Submit</button>
</div>
```

**JavaScript for Focus Trap:**

```javascript
function trapFocus(element) {
  const focusableElements = element.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const firstFocusable = focusableElements[0];
  const lastFocusable = focusableElements[focusableElements.length - 1];

  element.addEventListener('keydown', function(e) {
    if (e.key === 'Tab') {
      if (e.shiftKey) {
        if (document.activeElement === firstFocusable) {
          lastFocusable.focus();
          e.preventDefault();
        }
      } else {
        if (document.activeElement === lastFocusable) {
          firstFocusable.focus();
          e.preventDefault();
        }
      }
    }
  });
}
```

**Checklist:**
- [ ] All functionality works with keyboard only
- [ ] Tab order is logical
- [ ] Focus is visible (not `outline: none`)
- [ ] No keyboard traps (can Tab out of all elements)
- [ ] Modal dialogs trap focus
- [ ] Skip links available
- [ ] Custom shortcuts don't conflict with screen readers

### 2.2 Enough Time

**Guideline:** Provide users enough time to read and use content.

#### Implementation

```javascript
// No automatic timeouts for essential tasks
// If timeout needed, provide warning

function startSession() {
  // Warn before timeout
  setTimeout(() => {
    showWarning("Your session will expire in 2 minutes");
  }, 18 * 60 * 1000); // 18 minutes

  // Allow extension
  setTimeout(() => {
    if (confirm("Extend session?")) {
      startSession(); // Reset timer
    }
  }, 20 * 60 * 1000); // 20 minutes
}
```

**For Mail Parser Dashboard:**
- No session timeouts (static content)
- Search operations have reasonable timeouts (30s+)
- Loading indicators show progress
- No auto-refresh without user control

**Checklist:**
- [ ] No time limits on essential tasks
- [ ] Timeouts can be turned off or extended
- [ ] Users warned before timeout
- [ ] Auto-updating content can be paused

### 2.3 Seizures and Physical Reactions

**Guideline:** Do not design content in a way that is known to cause seizures or physical reactions.

#### Implementation

```css
/* Avoid rapid flashing */
@keyframes safe-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

/* Duration > 333ms (less than 3 flashes per second) */
.loading-indicator {
  animation: safe-pulse 2s ease-in-out infinite;
}

/* No rapidly changing colors */
/* No large bright flashing areas */
```

**Checklist:**
- [ ] No content flashes more than 3 times per second
- [ ] Animations can be paused or disabled
- [ ] Respects `prefers-reduced-motion` setting

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### 2.4 Navigable

**Guideline:** Provide ways to help users navigate, find content, and determine where they are.

#### Implementation

```html
<!-- Page title -->
<title>Email Archive - Search Results</title>

<!-- Descriptive link text -->
<a href="email.html">Read email from John Doe about project update</a>
<!-- Not: <a href="email.html">Click here</a> -->

<!-- Breadcrumb navigation -->
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/emails">Emails</a></li>
    <li aria-current="page">Search Results</li>
  </ol>
</nav>

<!-- Heading structure -->
<h1>Email Archive</h1>
  <h2>Search and Filter</h2>
  <h2>Email List</h2>
    <h3>October 2025</h3>

<!-- Multiple ways to find content -->
<!-- 1. Search -->
<!-- 2. Filter by date -->
<!-- 3. Filter by sender -->
<!-- 4. Browse by thread -->
```

**Checklist:**
- [ ] Page has descriptive title
- [ ] Focus order is logical
- [ ] Link purpose clear from link text
- [ ] Multiple ways to find pages
- [ ] Headings and labels are descriptive
- [ ] Current location is indicated
- [ ] Keyboard focus is visible

### 2.5 Input Modalities

**Guideline:** Make it easier for users to operate functionality through various inputs beyond keyboard.

#### Implementation

```html
<!-- Touch targets minimum 44x44px -->
<button style="min-width: 44px; min-height: 44px;">
  Open
</button>

<!-- Pointer cancellation -->
<button onmousedown="startAction()"
        onmouseup="completeAction()"
        onmouseleave="cancelAction()">
  <!-- Action completes on mouseup, can be cancelled -->
</button>

<!-- Label for input -->
<label for="search">Search emails</label>
<input type="text" id="search">

<!-- Motion actuation alternative -->
<!-- If shake-to-refresh exists -->
<button onclick="refresh()">Refresh</button>
```

**Checklist:**
- [ ] Touch targets at least 44x44px
- [ ] Actions can be cancelled before completion
- [ ] Labels visible for all inputs
- [ ] Motion/gesture alternatives provided

---

## Understandable

Information and the operation of user interface must be understandable.

### 3.1 Readable

**Guideline:** Make text content readable and understandable.

#### Implementation

```html
<!-- Language of page -->
<html lang="en">

<!-- Language of parts -->
<p>The conference will be held in <span lang="fr">Paris</span>.</p>

<!-- Unusual words explained -->
<p>We use <abbr title="Model Context Protocol">MCP</abbr> servers.</p>

<!-- Pronunciation -->
<p>Lead <span role="text">
  <span aria-label="the metal">lead</span>
</span> vs. <span role="text">
  <span aria-label="to guide">lead</span>
</span></p>
```

**Checklist:**
- [ ] Page language is declared
- [ ] Language changes are marked
- [ ] Abbreviations explained on first use
- [ ] Reading level appropriate for audience
- [ ] Unusual words have definitions

### 3.2 Predictable

**Guideline:** Make Web pages appear and operate in predictable ways.

#### Implementation

```html
<!-- Consistent navigation -->
<header>
  <nav aria-label="Main navigation">
    <!-- Same navigation on every page -->
  </nav>
</header>

<!-- No automatic context changes on focus -->
<select onchange="navigate()" <!-- Bad: Changes on focus -->
        onblur="navigate()">   <!-- Better: User must confirm -->

<!-- Forms with clear submission -->
<form onsubmit="handleSubmit()">
  <input type="text" name="search">
  <button type="submit">Search</button> <!-- Clear submit action -->
</form>

<!-- Consistent identification -->
<!-- Search icon always means search -->
<button aria-label="Search">🔍</button>
```

**Checklist:**
- [ ] Navigation is consistent across pages
- [ ] Components work consistently
- [ ] Focus doesn't cause unexpected changes
- [ ] Input doesn't cause unexpected changes (unless warned)
- [ ] Consistent component identification

### 3.3 Input Assistance

**Guideline:** Help users avoid and correct mistakes.

#### Implementation

```html
<!-- Error identification -->
<form>
  <label for="email">Email Address</label>
  <input type="email" id="email" aria-invalid="true"
         aria-describedby="email-error">
  <span id="email-error" role="alert">
    Error: Please enter a valid email address (e.g., user@example.com)
  </span>
</form>

<!-- Labels and instructions -->
<label for="password">
  Password
  <span class="required" aria-label="required">*</span>
</label>
<span id="password-help">
  Must be at least 8 characters with one number
</span>
<input type="password" id="password"
       aria-describedby="password-help"
       required>

<!-- Error suggestions -->
<div role="alert">
  <p>Error: No emails found for "github.co"</p>
  <p>Did you mean <a href="?q=github.com">github.com</a>?</p>
</div>

<!-- Confirmation for important actions -->
<button onclick="if(confirm('Delete all emails?'))deleteAll()">
  Delete All
</button>

<!-- Reversible actions -->
<button onclick="deleteEmail()">Delete</button>
<button onclick="undoDelete()" style="display:none">Undo</button>
```

**Checklist:**
- [ ] Errors are identified in text
- [ ] Labels or instructions provided
- [ ] Error suggestions offered
- [ ] Important actions can be reversed, checked, or confirmed
- [ ] Form validation provides helpful messages

---

## Robust

Content must be robust enough that it can be interpreted by a wide variety of user agents, including assistive technologies.

### 4.1 Compatible

**Guideline:** Maximize compatibility with current and future user agents, including assistive technologies.

#### Implementation

```html
<!-- Valid HTML -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Page Title</title>
</head>
<body>
  <!-- Well-formed markup -->
  <div>
    <p>Paragraph</p>
  </div>
</body>
</html>

<!-- Unique IDs -->
<label for="search">Search</label>
<input type="text" id="search"> <!-- Each ID used once -->

<!-- Name, Role, Value -->
<button role="button" aria-pressed="false" onclick="toggle()">
  Toggle
</button>

<!-- Status messages -->
<div role="status" aria-live="polite">
  Loading emails...
</div>

<div role="alert" aria-live="assertive">
  Error: Connection failed
</div>
```

**ARIA Roles:**

```html
<!-- Landmark roles -->
<header role="banner">...</header>
<nav role="navigation">...</nav>
<main role="main">...</main>
<aside role="complementary">...</aside>
<footer role="contentinfo">...</footer>

<!-- Widget roles -->
<div role="button" tabindex="0">Custom Button</div>
<div role="dialog" aria-modal="true">Modal</div>
<div role="tablist">
  <button role="tab" aria-selected="true">Tab 1</button>
</div>

<!-- Live region roles -->
<div role="alert">Error!</div>
<div role="status">Loading...</div>
<div role="log">Activity feed...</div>
```

**Checklist:**
- [ ] HTML validates
- [ ] All IDs are unique
- [ ] ARIA used correctly (no invalid combinations)
- [ ] Status messages announced to screen readers
- [ ] Name, role, value accessible for all components
- [ ] No parsing errors

---

## Testing Checklist

### Automated Testing

**Tools:**
- axe DevTools (browser extension)
- WAVE (browser extension)
- Lighthouse (Chrome DevTools)
- pa11y (command-line)

**Run automated tests:**
```bash
# Install pa11y
npm install -g pa11y

# Test page
pa11y http://localhost:8000/index.html

# Test with specific standard
pa11y --standard WCAG2AA http://localhost:8000/index.html
```

### Manual Testing

#### Keyboard Testing
1. [ ] Unplug mouse
2. [ ] Navigate entire site with Tab/Shift+Tab
3. [ ] Activate all controls with Enter/Space
4. [ ] Use arrow keys in custom controls
5. [ ] Verify focus is always visible
6. [ ] Ensure no keyboard traps

#### Screen Reader Testing

**NVDA (Windows - Free)**
1. [ ] Install NVDA
2. [ ] Navigate with Tab
3. [ ] Read content with arrows
4. [ ] Verify all content announced
5. [ ] Verify landmarks work (D key)
6. [ ] Verify headings work (H key)
7. [ ] Verify forms work (F key)

**VoiceOver (macOS - Built-in)**
1. [ ] Enable VoiceOver (Cmd+F5)
2. [ ] Navigate with VO+arrows
3. [ ] Use rotor (VO+U)
4. [ ] Verify all content announced
5. [ ] Verify controls work

**Commands:**
- Read next: Down arrow
- Read previous: Up arrow
- Next heading: H
- Next link: Tab
- Next form field: F
- List landmarks: D

#### Color Contrast Testing

**Tools:**
- Chrome DevTools (Inspect > Accessibility)
- Colour Contrast Analyser app
- WebAIM Contrast Checker

**Steps:**
1. [ ] Test all text colors
2. [ ] Test all button colors
3. [ ] Test all focus indicators
4. [ ] Test all icons
5. [ ] Take screenshot
6. [ ] Convert to grayscale
7. [ ] Verify still usable

#### Mobile Testing
1. [ ] Test on real iOS device
2. [ ] Test on real Android device
3. [ ] Enable VoiceOver/TalkBack
4. [ ] Navigate with gestures
5. [ ] Verify touch targets (44px+)
6. [ ] Test landscape orientation

---

## Common Issues & Fixes

### Issue: Low Color Contrast

**Problem:**
```css
.button {
  background: #8c9eff;
  color: #ffffff;
  /* Contrast ratio: 3.4:1 ✗ */
}
```

**Fix:**
```css
.button {
  background: #667eea;
  color: #ffffff;
  /* Contrast ratio: 4.6:1 ✓ */
}
```

### Issue: Missing Alt Text

**Problem:**
```html
<img src="icon.png">
```

**Fix:**
```html
<!-- Functional image -->
<img src="icon.png" alt="Email attachment icon">

<!-- Decorative image -->
<img src="icon.png" alt="" aria-hidden="true">
```

### Issue: Div Buttons

**Problem:**
```html
<div onclick="submit()">Submit</div>
```

**Fix:**
```html
<button onclick="submit()">Submit</button>

<!-- If must use div -->
<div role="button" tabindex="0"
     onclick="submit()"
     onkeydown="if(event.key==='Enter')submit()">
  Submit
</div>
```

### Issue: No Focus Indicator

**Problem:**
```css
button:focus {
  outline: none; /* ✗ */
}
```

**Fix:**
```css
button:focus-visible {
  outline: 2px solid #667eea;
  outline-offset: 2px;
}
```

### Issue: Unclear Link Text

**Problem:**
```html
<a href="email.html">Click here</a>
```

**Fix:**
```html
<a href="email.html">Read email from John Doe</a>

<!-- Or -->
<a href="email.html">
  Click here
  <span class="sr-only">to read email from John Doe</span>
</a>
```

### Issue: Form Without Labels

**Problem:**
```html
<input type="text" placeholder="Search">
```

**Fix:**
```html
<label for="search">Search emails</label>
<input type="text" id="search" placeholder="Search">

<!-- Or -->
<input type="text" aria-label="Search emails" placeholder="Search">
```

### Issue: Table Without Headers

**Problem:**
```html
<table>
  <tr>
    <td>Date</td>
    <td>From</td>
  </tr>
</table>
```

**Fix:**
```html
<table>
  <thead>
    <tr>
      <th scope="col">Date</th>
      <th scope="col">From</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Oct 28</td>
      <td>John Doe</td>
    </tr>
  </tbody>
</table>
```

---

## Resources

### Official Guidelines
- [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
- [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)

### Testing Tools
- [axe DevTools](https://www.deque.com/axe/devtools/)
- [WAVE](https://wave.webaim.org/)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [Colour Contrast Analyser](https://www.tpgi.com/color-contrast-checker/)

### Screen Readers
- [NVDA](https://www.nvaccess.org/) (Windows, free)
- [JAWS](https://www.freedomscientific.com/products/software/jaws/) (Windows)
- VoiceOver (macOS/iOS, built-in)
- TalkBack (Android, built-in)

### Validation
- [W3C HTML Validator](https://validator.w3.org/)
- [W3C CSS Validator](https://jigsaw.w3.org/css-validator/)

---

## Certification

To claim WCAG 2.1 AA compliance:

1. [ ] Complete all automated tests (0 errors)
2. [ ] Complete all manual tests (100% pass)
3. [ ] Test with screen readers (NVDA + VoiceOver)
4. [ ] Test with keyboard only (100% functional)
5. [ ] Test color contrast (all 4.5:1+)
6. [ ] Test on mobile devices (iOS + Android)
7. [ ] Document any exceptions
8. [ ] Create accessibility statement
9. [ ] Provide feedback mechanism
10. [ ] Commit to ongoing monitoring

## Accessibility Statement Template

```markdown
# Accessibility Statement

We are committed to ensuring digital accessibility for people with disabilities.
We are continually improving the user experience for everyone and applying the
relevant accessibility standards.

## Conformance Status

The Email Archive Dashboard is fully conformant with WCAG 2.1 Level AA.

## Feedback

We welcome your feedback on the accessibility of this application. Please let
us know if you encounter accessibility barriers:

- Email: accessibility@example.com
- Phone: (555) 123-4567

We try to respond to feedback within 2 business days.

## Date

This statement was created on [DATE] using guidance from the W3C.
```

---

**Remember:** Accessibility is not a checklist—it's an ongoing commitment to inclusive design.
