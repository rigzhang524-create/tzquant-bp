/**
 * TzQuant Investor Deck
 * Apple-style minimal interactions + i18n
 */

document.addEventListener('DOMContentLoaded', function() {
    'use strict';

    const header = document.getElementById('header');
    const menuToggle = document.getElementById('menuToggle');
    const siteNav = document.getElementById('siteNav');
    const langToggle = document.getElementById('langToggle');

    // Header scroll state
    function updateHeader() {
        header.classList.toggle('scrolled', window.scrollY > 20);
    }
    window.addEventListener('scroll', updateHeader, { passive: true });
    updateHeader();

    // Mobile menu
    menuToggle.addEventListener('click', function() {
        this.classList.toggle('active');
        siteNav.classList.toggle('open');
    });

    document.querySelectorAll('.site-nav a').forEach(link => {
        link.addEventListener('click', () => {
            menuToggle.classList.remove('active');
            siteNav.classList.remove('open');
        });
    });

    // Smooth scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                const top = target.getBoundingClientRect().top + window.scrollY - 60;
                window.scrollTo({ top: top, behavior: 'smooth' });
            }
        });
    });

    // Language switcher
    function setLanguage(lang) {
        document.documentElement.lang = lang === 'zh' ? 'zh-CN' : 'en';
        document.documentElement.classList.toggle('lang-en', lang === 'en');
        localStorage.setItem('tzquant-lang', lang);

        // Toggle active state
        document.querySelectorAll('.lang-option').forEach(opt => {
            opt.classList.toggle('active', opt.dataset.lang === lang);
        });

        // Update text content
        document.querySelectorAll('[data-zh][data-en]').forEach(el => {
            const text = el.dataset[lang];
            if (text !== undefined) {
                el.textContent = text;
            }
        });

        // Update HTML content (for elements with <br>)
        document.querySelectorAll('[data-zh-html][data-en-html]').forEach(el => {
            const html = el.dataset[lang + '-html'];
            if (html !== undefined) {
                el.innerHTML = html;
            }
        });
    }

    if (langToggle) {
        langToggle.addEventListener('click', function(e) {
            const option = e.target.closest('.lang-option');
            if (!option) return;

            const currentLang = localStorage.getItem('tzquant-lang') || 'zh';
            const newLang = option.dataset.lang;
            if (newLang && newLang !== currentLang) {
                setLanguage(newLang);
            }
        });
    }

    // Initialize language
    const savedLang = localStorage.getItem('tzquant-lang') || 'zh';
    setLanguage(savedLang);

    // Subtle reveal on scroll
    const revealElements = document.querySelectorAll(
        '.section-head, .metrics-row, .solution-grid, .competitor-card, .competitor-summary, ' +
        '.product-card, .traction-statement, .traction-quote, .traction-cite, ' +
        '.business-item, .market-item, .advantage-card, .roadmap-card, .team-card, .contact-email'
    );

    revealElements.forEach(el => el.classList.add('reveal'));

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -40px 0px'
    });

    revealElements.forEach(el => observer.observe(el));
});
