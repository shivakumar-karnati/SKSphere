/* ==========================================================
   SKSphere — Interactions & Animations
   ========================================================== */

document.addEventListener('DOMContentLoaded', function () {

    /* ---------- 1. Navbar shrink on scroll ---------- */
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 30) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    /* ---------- 2. Scroll reveal for elements with .reveal ---------- */
    const revealEls = document.querySelectorAll('.reveal');
    if (revealEls.length) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15 });

        revealEls.forEach(el => observer.observe(el));
    }

    /* ---------- 3. Ripple effect on buttons ---------- */
    document.querySelectorAll('.shop-btn, .btn-gradient').forEach(btn => {
        btn.style.position = btn.style.position || 'relative';
        btn.style.overflow = 'hidden';

        btn.addEventListener('click', function (e) {
            const rect = btn.getBoundingClientRect();
            const ripple = document.createElement('span');
            const size = Math.max(rect.width, rect.height);

            ripple.className = 'ripple';
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
            ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';

            btn.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });

    /* ---------- 4. 3D tilt on product / category cards ---------- */
    const tiltCards = document.querySelectorAll('.product-card, .category-card, .related-card');
    const isTouchDevice = window.matchMedia('(hover: none)').matches;

    if (!isTouchDevice) {
        tiltCards.forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                const centerX = rect.width / 2;
                const centerY = rect.height / 2;

                const rotateX = ((y - centerY) / centerY) * -6;
                const rotateY = ((x - centerX) / centerX) * 6;

                card.style.transform =
                    `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-6px)`;
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform =
                    'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0)';
            });
        });
    }

    /* ---------- 5. Decorative cursor glow (desktop only) ---------- */
    if (!isTouchDevice && window.innerWidth > 991) {
        const glow = document.createElement('div');
        glow.className = 'cursor-glow';
        document.body.appendChild(glow);

        window.addEventListener('mousemove', (e) => {
            glow.style.left = e.clientX + 'px';
            glow.style.top = e.clientY + 'px';
        });
    }

    /* ---------- 6. Product sliders: arrow buttons + drag-to-scroll ---------- */
    document.querySelectorAll('.slider-wrapper').forEach(wrapper => {
        const track = wrapper.querySelector('.products-slider');
        const prevBtn = wrapper.querySelector('.slider-btn.prev');
        const nextBtn = wrapper.querySelector('.slider-btn.next');
        if (!track) return;

        const scrollByAmount = () => {
            const card = track.querySelector('.product-card');
            const cardWidth = card ? card.getBoundingClientRect().width : 250;
            const gap = 20;
            return (cardWidth + gap) * 2; // scroll ~2 cards per click
        };

        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                track.scrollBy({ left: -scrollByAmount(), behavior: 'smooth' });
            });
        }
        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                track.scrollBy({ left: scrollByAmount(), behavior: 'smooth' });
            });
        }

        // Hide arrows when there's nothing to scroll
        const updateArrowVisibility = () => {
            const maxScroll = track.scrollWidth - track.clientWidth;
            if (prevBtn) prevBtn.style.display = track.scrollLeft <= 5 ? 'none' : 'flex';
            if (nextBtn) nextBtn.style.display = track.scrollLeft >= maxScroll - 5 ? 'none' : 'flex';
        };
        updateArrowVisibility();
        track.addEventListener('scroll', updateArrowVisibility);
        window.addEventListener('resize', updateArrowVisibility);

        // Drag-to-scroll with mouse (desktop)
        let isDown = false;
        let startX = 0;
        let scrollStart = 0;

        track.addEventListener('mousedown', (e) => {
            isDown = true;
            track.classList.add('dragging');
            startX = e.pageX;
            scrollStart = track.scrollLeft;
        });

        window.addEventListener('mouseup', () => {
            isDown = false;
            track.classList.remove('dragging');
        });

        window.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const dx = e.pageX - startX;
            track.scrollLeft = scrollStart - dx;
        });
    });

    /* ---------- 7. Auto-dismiss success alerts ---------- */
    document.querySelectorAll('.alert-success').forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity .6s ease, transform .6s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => alert.remove(), 600);
        }, 4000);
    });

});

/* ==========================================================
   ORDER SUCCESS — confetti burst (vanilla JS, no libraries)
   Runs once on page load, cleans itself up after ~3.5s
   ========================================================== */

document.addEventListener('DOMContentLoaded', function () {

    const canvas = document.getElementById('confetti-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width, height;

    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    const colors = ['#2563eb', '#059669', '#f59e0b', '#e11d48', '#7c3aed'];
    const pieceCount = window.innerWidth < 576 ? 70 : 140;
    const pieces = [];

    function randomBetween(min, max) {
        return Math.random() * (max - min) + min;
    }

    for (let i = 0; i < pieceCount; i++) {
        pieces.push({
            x: randomBetween(0, width),
            y: randomBetween(-height, 0),
            size: randomBetween(6, 11),
            color: colors[Math.floor(Math.random() * colors.length)],
            speedY: randomBetween(2, 5),
            speedX: randomBetween(-1.5, 1.5),
            rotation: randomBetween(0, 360),
            rotationSpeed: randomBetween(-6, 6),
            shape: Math.random() > 0.5 ? 'rect' : 'circle'
        });
    }

    let startTime = null;
    const duration = 3200; // ms

    function draw(timestamp) {
        if (!startTime) startTime = timestamp;
        const elapsed = timestamp - startTime;

        ctx.clearRect(0, 0, width, height);

        pieces.forEach(p => {
            p.x += p.speedX;
            p.y += p.speedY;
            p.rotation += p.rotationSpeed;

            ctx.save();
            ctx.translate(p.x, p.y);
            ctx.rotate((p.rotation * Math.PI) / 180);
            ctx.fillStyle = p.color;

            if (p.shape === 'rect') {
                ctx.fillRect(-p.size / 2, -p.size / 4, p.size, p.size / 2);
            } else {
                ctx.beginPath();
                ctx.arc(0, 0, p.size / 2, 0, Math.PI * 2);
                ctx.fill();
            }

            ctx.restore();
        });

        if (elapsed < duration) {
            requestAnimationFrame(draw);
        } else {
            // Fade out canvas, then remove it from the DOM
            canvas.style.transition = 'opacity .6s ease';
            canvas.style.opacity = '0';
            setTimeout(() => canvas.remove(), 600);
        }
    }

    requestAnimationFrame(draw);
});



/* ==========================================================
   PAYMENT PENDING — rotating status messages + elapsed timer
   Purely cosmetic (real status comes from your backend/admin
   verification), but gives the waiting page a "live" feel.
   ========================================================== */

document.addEventListener('DOMContentLoaded', function () {

    const messageEl = document.getElementById('status-message');
    const timerEl = document.getElementById('status-timer-value');

    if (!messageEl && !timerEl) return;

    /* ---------- Rotating status messages ---------- */
    if (messageEl) {
        const messages = [
            'Checking your payment screenshot...',
            'Verifying transaction details...',
            'Almost there, hang tight...',
            'Our team is reviewing your payment...'
        ];

        let index = 0;
        messageEl.textContent = messages[0];

        setInterval(() => {
            index = (index + 1) % messages.length;
            messageEl.style.opacity = '0';

            setTimeout(() => {
                messageEl.textContent = messages[index];
                messageEl.style.opacity = '1';
            }, 300);
        }, 3200);
    }

    /* ---------- Elapsed time counter ---------- */
    if (timerEl) {
        let seconds = 0;

        setInterval(() => {
            seconds++;
            const mins = Math.floor(seconds / 60).toString().padStart(2, '0');
            const secs = (seconds % 60).toString().padStart(2, '0');
            timerEl.textContent = `${mins}:${secs}`;
        }, 1000);
    }

});



/* ==========================================================
   PAYMENT PAGE — interactive behaviors
   1. Clickable UPI app chips -> highlight + guide to QR + toast
   2. Drag-and-drop screenshot upload with live preview
   3. Countdown timer for payment urgency
   ========================================================== */

document.addEventListener('DOMContentLoaded', function () {

    /* ---------- Toast helper ---------- */
    let toastEl = document.querySelector('.payment-toast');
    if (!toastEl) {
        toastEl = document.createElement('div');
        toastEl.className = 'payment-toast';
        document.body.appendChild(toastEl);
    }

    let toastTimeout;
    function showToast(message) {
        toastEl.textContent = message;
        toastEl.classList.add('show');
        clearTimeout(toastTimeout);
        toastTimeout = setTimeout(() => {
            toastEl.classList.remove('show');
        }, 2600);
    }

    /* ---------- 1. UPI app chips ---------- */
    const appChips = document.querySelectorAll('.app-chip');
    const qrBox = document.querySelector('.qr-box');

    const appNames = {
        phonepe: 'PhonePe',
        gpay: 'Google Pay',
        paytm: 'Paytm'
    };

    appChips.forEach(chip => {
        chip.addEventListener('click', function (e) {
            // If the chip is a real deep-link (has an href starting with a scheme other than '#'),
            // let the browser attempt to open the app naturally — we just also show guidance.
            const app = chip.dataset.app;

            appChips.forEach(c => c.classList.remove('selected'));
            chip.classList.add('selected');

            if (qrBox) {
                qrBox.classList.remove('pulse');
                void qrBox.offsetWidth; // restart animation
                qrBox.classList.add('pulse');
                qrBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }

            showToast(`Scan the QR code above using ${appNames[app] || 'your UPI app'}`);
        });
    });

    /* ---------- 2. Drag-and-drop upload with preview ---------- */
    const uploadArea = document.querySelector('.upload-area');
    const fileInput = uploadArea ? uploadArea.querySelector('input[type="file"]') : null;

    if (uploadArea && fileInput) {

        const icon = document.createElement('i');
        icon.className = 'bi bi-cloud-arrow-up-fill upload-icon';

        const label = document.createElement('div');
        label.className = 'upload-label';
        label.textContent = 'Tap or drag your screenshot here';

        const filename = document.createElement('div');
        filename.className = 'upload-filename';

        const preview = document.createElement('img');
        preview.className = 'upload-preview';

        // Move the file input to the end so our custom UI renders above it visually,
        // while the input itself still covers the area for click/drag handling.
        uploadArea.prepend(preview);
        uploadArea.prepend(filename);
        uploadArea.prepend(label);
        uploadArea.prepend(icon);

        function handleFile(file) {
            if (!file) return;

            uploadArea.classList.add('has-file');
            icon.className = 'bi bi-check-circle-fill upload-icon';
            label.textContent = 'Screenshot ready';
            filename.textContent = file.name;

            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    preview.src = e.target.result;
                    preview.classList.add('show');
                };
                reader.readAsDataURL(file);
            }
        }

        fileInput.addEventListener('change', () => {
            if (fileInput.files && fileInput.files[0]) {
                handleFile(fileInput.files[0]);
            }
        });

        ['dragenter', 'dragover'].forEach(evt => {
            uploadArea.addEventListener(evt, (e) => {
                e.preventDefault();
                uploadArea.classList.add('drag-over');
            });
        });

        ['dragleave', 'drop'].forEach(evt => {
            uploadArea.addEventListener(evt, (e) => {
                e.preventDefault();
                uploadArea.classList.remove('drag-over');
            });
        });

        uploadArea.addEventListener('drop', (e) => {
            const file = e.dataTransfer.files[0];
            if (file) {
                fileInput.files = e.dataTransfer.files;
                handleFile(file);
            }
        });
    }

    /* ---------- 3. Countdown timer ---------- */
    const timerEl = document.getElementById('payment-timer-value');
    const timerWrap = document.querySelector('.payment-timer');

    if (timerEl && timerWrap) {
        let remaining = 10 * 60; // 10 minutes, cosmetic urgency cue

        const tick = () => {
            if (remaining <= 0) {
                timerEl.textContent = '00:00';
                return;
            }
            remaining--;
            const mins = Math.floor(remaining / 60).toString().padStart(2, '0');
            const secs = (remaining % 60).toString().padStart(2, '0');
            timerEl.textContent = `${mins}:${secs}`;

            if (remaining <= 120) {
                timerWrap.classList.add('urgent');
            }
        };

        setInterval(tick, 1000);
    }

});


/* ==========================================================
   MY ORDERS — status filter tabs (client-side, no reload)
   ========================================================== */

document.addEventListener('DOMContentLoaded', function () {

    const filterChips = document.querySelectorAll('.filter-chip');
    const orderCards = document.querySelectorAll('.order-card');

    if (!filterChips.length || !orderCards.length) return;

    filterChips.forEach(chip => {
        chip.addEventListener('click', function () {
            const filter = chip.dataset.filter;

            filterChips.forEach(c => c.classList.remove('active'));
            chip.classList.add('active');

            let visibleCount = 0;

            orderCards.forEach(card => {
                const status = card.dataset.status;

                if (filter === 'all' || status === filter) {
                    card.classList.remove('filtered-out');
                    visibleCount++;
                } else {
                    card.classList.add('filtered-out');
                }
            });

            // Show/hide a "no orders match this filter" message
            let emptyMsg = document.getElementById('filter-empty-msg');
            const ordersList = document.querySelector('.orders-list');

            if (visibleCount === 0) {
                if (!emptyMsg && ordersList) {
                    emptyMsg = document.createElement('div');
                    emptyMsg.id = 'filter-empty-msg';
                    emptyMsg.className = 'orders-empty';
                    emptyMsg.innerHTML = `
                        <div class="empty-icon">🔍</div>
                        <h3>No orders in this category</h3>
                        <p>Try a different filter above.</p>
                    `;
                    ordersList.appendChild(emptyMsg);
                }
            } else if (emptyMsg) {
                emptyMsg.remove();
            }
        });
    });

});




/* ==========================================================
   ORDER DETAIL — animated tracker fill, copy address, print
   ========================================================== */

document.addEventListener('DOMContentLoaded', function () {

    /* ---------- 1. Animate the tracker fill line ---------- */
    const wrapper = document.querySelector('.tracking-wrapper');

    if (wrapper) {
        const steps = wrapper.querySelectorAll('.step');
        const activeSteps = wrapper.querySelectorAll('.step.active');
        const totalSteps = steps.length;

        // Mark the last active step as "current" for the pulsing highlight
        if (activeSteps.length > 0) {
            activeSteps[activeSteps.length - 1].classList.add('current');
        }

        // Build the fill line element and animate its width in
        if (totalSteps > 1) {
            const fillLine = document.createElement('div');
            fillLine.className = 'line-fill';
            wrapper.prepend(fillLine);

            // Percentage of the track filled, based on completed steps
            const completedRatio = (activeSteps.length - 1) / (totalSteps - 1);
            const percent = Math.max(0, Math.min(100, completedRatio * 88)); // 88% ~ matches step-center spacing

            requestAnimationFrame(() => {
                setTimeout(() => {
                    fillLine.style.width = percent + '%';
                }, 200);
            });
        }
    }

    /* ---------- 2. Copy address to clipboard ---------- */
    const copyBtn = document.getElementById('copy-address-btn');

    if (copyBtn) {
        copyBtn.addEventListener('click', function () {
            const addressText = copyBtn.dataset.address || '';

            if (!addressText) return;

            navigator.clipboard.writeText(addressText).then(() => {
                const originalHTML = copyBtn.innerHTML;
                copyBtn.classList.add('copied');
                copyBtn.innerHTML = '<i class="bi bi-check-lg"></i> Copied';

                setTimeout(() => {
                    copyBtn.classList.remove('copied');
                    copyBtn.innerHTML = originalHTML;
                }, 2000);
            }).catch(() => {
                // Clipboard API unavailable (e.g. non-HTTPS) — fail silently, no broken UI
            });
        });
    }

    /* ---------- 3. Print order summary ---------- */
    const printBtn = document.getElementById('print-order-btn');

    if (printBtn) {
        printBtn.addEventListener('click', function () {
            window.print();
        });
    }

});







/* ==========================================================
   PROFILE PAGE — animated count-up for stat numbers
   ========================================================== */

document.addEventListener('DOMContentLoaded', function () {

    const statNumbers = document.querySelectorAll('.stat-number');
    if (!statNumbers.length) return;

    function animateCount(el) {
        const raw = el.dataset.value || '0';
        const prefix = el.dataset.prefix || '';
        const target = parseFloat(raw.replace(/[^0-9.]/g, '')) || 0;
        const hasDecimal = raw.includes('.');
        const duration = 1100;
        let startTime = null;

        function step(timestamp) {
            if (!startTime) startTime = timestamp;
            const progress = Math.min((timestamp - startTime) / duration, 1);
            // ease-out cubic
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = target * eased;

            el.textContent = prefix + (hasDecimal ? current.toFixed(2) : Math.round(current));

            if (progress < 1) {
                requestAnimationFrame(step);
            } else {
                el.textContent = prefix + (hasDecimal ? target.toFixed(2) : target);
            }
        }

        requestAnimationFrame(step);
    }

    // Animate once each card scrolls into view (also fires immediately if already visible)
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCount(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 });

    statNumbers.forEach(el => observer.observe(el));

});





/* ==========================================================
   EDIT PROFILE — live avatar preview, bio counter, save feedback
   ========================================================== */

document.addEventListener('DOMContentLoaded', function () {

    /* ---------- 1. Live avatar preview on file select ---------- */
    const avatarWrapper = document.querySelector('.profile-avatar-wrapper');
    const fileInput = document.getElementById('profile-pic-input');

    if (avatarWrapper && fileInput) {

        avatarWrapper.addEventListener('click', () => fileInput.click());

        fileInput.addEventListener('change', function () {
            const file = fileInput.files && fileInput.files[0];
            if (!file || !file.type.startsWith('image/')) return;

            const reader = new FileReader();
            reader.onload = (e) => {
                let img = avatarWrapper.querySelector('.profile-avatar-img');
                const placeholder = avatarWrapper.querySelector('.profile-avatar');

                if (!img) {
                    img = document.createElement('img');
                    img.className = 'profile-avatar-img';
                    avatarWrapper.insertBefore(img, avatarWrapper.firstChild);
                    if (placeholder) placeholder.style.display = 'none';
                }

                img.src = e.target.result;
            };
            reader.readAsDataURL(file);
        });
    }

    /* ---------- 2. Bio character counter ---------- */
    const bioField = document.getElementById('bio-field');
    const counterEl = document.getElementById('bio-char-counter');
    const maxLength = 250;

    if (bioField && counterEl) {

        function updateCounter() {
            const remaining = maxLength - bioField.value.length;
            counterEl.textContent = `${bioField.value.length} / ${maxLength}`;

            counterEl.classList.remove('warning', 'limit');
            if (remaining <= 0) {
                counterEl.classList.add('limit');
            } else if (remaining <= 30) {
                counterEl.classList.add('warning');
            }
        }

        bioField.addEventListener('input', updateCounter);
        updateCounter();
    }

    /* ---------- 3. Save button loading feedback ---------- */
    const form = document.querySelector('.edit-profile-card form');
    const saveBtn = document.querySelector('.save-btn');

    if (form && saveBtn) {
        form.addEventListener('submit', function () {
            saveBtn.classList.add('saving');
            saveBtn.innerHTML = '⏳ Saving...';
        });
    }

});



/* ==========================================================
   WISHLIST — heart burst micro-animation on "Add to Cart"
   Purely a delight touch; the actual add-to-cart still
   happens via the normal link/URL, this just adds flair
   before the page navigates.
   ========================================================== */

document.addEventListener('DOMContentLoaded', function () {

    document.querySelectorAll('.wishlist-btn.add-cart').forEach(btn => {
        btn.addEventListener('click', function (e) {
            const card = btn.closest('.product-card');
            if (!card) return;

            for (let i = 0; i < 6; i++) {
                const heart = document.createElement('span');
                heart.textContent = '💙';
                heart.style.position = 'absolute';
                heart.style.left = (40 + Math.random() * 20) + '%';
                heart.style.bottom = '70px';
                heart.style.fontSize = (14 + Math.random() * 10) + 'px';
                heart.style.pointerEvents = 'none';
                heart.style.zIndex = '5';
                heart.style.animation = `floatUp ${0.8 + Math.random() * 0.4}s ease-out forwards`;
                card.appendChild(heart);

                setTimeout(() => heart.remove(), 1300);
            }
        });
    });

    // Inject the keyframe once
    if (!document.getElementById('wishlist-float-keyframes')) {
        const style = document.createElement('style');
        style.id = 'wishlist-float-keyframes';
        style.textContent = `
            @keyframes floatUp {
                0% { transform: translateY(0) scale(0.6); opacity: 1; }
                100% { transform: translateY(-60px) scale(1.1); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }

});


/* ==========================================================
   EDIT REVIEW — clickable star rating, char counter, save feedback
   ========================================================== */

document.addEventListener('DOMContentLoaded', function () {

    /* ---------- 1. Star rating widget ---------- */
    const stars = document.querySelectorAll('.star-rating .star');
    const ratingInput = document.getElementById('rating-input');
    const ratingText = document.getElementById('rating-text');

    const labels = {
        1: 'Poor',
        2: 'Fair',
        3: 'Good',
        4: 'Very Good',
        5: 'Excellent'
    };

    function paintStars(value) {
        stars.forEach(star => {
            const starValue = parseInt(star.dataset.value, 10);
            star.classList.toggle('filled', starValue <= value);
        });
    }

    if (stars.length && ratingInput) {

        let currentRating = parseInt(ratingInput.value, 10) || 5;
        paintStars(currentRating);
        if (ratingText) ratingText.textContent = labels[currentRating] || '';

        stars.forEach(star => {
            const starValue = parseInt(star.dataset.value, 10);

            star.addEventListener('mouseenter', () => paintStars(starValue));

            star.addEventListener('mouseleave', () => paintStars(currentRating));

            star.addEventListener('click', () => {
                currentRating = starValue;
                ratingInput.value = starValue;
                paintStars(starValue);

                if (ratingText) ratingText.textContent = labels[starValue] || '';

                star.classList.remove('pop');
                void star.offsetWidth;
                star.classList.add('pop');
            });
        });
    }

    /* ---------- 2. Comment character counter ---------- */
    const commentField = document.getElementById('comment-field');
    const counterEl = document.getElementById('comment-char-counter');
    const maxLength = 500;

    if (commentField && counterEl) {

        function updateCounter() {
            const remaining = maxLength - commentField.value.length;
            counterEl.textContent = `${commentField.value.length} / ${maxLength}`;

            counterEl.classList.remove('warning', 'limit');
            if (remaining <= 0) {
                counterEl.classList.add('limit');
            } else if (remaining <= 40) {
                counterEl.classList.add('warning');
            }
        }

        commentField.addEventListener('input', updateCounter);
        updateCounter();
    }

    /* ---------- 3. Save button feedback ---------- */
    const form = document.querySelector('.review-card form');
    const updateBtn = document.querySelector('.update-btn');

    if (form && updateBtn) {
        form.addEventListener('submit', function () {
            updateBtn.classList.add('saving');
            updateBtn.innerHTML = '⏳ Updating...';
        });
    }

});



/* ==========================================================
   ADMIN DASHBOARD — animated count-up for stat numbers
   ========================================================== */

document.addEventListener('DOMContentLoaded', function () {

    const statNumbers = document.querySelectorAll('.dashboard-card .stat-number');
    if (!statNumbers.length) return;

    function animateCount(el) {
        const raw = el.dataset.value || '0';
        const prefix = el.dataset.prefix || '';
        const target = parseFloat(raw.replace(/[^0-9.]/g, '')) || 0;
        const hasDecimal = raw.includes('.');
        const duration = 1000;
        let startTime = null;

        function step(timestamp) {
            if (!startTime) startTime = timestamp;
            const progress = Math.min((timestamp - startTime) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = target * eased;

            el.textContent = prefix + (hasDecimal ? current.toFixed(2) : Math.round(current));

            if (progress < 1) {
                requestAnimationFrame(step);
            } else {
                el.textContent = prefix + (hasDecimal ? target.toFixed(2) : target);
            }
        }

        requestAnimationFrame(step);
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCount(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 });

    statNumbers.forEach(el => observer.observe(el));

});