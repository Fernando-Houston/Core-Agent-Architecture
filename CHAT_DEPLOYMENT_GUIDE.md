# Houston Intelligence Chat Interface - Deployment Guide

## 🚀 Quick Deployment Options

### Option 1: Streamlit Cloud (RECOMMENDED - FREE)

1. **Push chat app to GitHub**
```bash
git add houston_intelligence_chat.py requirements_streamlit.txt
git commit -m "Add Streamlit chat interface"
git push
```

2. **Deploy on Streamlit**
- Go to: https://streamlit.io/cloud
- Sign in with GitHub
- New app → Select `Core-Agent-Architecture` repo
- Main file: `houston_intelligence_chat.py`
- Click Deploy!

3. **Set Environment Variable**
In Streamlit Cloud settings, add:
```
API_URL=https://your-railway-app.railway.app
```

**Live in 2 minutes at: https://yourapp.streamlit.app**

### Option 2: Simple HTML/JS (No Backend Needed)

Create `chat.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Houston Intelligence Chat</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 0 auto; padding: 20px; }
        #chat { height: 400px; overflow-y: scroll; border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; }
        .message { margin: 10px 0; }
        .user { color: blue; }
        .assistant { color: green; }
        #input-area { display: flex; gap: 10px; }
        #query { flex: 1; padding: 10px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h1>🏗️ Houston Intelligence Platform</h1>
    <div id="chat"></div>
    <div id="input-area">
        <input type="text" id="query" placeholder="Ask about Houston real estate..." />
        <button onclick="sendQuery()">Send</button>
        <button onclick="startVoice()">🎤 Voice</button>
    </div>

    <script>
        const API_URL = 'https://your-railway-app.railway.app';
        
        async function sendQuery() {
            const query = document.getElementById('query').value;
            if (!query) return;
            
            addMessage('user', query);
            document.getElementById('query').value = '';
            
            try {
                const response = await fetch(`${API_URL}/api/v1/query`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query })
                });
                
                const data = await response.json();
                addMessage('assistant', data.response?.answer || 'No response');
            } catch (error) {
                addMessage('assistant', 'Error: ' + error.message);
            }
        }
        
        function addMessage(role, content) {
            const chat = document.getElementById('chat');
            chat.innerHTML += `<div class="message ${role}"><b>${role}:</b> ${content}</div>`;
            chat.scrollTop = chat.scrollHeight;
        }
        
        function startVoice() {
            if ('webkitSpeechRecognition' in window) {
                const recognition = new webkitSpeechRecognition();
                recognition.onresult = (event) => {
                    document.getElementById('query').value = event.results[0][0].transcript;
                    sendQuery();
                };
                recognition.start();
            } else {
                alert('Voice input not supported in this browser');
            }
        }
        
        // Enter key to send
        document.getElementById('query').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendQuery();
        });
    </script>
</body>
</html>
```

Deploy on Vercel/Netlify in 1 minute!

### Option 3: Vercel with Next.js (More Advanced)

```bash
npx create-next-app houston-chat --typescript --tailwind
cd houston-chat
```

Create `app/page.tsx`:
```typescript
'use client';
import { useState } from 'react';

export default function Chat() {
  const [messages, setMessages] = useState<Array<{role: string, content: string}>>([]);
  const [input, setInput] = useState('');
  
  const sendMessage = async () => {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: input })
    });
    
    const data = await response.json();
    setMessages([...messages, 
      { role: 'user', content: input },
      { role: 'assistant', content: data.response?.answer || 'No response' }
    ]);
    setInput('');
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Houston Intelligence Chat</h1>
      <div className="border rounded p-4 h-96 overflow-y-auto mb-4">
        {messages.map((msg, i) => (
          <div key={i} className={`mb-2 ${msg.role === 'user' ? 'text-blue-600' : 'text-green-600'}`}>
            <strong>{msg.role}:</strong> {msg.content}
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <input 
          className="flex-1 border rounded px-3 py-2"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Ask about Houston real estate..."
        />
        <button 
          className="bg-blue-500 text-white px-4 py-2 rounded"
          onClick={sendMessage}
        >
          Send
        </button>
      </div>
    </div>
  );
}
```

## 🎯 Recommendation

**Use Streamlit** - It's the fastest and includes:
- ✅ Chat interface
- ✅ Voice input/output
- ✅ Example queries
- ✅ API testing tools
- ✅ Real-time insights
- ✅ FREE hosting

## 📱 Testing Features

The chat interface includes:
1. **Natural language queries** - "Show me investment opportunities"
2. **Voice input** - Click microphone to speak
3. **Quick actions** - Pre-built example queries
4. **API status** - Live connection monitoring
5. **Data insights** - Latest permits, trends, etc.

## 🔗 After Deployment

Share the chat URL with testers:
```
https://houston-intelligence.streamlit.app
```

They can immediately start testing:
- Natural language queries
- Voice commands
- API endpoints
- Real-time data

Perfect for getting feedback on the system!