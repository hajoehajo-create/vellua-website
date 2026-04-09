/* ============================================
   VELLÚA CONSENT MANAGER
   DSGVO/GDPR-konformer Cookie Consent Banner
   ============================================ */

(function() {
    'use strict';

    const STORAGE_KEY = 'vellua_consent';
    const GTM_ID = 'GTM-TQQWGRV';

    // --- Consent State ---
    function getConsent() {
        try {
            const stored = localStorage.getItem(STORAGE_KEY);
            return stored ? JSON.parse(stored) : null;
        } catch(e) { return null; }
    }

    function setConsent(consent) {
        consent.timestamp = new Date().toISOString();
        localStorage.setItem(STORAGE_KEY, JSON.stringify(consent));
    }

    // --- GTM Loader ---
    function loadGTM() {
        if (document.querySelector('script[src*="googletagmanager"]')) return;
        (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
        new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
        j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
        'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
        })(window,document,'script','dataLayer', GTM_ID);
    }

    // --- Spotify Embed Loader ---
    function activateSpotifyEmbeds() {
        document.querySelectorAll('.spotify-consent-placeholder').forEach(function(placeholder) {
            var src = placeholder.getAttribute('data-spotify-src');
            if (!src) return;
            var iframe = document.createElement('iframe');
            iframe.style.borderRadius = '12px';
            iframe.src = src;
            iframe.width = '100%';
            iframe.height = '152';
            iframe.frameBorder = '0';
            iframe.allowFullscreen = true;
            iframe.allow = 'autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture';
            iframe.loading = 'lazy';
            placeholder.parentNode.replaceChild(iframe, placeholder);
        });
    }

    // --- Apply Consent ---
    function applyConsent(consent) {
        if (consent.analytics) {
            loadGTM();
        }
        if (consent.media) {
            activateSpotifyEmbeds();
        }
    }

    // --- Create Banner ---
    function showBanner() {
        if (document.getElementById('consentBanner')) return;

        var banner = document.createElement('div');
        banner.id = 'consentBanner';
        banner.innerHTML = `
            <div class="consent-inner">
                <div class="consent-text">
                    <h3>Your Privacy Matters</h3>
                    <p>We use cookies for analytics and embed external media (Spotify). You choose what's activated.</p>
                </div>
                <div class="consent-actions">
                    <button id="consentAcceptAll" class="consent-btn consent-btn-accept">Accept All</button>
                    <button id="consentEssential" class="consent-btn consent-btn-essential">Essential Only</button>
                    <button id="consentSettings" class="consent-btn consent-btn-settings">Settings</button>
                </div>
                <div class="consent-details" id="consentDetails">
                    <div class="consent-toggle-row">
                        <label>
                            <input type="checkbox" checked disabled>
                            <span><strong>Essential</strong> — Always active. Site functionality.</span>
                        </label>
                    </div>
                    <div class="consent-toggle-row">
                        <label>
                            <input type="checkbox" id="toggleAnalytics">
                            <span><strong>Analytics</strong> — Google Analytics 4 via Tag Manager. Helps us understand our audience.</span>
                        </label>
                    </div>
                    <div class="consent-toggle-row">
                        <label>
                            <input type="checkbox" id="toggleMedia">
                            <span><strong>External Media</strong> — Spotify player embeds for listening to our music.</span>
                        </label>
                    </div>
                    <button id="consentSaveCustom" class="consent-btn consent-btn-accept" style="margin-top: 1rem;">Save Preferences</button>
                </div>
            </div>
        `;
        document.body.appendChild(banner);

        // Animation
        requestAnimationFrame(function() {
            requestAnimationFrame(function() {
                banner.classList.add('visible');
            });
        });

        // Button listeners
        document.getElementById('consentAcceptAll').addEventListener('click', function() {
            var consent = { essential: true, analytics: true, media: true };
            setConsent(consent);
            applyConsent(consent);
            closeBanner();
        });

        document.getElementById('consentEssential').addEventListener('click', function() {
            var consent = { essential: true, analytics: false, media: false };
            setConsent(consent);
            applyConsent(consent);
            closeBanner();
        });

        document.getElementById('consentSettings').addEventListener('click', function() {
            var details = document.getElementById('consentDetails');
            details.classList.toggle('open');
            this.textContent = details.classList.contains('open') ? 'Hide Settings' : 'Settings';
        });

        document.getElementById('consentSaveCustom').addEventListener('click', function() {
            var consent = {
                essential: true,
                analytics: document.getElementById('toggleAnalytics').checked,
                media: document.getElementById('toggleMedia').checked
            };
            setConsent(consent);
            applyConsent(consent);
            closeBanner();
        });
    }

    function closeBanner() {
        var banner = document.getElementById('consentBanner');
        if (banner) {
            banner.classList.remove('visible');
            setTimeout(function() { banner.remove(); }, 400);
        }
    }

    // --- Footer Link: Re-open Settings ---
    window.velluaOpenConsentSettings = function() {
        localStorage.removeItem(STORAGE_KEY);
        showBanner();
    };

    // --- Init ---
    document.addEventListener('DOMContentLoaded', function() {
        var consent = getConsent();
        if (consent) {
            applyConsent(consent);
        } else {
            showBanner();
        }
    });

})();
