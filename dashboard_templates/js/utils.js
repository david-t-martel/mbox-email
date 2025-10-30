/**
 * Utility Functions for Email Archive Dashboard
 * Shared utilities used across the application
 */

// ============================================
// Date & Time Utilities
// ============================================

/**
 * Format date for display
 * @param {Date|string} date - Date to format
 * @returns {string} Formatted date string
 */
function formatDate(date) {
  if (!date) return 'Unknown';

  const d = new Date(date);
  if (isNaN(d.getTime())) return 'Invalid Date';

  const options = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  };

  return d.toLocaleDateString('en-US', options);
}

/**
 * Format date and time for display
 * @param {Date|string} date - Date to format
 * @returns {string} Formatted date and time string
 */
function formatDateTime(date) {
  if (!date) return 'Unknown';

  const d = new Date(date);
  if (isNaN(d.getTime())) return 'Invalid Date';

  const options = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
  };

  return d.toLocaleDateString('en-US', options);
}

/**
 * Get relative time (e.g., "2 hours ago")
 * @param {Date|string} date - Date to compare
 * @returns {string} Relative time string
 */
function getRelativeTime(date) {
  if (!date) return 'Unknown';

  const d = new Date(date);
  if (isNaN(d.getTime())) return 'Invalid Date';

  const now = new Date();
  const seconds = Math.floor((now - d) / 1000);

  const intervals = {
    year: 31536000,
    month: 2592000,
    week: 604800,
    day: 86400,
    hour: 3600,
    minute: 60,
  };

  for (const [unit, secondsInUnit] of Object.entries(intervals)) {
    const interval = Math.floor(seconds / secondsInUnit);
    if (interval >= 1) {
      return interval === 1
        ? `1 ${unit} ago`
        : `${interval} ${unit}s ago`;
    }
  }

  return 'Just now';
}

// ============================================
// String Utilities
// ============================================

/**
 * Truncate string to specified length
 * @param {string} str - String to truncate
 * @param {number} maxLength - Maximum length
 * @returns {string} Truncated string
 */
function truncate(str, maxLength = 50) {
  if (!str) return '';
  if (str.length <= maxLength) return str;
  return str.substring(0, maxLength - 3) + '...';
}

/**
 * Escape HTML to prevent XSS
 * @param {string} str - String to escape
 * @returns {string} Escaped string
 */
function escapeHtml(str) {
  if (!str) return '';

  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

/**
 * Highlight search terms in text
 * @param {string} text - Text to highlight
 * @param {string} searchTerm - Term to highlight
 * @returns {string} HTML with highlighted terms
 */
function highlightSearchTerm(text, searchTerm) {
  if (!text || !searchTerm) return escapeHtml(text);

  const escapedText = escapeHtml(text);
  const escapedTerm = escapeHtml(searchTerm);

  const regex = new RegExp(`(${escapedTerm})`, 'gi');
  return escapedText.replace(regex, '<mark>$1</mark>');
}

/**
 * Convert string to kebab-case
 * @param {string} str - String to convert
 * @returns {string} Kebab-case string
 */
function toKebabCase(str) {
  return str
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
}

// ============================================
// Array & Object Utilities
// ============================================

/**
 * Deep clone an object
 * @param {*} obj - Object to clone
 * @returns {*} Cloned object
 */
function deepClone(obj) {
  return JSON.parse(JSON.stringify(obj));
}

/**
 * Group array items by key
 * @param {Array} array - Array to group
 * @param {string} key - Key to group by
 * @returns {Object} Grouped object
 */
function groupBy(array, key) {
  return array.reduce((result, item) => {
    const group = item[key];
    if (!result[group]) {
      result[group] = [];
    }
    result[group].push(item);
    return result;
  }, {});
}

/**
 * Sort array by multiple keys
 * @param {Array} array - Array to sort
 * @param {string} key - Key to sort by
 * @param {string} direction - 'asc' or 'desc'
 * @returns {Array} Sorted array
 */
function sortBy(array, key, direction = 'asc') {
  const sorted = [...array].sort((a, b) => {
    let valA = a[key];
    let valB = b[key];

    // Handle dates
    if (key === 'date' || key.includes('date')) {
      valA = new Date(valA).getTime();
      valB = new Date(valB).getTime();
    }

    // Handle strings (case-insensitive)
    if (typeof valA === 'string') {
      valA = valA.toLowerCase();
      valB = valB.toLowerCase();
    }

    if (valA < valB) return direction === 'asc' ? -1 : 1;
    if (valA > valB) return direction === 'asc' ? 1 : -1;
    return 0;
  });

  return sorted;
}

// ============================================
// DOM Utilities
// ============================================

/**
 * Create element with attributes
 * @param {string} tag - Element tag
 * @param {Object} attributes - Element attributes
 * @param {string} content - Element content
 * @returns {HTMLElement} Created element
 */
function createElement(tag, attributes = {}, content = '') {
  const element = document.createElement(tag);

  Object.entries(attributes).forEach(([key, value]) => {
    if (key === 'className') {
      element.className = value;
    } else if (key === 'dataset') {
      Object.entries(value).forEach(([dataKey, dataValue]) => {
        element.dataset[dataKey] = dataValue;
      });
    } else if (key.startsWith('aria-') || key.startsWith('data-')) {
      element.setAttribute(key, value);
    } else {
      element[key] = value;
    }
  });

  if (content) {
    element.innerHTML = content;
  }

  return element;
}

/**
 * Get element(s) safely
 * @param {string} selector - CSS selector
 * @param {boolean} multiple - Return all matches
 * @returns {HTMLElement|NodeList|null} Element(s) or null
 */
function $(selector, multiple = false) {
  return multiple
    ? document.querySelectorAll(selector)
    : document.querySelector(selector);
}

/**
 * Add event listener with delegation
 * @param {string} selector - CSS selector
 * @param {string} event - Event name
 * @param {Function} handler - Event handler
 * @param {HTMLElement} parent - Parent element (default: document)
 */
function delegate(selector, event, handler, parent = document) {
  parent.addEventListener(event, (e) => {
    const target = e.target.closest(selector);
    if (target) {
      handler.call(target, e);
    }
  });
}

/**
 * Debounce function calls
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in ms
 * @returns {Function} Debounced function
 */
function debounce(func, wait = 300) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/**
 * Throttle function calls
 * @param {Function} func - Function to throttle
 * @param {number} limit - Limit time in ms
 * @returns {Function} Throttled function
 */
function throttle(func, limit = 300) {
  let inThrottle;
  return function executedFunction(...args) {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

// ============================================
// Accessibility Utilities
// ============================================

/**
 * Trap focus within element (for modals)
 * @param {HTMLElement} element - Element to trap focus in
 * @returns {Function} Cleanup function
 */
function trapFocus(element) {
  const focusableElements = element.querySelectorAll(
    'a[href], button:not([disabled]), textarea:not([disabled]), ' +
    'input:not([disabled]), select:not([disabled]), ' +
    '[tabindex]:not([tabindex="-1"])'
  );

  const firstFocusable = focusableElements[0];
  const lastFocusable = focusableElements[focusableElements.length - 1];

  const handleKeydown = (e) => {
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
  };

  element.addEventListener('keydown', handleKeydown);

  // Focus first element
  firstFocusable?.focus();

  // Return cleanup function
  return () => {
    element.removeEventListener('keydown', handleKeydown);
  };
}

/**
 * Announce message to screen readers
 * @param {string} message - Message to announce
 * @param {string} priority - 'polite' or 'assertive'
 */
function announceToScreenReader(message, priority = 'polite') {
  const announcement = createElement('div', {
    role: priority === 'assertive' ? 'alert' : 'status',
    'aria-live': priority,
    'aria-atomic': 'true',
    className: 'sr-only',
  }, message);

  document.body.appendChild(announcement);

  // Remove after announcement
  setTimeout(() => {
    announcement.remove();
  }, 1000);
}

// ============================================
// Local Storage Utilities
// ============================================

/**
 * Save to local storage
 * @param {string} key - Storage key
 * @param {*} value - Value to store
 */
function saveToStorage(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch (e) {
    console.error('Failed to save to localStorage:', e);
  }
}

/**
 * Load from local storage
 * @param {string} key - Storage key
 * @param {*} defaultValue - Default value if not found
 * @returns {*} Stored value or default
 */
function loadFromStorage(key, defaultValue = null) {
  try {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : defaultValue;
  } catch (e) {
    console.error('Failed to load from localStorage:', e);
    return defaultValue;
  }
}

/**
 * Remove from local storage
 * @param {string} key - Storage key
 */
function removeFromStorage(key) {
  try {
    localStorage.removeItem(key);
  } catch (e) {
    console.error('Failed to remove from localStorage:', e);
  }
}

// ============================================
// URL Utilities
// ============================================

/**
 * Get URL parameters
 * @returns {Object} URL parameters as object
 */
function getUrlParams() {
  const params = new URLSearchParams(window.location.search);
  const result = {};

  for (const [key, value] of params.entries()) {
    result[key] = value;
  }

  return result;
}

/**
 * Update URL without reload
 * @param {Object} params - Parameters to update
 */
function updateUrl(params) {
  const url = new URL(window.location);

  Object.entries(params).forEach(([key, value]) => {
    if (value === null || value === undefined || value === '') {
      url.searchParams.delete(key);
    } else {
      url.searchParams.set(key, value);
    }
  });

  window.history.pushState({}, '', url);
}

// ============================================
// Validation Utilities
// ============================================

/**
 * Validate email address
 * @param {string} email - Email to validate
 * @returns {boolean} Is valid email
 */
function isValidEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

/**
 * Validate URL
 * @param {string} url - URL to validate
 * @returns {boolean} Is valid URL
 */
function isValidUrl(url) {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
}

// ============================================
// Performance Utilities
// ============================================

/**
 * Lazy load images
 * @param {string} selector - Image selector
 */
function lazyLoadImages(selector = 'img[data-src]') {
  const images = document.querySelectorAll(selector);

  const imageObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        img.removeAttribute('data-src');
        imageObserver.unobserve(img);
      }
    });
  });

  images.forEach((img) => imageObserver.observe(img));
}

/**
 * Measure performance
 * @param {string} name - Performance mark name
 * @param {Function} func - Function to measure
 * @returns {*} Function result
 */
async function measurePerformance(name, func) {
  performance.mark(`${name}-start`);
  const result = await func();
  performance.mark(`${name}-end`);
  performance.measure(name, `${name}-start`, `${name}-end`);

  const measure = performance.getEntriesByName(name)[0];
  console.log(`${name} took ${measure.duration.toFixed(2)}ms`);

  return result;
}

// ============================================
// Export for ES6 modules (if needed)
// ============================================

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    // Date & Time
    formatDate,
    formatDateTime,
    getRelativeTime,

    // String
    truncate,
    escapeHtml,
    highlightSearchTerm,
    toKebabCase,

    // Array & Object
    deepClone,
    groupBy,
    sortBy,

    // DOM
    createElement,
    $,
    delegate,
    debounce,
    throttle,

    // Accessibility
    trapFocus,
    announceToScreenReader,

    // Storage
    saveToStorage,
    loadFromStorage,
    removeFromStorage,

    // URL
    getUrlParams,
    updateUrl,

    // Validation
    isValidEmail,
    isValidUrl,

    // Performance
    lazyLoadImages,
    measurePerformance,
  };
}
