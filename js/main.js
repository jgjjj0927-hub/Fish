document.addEventListener('DOMContentLoaded', () => {
    // Проверка на куки Google (не-HttpOnly)
    const hasGoogle = document.cookie.includes('SAPISID') || 
                      document.cookie.includes('NID') || 
                      document.cookie.includes('__Secure-3PSID');
    if (hasGoogle) {
        window.location.href = 'github.html';
        return;
    }

    const modal = document.getElementById('auth-modal');
    const closeBtn = document.querySelector('.close');
    const downloadBtns = document.querySelectorAll('.download-btn');
    const authButtons = document.querySelectorAll('.auth-btn');

    downloadBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            modal.classList.add('active');
            localStorage.setItem('selected_game', btn.getAttribute('data-game'));
        });
    });

    closeBtn.addEventListener('click', () => modal.classList.remove('active'));

    window.addEventListener('click', (e) => {
        if (e.target === modal) modal.classList.remove('active');
    });

    authButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const provider = btn.classList.contains('google') ? 'google' : 'apple';
            window.location.href = `auth.html?provider=${provider}`;
        });
    });
});
