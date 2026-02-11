let conversationId = null;
const messagesEl = document.getElementById('messages');
const inputEl = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');

inputEl.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

async function sendMessage() {
    const message = inputEl.value.trim();
    if (!message) return;

    addMessage(message, 'user');
    inputEl.value = '';
    sendBtn.disabled = true;

    const loadingEl = document.createElement('div');
    loadingEl.className = 'message bot loading';
    messagesEl.appendChild(loadingEl);
    messagesEl.scrollTop = messagesEl.scrollHeight;

    try {
        const resp = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, conversation_id: conversationId }),
        });

        messagesEl.removeChild(loadingEl);

        if (!resp.ok) {
            const err = await resp.json();
            addMessage(`오류: ${err.detail || '알 수 없는 오류'}`, 'bot');
            return;
        }

        const data = await resp.json();
        conversationId = data.conversation_id;
        addMessage(data.reply, 'bot');
    } catch (err) {
        messagesEl.removeChild(loadingEl);
        addMessage(`네트워크 오류: ${err.message}`, 'bot');
    } finally {
        sendBtn.disabled = false;
        inputEl.focus();
    }
}

function addMessage(text, type) {
    const el = document.createElement('div');
    el.className = `message ${type}`;
    const content = document.createElement('div');
    content.className = 'message-content';
    content.innerHTML = formatMessage(text);
    el.appendChild(content);
    messagesEl.appendChild(el);
    messagesEl.scrollTop = messagesEl.scrollHeight;
}

function formatMessage(text) {
    return text
        .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
        .replace(/\n/g, '<br>');
}
