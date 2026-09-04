# 🚀 Antigravity & Hermes Agent ACP Integration

Интеграция между средой разработки **Antigravity IDE** и автономным агентом **Hermes Agent** (Nous Research) по протоколу **Agent Client Protocol (ACP)**.

---

## 🌟 Возможности

- **Agent Client Protocol (ACP)**: Полноценный двусторонний протокол с JSON-RPC 2.0 streaming (ход мыслей, вызовы инструментов, текст ответа).
- **Windows Deadlock-Free**: Прямой запуск через `python -m acp_adapter` без утечек потоков ввода-вывода CMD.
- **Client-side Auto-Saver (`--save-file`)**: Автоматический парсинг блоков кода из ACP-потока и сохранение на диск за считанные секунды в обход зависаний виртуального bash-окружения на Windows.
- **Hermes Bot Profiles (`--profile`)**: Поддержка запуска специализированных ботов/профилей из `F:\AI\hermes\profiles\<profile>` с персональными `SOUL.md`, инструкциями и памятью.
- **OmniRoute Ready**: Поддержка работы через локальный AI-шлюз OmniRoute (порт 20128) с поддержкой Combos (цепочки fallback, smart routing).

---

## 📁 Структура проекта

```
Hermes_Integration/
├── hermes_acp_runner.py          # Основной ACP клиент и раннер задач
├── HERMES_INTEGRATION_GUIDE.md   # Подробное руководство по настройке и архитектуре
├── HANDOFF.md                    # История решений, статус и контрольные точки
├── check_disk.py                 # Проверочный скрипт, сгенерированный Hermes через ACP
├── mcp_config.json               # Конфигурация MCP серверов
├── .gitignore                    # Исключения для Git
└── README.md                     # Документация проекта
```

---

## ⚙️ Системные требования и пути

- **Hermes Core**: `F:\AI\hermes\hermes-agent`
- **Hermes Python Venv**: `F:\AI\hermes\hermes-agent\venv\Scripts\python.exe`
- **Профили ботов**: `F:\AI\hermes\profiles\`
- **Git Bash**: `C:\Program Files\Git\bin` (для работы unix-утилит)

---

## 💻 Использование

### 1. Обычный текстовый запрос / ресерч:
```powershell
& "F:\AI\hermes\hermes-agent\venv\Scripts\python.exe" "hermes_acp_runner.py" "Исследуй архитектуру проекта" "C:\path\to\workspace"
```

### 2. Генерация и сохранение кода:
```powershell
& "F:\AI\hermes\hermes-agent\venv\Scripts\python.exe" "hermes_acp_runner.py" "Напиши скрипт парсинга логов" "C:\path\to\workspace" --save-file "parse_logs.py"
```

### 3. Запуск через конкретного бота:
```powershell
& "F:\AI\hermes\hermes-agent\venv\Scripts\python.exe" "hermes_acp_runner.py" "Твоя задача" "C:\path\to\workspace" --profile antigravity
```

---

## 🤖 Боты в Hermes (Bot Mode)

Боты создаются в каталоге `F:\AI\hermes\profiles\<имя_бота>/`:
- `SOUL.md` — системная личность, правила поведения и специализация.
- `config.yaml` — персональная модель (или OmniRoute combo), температура, скиллы.
- `memories/` — контекстная память сессий бота.

Пример встроенного бота **`antigravity`**:
- Расположение: `F:\AI\hermes\profiles\antigravity`
- Роль: Ко-пилот и автономный рабочий узел для задач из Antigravity IDE.

---

## 🛡️ Безопасность
Авто-одобрение действий реализовано в клиенте `AntigravityACPClient.request_permission` со статусом `AllowedOutcome(outcome="selected")`.

---

## 📄 Лицензия
MIT
