# Руководство по интеграции Hermes Agent и Google Antigravity

В данном документе описаны способы совместного использования **Hermes Agent** (Nous Research, каталог `F:\AI\hermes`) и **Google Antigravity** (AGY IDE / CLI).

---

## 1. Архитектура и компоненты

- **Hermes Agent Path:** `F:\AI\hermes`
- **Python venv:** `F:\AI\hermes\hermes-agent\venv\Scripts\python.exe`
- **Hermes CLI:** `F:\AI\hermes\bin\hermes.cmd`
- **Hermes ACP:** `F:\AI\hermes\bin\hermes-acp.cmd`
- **MCP Server:** `F:\AI\hermes\hermes-agent\agent\transports\hermes_tools_mcp_server.py`
- **Конфигурация модели:** `F:\AI\hermes\config.yaml`
- **База задач / Kanban:** `F:\AI\hermes\kanban.db`

---

## 2. Способы подключения

### Вариант 1: Hermes как MCP-сервер инструментов для Antigravity

Hermes содержит модуль `agent.transports.hermes_tools_mcp_server`, реализующий стандартный протокол **Model Context Protocol (stdio MCP)**.

#### Доступные инструменты Hermes через MCP:
- `web_search`, `web_extract` — поиск и парсинг через Firecrawl.
- `browser_navigate`, `browser_click`, `browser_type`, `browser_snapshot`, `browser_scroll` — автоматизация браузера (Camofox/Playwright).
- `vision_analyze` — анализ изображений мультимодальной моделью.
- `image_generate` — генерация изображений.
- `text_to_speech` — озвучка текста.
- `skill_view`, `skills_list` — доступ к библиотеке навыков Hermes.
- `kanban_*` — управление задачами через общую БД (`kanban.db`).

#### Конфигурация в Antigravity (`mcp_config.json` или `.mcp.json`):
```json
{
  "mcpServers": {
    "hermes-tools": {
      "command": "F:\\AI\\hermes\\hermes-agent\\venv\\Scripts\\python.exe",
      "args": [
        "-m",
        "agent.transports.hermes_tools_mcp_server"
      ],
      "cwd": "F:\\AI\\hermes\\hermes-agent",
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

---

### Вариант 2: CLI-делегирование (Hermes как субагент)

Antigravity может запускать задачи через CLI Hermes в автономном фоновом или синхронном режиме.

#### Быстрый запуск one-shot задачи:
```powershell
& "F:\AI\hermes\bin\hermes.cmd" -z "Проведи исследование API и верни краткий отчет" --yolo
```

#### Запуск с выбором модели и записью метрик:
```powershell
& "F:\AI\hermes\bin\hermes.cmd" -z "Сделай рефакторинг модуля" --model deepseek-v4-flash --yolo --usage-file usage.json
```

#### Запуск в изолированном Git Worktree:
```powershell
& "F:\AI\hermes\bin\hermes.cmd" -w -z "Протестируй изменения в ветке" --yolo
```

#### Оформление в виде кастомного Skill Antigravity:
Путь: `~/.gemini/config/skills/hermes/SKILL.md`
```yaml
---
name: hermes-subagent
description: Запуск Hermes Agent для делегирования автономных задач кодинга, браузинга или исследований.
---

При необходимости делегировать задачу агенту Hermes:
1. Выполнить команду:
   & "F:\AI\hermes\bin\hermes.cmd" -z "$TASK_DESCRIPTION" --yolo
2. Прочитать результат и использовать в текущей сессии.
```

---

### Вариант 3: ACP (Agent Client Protocol) / Сайдкар (Реализовано)

В Hermes встроен готовый сервер протокола ACP. Создан нативный клиент-раннер [hermes_acp_runner.py](file:///C:/Users/may/.gemini/antigravity-ide/scratch/Hermes_Integration/hermes_acp_runner.py).

#### Запуск ACP:
```powershell
& "F:\AI\hermes\hermes-agent\venv\Scripts\python.exe" "C:\Users\may\.gemini\antigravity-ide\scratch\Hermes_Integration\hermes_acp_runner.py" "<Запрос>" "<Рабочая директория>"
```

#### Флаги раннера:
- `--save-file <имя_файла>`: Перехватывает сгенерированный markdown-блок кода из ACP-потока и сохраняет файл напрямую через клиент, обходя Windows-зависания виртуального bash.
- `--profile <имя_бота>`: Направляет запрос конкретному боту/профилю из `F:\AI\hermes\profiles\<имя_бота>`.

---

### Вариант 4: Hermes Bot Mode (Мульти-боты)

В Hermes каждый бот из вкладки BOTS — это изолированный профиль в `F:\AI\hermes\profiles\<profile_name>`:
- `SOUL.md`: Личность, системный промпт, специализация.
- `config.yaml`: Настройки модели, провайдера, температуры и скиллов.
- `memories/`: Долговременная память сессий.

Создан бот **`antigravity`**:
- Путь: `F:\AI\hermes\profiles\antigravity`
- Задача: Выделенный ко-пилот для задач Antigravity IDE.
- Тест скорости отклика: **4.6 секунды**.

---

### Вариант 5: Единое рабочее пространство и координация

Hermes и Antigravity могут работать над одним проектом параллельно:

1. **Единые правила проекта (`AGENTS.md`):**
   Оба агента автоматически считывают файл `AGENTS.md` в корне рабочего каталога.
2. **Общий трекер задач (Kanban):**
   Hermes хранит задачи в `F:\AI\hermes\kanban.db`. Antigravity может читать статус задач или обновлять их через SQLite/MCP.
3. **Разделение ролей:**
   - **Antigravity:** Архитектура, глубокое редактирование кода, интеграционные тесты, планирование.
   - **Hermes:** Фоновые исследования через Firecrawl, автоматизация браузера, автономные подзадачи в git worktree.

