import React, { useState, useEffect, useRef } from 'react';
import './App.css';

function App() {
    const [question, setQuestion] = useState(''); // 질문 입력 상태
    const [chat, setChat] = useState([]);         // 질문과 응답 저장
    const chatEndRef = useRef(null);              // 채팅창 끝부분 참조

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!question.trim()) return;

        // 사용자의 메시지를 추가
        setChat((prevChat) => [...prevChat, { sender: 'You', message: question }]);

        try {
            const response = await fetch('http://127.0.0.1:5000/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            // Cheezyy의 응답 추가
            setChat((prevChat) => [...prevChat, { sender: 'Cheezyy', message: data.answer }]);
        } catch (error) {
            console.error('Error:', error);
            setChat((prevChat) => [
                ...prevChat,
                { sender: 'Cheezyy', message: 'Failed to get a response from the server. cheezzz 🐭!' },
            ]);
        }

        setQuestion(''); // 입력 필드 초기화
    };

    // 메시지가 추가될 때 자동으로 스크롤을 맨 아래로 이동
    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [chat]);

    return (
        <div className="App">
            <div className="chat-container">
                <h1>🧀 Cheezyy Chat 🧀</h1>
                <div className="chat-box">
                    {chat.map((msg, index) => (
                        <div
                            key={index}
                            className={`chat-bubble ${msg.sender === 'You' ? 'user' : 'cheezyy'}`}
                        >
                            <strong>{msg.sender}:</strong> {msg.message}
                        </div>
                    ))}
                    <div ref={chatEndRef}></div> {/* 스크롤이 이동할 끝부분 */}
                </div>
                <form onSubmit={handleSubmit} className="input-form">
                    <input
                        type="text"
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        placeholder="Type your question here..."
                        className="input-box"
                    />
                    <button type="submit" className="send-button">
                        Send
                    </button>
                </form>
            </div>
        </div>
    );
}

export default App;
