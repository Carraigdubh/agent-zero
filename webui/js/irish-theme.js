// Irish Theme JavaScript Enhancements for Father Ted Interface

document.addEventListener('DOMContentLoaded', function() {
    // Add shamrock icons to specific elements
    const addShamrocks = () => {
        // Add shamrocks to persona headers
        const personaHeaders = document.querySelectorAll('.message-header');
        personaHeaders.forEach(header => {
            if (!header.querySelector('.shamrock-left')) {
                const shamrockLeft = document.createElement('span');
                shamrockLeft.className = 'shamrock-left';
                shamrockLeft.innerHTML = '☘️';
                shamrockLeft.style.cssText = 'position: absolute; left: 10px; opacity: 0.6;';
                header.style.position = 'relative';
                header.appendChild(shamrockLeft);
            }
        });

        // Add Celtic cross to settings button
        const settingsBtn = document.querySelector('button:has(.fa-cog)');
        if (settingsBtn && !settingsBtn.querySelector('.celtic-icon')) {
            const celticIcon = document.createElement('span');
            celticIcon.className = 'celtic-icon';
            celticIcon.innerHTML = '✝️';
            celticIcon.style.cssText = 'margin-left: 5px; font-size: 0.8em;';
            settingsBtn.appendChild(celticIcon);
        }
    };

    // Add Irish greeting to messages and emphasis to FECK
    const addIrishGreeting = () => {
        const messages = document.querySelectorAll('.message');
        messages.forEach(msg => {
            if (!msg.dataset.irishProcessed) {
                // Find all text nodes that might contain FECK
                const walker = document.createTreeWalker(
                    msg,
                    NodeFilter.SHOW_TEXT,
                    null,
                    false
                );

                const textNodes = [];
                let node;
                while (node = walker.nextNode()) {
                    if (node.nodeValue && (node.nodeValue.includes('FECK') || node.nodeValue.includes('Feck') || node.nodeValue.includes('feck'))) {
                        textNodes.push(node);
                    }
                }

                // Replace FECK with emphasized version in text nodes
                textNodes.forEach(textNode => {
                    const span = document.createElement('span');
                    span.innerHTML = textNode.nodeValue.replace(/FECK(!)?|Feck(!)?|feck(!)?/g, '<span class="feck-emphasis">$&</span>');
                    textNode.parentNode.replaceChild(span, textNode);
                });

                msg.dataset.irishProcessed = 'true';
            }
        });
    };

    // Create floating shamrock animation
    const createFloatingShamrock = () => {
        const shamrock = document.createElement('div');
        shamrock.className = 'floating-shamrock';
        shamrock.innerHTML = '🍀';
        shamrock.style.cssText = `
            position: fixed;
            font-size: 2rem;
            opacity: 0.1;
            pointer-events: none;
            z-index: 1000;
            animation: float-across 15s linear infinite;
            top: ${Math.random() * window.innerHeight}px;
            left: -50px;
        `;
        document.body.appendChild(shamrock);
        
        setTimeout(() => shamrock.remove(), 15000);
    };

    // Add floating shamrock CSS animation
    if (!document.querySelector('#irish-animations')) {
        const style = document.createElement('style');
        style.id = 'irish-animations';
        style.textContent = `
            @keyframes float-across {
                from {
                    transform: translateX(0) rotate(0deg);
                }
                to {
                    transform: translateX(calc(100vw + 100px)) rotate(360deg);
                }
            }
            
            .message-header .shamrock-left {
                animation: gentle-sway 3s ease-in-out infinite;
            }
            
            @keyframes gentle-sway {
                0%, 100% { transform: translateX(0) rotate(0deg); }
                50% { transform: translateX(3px) rotate(10deg); }
            }
        `;
        document.head.appendChild(style);
    }

    // Run enhancements
    addShamrocks();
    addIrishGreeting();
    
    // Run again after a short delay to catch any dynamically loaded content
    setTimeout(() => {
        addShamrocks();
        addIrishGreeting();
    }, 1000);
    
    // Add floating shamrocks occasionally
    setInterval(() => {
        if (Math.random() < 0.1) { // 10% chance every interval
            createFloatingShamrock();
        }
    }, 5000);

    // Watch for new messages and apply Irish styling
    const observer = new MutationObserver(() => {
        addShamrocks();
        addIrishGreeting();
    });

    const chatContainer = document.querySelector('#chat-messages');
    if (chatContainer) {
        observer.observe(chatContainer, { childList: true, subtree: true });
    }
});