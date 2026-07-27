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