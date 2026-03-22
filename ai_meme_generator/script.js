// Floating emojis — runs immediately without waiting for DOM load
(function initFloatingEmojis() {
    const emojis = ['😂', '🤣', '💀', '🔥', '🤡', '😭', '🤯', '🥑', '🌮', '🍌', '💅', '🎃', '👀', '🫠', '🗿', '💩', '🧠', '👽', '🤖', '🦆', '🐸', '🎭', '🎪', '🤦', '😈', '🥲', '😤', '🙃', '🫡', '🤌', '⚡', '🌈'];

    function createEmoji() {
        const container = document.getElementById('emojiContainer');
        if (!container) return;

        const el = document.createElement('div');
        el.className = 'floating-emoji';
        el.innerText = emojis[Math.floor(Math.random() * emojis.length)];

        // Random horizontal position
        el.style.left = (Math.random() * 98) + 'vw';

        // Random size between 1.5rem and 4rem
        const size = 1.5 + Math.random() * 2.5;
        el.style.fontSize = size + 'rem';

        // Duration 8–18s
        const duration = 8 + Math.random() * 10;
        el.style.animationDuration = duration + 's';

        // Random delay offset so they don't all start together
        el.style.animationDelay = '0s';

        // Opacity 0.25–0.7
        el.style.opacity = (0.25 + Math.random() * 0.45).toFixed(2);

        container.appendChild(el);

        // Clean up once animation completes
        setTimeout(() => el.remove(), duration * 1000 + 500);
    }

    // Wait until DOM is ready
    document.addEventListener('DOMContentLoaded', () => {
        // Initial burst with staggered timings
        for (let i = 0; i < 30; i++) {
            setTimeout(createEmoji, i * 200);
        }
        // Keep generating continuously
        setInterval(createEmoji, 800);
    });
})();

document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const dropzone       = document.getElementById('dropzone');
    const imageInput     = document.getElementById('imageInput');
    const imagePreview   = document.getElementById('imagePreview');
    const removeImageBtn = document.getElementById('removeImageBtn');
    const generateBtn    = document.getElementById('generateBtn');
    const humorStyleSelect = document.getElementById('humorStyle');
    const resultsContainer = document.getElementById('resultsContainer');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const uploadContent    = document.querySelector('.upload-content');
    const resultsBadge     = document.getElementById('resultsBadge');

    let selectedFile = null;

    const emptyStateHTML = `
        <div class="placeholder-icon bounce">😶‍🌫️</div>
        <p>Your hilarious captions will appear here.</p>
        <p class="hint">Upload an image to get started!</p>
    `;

    // --- Validate Form State ---
    function validateForm() {
        generateBtn.disabled = !selectedFile;
    }

    // --- Drag and Drop ---
    dropzone.addEventListener('click', (e) => {
        if (e.target !== removeImageBtn && !removeImageBtn.contains(e.target)) {
            imageInput.click();
        }
    });

    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
    });

    ['dragleave', 'dragend'].forEach(type => {
        dropzone.addEventListener(type, (e) => {
            e.preventDefault();
            dropzone.classList.remove('dragover');
        });
    });

    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    imageInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    function handleFile(file) {
        if (!file.type.match('image.*')) {
            alert('Please upload a valid image file (JPG, PNG).');
            return;
        }
        selectedFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block';
            removeImageBtn.style.display = 'flex';
            uploadContent.style.opacity = '0';
        };
        reader.readAsDataURL(file);
        validateForm();
    }

    removeImageBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        selectedFile = null;
        imageInput.value = '';
        imagePreview.src = '';
        imagePreview.style.display = 'none';
        removeImageBtn.style.display = 'none';
        uploadContent.style.opacity = '1';
        resultsBadge.style.display = 'none';
        validateForm();
    });

    // --- Generate ---
    generateBtn.addEventListener('click', async () => {
        if (!selectedFile) return;

        generateBtn.disabled = true;
        generateBtn.innerHTML = '<span>Working...</span>';
        loadingIndicator.style.display = 'flex';
        resultsContainer.innerHTML = '';
        resultsContainer.classList.remove('empty-state');
        resultsBadge.style.display = 'none';

        const formData = new FormData();
        formData.append('image', selectedFile);
        formData.append('humor_style', humorStyleSelect.value);

        try {
            const response = await fetch('/api/generate', { method: 'POST', body: formData });
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Something went wrong on the server');
            }

            const htmlContent = marked.parse(data.captions);
            resultsContainer.innerHTML = htmlContent;
            resultsBadge.style.display = 'inline-block';

        } catch (error) {
            console.error(error);
            resultsContainer.innerHTML = `
                <div style="color: var(--error); display:flex; align-items:center; gap:0.5rem;">
                    <i class="fa-solid fa-triangle-exclamation"></i>
                    <span>Error: ${error.message}</span>
                </div>`;
        } finally {
            loadingIndicator.style.display = 'none';
            generateBtn.innerHTML = '<span>Generate Memes</span><i class="fa-solid fa-wand-magic-sparkles"></i>';
            validateForm();
        }
    });
});
