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
        if (window.scrollY > 20) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
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

    // Scrollspy: highlight current nav item based on scroll position
    (function initScrollSpy() {
        const navLinks = Array.from(document.querySelectorAll('.site-nav a[href^="#"]'));
        const sections = navLinks
            .map(link => {
                const id = link.getAttribute('href').slice(1);
                return { link, section: document.getElementById(id) };
            })
            .filter(item => item.section);

        if (!sections.length) return;

        function setActive(link) {
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        }

        function updateActiveNav() {
            const scrollPos = window.scrollY + 100;
            let active = sections[0];

            for (let i = sections.length - 1; i >= 0; i--) {
                if (sections[i].section.offsetTop <= scrollPos) {
                    active = sections[i];
                    break;
                }
            }

            setActive(active.link);
        }

        navLinks.forEach(link => {
            link.addEventListener('click', () => setActive(link));
        });

        window.addEventListener('scroll', updateActiveNav, { passive: true });
        updateActiveNav();
    })();

    // Language switcher
    function setLanguage(lang) {
        document.documentElement.lang = lang === 'zh' ? 'zh-CN' : 'en';
        if (lang === 'en') {
            document.documentElement.classList.add('lang-en');
        } else {
            document.documentElement.classList.remove('lang-en');
        }
        localStorage.setItem('tzquant-lang', lang);

        // Toggle active state
        document.querySelectorAll('.lang-option').forEach(opt => {
            if (opt.dataset.lang === lang) {
                opt.classList.add('active');
            } else {
                opt.classList.remove('active');
            }
        });

        // Update text content
        document.querySelectorAll('[data-zh][data-en]').forEach(el => {
            const text = el.dataset[lang];
            if (text !== undefined) {
                el.textContent = text;
            }
        });

        // Update HTML content (for elements with <br>)
        // Note: dataset property names are camelCase, so data-en-html -> enHtml
        document.querySelectorAll('[data-zh-html][data-en-html]').forEach(el => {
            const html = el.dataset[lang + 'Html'];
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

    // Hero video mobile compatibility + fallback
    (function initHeroVideo() {
        const heroMedia = document.getElementById('heroMedia');
        const heroVideo = document.getElementById('heroVideo');
        const heroPoster = document.getElementById('heroPoster');
        const posterPlay = document.getElementById('posterPlay');
        if (!heroMedia || !heroVideo) return;

        let fallbackTimer = null;
        let autoplayFailed = false;

        function showPoster() {
            if (heroMedia.classList.contains('is-poster')) return;
            heroMedia.classList.add('is-poster');
            autoplayFailed = true;
            try {
                heroVideo.pause();
            } catch (e) {
                // ignore
            }
        }

        function hidePoster() {
            heroMedia.classList.remove('is-poster');
            autoplayFailed = false;
        }

        function attemptPlay(isUserGesture) {
            if (!heroVideo.paused) return;
            heroVideo.muted = true;
            const playPromise = heroVideo.play();
            if (playPromise && typeof playPromise.then === 'function') {
                playPromise.then(function() {
                    hidePoster();
                    clearTimeout(fallbackTimer);
                }).catch(function(err) {
                    clearTimeout(fallbackTimer);
                    // Autoplay blocked (WeChat WebView, iOS low power, etc.)
                    showPoster();
                    if (isUserGesture) {
                        // User already clicked, some browsers still block; keep poster visible
                        showPoster();
                    }
                });
            } else {
                // Older browsers may not return a promise
                startFallbackTimer();
            }
        }

        function startFallbackTimer() {
            clearTimeout(fallbackTimer);
            fallbackTimer = setTimeout(function() {
                if (heroVideo.paused || heroVideo.readyState < 2) {
                    showPoster();
                }
            }, 3000);
        }

        heroVideo.addEventListener('error', showPoster, { once: true });
        heroVideo.addEventListener('stalled', showPoster, { once: true });
        heroVideo.addEventListener('abort', showPoster, { once: true });

        heroVideo.addEventListener('playing', function() {
            hidePoster();
            clearTimeout(fallbackTimer);
        });

        heroVideo.addEventListener('pause', function() {
            // If paused and autoplay already failed, keep poster shown
            if (autoplayFailed) {
                showPoster();
            }
        });

        if (heroPoster) {
            heroPoster.addEventListener('click', function() {
                attemptPlay(true);
            });
        }

        if (posterPlay) {
            posterPlay.addEventListener('click', function(e) {
                e.stopPropagation();
                attemptPlay(true);
            });
        }

        // WeChat WebView and other strict environments often need a user gesture.
        // Try autoplay first, then show poster + play button on failure.
        startFallbackTimer();
        attemptPlay(false);
    })();

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
