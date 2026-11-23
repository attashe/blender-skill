# Blender Modular Scenes

Скилл для работы с Blender в Codex и Pi. Помогает агенту править существующую сцену, моделировать, работать с материалами и ригами, разбивать анимацию на этапы и проверять результат после сохранения. В комплект входят Python-хелперы, карточки приёмов и редактируемые примеры.

[Сводная таблица кейсов](CASES.md) показывает, что проверено, какие попытки дали частичный результат и по каким критериям принимать следующую доработку.

## Добавить в существующий проект

Из корня своего Git-проекта выполни одну команду. Git поместит скилл рядом с другими проектными скиллами.

```sh
git submodule add https://github.com/attashe/blender-skill.git .agents/skills/blender-modular-scenes
```

Включи файл `.gitmodules` и запись подмодуля в коммит проекта. При клонировании проекта на другой машине выполни `git submodule update --init`. Проект получит ту же версию скилла. Чтобы перейти на новую версию, выполни `git submodule update --remote .agents/skills/blender-modular-scenes` и закоммить новый указатель.

Для установки без подмодулей скачай ZIP репозитория и скопируй папку, в которой лежит `SKILL.md`, вместе со всем содержимым в `.agents/skills/blender-modular-scenes/` своего проекта. Если эта папка уже содержит твою редакцию, сначала сравни версии.

Открой новую сессию агента в проекте. В Codex скилл можно вызвать как `$blender-modular-scenes`, в Pi — как `/skill:blender-modular-scenes`.

## Попробовать

В [каталоге ранних примеров](references/early-examples.md) собраны готовые сцены, превью и задания для проверки. Можно проследить квартиру от [блокинга](assets/studies/room-blockout/scene.blend) до [плана с мебелью](assets/studies/dining-layout/preview.png), открыть [материал дубового шпона](assets/studies/oak-veneer/scene.blend) с исходными картами, изменить [паттерн Geometry Nodes](assets/studies/geometry-nodes/scene.blend) или разобрать [cel-шейдер](assets/studies/cel-bands/scene.blend). Для мультфильма «Белый кролик» доступны и [сцена с ключами](assets/studies/rabbit-cartoon/scene.blend), и [готовый ролик](assets/studies/rabbit-cartoon/preview.mp4).

В установленном скилле открой `assets/lattice-example/rock.blend`. Попроси агента: «Сделай выступ чуть выше, сохрани результат в отдельную сцену моего проекта и проверь, что основание осталось на плоскости». В [карточке Lattice](references/techniques/lattice-region.md) есть изображения до и после и способ измерить контакт.

| Пример | Что можно изменить и проверить |
| --- | --- |
| [Рог на кривой](assets/sweep-example/horn.blend) | Сдвинуть кончик и проверить форму основания |
| [Скала с Lattice](assets/lattice-example/rock.blend) | Поднять локальный выступ и измерить подошву |
| [Вал](assets/motor-example/shaft.blend) и [крепёж](assets/motor-example/fasteners.blend) | Сменить скорость вращения или проверить ход гайки за оборот |
| [FK-приветствие Momo](assets/momo-example/gesture.blend) | Изменить жест и проверить задержку движения и опору стоп |
| [Походка и приветствие Rigify](assets/walk-example/greeting.blend) · [Видео](assets/walk-example/greeting.mp4) | Сравнить шаги, перенос веса, взгляд и момент подъёма руки |

Сцены сохранены в Blender 5.2.1 LTS. Для работы через открытый Blender можно подключить [BlenderMCP Minimal](https://github.com/attashe/blender-mcp/tree/minimal-core). Для пакетных задач подойдёт установленный Blender через командную строку. У файла результата выбирай путь в рабочем проекте. [Вход в скилл](SKILL.md) · [Кривые, Lattice и анимация](references/implementation-examples.md) · [Интерьеры, материалы, ноды и мультфильмы](references/early-examples.md)
