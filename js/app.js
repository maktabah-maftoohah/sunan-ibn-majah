/**
 * Maktabah Maftoohah Sunan Ibn Majah - Reader Application
 * Zero-Build Vanilla ES6 Architecture & Offline PWA
 * Full Multi-Numbering System Support with Muhammad Fu'ad 'Abd al-Baqi as Default
 */

import { analytics } from './analytics.js';

class IbnMajahReader {
  constructor() {
    this.currentLang = 'ms'; // Default Nusantara Malay
    this.currentBook = 0; // Book 0: Kitab al-Muqaddimah
    this.currentNumberingSystem = 'abdul_baqi'; // Default: Muhammad Fu'ad 'Abd al-Baqi
    this.books = [];
    this.hadiths = [];
    this.numberingIndex = null;
    this.searchIndex = null;
    this.searchQuery = '';
    this.arabicFontSize = 1.65; // in rem

    // DOM Elements
    this.contentView = document.getElementById('contentView');
    this.bookSelector = document.getElementById('bookSelector');
    this.numberingSelector = document.getElementById('numberingSelector');
    this.numberingInfoText = document.getElementById('numberingInfoText');
    this.hadithSearch = document.getElementById('hadithSearch');
    this.searchClear = document.getElementById('searchClear');
    this.jumpInput = document.getElementById('jumpInput');
    this.jumpBtn = document.getElementById('jumpBtn');
    this.langToggle = document.getElementById('langToggle');
    this.themeToggle = document.getElementById('themeToggle');
    this.fontInc = document.getElementById('fontInc');
    this.fontDec = document.getElementById('fontDec');
    this.toastMsg = document.getElementById('toastMsg');
    this.docsToggle = document.getElementById('docsToggle');
    this.docsModal = document.getElementById('docsModal');
    this.closeDocsModal = document.getElementById('closeDocsModal');
  }

  async init() {
    analytics.init();
    this.registerServiceWorker();

    // Check saved theme
    const savedTheme = localStorage.getItem('maktabah_theme') || 'light';
    document.body.setAttribute('data-theme', savedTheme);
    if (this.themeToggle) {
      this.themeToggle.textContent = savedTheme === 'dark' ? '☀️' : '🌙';
    }

    // Check saved font size
    const savedSize = localStorage.getItem('maktabah_arabic_font_size');
    if (savedSize) {
      this.arabicFontSize = parseFloat(savedSize);
    }

    // Check saved or URL numbering system
    const savedNumSys = localStorage.getItem('maktabah_ibnmajah_numbering');
    if (savedNumSys && ['abdul_baqi', 'in_book', 'darussalam', 'alamiyah', 'universal'].includes(savedNumSys)) {
      this.currentNumberingSystem = savedNumSys;
    }

    // Check URL search params e.g. ?lang=en, ?numbering=abdul_baqi
    if (window.location.search) {
      const sp = new URLSearchParams(window.location.search);
      const urlLang = sp.get('lang');
      if (urlLang === 'en' || urlLang === 'ms') {
        this.currentLang = urlLang;
      }
      const urlNum = sp.get('numbering') || sp.get('system');
      if (urlNum && ['abdul_baqi', 'in_book', 'darussalam', 'alamiyah', 'universal'].includes(urlNum)) {
        this.currentNumberingSystem = urlNum;
      }
    }

    if (this.langToggle) {
      this.langToggle.textContent = this.currentLang === 'ms' ? 'MY' : 'EN';
    }

    if (this.numberingSelector) {
      this.numberingSelector.value = this.currentNumberingSystem;
    }
    this.updateNumberingBanner();

    this.setupEventListeners();
    await this.loadNumberingIndex();
    await this.loadBooks();
    this.populateBookSelector();
    await this.handleRouting();

    window.addEventListener('hashchange', () => this.handleRouting());
    window.addEventListener('popstate', () => this.handleRouting());
  }

  async loadNumberingIndex() {
    try {
      const res = await fetch('./data/numbering_index.json');
      if (res.ok) {
        this.numberingIndex = await res.json();
      }
    } catch (e) {
      console.warn('Numbering index not available:', e);
    }
  }

  async loadBooks() {
    try {
      const res = await fetch('./data/books.json');
      if (res.ok) {
        this.books = await res.json();
      }
    } catch (e) {
      console.error('Failed to load books catalog:', e);
      this.showToast('Gagal memuat katalog kitab.');
    }
  }

  populateBookSelector() {
    if (!this.bookSelector || !this.books.length) return;
    this.bookSelector.innerHTML = '';
    this.books.forEach(b => {
      const opt = document.createElement('option');
      opt.value = b.book_number;
      const bTitle = this.currentLang === 'ms' ? b.book_title.ms : b.book_title.en;
      opt.textContent = `Kitab ${b.book_number}: ${bTitle} (${b.hadith_count} hadis)`;
      if (b.book_number === this.currentBook) {
        opt.selected = true;
      }
      this.bookSelector.appendChild(opt);
    });
  }

  updateNumberingBanner() {
    if (!this.numberingInfoText) return;
    const sysNames = {
      abdul_baqi: 'Muhammad Fu\'ad \'Abd al-Baqi (#1–4341, Default Utama)',
      in_book: 'Nombor Dalam Kitab (Kitab : Hadis)',
      darussalam: 'Darussalam Riyadh (#1–4341)',
      alamiyah: 'Al-Alamiyah / Lidwa Pusaka (Kitab 9 Imam)',
      universal: 'Universal Maktabah Maftoohah'
    };
    const desc = sysNames[this.currentNumberingSystem] || sysNames.abdul_baqi;
    this.numberingInfoText.innerHTML = `Piawaian penomoran aktif: <strong>${desc}</strong>.`;
  }

  setupEventListeners() {
    // Book selector
    if (this.bookSelector) {
      this.bookSelector.addEventListener('change', (e) => {
        this.currentBook = parseInt(e.target.value, 10);
        this.loadHadiths(this.currentBook);
        history.pushState(null, '', `#book/${this.currentBook}`);
      });
    }

    // Numbering system selector
    if (this.numberingSelector) {
      this.numberingSelector.addEventListener('change', (e) => {
        this.currentNumberingSystem = e.target.value;
        localStorage.setItem('maktabah_ibnmajah_numbering', this.currentNumberingSystem);
        this.updateNumberingBanner();
        this.renderHadiths();
        this.showToast(`Sistem penomoran ditukar ke: ${e.target.options[e.target.selectedIndex].text}`);
      });
    }

    // Search
    if (this.hadithSearch) {
      this.hadithSearch.addEventListener('input', (e) => {
        this.searchQuery = e.target.value.trim();
        if (this.searchClear) {
          this.searchClear.style.display = this.searchQuery ? 'block' : 'none';
        }
        this.handleSearch();
      });
    }

    if (this.searchClear) {
      this.searchClear.addEventListener('click', () => {
        this.hadithSearch.value = '';
        this.searchQuery = '';
        this.searchClear.style.display = 'none';
        this.loadHadiths(this.currentBook);
      });
    }

    // Jump
    if (this.jumpBtn && this.jumpInput) {
      const doJump = () => {
        const val = this.jumpInput.value.trim();
        if (val) this.jumpToRef(val);
      };
      this.jumpBtn.addEventListener('click', doJump);
      this.jumpInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') doJump();
      });
    }

    // Language Toggle
    if (this.langToggle) {
      this.langToggle.addEventListener('click', () => {
        this.currentLang = this.currentLang === 'ms' ? 'en' : 'ms';
        this.langToggle.textContent = this.currentLang === 'ms' ? 'MY' : 'EN';
        this.populateBookSelector();
        this.renderHadiths();
      });
    }

    // Theme Toggle
    if (this.themeToggle) {
      this.themeToggle.addEventListener('click', () => {
        const curTheme = document.body.getAttribute('data-theme') || 'light';
        const newTheme = curTheme === 'dark' ? 'light' : 'dark';
        document.body.setAttribute('data-theme', newTheme);
        localStorage.setItem('maktabah_theme', newTheme);
        this.themeToggle.textContent = newTheme === 'dark' ? '☀️' : '🌙';
      });
    }

    // Font Controls
    if (this.fontInc) {
      this.fontInc.addEventListener('click', () => {
        if (this.arabicFontSize < 2.5) {
          this.arabicFontSize += 0.15;
          this.applyArabicFontSize();
        }
      });
    }

    if (this.fontDec) {
      this.fontDec.addEventListener('click', () => {
        if (this.arabicFontSize > 1.2) {
          this.arabicFontSize -= 0.15;
          this.applyArabicFontSize();
        }
      });
    }

    // Documents Modal
    if (this.docsToggle && this.docsModal) {
      this.docsToggle.addEventListener('click', () => this.docsModal.showModal());
    }
    if (this.closeDocsModal && this.docsModal) {
      this.closeDocsModal.addEventListener('click', () => this.docsModal.close());
    }
  }

  applyArabicFontSize() {
    localStorage.setItem('maktabah_arabic_font_size', this.arabicFontSize.toFixed(2));
    const elements = document.querySelectorAll('.hadith-arabic');
    elements.forEach(el => {
      el.style.fontSize = `${this.arabicFontSize}rem`;
    });
  }

  parseRoute() {
    // 1. Check pathname e.g. /sunan-ibn-majah/42 or /42
    const pathname = window.location.pathname;
    let sub = pathname;
    if (sub.startsWith('/sunan-ibn-majah')) {
      sub = sub.slice('/sunan-ibn-majah'.length);
    }
    sub = sub.replace(/^\/+|\/+$/g, '');
    if (sub && sub !== 'index.html' && sub !== '404.html') {
      const pathMatch = sub.match(/^(?:hadith\/|h\/|ref\/)?(\d+(?:\.\d+)?)$/i);
      if (pathMatch) {
        return { type: 'abdul_baqi', number: pathMatch[1] };
      }
    }

    // 2. Check hash e.g. #ref/42, #abdulbaqi/42, #hadith/42, #42, #book/2
    const hash = window.location.hash.slice(1);
    if (hash) {
      const refHash = hash.match(/^(?:ref\/|abdulbaqi\/|abdul-baqi\/|baqi\/)(\d+(?:\.\d+)?)$/i);
      if (refHash) {
        return { type: 'abdul_baqi', number: refHash[1] };
      }
      const hadithHash = hash.match(/^(?:hadith\/|h\/|ibnmajah:)?(\d+(?:\.\d+)?)$/i);
      if (hadithHash) {
        return { type: 'abdul_baqi', number: hadithHash[1] };
      }
      const inBookHash = hash.match(/^book\/(\d+)(?:\/(\d+))?$/i);
      if (inBookHash) {
        return {
          type: 'book',
          book: parseInt(inBookHash[1], 10),
          inBook: inBookHash[2] ? parseInt(inBookHash[2], 10) : null
        };
      }
    }

    // 3. Check query param e.g. ?ref=42, ?abdulbaqi=42, ?h=42, ?alamiyah=42, ?book=0&in_book=1
    if (window.location.search) {
      const sp = new URLSearchParams(window.location.search);
      const ref = sp.get('ref') || sp.get('abdulbaqi') || sp.get('abdul_baqi') || sp.get('baqi');
      if (ref) {
        return { type: 'abdul_baqi', number: String(ref).trim() };
      }
      const al = sp.get('alamiyah') || sp.get('lidwa');
      if (al) {
        return { type: 'alamiyah', number: String(al).trim() };
      }
      const dar = sp.get('darussalam') || sp.get('dar');
      if (dar) {
        return { type: 'darussalam', number: String(dar).trim() };
      }
      const b = sp.get('book') || sp.get('b') || sp.get('kitab');
      const inBook = sp.get('in_book') || sp.get('inbook') || sp.get('ib');
      if (b !== null && inBook !== null) {
        return { type: 'in_book', book: parseInt(b, 10), inBook: parseInt(inBook, 10) };
      }
      const h = sp.get('hadith') || sp.get('h');
      if (h) {
        return { type: 'abdul_baqi', number: String(h).trim() };
      }
      if (b !== null) {
        return { type: 'book', book: parseInt(b, 10), inBook: null };
      }
    }

    return null;
  }

  async handleRouting() {
    const route = this.parseRoute();

    if (route && route.type === 'abdul_baqi') {
      const cleanRef = String(route.number).trim();
      const match = this.numberingIndex?.abdul_baqi_to_universal?.[cleanRef];
      if (match) {
        const [uHadith, bookNum] = match;
        this.currentBook = bookNum;
        if (this.bookSelector) this.bookSelector.value = bookNum;
        await this.loadHadiths(bookNum);
        this.scrollToHadith(uHadith);
        analytics.trackHadithView(cleanRef, bookNum, 'abdul_baqi');
        return;
      }
    }

    if (route && route.type === 'alamiyah') {
      const cleanRef = String(route.number).trim();
      const match = this.numberingIndex?.alamiyah_to_universal?.[cleanRef];
      if (match) {
        const [uHadith, bookNum] = match;
        this.currentBook = bookNum;
        if (this.bookSelector) this.bookSelector.value = bookNum;
        await this.loadHadiths(bookNum);
        this.scrollToHadith(uHadith);
        analytics.trackHadithView(cleanRef, bookNum, 'alamiyah');
        return;
      }
    }

    if (route && route.type === 'darussalam') {
      const cleanRef = String(route.number).trim();
      const match = this.numberingIndex?.darussalam_to_universal?.[cleanRef];
      if (match) {
        const [uHadith, bookNum] = match;
        this.currentBook = bookNum;
        if (this.bookSelector) this.bookSelector.value = bookNum;
        await this.loadHadiths(bookNum);
        this.scrollToHadith(uHadith);
        analytics.trackHadithView(cleanRef, bookNum, 'darussalam');
        return;
      }
    }

    if (route && route.type === 'in_book') {
      const key = `${route.book}:${route.inBook}`;
      const targetHadith = this.numberingIndex?.in_book_to_universal?.[key];
      this.currentBook = route.book;
      if (this.bookSelector) this.bookSelector.value = route.book;
      await this.loadHadiths(route.book);
      if (targetHadith) {
        this.scrollToHadith(targetHadith);
      }
      return;
    }

    if (route && route.type === 'book') {
      this.currentBook = route.book;
      if (this.bookSelector) this.bookSelector.value = route.book;
      await this.loadHadiths(route.book);
      if (route.inBook) {
        const key = `${route.book}:${route.inBook}`;
        const targetHadith = this.numberingIndex?.in_book_to_universal?.[key];
        if (targetHadith) this.scrollToHadith(targetHadith);
      }
    } else {
      await this.loadHadiths(this.currentBook);
    }
  }

  jumpToRef(input) {
    const clean = input.trim().replace(/^#/, '');

    // 1. Check in_book format "book:in_book" e.g. "0:5" or "1:10"
    if (clean.includes(':')) {
      const parts = clean.split(':');
      const b = parseInt(parts[0], 10);
      const ib = parseInt(parts[1], 10);
      const key = `${b}:${ib}`;
      const match = this.numberingIndex?.in_book_to_universal?.[key];
      if (match) {
        this.currentBook = b;
        if (this.bookSelector) this.bookSelector.value = b;
        this.loadHadiths(b).then(() => this.scrollToHadith(match));
        return;
      }
    }

    // 2. Resolve via active numbering system or Abd al-Baqi default
    if (this.currentNumberingSystem === 'abdul_baqi' || !this.numberingIndex) {
      const match = this.numberingIndex?.abdul_baqi_to_universal?.[clean];
      if (match) {
        const [uId, bNum] = match;
        this.currentBook = bNum;
        if (this.bookSelector) this.bookSelector.value = bNum;
        this.loadHadiths(bNum).then(() => this.scrollToHadith(uId));
        return;
      }
    } else if (this.currentNumberingSystem === 'alamiyah') {
      const match = this.numberingIndex?.alamiyah_to_universal?.[clean];
      if (match) {
        const [uId, bNum] = match;
        this.currentBook = bNum;
        if (this.bookSelector) this.bookSelector.value = bNum;
        this.loadHadiths(bNum).then(() => this.scrollToHadith(uId));
        return;
      }
    } else if (this.currentNumberingSystem === 'darussalam') {
      const match = this.numberingIndex?.darussalam_to_universal?.[clean];
      if (match) {
        const [uId, bNum] = match;
        this.currentBook = bNum;
        if (this.bookSelector) this.bookSelector.value = bNum;
        this.loadHadiths(bNum).then(() => this.scrollToHadith(uId));
        return;
      }
    }

    // Fallback: Check 'Abd al-Baqi index directly
    const fallbackMatch = this.numberingIndex?.abdul_baqi_to_universal?.[clean];
    if (fallbackMatch) {
      const [uId, bNum] = fallbackMatch;
      this.currentBook = bNum;
      if (this.bookSelector) this.bookSelector.value = bNum;
      this.loadHadiths(bNum).then(() => this.scrollToHadith(uId));
    } else {
      this.showToast(`Nombor hadis #${clean} tidak dijumpai.`);
    }
  }

  async loadHadiths(bookNumber) {
    if (!this.contentView) return;
    this.contentView.innerHTML = '<p class="loading-state">Memuatkan hadis...</p>';

    const bookPad = String(bookNumber).padStart(2, '0');
    try {
      const res = await fetch(`./data/hadiths/${bookPad}.json`);
      if (res.ok) {
        this.hadiths = await res.json();
        this.renderHadiths();
        window.scrollTo({ top: 0, behavior: 'smooth' });
      } else {
        this.contentView.innerHTML = '<p class="empty-state">Kitab ini belum mempunyai fail hadis.</p>';
      }
    } catch (e) {
      console.error('Failed to load hadith shard:', e);
      this.contentView.innerHTML = '<p class="empty-state">Ralat memuatkan fail hadis.</p>';
    }
  }

  renderHadiths(hadithList = null) {
    if (!this.contentView) return;
    const items = hadithList || this.hadiths;

    if (!items || items.length === 0) {
      this.contentView.innerHTML = '<p class="empty-state">Tiada hadis ditemui.</p>';
      return;
    }

    const frag = document.createDocumentFragment();

    items.forEach(h => {
      const card = document.createElement('article');
      card.className = 'hadith-card';
      const uId = h.numbering?.universal || h.hadith_number;
      card.id = `h-${uId}`;
      card.setAttribute('data-hadith-universal', uId);
      card.setAttribute('data-hadith-abdulbaqi', h.numbering?.abdul_baqi || h.hadith_number);

      // 1. Header & Numbering
      const header = document.createElement('div');
      header.className = 'hadith-header';

      const titleGroup = document.createElement('div');
      titleGroup.className = 'hadith-title-group';

      // Primary badge based on current active numbering system
      const primaryBadge = document.createElement('div');
      primaryBadge.className = 'hadith-primary-badge';

      const abNum = h.numbering?.abdul_baqi || h.hadith_number;
      const ibNum = h.in_book_number || h.numbering?.in_book;
      const bNum = h.book_number;

      if (this.currentNumberingSystem === 'abdul_baqi') {
        primaryBadge.innerHTML = `<span>Hadis #${abNum}</span> <small style="font-size:0.75rem; opacity:0.85;">('Abd al-Baqi)</small>`;
      } else if (this.currentNumberingSystem === 'in_book') {
        primaryBadge.innerHTML = `<span>Kitab ${bNum}, Hadis ${ibNum}</span>`;
      } else if (this.currentNumberingSystem === 'darussalam') {
        primaryBadge.innerHTML = `<span>Darussalam #${h.numbering?.darussalam || abNum}</span>`;
      } else if (this.currentNumberingSystem === 'alamiyah') {
        primaryBadge.innerHTML = `<span>Alamiyah #${h.numbering?.alamiyah || uId}</span>`;
      } else {
        primaryBadge.innerHTML = `<span>Universal #${uId}</span>`;
      }
      titleGroup.appendChild(primaryBadge);

      // Multi-numbering chips row showing all coordinates
      const chipsRow = document.createElement('div');
      chipsRow.className = 'numbering-chips';

      const chipAb = document.createElement('span');
      chipAb.className = `num-chip ${this.currentNumberingSystem === 'abdul_baqi' ? 'active-chip primary' : ''}`;
      chipAb.textContent = `'Abd al-Baqi: #${abNum}`;

      const chipIb = document.createElement('span');
      chipIb.className = `num-chip ${this.currentNumberingSystem === 'in_book' ? 'active-chip primary' : ''}`;
      chipIb.textContent = `Dalam Kitab: ${bNum}:${ibNum}`;

      const chipDar = document.createElement('span');
      chipDar.className = `num-chip ${this.currentNumberingSystem === 'darussalam' ? 'active-chip primary' : ''}`;
      chipDar.textContent = `Darussalam: #${h.numbering?.darussalam || abNum}`;

      const chipAl = document.createElement('span');
      chipAl.className = `num-chip ${this.currentNumberingSystem === 'alamiyah' ? 'active-chip primary' : ''}`;
      chipAl.textContent = `Alamiyah: #${h.numbering?.alamiyah || uId}`;

      chipsRow.appendChild(chipAb);
      chipsRow.appendChild(chipIb);
      chipsRow.appendChild(chipDar);
      chipsRow.appendChild(chipAl);

      titleGroup.appendChild(chipsRow);
      header.appendChild(titleGroup);

      // Actions buttons
      const actions = document.createElement('div');
      actions.className = 'hadith-actions';

      const btnCopyAll = document.createElement('button');
      btnCopyAll.className = 'btn-action';
      btnCopyAll.title = 'Salin Hadis Lengkap';
      btnCopyAll.innerHTML = '📋 Salin';
      btnCopyAll.addEventListener('click', () => this.copyHadithText(h));

      const btnShare = document.createElement('button');
      btnShare.className = 'btn-action';
      btnShare.title = 'Salin Pautan Hadis';
      btnShare.innerHTML = '🔗 Kongsi';
      btnShare.addEventListener('click', () => this.copyPermalink(h));

      actions.appendChild(btnCopyAll);
      actions.appendChild(btnShare);
      header.appendChild(actions);

      card.appendChild(header);

      // 2. Arabic Text
      const arP = document.createElement('div');
      arP.className = 'hadith-arabic';
      arP.style.fontSize = `${this.arabicFontSize}rem`;
      arP.textContent = h.arabic;
      card.appendChild(arP);

      // 3. Scholarly Gradings
      if (h.gradings && h.gradings.length > 0) {
        const gradingsDiv = document.createElement('div');
        gradingsDiv.className = 'hadith-gradings';

        h.gradings.forEach(g => {
          const pill = document.createElement('span');
          const gradeLow = (g.grade || '').toLowerCase();
          let cls = 'sahih';
          if (gradeLow.includes('hasan')) cls = 'hasan';
          else if (gradeLow.includes('daif') || gradeLow.includes("da'if") || gradeLow.includes('munkar')) cls = 'daif';

          pill.className = `grade-pill ${cls}`;
          pill.innerHTML = `<span class="grade-scholar">${g.scholar}:</span> <strong>${g.grade_ar || g.grade} (${g.grade})</strong>`;
          gradingsDiv.appendChild(pill);
        });

        card.appendChild(gradingsDiv);
      }

      // 4. Translation
      const transText = (this.currentLang === 'ms' ? h.translations?.ms : h.translations?.en) || h.translations?.ms || h.translations?.en;
      if (transText) {
        const transDiv = document.createElement('div');
        transDiv.className = 'hadith-translation';

        const metaLabel = document.createElement('span');
        metaLabel.className = 'translation-meta';
        metaLabel.textContent = this.currentLang === 'ms' ? 'Terjemahan Bahasa Melayu (Nusantara):' : 'English Translation (Darussalam):';

        const p = document.createElement('p');
        p.textContent = transText;

        transDiv.appendChild(metaLabel);
        transDiv.appendChild(p);
        card.appendChild(transDiv);
      }

      frag.appendChild(card);
    });

    this.contentView.innerHTML = '';
    this.contentView.appendChild(frag);
  }

  scrollToHadith(universalId) {
    setTimeout(() => {
      const el = document.getElementById(`h-${universalId}`);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        el.classList.add('highlighted');
        setTimeout(() => el.classList.remove('highlighted'), 3000);
      }
    }, 250);
  }

  async handleSearch() {
    if (!this.searchQuery) {
      this.loadHadiths(this.currentBook);
      return;
    }

    if (!this.searchIndex) {
      try {
        const res = await fetch('./data/search-index.json');
        if (res.ok) {
          this.searchIndex = await res.json();
        }
      } catch (e) {
        console.error('Failed to load search index:', e);
      }
    }

    if (!this.searchIndex) return;

    const q = this.searchQuery.toLowerCase();
    const hits = this.searchIndex.filter(item => {
      return (
        item.ab === q ||
        String(item.ib) === q ||
        (item.ar && item.ar.toLowerCase().includes(q)) ||
        (item.ms && item.ms.toLowerCase().includes(q)) ||
        (item.en && item.en.toLowerCase().includes(q))
      );
    }).slice(0, 50);

    if (hits.length === 0) {
      this.contentView.innerHTML = `<p class="empty-state">Tiada hadis sepadan dengan carian "${this.searchQuery}".</p>`;
      return;
    }

    // Load shard for top match if single book
    const firstHit = hits[0];
    if (hits.length === 1 && firstHit.b !== this.currentBook) {
      this.currentBook = firstHit.b;
      if (this.bookSelector) this.bookSelector.value = firstHit.b;
      await this.loadHadiths(firstHit.b);
      this.scrollToHadith(firstHit.u);
      return;
    }

    // Render search results cards
    this.contentView.innerHTML = `<p style="padding:0.75rem; color:var(--primary); font-weight:700;">Ditemui ${hits.length} hadis sepadan:</p>`;
    const container = document.createElement('div');
    container.className = 'content-container';

    hits.forEach(hit => {
      const card = document.createElement('div');
      card.className = 'hadith-card';
      card.style.cursor = 'pointer';
      card.innerHTML = `
        <div class="hadith-header">
          <div class="hadith-primary-badge">Hadis #${hit.ab} ('Abd al-Baqi) &bull; Kitab ${hit.b}</div>
        </div>
        <p class="hadith-arabic" style="font-size:1.3rem; margin:0.5rem 0;">${hit.ar}...</p>
        <p style="font-size:0.92rem; color:var(--text-secondary);">${hit.ms || hit.en}...</p>
      `;
      card.addEventListener('click', async () => {
        this.currentBook = hit.b;
        if (this.bookSelector) this.bookSelector.value = hit.b;
        await this.loadHadiths(hit.b);
        this.scrollToHadith(hit.u);
      });
      container.appendChild(card);
    });
    this.contentView.appendChild(container);
  }

  copyHadithText(h) {
    const abNum = h.numbering?.abdul_baqi || h.hadith_number;
    const bTitle = this.currentLang === 'ms' ? h.book_title.ms : h.book_title.en;
    const trans = (this.currentLang === 'ms' ? h.translations?.ms : h.translations?.en) || '';
    const gradings = (h.gradings || []).map(g => `${g.scholar}: ${g.grade}`).join(', ');

    const text = `Sunan Ibn Majah #${abNum} (Piawaian 'Abd al-Baqi)
${bTitle} (Kitab ${h.book_number}, Hadis ${h.in_book_number})

${h.arabic}

Terjemahan:
${trans}

Takhrij: ${gradings}

Rujukan: https://maktabah-maftoohah.github.io/sunan-ibn-majah/?ref=${abNum}`;

    navigator.clipboard.writeText(text).then(() => {
      this.showToast('Hadis lengkap disalin ke papan keratan!');
    });
  }

  copyPermalink(h) {
    const abNum = h.numbering?.abdul_baqi || h.hadith_number;
    const url = `${window.location.origin}${window.location.pathname}?ref=${abNum}`;
    navigator.clipboard.writeText(url).then(() => {
      this.showToast(`Pautan Hadis #${abNum} ('Abd al-Baqi) berjaya disalin!`);
    });
  }

  showToast(msg) {
    if (!this.toastMsg) return;
    this.toastMsg.textContent = msg;
    this.toastMsg.classList.add('show');
    setTimeout(() => {
      this.toastMsg.classList.remove('show');
    }, 2800);
  }

  registerServiceWorker() {
    if ('serviceWorker' in navigator && window.location.protocol.startsWith('http')) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('./sw.js').catch(err => {
          console.warn('Service worker registration failed:', err);
        });
      });
    }
  }
}

// Instantiate on DOM load
window.addEventListener('DOMContentLoaded', () => {
  const app = new IbnMajahReader();
  app.init();
});
