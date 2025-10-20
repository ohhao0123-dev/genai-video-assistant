import React, { useState } from 'react'
import { invoke } from '@tauri-apps/api/core'

type Msg = { role: 'user' | 'assistant', content: string }

export default function App() {
  const [videoPath, setVideoPath] = useState<string>('')
  const [input, setInput] = useState<string>('')
  const [sessionId, setSessionId] = useState<string>('default')
  const [chat, setChat] = useState<Msg[]>([])
  const [artifacts, setArtifacts] = useState<string[]>([])
  const [clar, setClar] = useState<string>('')

  // === send() ===
  async function send() {
    if (!input.trim()) return
    const query = input.trim()
    setChat(c => [...c, { role: 'user', content: query }])
    setInput('')

    try {
      const resp = await invoke<any>('process_query', { videoPath, query, sessionId })
      if (resp.clarification_prompt) setClar(resp.clarification_prompt)
      if (resp.answer) setChat(c => [...c, { role: 'assistant', content: resp.answer }])
      if (resp.artifacts?.length) setArtifacts(a => [...a, ...resp.artifacts])
    } catch (err: any) {
      setClar(`Frontend request failed: ${String(err?.message || err)}`)
    }
  }

  // === genReport() ===
  async function genReport(fmt: 'pdf' | 'pptx') {
    try {
      const resp = await invoke<any>('generate_report', { sessionId, fmt })
      setArtifacts(a => [...a, resp.path])
      setChat(c => [
        ...c,
        { role: 'assistant', content: `Generated ${fmt.toUpperCase()} at ${resp.path}` },
      ])
    } catch (err: any) {
      setClar(`Report generation failed: ${String(err?.message || err)}`)
    }
  }

  return (
    <div style={{ fontFamily: 'ui-sans-serif', padding: 16 }}>
      <h1>GenAI Video Assistant</h1>

      {/* Video path input and report generation buttons */}
      <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
        <input
          style={{ flex: 1 }}
          placeholder="Absolute path to .mp4"
          value={videoPath}
          onChange={e => setVideoPath(e.target.value)}
        />
        <button onClick={() => genReport('pdf')}>PDF</button>
        <button onClick={() => genReport('pptx')}>PPTX</button>
      </div>

      {/* Chat display */}
      <div
        style={{
          marginTop: 16,
          border: '1px solid #ddd',
          borderRadius: 8,
          padding: 12,
          height: 360,
          overflow: 'auto',
        }}
      >
        {chat.map((m, i) => (
          <div key={i} style={{ marginBottom: 8 }}>
            <b>{m.role === 'user' ? 'You' : 'Assistant'}:</b> {m.content}
          </div>
        ))}
        {clar && (
          <div
            style={{
              background: '#fff3cd',
              padding: 8,
              borderRadius: 6,
              border: '1px solid #ffeeba',
            }}
          >
            <b>Clarification:</b> {clar}
          </div>
        )}
      </div>

      {/* Input bar for user queries */}
      <div style={{ display: 'flex', gap: 8, marginTop: 8 }}>
        <input
          style={{ flex: 1 }}
          placeholder="Ask: Transcribe the video / What objects are shown / Create a PowerPoint / Summarize to PDF"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => (e.key === 'Enter' ? send() : null)}
        />
        <button onClick={send}>Send</button>
      </div>

      {/* Artifact list */}
      <div style={{ marginTop: 16 }}>
        <h3>Artifacts</h3>
        <ul>
          {artifacts.map((a, i) => (
            <li key={i}>{a}</li>
          ))}
        </ul>
      </div>
    </div>
  )
}
