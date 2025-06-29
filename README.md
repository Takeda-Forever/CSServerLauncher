# 🎮 CS2 Local Server Launcher

Графическая оболочка для запуска локального сервера CS2. Работает на Python с GUI на базе `customtkinter`.

## Возможности

- Выбор папки с `cs2.exe`
- Проверка наличия `cs2.exe`
- Ввод GSLT-ключа (необязательный)
- Выбор карты из предложенного списка
- Запуск сервера с нужными параметрами

## Установка

```bash
pip install customtkinter
```

## Запуск

```bash
python window.py
```

## Сборка в exe

```bash
pyinstaller --noconfirm --onefile --windowed window.py -i icon.ico
```

## Пример аргументов запуска

```text
-dedicated -maxplayers 10 -usercon -console -dev +game_type 0 +game_mode 1 +map de_mirage
```

## Пример структуры проекта

```
.
├── window.py
├── icon.ico
├── README.md
└── dist/
```

## Лицензия

MIT
