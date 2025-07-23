'use client';

import { useEffect, useState } from 'react';
import { Toaster, toast } from 'react-hot-toast';
import axios from 'axios';
import './globals.css';

export default function Home() {
  const [question, setQuestion] = useState('');
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingStage, setLoadingStage] = useState(0);

  const loadingMessages = [
    '🧠 Thinking hard...',
    '🔍 Searching the AI brain...',
    '📚 Looking through knowledge base...',
    '💬 Formulating the perfect response...',
    '✨ Finalizing your answer...',
  ];

  useEffect(() => {
    fetchConversations();
  }, []);

  const fetchConversations = async () => {
    try {
      const res = await axios.get('https://test-production-d202.up.railway.app/conversations');
      setConversations(res.data.reverse());
    } catch {
      toast.error('Failed to load conversations');
    }
  };

  useEffect(() => {
    
    let interval: NodeJS.Timeout;

    interval = setInterval(() => {
      console.log('Running...');
    }, 1000);

    return () => clearInterval(interval);
  }, [loading]);

  const handleSubmit = async () => {
    if (!question.trim()) {
      toast.error('Please enter a question');
      return;
    }

    setLoading(true);
    try {
      await axios.post('https://test-production-d202.up.railway.app/query', { question });
      await fetchConversations();
      toast.success('Answer received!');
      setQuestion('');
    } catch {
      toast.error('Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = async () => {
    try {
      await axios.delete('https://test-production-d202.up.railway.app/conversations');
      setConversations([]);
      toast.success('Conversations cleared!');
    } catch {
      toast.error('Failed to clear');
    }
  };

  return (
    <main className="main-wrapper">
      <Toaster />
      <div className="chat-container">
        <header className="chat-header">
          Ask Me Anything 🤖
        </header>

        <div className="chat-history">
          {loading && (
            <div className="chat-message ai italic">
              {loadingMessages[loadingStage]}
            </div>
          )}
          {conversations.map((conv, idx) => (
            <div key={idx} className="chat-pair">
              <div className="chat-message user">
                <strong>You:</strong> {conv.question}
              </div>
              <div className="chat-message ai">
                <strong>AI:</strong> {conv.answer}
              </div>
            </div>
          ))}
        </div>

        <div className="chat-input">
          <textarea
            className="chat-textarea"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Type your question..."
            rows={2}
          />
          <div className="chat-actions">
            <button onClick={handleSubmit} disabled={loading} className="submit-btn">
              {loading ? 'Thinking...' : '💬 Get Answer'}
            </button>
            <button onClick={handleClear} className="clear-btn">
              🗑️ Clear Chat
            </button>
          </div>
        </div>
      </div>
    </main>
  );
}





