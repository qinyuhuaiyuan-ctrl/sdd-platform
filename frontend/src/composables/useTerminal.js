// frontend/src/composables/useTerminal.js
import { ref } from 'vue'
import { Terminal } from '@xterm/xterm'
import { FitAddon } from '@xterm/addon-fit'
import { WebLinksAddon } from '@xterm/addon-web-links'

export function useTerminal() {
  const terminal = ref(null)
  const connected = ref(false)
  let ws = null
  let fitAddon = null

  function init(container) {
    const term = new Terminal({
      cursorBlink: true,
      fontSize: 14,
      fontFamily: 'Menlo, Monaco, "Courier New", monospace',
      theme: {
        background: '#1e1e2e',
        foreground: '#cdd6f4',
        cursor: '#f5e0dc',
      },
      rows: 24,
    })

    fitAddon = new FitAddon()
    term.loadAddon(fitAddon)
    term.loadAddon(new WebLinksAddon())
    term.open(container)
    fitAddon.fit()

    terminal.value = term

    const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:'
    ws = new WebSocket(`${protocol}//${location.host}/api/terminal`)

    ws.onopen = () => { connected.value = true }
    ws.onclose = () => { connected.value = false }
    ws.onmessage = (event) => {
      if (event.data instanceof Blob) {
        event.data.arrayBuffer().then(buf => {
          term.write(new Uint8Array(buf))
        })
      } else {
        term.write(event.data)
      }
    }

    term.onData((data) => {
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(data)
      }
    })

    fitAddon.fit()
    term.onResize(({ cols, rows }) => {
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ cols, rows }))
      }
    })

    window.addEventListener('resize', () => fitAddon.fit())
  }

  function dispose() {
    if (ws) ws.close()
    if (terminal.value) terminal.value.dispose()
  }

  return { terminal, connected, init, dispose }
}
