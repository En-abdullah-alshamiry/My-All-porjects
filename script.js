document.addEventListener('DOMContentLoaded', () => {
    const card = document.getElementById('card');
    const encryptBtn = document.getElementById('encrypt-btn');
    const decryptBtn = document.getElementById('decrypt-btn');
    const copyBtn = document.getElementById('copy-btn');
    const algoSelect = document.getElementById('algo-select');
    const dataInput = document.getElementById('data-input');
    const keyInput = document.getElementById('key-input');
    const resultOutput = document.getElementById('result-output');

    // --- 3D Tilt Effect ---
    const handleMove = (e) => {
        const { clientX, clientY } = e.touches ? e.touches[0] : e;
        const { left, top, width, height } = card.getBoundingClientRect();
        
        const x = (clientX - left) / width - 0.5;
        const y = (clientY - top) / height - 0.5;

        // Limit rotation to 15 degrees
        const tiltX = y * 15; 
        const tiltY = -x * 15;

        card.style.transform = `rotateX(${tiltX}deg) rotateY(${tiltY}deg)`;
    };

    const resetTilt = () => {
        card.style.transform = `rotateX(0deg) rotateY(0deg)`;
    };

    document.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const isInCard = e.clientX >= rect.left - 50 && e.clientX <= rect.right + 50 &&
                         e.clientY >= rect.top - 50 && e.clientY <= rect.bottom + 50;
        
        if (isInCard) {
            handleMove(e);
        } else {
            resetTilt();
        }
    });

    card.addEventListener('mouseleave', resetTilt);
    card.addEventListener('touchmove', handleMove);
    card.addEventListener('touchend', resetTilt);


    // --- Encryption Logic ---

    const processCrypto = (action) => {
        const data = dataInput.value.trim();
        const key = keyInput.value.trim();
        const algo = algoSelect.value;

        if (!data || !key) {
            alert('يرجى إدخال النص والمفتاح السري!');
            return;
        }

        try {
            let result = '';
            
            if (action === 'encrypt') {
                switch (algo) {
                    case 'AES':
                        result = CryptoJS.AES.encrypt(data, key).toString();
                        break;
                    case 'DES':
                        result = CryptoJS.DES.encrypt(data, key).toString();
                        break;
                    case 'TripleDES':
                        result = CryptoJS.TripleDES.encrypt(data, key).toString();
                        break;
                }
            } else {
                let bytes;
                switch (algo) {
                    case 'AES':
                        bytes = CryptoJS.AES.decrypt(data, key);
                        break;
                    case 'DES':
                        bytes = CryptoJS.DES.decrypt(data, key);
                        break;
                    case 'TripleDES':
                        bytes = CryptoJS.TripleDES.decrypt(data, key);
                        break;
                }
                result = bytes.toString(CryptoJS.enc.Utf8);
                
                if (!result) {
                    throw new Error('Key or Data is incorrect');
                }
            }

            resultOutput.value = result;
            
            // Subtle success animation on result box
            resultOutput.parentElement.animate([
                { transform: 'scale(1)', opacity: 1 },
                { transform: 'scale(1.02)', opacity: 0.8 },
                { transform: 'scale(1)', opacity: 1 }
            ], { duration: 300 });

        } catch (error) {
            console.error(error);
            alert('حدث خطأ! تأكد من صحة البيانات أو المفتاح المستخدم.');
            resultOutput.value = '';
        }
    };

    encryptBtn.addEventListener('click', () => processCrypto('encrypt'));
    decryptBtn.addEventListener('click', () => processCrypto('decrypt'));

    // --- Copy to Clipboard ---
    copyBtn.addEventListener('click', () => {
        if (!resultOutput.value) return;
        
        navigator.clipboard.writeText(resultOutput.value).then(() => {
            const originalSvg = copyBtn.innerHTML;
            copyBtn.innerHTML = '<span style="color: #4ade80; font-size: 12px;">تم!</span>';
            setTimeout(() => {
                copyBtn.innerHTML = originalSvg;
            }, 2000);
        });
    });
});
