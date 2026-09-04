# 🚀 Antigravity & Hermes Agent ACP Integration

Интеграция между средой разработки **Antigravity IDE** и автономным агентом **Hermes Agent** (Nous Research) по открытому протоколу **Agent Client Protocol (ACP)**.

---

## 🌟 Возможности

- **Agent Client Protocol (ACP)**: Полноценный двусторонний протокол с JSON-RPC 2.0 streaming (ход мыслей, вызовы инструментов, текст ответа).
- **Windows Deadlock-Free**: Прямой запуск через `python -m acp_adapter` без утечек потоков ввода-вывода CMD.
- **Client-side Auto-Saver (`--save-file`)**: Автоматический парсинг блоков кода из ACP-потока и сохранение на диск за считанные секунды в обход зависаний виртуального bash-окружения на Windows.
- **Hermes Bot Profiles (`--profile`)**: Поддержка запуска специализированных ботов/профилей из каталога профилей Hermes с персональными `SOUL.md`, инструкциями и памятью.
- **Гибкая настройка провайдеров**: Поддержка любых LLM-провайдеров и локальных OpenAI-совместимых шлюзов через конфигурацию Hermes.

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

## ⚙️ Настройка путей и окружения

Раннер автоматически определяет окружение Hermes или использует переменные среды:

| Переменная | Описание | Значение по умолчанию |
|---|---|---|
| `HERMES_DIR` | Корневой каталог установки Hermes | Автопоиск (`~/.hermes`, `~/hermes` или локальный путь) |
| `HERMES_PYTHON` | Путь к Python интерпретатору venv | `<HERMES_DIR>/hermes-agent/venv/Scripts/python.exe` |

---

## 💻 Использование

### 1. Обычный текстовый запрос / ресерч:
```bash
python hermes_acp_runner.py "Исследуй архитектуру проекта" "path/to/workspace"
```

### 2. Генерация и сохранение кода:
```bash
python hermes_acp_runner.py "Напиши скрипт парсинга логов" "path/to/workspace" --save-file "parse_logs.py"
```

### 3. Запуск через конкретного бота:
```bash
python hermes_acp_runner.py "Твоя задача" "path/to/workspace" --profile antigravity
```

---

## 🤖 Боты в Hermes (Bot Mode)

Боты создаются в каталоге `<HERMES_DIR>/profiles/<имя_бота>/`:
- `SOUL.md` — системная личность, правила поведения и специализация.
- `config.yaml` — персональная модель, температура, скиллы.
- `memories/` — контекстная память сессий бота.

Пример бота **`antigravity`**:
- Расположение: `<HERMES_DIR>/profiles/antigravity`
- Роль: Ко-пилот и автономный рабочий узел для задач из Antigravity IDE.

---

## 🛡️ Безопасность
Авто-одобрение действий реализовано в клиенте `AntigravityACPClient.request_permission` со статусом `AllowedOutcome(outcome="selected")`.

---

## 📄 Лицензия
MIT
