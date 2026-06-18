/**
 * TzQuant Investor Deck
 * Minimal, functional interactions
 */

document.addEventListener('DOMContentLoaded', function() {
    'use strict';

    const header = document.getElementById('header');
    const menuToggle = document.getElementById('menuToggle');
    const siteNav = document.getElementById('siteNav');

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

    // Subtle reveal on scroll
    const revealElements = document.querySelectorAll(
        '.section-preamble, .section-lead, .opportunity-body, .metrics-row, .solution-stack, ' +
        '.product-item, .traction-statement, .traction-quote, .business-item, ' +
        '.market-item, .advantage-row, .roadmap-card, .team-member, .contact-block'
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
