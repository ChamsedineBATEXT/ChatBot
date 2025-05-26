import React, { useState } from 'react';

function ChatBot() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);

    const sendMessage = async () => {
        if (!input.trim()) return;

        const userMessage = { sender: 'user', text: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setLoading(true);

        try {
            const response = await fetch('http://localhost:5000/api/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: input })
            });

            const data = await response.json();
            const botMessage = {
                sender: 'bot',
                text: data.response || 'Erreur dans la réponse.'
            };

            setMessages(prev => [...prev, botMessage]);
        } catch (error) {
            setMessages(prev => [...prev, { sender: 'bot', text: "❌ Erreur lors de la requête à l'API." }]);
            console.error(error);
        }

        setLoading(false);
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') sendMessage();
    };

    return (
        <div style={styles.container}>
            <h2 style={styles.title}>💬 ChatBot PDF</h2>

            <div style={styles.chatBox}>
                {messages.map((msg, i) => (
                    <div
                        key={i}
                        style={{
                            ...styles.message,
                            alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start',
                            backgroundColor: msg.sender === 'user' ? '#dcf8c6' : '#e2e2e2',
                        }}
                    >
                        <strong>{msg.sender === 'user' ? '👤' : '🤖'}</strong> {msg.text}
                    </div>
                ))}
                {loading && (
                    <div style={{ ...styles.message, fontStyle: 'italic', color: '#888' }}>
                        🤖 est en train de réfléchir...
                    </div>
                )}
            </div>

            <div style={styles.inputContainer}>
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Pose ta question..."
                    style={styles.input}
                />
                <button onClick={sendMessage} disabled={loading} style={styles.button}>
                    {loading ? '...' : 'Envoyer'}
                </button>
            </div>
        </div>
    );
}

const styles = {
    container: {
        maxWidth: 700,
        margin: '2rem auto',
        padding: '1rem',
        fontFamily: 'sans-serif',
    },
    title: {
        textAlign: 'center',
        marginBottom: '1rem',
    },
    chatBox: {
        border: '1px solid #ccc',
        borderRadius: '8px',
        padding: '1rem',
        height: '400px',
        overflowY: 'auto',
        display: 'flex',
        flexDirection: 'column',
        gap: '0.5rem',
        marginBottom: '1rem',
        backgroundColor: '#f9f9f9',
    },
    message: {
        padding: '0.6rem 1rem',
        borderRadius: '16px',
        maxWidth: '75%',
    },
    inputContainer: {
        display: 'flex',
        gap: '0.5rem',
    },
    input: {
        flex: 1,
        padding: '0.6rem',
        borderRadius: '8px',
        border: '1px solid #ccc',
    },
    button: {
        padding: '0.6rem 1rem',
        borderRadius: '8px',
        border: 'none',
        backgroundColor: '#4CAF50',
        color: 'white',
        cursor: 'pointer',
    },
};

export default ChatBot;
