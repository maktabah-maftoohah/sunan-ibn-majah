/**
 * Maktabah Maftoohah Sunan Ibn Majah - Analytics Module (analytics.js)
 * Google Tag Manager (GTM) and Google Analytics 4 (GA4) integration
 * with SPA virtual pageview tracking and specialized Hadith metrics.
 */

const DEFAULT_CONTAINER_ID = 'GTM-XXXXXXXX';

class AnalyticsService {
  constructor() {
    this.initialized = false;
    this.containerId = null;
    this.lastTrackedPath = null;
  }

  getContainerId() {
    try {
      const stored = localStorage.getItem('maktabah_ga_id');
      if (stored && stored.trim()) return stored.trim();
    } catch {
      // ignore
    }
    return DEFAULT_CONTAINER_ID;
  }

  init(customId = null) {
    if (this.initialized) return;

    this.containerId = customId || this.getContainerId();

    if (!this.containerId || this.containerId === 'GTM-XXXXXXXX' || this.containerId === 'G-XXXXXXXXXX') {
      return;
    }

    if (typeof navigator !== 'undefined') {
      const dnt = navigator.doNotTrack || window.doNotTrack || navigator.msDoNotTrack;
      if (dnt === '1' || dnt === 'yes') {
        return;
      }
    }

    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function() {
      window.dataLayer.push(arguments);
    };

    window.gtag('js', new Date());

    if (this.containerId.startsWith('GTM-')) {
      const script = document.createElement('script');
      script.async = true;
      script.src = `https://www.googletagmanager.com/gtm.js?id=${this.containerId}`;
      document.head.appendChild(script);
    } else if (this.containerId.startsWith('G-')) {
      const script = document.createElement('script');
      script.async = true;
      script.src = `https://www.googletagmanager.com/gtag/js?id=${this.containerId}`;
      document.head.appendChild(script);
      window.gtag('config', this.containerId, { send_page_view: false });
    }

    this.initialized = true;
  }

  pageview(path = null, title = null) {
    if (!this.initialized) return;

    const currentPath = path || window.location.pathname + window.location.search + window.location.hash;
    const currentTitle = title || document.title;

    if (this.lastTrackedPath === currentPath) return;
    this.lastTrackedPath = currentPath;

    window.dataLayer.push({
      event: 'virtual_pageview',
      page_path: currentPath,
      page_title: currentTitle,
      timestamp: new Date().toISOString()
    });
  }

  event(eventName, params = {}) {
    if (!this.initialized) return;

    window.dataLayer.push({
      event: eventName,
      ...params,
      timestamp: new Date().toISOString()
    });
  }

  trackHadithView(hadithNumber, bookNumber, numberingSystem = 'abdul_baqi') {
    this.event('hadith_view', {
      hadith_number: hadithNumber,
      book_number: bookNumber,
      numbering_system: numberingSystem
    });
  }
}

export const analytics = new AnalyticsService();
