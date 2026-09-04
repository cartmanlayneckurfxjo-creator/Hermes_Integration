# Hermes & Antigravity Integration — Handoff

**Дата актуализации:** 2026-09-04  
**Проект:** `C:\Users\may\.gemini\antigravity-ide\scratch\Hermes_Integration`  
**Текущий статус:** ACP протокол отлажен, Windows дедлоки устранены, бот-профиль `antigravity` создан и проверен, подготовлен Git/GitHub репозиторий.

---

## 1. Архитектура интеграции

```
┌──────────────────────────────────────────────────────────┐
│                   Antigravity IDE                        │
│             (Главный архитектор, оркестратор)            │
└──────────────────────────┬───────────────────────────────┘
                           │ Agent Client Protocol (ACP)
                           │ stdio (JSON-RPC 2.0 streaming)
                           ▼
┌──────────────────────────────────────────────────────────┐
│                hermes_acp_runner.py                      │
│      (Python ACP клиент, авто-одобрение, парсер файлов)  │
└──────────────────────────┬───────────────────────────────┘
                           │ subprocess (python -m acp_adapter)
                           │ env: HERMES_HOME=profiles/<name>
                           ▼
┌──────────────────────────────────────────────────────────┐
│                   Hermes Agent                           │
│   (Автономный агент / специализированные бот-профили)   │
│   • Profile: antigravity (F:\AI\hermes\profiles\antigravity)│
│   • Core: F:\AI\hermes\hermes-agent                      │
│   • Python: F:\AI\hermes\hermes-agent\venv               │
└──────────────────────────┬───────────────────────────────┘
                           │ HTTP / OpenAI API (порт 20128)
                           ▼
┌──────────────────────────────────────────────────────────┐
│                     OmniRoute                            │
│  (Умный шлюз, 18 стратегий Combos, квоты, fallback)     │
└──────────────────────────────────────────────────────────┘
```

---

## 2. Что сделано и решено

1. **Решение проблемы зависаний (Deadlock в Windows):**
   - Проблема: запуск через `hermes-acp.cmd` вызывал утечку открытых дескрипторов Windows CMD, а `tools.file_tools` внутри Hermes подвисал на создании сессионного bash-снимка среды (`LocalEnvironment`).
   - Решение:
     - Запуск напрямую: `python.exe -m acp_adapter` из `hermes_acp_runner.py`.
     - Добавлен ключ `--save-file <filename>`: перехватывает сгенерированный markdown-блок кода из ACP-потока и сохраняет его на диск силами клиента (скорость генерации скриптов: **~5 секунд**).

2. **Поддержка бот-профилей (Hermes Bot Mode):**
   - Боты в Hermes — это изолированные профили в `F:\AI\hermes\profiles\<profile_name>` со своими `config.yaml`, `SOUL.md` и памятью.
   - Создан выделенный профиль бота `antigravity` в `F:\AI\hermes\profiles\antigravity`.
   - В `hermes_acp_runner.py` добавлен ключ `--profile <name>` (устанавливает переменную среды `HERMES_HOME`).
   - Тест отклика бота `antigravity`: **4.6 секунды**.

3. **Сквозной тест генерации и исполнения:**
   - Сгенерирован скрипт [`check_disk.py`](file:///C:/Users/may/.gemini/antigravity-ide/scratch/Hermes_Integration/check_disk.py) через модель `laguna-s-2.1-free` за 5.3 сек.
   - Скрипт проверен и выполнен:
     - Диск `C:\`: 26.43 ГБ свободно.
     - Диск `F:\`: 172.87 ГБ свободно.

4. **Очистка и ускорение старта Hermes:**
   - Отключены подвисающие MCP-серверы в `config.yaml`.
   - Время старта снижено с 2 минут до 1.5 секунд.

---

## 3. Команды запуска

### Базовый запрос к Hermes:
```powershell
& "F:\AI\hermes\hermes-agent\venv\Scripts\python.exe" "C:\Users\may\.gemini\antigravity-ide\scratch\Hermes_Integration\hermes_acp_runner.py" "Твой запрос" "C:\Users\may\.gemini\antigravity-ide\scratch\Hermes_Integration"
```

### Генерация файла с автосохранением на диск:
```powershell
& "F:\AI\hermes\hermes-agent\venv\Scripts\python.exe" "C:\Users\may\.gemini\antigravity-ide\scratch\Hermes_Integration\hermes_acp_runner.py" "Напиши скрипт..." "C:\Users\may\.gemini\antigravity-ide\scratch\Hermes_Integration" --save-file "myscript.py"
```

### Запрос к конкретному боту (например, antigravity):
```powershell
& "F:\AI\hermes\hermes-agent\venv\Scripts\python.exe" "C:\Users\may\.gemini\antigravity-ide\scratch\Hermes_Integration\hermes_acp_runner.py" "Кто ты и какая твоя задача?" "C:\Users\may\.gemini\antigravity-ide\scratch\Hermes_Integration" --profile antigravity
```

---

## 4. Следующие задачи
- Связать локальный Git репозиторий с удаленным GitHub (`git remote add origin <url>`, `git push`).
- Настроить Combos в OmniRoute для отказоустойчивой связки моделей (Claude / DeepSeek / Free).
- Делегировать автономные задачи ресерча и написания тестов Hermes-ботам.
