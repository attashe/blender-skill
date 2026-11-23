# Ранние примеры Blender

Открывай сцену из таблицы и сохраняй изменённую копию в своём проекте. Каждая строка указывает наблюдаемое свойство, которое можно проверить в Blender. Превью показывают исходную постановку.

## Планировка и интерьер

| Сцена | Превью | Что попробовать |
| --- | --- | --- |
| [Блокинг квартиры](../assets/studies/room-blockout/scene.blend) | [Открыть](../assets/studies/room-blockout/preview.png) | Сверить границы комнат и проёмов перед расстановкой мебели. |
| [Кухня и столовая](../assets/studies/dining-layout/scene.blend) | [Открыть](../assets/studies/dining-layout/preview.png) | Сопоставить план и перспективу. Остальные комнаты и диван оставлены прокси. |
| [Проходы и открывание техники](../assets/studies/kitchen-operation/scene.blend) | [Открыть](../assets/studies/kitchen-operation/preview.png) | Сравнить габариты и проходы в состояниях на кадрах 1, 31, 91 и 151. |
| [Стык фартука и столешницы](../assets/studies/tile-junction/scene.blend) | [Открыть](../assets/studies/tile-junction/preview.png) | Осмотреть крайние подрезки, толщину швов и утопленную затирку. |

## Текстурирование, UV и шейдеры

| Сцена | Превью | Что попробовать |
| --- | --- | --- |
| [Текстурирование дубового шпона](../assets/studies/oak-veneer/scene.blend) | [Открыть](../assets/studies/oak-veneer/preview.png) | Сравнить направление волокон на стойке и перекладине и сохранить физический масштаб трёх карт. |
| [Тиснение обивки и формованный пластик](../assets/studies/upholstery/scene.blend) | [Открыть](../assets/studies/upholstery/preview.png) | Изменить рельеф обивки, затем отдельно проверить блик покрытия. |
| [Матовое стекло и ткань](../assets/studies/window/scene.blend) | [Открыть](../assets/studies/window/preview.png) | Посмотреть на один предмет через стекло с разного расстояния, затем сравнить свет сквозь штору. |
| [UV и плотность текстуры](../assets/studies/uv-density/scene.blend) | [Открыть](../assets/studies/uv-density/preview.png) | Проверить размер клеток на гранях разной площади. |
| [Запекание карт](../assets/studies/bake/scene.blend) | [Открыть](../assets/studies/bake/preview.png) | Осмотреть Normal, Base Color, Roughness и Metallic на целевой сетке. |
| [Многослойные шейдеры](../assets/studies/layered-materials/scene.blend) | [Открыть](../assets/studies/layered-materials/preview.png) | Сравнить маску покрытия, ткань и поглощение в объёме смолы. |

## Ноды и мультфильмы

| Сцена | Превью | Что попробовать |
| --- | --- | --- |
| [Geometry Nodes](../assets/studies/geometry-nodes/scene.blend) | [Открыть](../assets/studies/geometry-nodes/preview.png) | Изменить число или шаг инстансов в ряду, сетке или кольце и проверить распределение цветов. |
| [Cel shading в EEVEE](../assets/studies/cel-bands/scene.blend) | [Открыть](../assets/studies/cel-bands/preview.png) | Изменить порог световой полосы и сравнить контуры при одинаковой камере. |
| [Мультяшный low-poly персонаж](../assets/studies/low-poly-toon/scene.blend) | [Открыть](../assets/studies/low-poly-toon/preview.png) | Сравнить силуэт и световые полосы в соседних позах. |
| [Мультфильм «Белый кролик»](../assets/studies/rabbit-cartoon/scene.blend) | [Открыть](../assets/studies/rabbit-cartoon/preview.mp4) | Посмотреть 176 кадров при 24 кадрах/с. Сопоставить взмах лапы, спуск камеры в нору и затемнение с метками сцены. |

## Изображение, свет и движение

| Сцена | Превью | Что попробовать |
| --- | --- | --- |
| [Ноды композитора](../assets/studies/compositing/scene.blend) | [Открыть](../assets/studies/compositing/preview.png) | Проверить маску объекта, край альфы и локальную коррекцию на исходном многослойном EXR. |
| [Предметный свет](../assets/studies/lighting/scene.blend) | [Открыть](../assets/studies/lighting/preview.png) | Сравнить форму бликов при ключевом и полном свете. |
| [Деформация рукава](../assets/studies/sleeve-deform/scene.blend) | [Открыть](../assets/studies/sleeve-deform/preview.png) | Сравнить объём и залом локтя в контрольных позах. |
| [Риг манипулятора](../assets/studies/manipulator/scene.blend) | [Открыть](../assets/studies/manipulator/preview.png) | Проверить ориентацию конечного звена и родительские зависимости. |
| [Искры в Geometry Nodes](../assets/studies/sparks/scene.blend) | [Открыть](../assets/studies/sparks/preview.png) | Проверить рождение, касание поверхности и исчезновение частиц на разных кадрах. |
| [Шарнир и кэш физики](../assets/studies/rigid-hinge/scene.blend) | [Открыть](../assets/studies/rigid-hinge/preview.png) | Сравнить положение створки при повторном переходе к одному и тому же кадру. |
| [Экспорт GLB](../assets/studies/glb-handoff/scene.blend) | [Открыть](../assets/studies/glb-handoff/preview.png) | Сравнить материалы и анимацию исходника с повторным импортом готового GLB. |

У квартиры есть [вид кухни](../assets/studies/dining-layout/composition.png) и [вид столовой](../assets/studies/dining-layout/dining.png). У примера экспорта есть [готовый GLB](../assets/studies/glb-handoff/assembly.glb).

Карты дуба для шпона и интерьеров имеют общий каталог `assets/studies/textures/`. Сцены обращаются к нему относительными путями. При переносе одной сцены отдельно можно упаковать карты через **File → External Data → Pack Resources** и сохранить копию.

Карты White Oak Veneer создала Jenelle van Heerden, Poly Haven, CC0. [Источник карт](https://polyhaven.com/a/white_oak_veneer)

[Кривые, Lattice, Rigify и механическая анимация](implementation-examples.md)
