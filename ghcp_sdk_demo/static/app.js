// ─── GitHub Copilot SDK Demo - Frontend ───

// タブ切り替え
document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    tab.classList.add('active');
    document.getElementById(`tab-${tab.dataset.tab}`).classList.add('active');
  });
});

// ─── ユーティリティ ───

function addMessage(containerId, role, text) {
  const container = document.getElementById(containerId);
  const div = document.createElement('div');
  div.className = `message ${role}`;
  div.textContent = text;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  return div;
}

function setFormLoading(formId, loading) {
  const form = document.getElementById(formId);
  const btn = form.querySelector('button');
  const inputs = form.querySelectorAll('input, select');
  btn.disabled = loading;
  inputs.forEach(i => i.disabled = loading);
  btn.textContent = loading ? '生成中...' : '送信';
  if (formId === 'codegen-form') btn.textContent = loading ? '生成中...' : '生成';
}

/**
 * SSE ストリームを読んで処理する共通関数
 * @param {string} url - API エンドポイント
 * @param {object} body - リクエストボディ
 * @param {object} handlers - イベントハンドラ { onDelta, onDone, onToolStart, onError }
 */
async function streamRequest(url, body, handlers) {
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      const errText = await res.text();
      handlers.onError?.(errText);
      return;
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        try {
          const data = JSON.parse(line.slice(6));
          if (data.type === 'delta') {
            handlers.onDelta?.(data.content);
          } else if (data.type === 'done') {
            handlers.onDone?.(data.content);
          } else if (data.type === 'tool_start') {
            handlers.onToolStart?.(data.tool);
          }
        } catch (e) {
          // JSON パースエラーは無視
        }
      }
    }
  } catch (err) {
    handlers.onError?.(err.message);
  }
}

// ─── チャットデモ ───

document.getElementById('chat-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const input = document.getElementById('chat-input');
  const prompt = input.value.trim();
  if (!prompt) return;

  input.value = '';
  addMessage('chat-messages', 'user', prompt);
  setFormLoading('chat-form', true);

  const assistantDiv = addMessage('chat-messages', 'assistant', '');

  await streamRequest('/api/chat', { prompt }, {
    onDelta(content) {
      assistantDiv.textContent += content;
      assistantDiv.parentElement.scrollTop = assistantDiv.parentElement.scrollHeight;
    },
    onDone() {
      // ストリーミング完了
    },
    onError(err) {
      assistantDiv.textContent = `⚠️ エラー: ${err}`;
      assistantDiv.style.color = '#f85149';
    },
  });

  setFormLoading('chat-form', false);
});

// ─── コード生成デモ ───

document.getElementById('codegen-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const input = document.getElementById('codegen-input');
  const lang = document.getElementById('codegen-language');
  const description = input.value.trim();
  if (!description) return;

  const codeEl = document.getElementById('codegen-code');
  codeEl.textContent = '';
  setFormLoading('codegen-form', true);

  await streamRequest('/api/codegen', { description, language: lang.value }, {
    onDelta(content) {
      codeEl.textContent += content;
    },
    onDone() {},
    onError(err) {
      codeEl.textContent = `⚠️ エラー: ${err}`;
    },
  });

  setFormLoading('codegen-form', false);
});

// ─── カスタムツールデモ ───

document.getElementById('tools-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const input = document.getElementById('tools-input');
  const prompt = input.value.trim();
  if (!prompt) return;

  input.value = '';
  addMessage('tools-messages', 'user', prompt);
  setFormLoading('tools-form', true);

  const assistantDiv = addMessage('tools-messages', 'assistant', '');

  await streamRequest('/api/tools', { prompt }, {
    onDelta(content) {
      assistantDiv.textContent += content;
      assistantDiv.parentElement.scrollTop = assistantDiv.parentElement.scrollHeight;
    },
    onDone() {},
    onToolStart(toolName) {
      addMessage('tools-messages', 'tool-call', `🔧 ツール呼び出し: ${toolName}`);
    },
    onError(err) {
      assistantDiv.textContent = `⚠️ エラー: ${err}`;
      assistantDiv.style.color = '#f85149';
    },
  });

  setFormLoading('tools-form', false);
});
