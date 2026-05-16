# Pre-defence speaking script

> Target: 10–12 minutes. Each slide has a spoken paragraph and a bullet
> fallback, in English and Russian. Terms are explained **on first use**
> (mostly Slides 3, 5, 8, 10); later slides reuse them without
> re-defining.

---

## For the presenter — what the system actually does (plain language)

**EN.** The system is a small Python pipeline. Once an hour it
(a) downloads fresh PM2.5 readings from 192 air-pollution sensors
scattered across Almaty, (b) downloads the current weather at the
same location — temperature, wind, humidity, pressure, and the
"mixing-layer height" (see glossary), (c) feeds everything into a
machine-learning model that was trained on about 18 months of
history, and (d) outputs a prediction of PM2.5 for the next 6, 12,
and 24 hours. The forecast is displayed on a map in a single-page
public web app anyone can open without registering. That is the
whole product.

**RU.** Система — это небольшой Python-пайплайн. Раз в час он:
(а) скачивает свежие показания PM2.5 с 192 датчиков загрязнения
воздуха в Алматы, (б) скачивает текущую погоду в той же точке —
температуру, ветер, влажность, давление и «высоту перемешивания»
(см. глоссарий), (в) передаёт всё это в модель машинного обучения,
которая была обучена примерно на 18 месяцах исторических данных, и
(г) выдаёт прогноз PM2.5 на следующие 6, 12 и 24 часа. Прогноз
показывается на карте в одностраничном публичном веб-приложении, к
которому можно зайти без регистрации. Это весь продукт.

---

## Glossary — plain-language definitions

| Term | EN plain meaning | RU простыми словами |
|---|---|---|
| **PM2.5** | Airborne dust smaller than 2.5 µm — small enough to enter the bloodstream from the lungs. The main health-damaging winter pollutant. | Пыль в воздухе размером меньше 2,5 микрометра — настолько мелкая, что попадает в кровь через лёгкие. Главный вредный загрязнитель зимой. |
| **Low-cost sensor (LCS)** | ~$200 device that measures PM2.5 with a laser. Less accurate than a government-grade station, but many of them give good spatial coverage. | Прибор ~$200 с лазерным датчиком PM2.5. По точности уступает госстанции, но их много и они покрывают весь город. |
| **OpenAQ** | Free worldwide hub of air-quality sensor data. Our PM2.5 source. | Бесплатный мировой агрегатор данных о качестве воздуха. Наш источник PM2.5. |
| **Open-Meteo** | Free weather API. Our meteorology + CAMS-forecast source. | Бесплатный погодный API. Наш источник метеоданных и прогноза CAMS. |
| **Temperature inversion** | In winter, warm air sits on top of cold air and acts like a lid. Pollution can't rise and escape, so it accumulates. | Зимой тёплый слой воздуха лежит на холодном и работает как крышка. Загрязнение не может подняться и рассеяться — оно накапливается. |
| **Boundary-layer height (BLH)** | How tall the "lid" is. In Almaty in winter it collapses to ~45 m — roughly the height of a 15-storey building. | Высота «крышки». В Алматы зимой падает до ~45 м — это примерно высота 15-этажного дома. |
| **CAMS** | European global air-quality forecast (Copernicus). 40 km grid — the whole of Almaty fits into ~one cell, so it cannot resolve mountain-basin effects. | Европейский глобальный прогноз качества воздуха (Copernicus). Сетка 40 км — вся Алматы помещается в одну ячейку, эффекты котловины не видны. |
| **Persistence** | Trivial baseline: "tomorrow = today". Beating it proves the model is actually learning something. | Тривиальный бейзлайн: «завтра будет как сегодня». Если модель его обыгрывает — значит, действительно чему-то научилась. |
| **XGBoost** | The main model: an ensemble of hundreds of small decision trees, each one fixing the previous tree's mistakes. Fast on CPU, strong on tabular data, interpretable. | Главная модель: ансамбль из сотен маленьких деревьев решений, каждое исправляет ошибки предыдущего. Быстрая на CPU, сильна на табличных данных, интерпретируема. |
| **MAE / RMSE / R²** | How we measure quality. **MAE** = average absolute error (µg/m³). **RMSE** = same idea but penalises big errors. **R²** = share of variance the model explains (0 = useless, 1 = perfect). | Как измеряем качество. **MAE** — средняя абсолютная ошибка (µг/м³). **RMSE** — то же, но сильнее штрафует большие ошибки. **R²** — доля объяснённой дисперсии (0 = бесполезно, 1 = идеально). |
| **SHAP** | Tells us which input variables drove the prediction most. Model-interpretation tool. | Показывает, какие входные признаки больше всего повлияли на предсказание. Инструмент интерпретации модели. |
| **Time-series CV, expanding window** | Train on an early history slice, test on the next slice, extend training forward, repeat. No random shuffling — that would leak future data into training. | Обучаемся на ранней истории, тестируем на следующей, расширяем обучение, повторяем. Без случайной перемешки — иначе будущее «протечёт» в обучение. |
| **Streamlit** | Python library that turns a script into a single-page web app. Free hosting on Streamlit Community Cloud. | Python-библиотека, превращающая скрипт в одностраничное веб-приложение. Бесплатный хостинг на Streamlit Community Cloud. |

---

## Slide 1 — Title

### EN · full speech
Good afternoon. My name is Alikhan Izimov, I am a master's student in
*7M06101 Information Systems* at Kazakh-British Technical University.
My scientific consultant is Professor Naizabayeva Lyazat Kydyrgaliyevna,
Doctor of Technical Sciences. The title of my thesis is *Development
of an intelligent system for investigating and solving ecological
problems*, with a case study on short-term air-quality forecasting for
Almaty. In one sentence — the system downloads readings from 192
air-pollution sensors across the city every hour, combines them with
weather data, and predicts pollution for the next 6, 12, and 24 hours
on a public map. Today I'll walk through why this is needed, how the
system works, and what it achieves.

### EN · bullets
- Izimov Alikhan, 7M06101 Information Systems, KBTU.
- Consultant: Prof. Naizabayeva L. K., DTS.
- Thesis: *Development of an intelligent system for investigating and
  solving ecological problems* — case study: Almaty PM2.5.
- One-sentence product: sensors + weather → predict next 6/12/24 h →
  public map.

### RU · полный текст
Добрый день. Меня зовут Изимов Алихан, я магистрант программы
*7M06101 — Информационные системы* Казахстанско-Британского
технического университета. Мой научный консультант — профессор
Найзабаева Лязат Кыдыргалиевна, доктор технических наук. Тема моей
диссертации — *«Разработка интеллектуальной системы для исследования
и решения экологических проблем»*, с прикладным исследованием на
примере краткосрочного прогнозирования качества воздуха в Алматы.
Одним предложением — система каждый час скачивает показания с 192
датчиков загрязнения по городу, соединяет их с погодными данными и
выдаёт прогноз загрязнения на 6, 12 и 24 часа вперёд на общедоступной
карте. Сегодня я расскажу, зачем это нужно, как система устроена и
какие результаты получены.

### RU · тезисы
- Изимов Алихан, 7M06101 Информационные системы, КБТУ.
- Консультант: проф. Найзабаева Л. К., д.т.н.
- Тема: *«Разработка интеллектуальной системы для исследования и
  решения экологических проблем»* — кейс: PM2.5 в Алматы.
- В одном предложении: датчики + погода → прогноз на 6/12/24 ч →
  публичная карта.

---

## Slide 2 — Table of contents

### EN · full speech
The presentation has nine sections: relevance, research goals and
objectives, object/subject/methods, significance, novelty, an
overview of current research, results, conclusion with future work,
and publications.

### EN · bullets
- Nine sections, roughly in this order — problem, approach, results,
  outlook.

### RU · полный текст
Презентация состоит из девяти разделов: актуальность, цели и задачи,
объект/предмет/методы, значимость, новизна, обзор исследований,
результаты, выводы и планы, публикации.

### RU · тезисы
- Девять разделов: проблема → подход → результаты → перспективы.

---

## Slide 3 — Relevance

### EN · full speech
Why does Almaty need this? Three reasons.

**First — the city has a severe winter air-pollution problem, and the
cause is very specific.** Almaty sits in a bowl of mountains. In cold
weather a layer of warm air settles on top of the cold air near the
ground and acts like a lid — this is called a **temperature
inversion**. Pollution from private coal-based home heating and
traffic cannot rise and disperse; it is trapped in a very thin layer,
sometimes only about 45 metres tall — roughly the height of a
15-storey building. The thickness of that trapped layer is called the
**boundary-layer height**, or BLH for short. It is the single most
important physical variable in this problem.

**Second — the data situation is unusual.** Almaty has almost no
government-grade reference stations streaming hourly data. Instead,
hourly coverage comes from **192 low-cost sensors** — roughly
$200 laser-based devices on rooftops and in backyards. Individually
they are less accurate than a reference station, but there are many
of them and they cover the whole city. Working with them is the only
option.

**Third — there is no published local forecast.** Closed commercial
dashboards exist, but they don't disclose their methodology, so they
cannot be reproduced or extended. This is the gap the thesis fills.

### EN · bullets
- **Inversion regime:** warm air lid traps pollution in a ~45 m
  layer (BLH). The key physical driver.
- **LCS-only data:** 192 low-cost sensors; no usable reference
  network — so we work with what exists.
- **No open local forecast published** — this is the gap.

### RU · полный текст
Зачем это нужно Алматы? Три причины.

**Первая — у города острая зимняя проблема с загрязнением, и причина
очень специфическая.** Алматы стоит в горной котловине. В холодную
погоду над приземным холодным воздухом ложится слой тёплого, и он
работает как крышка — это называется **температурная инверсия**.
Загрязнение от частного угольного отопления и от транспорта не может
подняться и рассеяться; оно оказывается заперто в очень тонком слое,
иногда высотой около 45 метров — это примерно высота 15-этажного
дома. Толщина этого слоя называется **высотой пограничного слоя**,
сокращённо BLH. Это самая важная физическая переменная в нашей
задаче.

**Вторая — ситуация с данными необычная.** В Алматы почти нет
эталонных государственных станций, которые бы транслировали
почасовые данные. Вместо них есть сеть из **192 низкостоимостных
датчиков** — небольших лазерных приборов по ~$200, установленных на
крышах и во дворах. По отдельности они уступают эталонной станции, но
их много и они покрывают весь город. Работать с ними — единственный
вариант.

**Третья — публичного локального прогноза не существует.** Есть
закрытые коммерческие дашборды, но они не раскрывают методологию —
их нельзя ни воспроизвести, ни расширить. Этот пробел закрывает
диссертация.

### RU · тезисы
- **Инверсия:** тёплая «крышка» запирает загрязнение в слое ~45 м
  (BLH) — ключевой физический фактор.
- **Только LCS:** 192 датчика, эталонной сети нет — работаем с тем,
  что есть.
- **Публичного локального прогноза нет** — это и есть пробел.

---

## Slide 4 — Research goals and objectives

### EN · full speech
The aim is to build an intelligent system that turns open ecological
data into a useful short-term forecast — demonstrated on Almaty
PM2.5 — and that runs entirely on free, open resources so that
anyone can reproduce or adapt it. **What the system does in
practice** is a pipeline of five steps.

**One — ingest.** Download the latest PM2.5 readings from the 192
sensors through a public API, plus matching hourly weather for the
city, and store everything locally in a small SQLite database.
**Two — feature engineering.** Turn the raw numbers into predictive
variables the model can actually use: recent pollution at 1, 3, 6,
12, and 24 hours ago; rolling averages; the time of day as a
cyclical feature; the boundary-layer height and how fast it is
changing; wind split into east-west and north-south components.
**Three — train.** Learn a model from about 18 months of hourly
history that predicts 6, 12, and 24 hours ahead.
**Four — benchmark.** Compare the model against three baselines, so
we know the accuracy gain is real.
**Five — deliver.** Serve the result as a single-page public web map.

### EN · bullets
- **Aim:** intelligent system over open ecological data → useful
  forecast; free/open stack only.
- 5 steps: **ingest → feature engineering → train → benchmark →
  deliver** (public web map).
- Horizons: 6 / 12 / 24 h.

### RU · полный текст
Цель — построить интеллектуальную систему, которая превращает
открытые экологические данные в полезный краткосрочный прогноз на
примере PM2.5 в Алматы, и которая целиком работает на бесплатных
открытых ресурсах, чтобы её можно было воспроизвести или адаптировать
без финансовых затрат. **Что система делает на практике** — это
пайплайн из пяти шагов.

**Один — ingest.** Скачиваем свежие показания PM2.5 с 192 датчиков
через публичный API плюс соответствующую почасовую погоду для
города и сохраняем всё локально в небольшую базу SQLite.
**Два — инженерия признаков.** Превращаем сырые числа в переменные,
которые модель может использовать: значения PM2.5 за 1, 3, 6, 12, 24
часа назад; скользящие средние; циклическое представление часа
суток; высота пограничного слоя и скорость её изменения; ветер,
разложенный на компоненты запад-восток и север-юг.
**Три — обучение.** Модель учится на примерно 18 месяцах почасовой
истории предсказывать на 6, 12 и 24 часа вперёд.
**Четыре — бенчмарк.** Сравниваем модель с тремя бейзлайнами —
чтобы удостовериться, что прирост точности реальный.
**Пять — развёртывание.** Выдаём результат в виде одностраничной
публичной веб-карты.

### RU · тезисы
- **Цель:** система над открытыми экологическими данными →
  полезный прогноз; только бесплатный/открытый стек.
- 5 шагов: **ingest → инженерия признаков → обучение → бенчмарк →
  развёртывание** (публичная карта).
- Горизонты: 6 / 12 / 24 ч.

---

## Slide 5 — Object, subject, methods

### EN · full speech
A short formal framing. The **object** — what in the world we study —
is the short-term dynamics of PM2.5 concentration in Almaty. The
**subject** — the tool by which we study it — is machine-learning
models built on low-cost sensor data in an inversion-dominated city.

On methods: the modelling core is **XGBoost**, which stands for
*extreme gradient boosting*. Mechanically, it is an ensemble of
hundreds of small decision trees, each one trying to correct the
mistakes of the trees built before it. It is strong on tabular data
of our size, runs on a laptop CPU, and we can inspect which inputs
mattered most. For evaluation we use **time-series cross-validation
with an expanding window** — we train on an early slice of history,
test on the next slice, then extend the training slice forward and
repeat. We deliberately do *not* shuffle examples at random: that
would allow the model to "see" the future during training and
produce an artificially good score.

### EN · bullets
- **Object:** short-term PM2.5 dynamics in Almaty.
- **Subject:** ML models on LCS data in inversion-dominated basin.
- **Model:** XGBoost — ensemble of small decision trees. Fast,
  interpretable, strong on tabular data.
- **Validation:** time-series CV, expanding window — no shuffle
  (leakage risk).

### RU · полный текст
Короткая формальная рамка. **Объект** — то, что мы изучаем в мире, —
краткосрочная динамика концентрации PM2.5 в Алматы. **Предмет** —
инструмент, которым мы это изучаем, — модели машинного обучения на
данных низкостоимостных датчиков в городе с доминирующей инверсией.

О методах. Ядро моделирования — **XGBoost**, или *extreme gradient
boosting*. Механически это ансамбль из сотен маленьких деревьев
решений, каждое из которых пытается исправить ошибки предыдущих.
Модель сильна на табличных данных нашего объёма, работает на
обычном CPU, и мы можем посмотреть, какие входы были важнее. Для
оценки применяется **кросс-валидация временных рядов с расширяющимся
окном**: обучаемся на ранней части истории, тестируем на следующей,
затем расширяем обучение и повторяем. Случайную перемешку намеренно
*не используем* — иначе модель «увидит» будущее и покажет
искусственно завышенный балл.

### RU · тезисы
- **Объект:** краткосрочная динамика PM2.5 в Алматы.
- **Предмет:** ML-модели на LCS-данных в инверсионной котловине.
- **Модель:** XGBoost — ансамбль деревьев. Быстрая,
  интерпретируемая, хороша для табличных данных.
- **Валидация:** time-series CV с расширяющимся окном, без
  перемешки (риск утечки).

---

## Slide 6 — Theoretical and practical significance

### EN · full speech
Theoretically, the empirical literature on PM2.5 forecasting is
dominated by European and North American cities. This work adds a
Central-Asian mountain basin to that corpus and provides the first
open quantitative comparison of a local model against the global
CAMS forecast in such a setting. Practically, residents of Almaty
gain a free public forecast they can check before planning outdoor
activity, and any city with a similar sensor footprint can reuse the
pipeline by changing only coordinates and time window.

### EN · bullets
- **Theoretical:** fills a Central-Asian gap; first open local-vs-CAMS
  comparison for the region.
- **Practical:** free public forecast for residents; template
  reusable by other cities via coords + window swap.

### RU · полный текст
Теоретически — эмпирическая литература по прогнозированию PM2.5
сосредоточена на городах Европы и Северной Америки. Работа
добавляет в этот корпус центрально-азиатскую горную котловину и
впервые даёт открытое количественное сравнение локальной модели с
глобальным прогнозом CAMS для такого региона. Практически — жители
Алматы получают бесплатный публичный прогноз для планирования
активностей на улице, а любой город с аналогичной сетью датчиков
может переиспользовать пайплайн, поменяв лишь координаты и временной
промежуток.

### RU · тезисы
- **Теор.:** закрывает пробел по Центральной Азии; первое открытое
  сравнение локальная модель vs. CAMS в регионе.
- **Практ.:** бесплатный публичный прогноз; шаблон для других
  городов через замену координат и окна.

---

## Slide 7 — Scientific novelty

### EN · full speech
Novelty is twofold. **Theoretically** — no previous public model was
calibrated specifically to Almaty's inversion meteorology, built on
low-cost sensors with a deliberate treatment of their known biases,
*and* accompanied by an explicit characterisation of the error
regime during multi-day pollution episodes. **Practically** — the
whole pipeline is fully open source, depends only on openly licensed
inputs, runs without any paid cloud service, and is delivered as a
public web app without paywalls or registration.

### EN · bullets
- **Theoretical:** first locally calibrated Almaty PM2.5 model with
  LCS-bias treatment + explicit error-regime description.
- **Practical:** fully open, reproducible, free-tier public web app.

### RU · полный текст
Новизна двойная. **Теоретически** — ни одна предыдущая открытая
модель не была калибрована именно под инверсионную метеорологию
Алматы, построена на низкостоимостных датчиках с обоснованным
учётом их известных смещений *и* снабжена явной характеристикой
режима ошибок на многодневных эпизодах загрязнения.
**Практически** — пайплайн полностью открыт, зависит только от
открыто лицензированных источников, работает без платных облачных
сервисов и развёрнут как публичное веб-приложение без paywall и
регистрации.

### RU · тезисы
- **Теор.:** первая локально откалиброванная PM2.5-модель для
  Алматы с учётом LCS-смещений и описанием режима ошибок.
- **Практ.:** полностью открытый, воспроизводимый, публичный
  веб-сервис на бесплатной инфраструктуре.

---

## Slide 8 — Overview of current research

### EN · full speech
A short tour of the field. **Internationally**, short-term
air-quality forecasting uses four method families: statistical
models like ARIMA and Kalman filters; classical machine learning on
tabular features — the family XGBoost belongs to; deep learning with
LSTMs and transformers; and hybrid physics-plus-ML approaches.
Foundational works include Feng on Beijing, Inness on CAMS, Morawska
and Di Antonio on low-cost sensor behaviour, and Zhang on method
comparison. Consensus: at our data size — about 18 months — classical
tree-based ML gives the best accuracy-to-interpretability trade-off.

**About CAMS specifically** — the Copernicus Atmosphere Monitoring
Service, a European global air-quality forecast. It operates on a
40 km grid, which means the whole of Almaty fits into one or two
grid cells. It cannot resolve mountain-bowl effects, but it is the
best openly available external reference, so we compare against it.

**Locally**, Kazakhstani research — the Kerimray group at Nazarbayev
University on Almaty's heating-season emission inventory and the
COVID-lockdown natural experiment, the Kazhydromet annual reports
on the reference network, and the Almaty Air Initiative community
with LCS observations — has described what Almaty emits and measures,
but has not published a forecasting product. That is where this
thesis plugs in.

### EN · bullets
- 4 method families (statistical, classical ML, deep learning,
  hybrid). Closest to our work: classical ML (XGBoost).
- CAMS — European global forecast on 40 km grid; cannot resolve
  Almaty basin; used as external baseline.
- Local work: Kerimray (NU) on emissions + COVID experiment,
  Kazhydromet, AAI — emission/observation focus, no forecast.
- Gap: locally calibrated, publicly deployed forecast.

### RU · полный текст
Короткий обзор области. **На международном уровне** краткосрочный
прогноз качества воздуха использует четыре семейства методов:
статистические модели (ARIMA, фильтр Калмана); классический ML на
табличных признаках — к нему относится XGBoost; глубокие нейросети
(LSTM, трансформеры); и гибриды физика+ML. Ключевые работы — Feng
(Пекин), Inness (CAMS), Morawska и Di Antonio (поведение LCS),
Zhang (сравнение методов). Вывод: при нашем объёме данных — около 18
месяцев — классический ML на деревьях даёт лучший баланс между
точностью и интерпретируемостью.

**Отдельно о CAMS** — это Copernicus Atmosphere Monitoring Service,
европейский глобальный прогноз качества воздуха. Работает на сетке
40 км: вся Алматы умещается в одну-две ячейки. Эффекты котловины
такая сетка разрешить не может, но это лучший открытый внешний
эталон — с ним и сравниваем.

**На локальном уровне** казахстанские исследования — группа Керимрая
в Назарбаев Университете по эмиссионной инвентаризации отопительного
сезона и естественному COVID-эксперименту, ежегодные отчёты
Казгидромета по эталонной сети, и проект Almaty Air Initiative с
LCS-наблюдениями — описали, *что* Алматы выбрасывает и *что*
измеряется, но не выпустили прогнозный продукт. Этот пробел и
закрывает диссертация.

### RU · тезисы
- 4 семейства (статистика, классический ML, deep learning, гибрид).
  К нам ближе всего — классический ML (XGBoost).
- CAMS — европейский глобальный прогноз, сетка 40 км; котловину
  не видит; используем как внешний бейзлайн.
- Локально: Керимрай (НУ), Казгидромет, AAI — эмиссии и наблюдения,
  прогнозного продукта нет.
- Пробел: локально откалиброванный публичный прогноз.

---

## Slide 9 — Architecture and data sources

### EN · full speech
Three data sources, one pipeline. From **OpenAQ** — a free worldwide
air-quality data hub — we pull hourly PM2.5 from the 192 sensors in
a 25 km circle around the city centre. From **Open-Meteo** — a free
weather service — we pull temperature, humidity, pressure, wind,
precipitation, and boundary-layer height for the same location. From
the same Open-Meteo air-quality endpoint we also fetch the CAMS
forecast for our external baseline. All three sources land as
immutable parquet files on disk; a loader assembles them into the
SQLite database; the feature-engineering module turns them into the
model-ready table; the modelling module trains XGBoost and the
baselines; and the application module — a Streamlit app — renders
the result. No server, no orchestrator, no container — one Python
repository.

### EN · bullets
- **OpenAQ** → PM2.5 (192 sensors, 25 km circle).
- **Open-Meteo** → weather + CAMS baseline.
- Flow: parquet → SQLite → features → XGBoost → Streamlit.
- One Python repo, no cloud.

### RU · полный текст
Три источника данных, один пайплайн. Из **OpenAQ** — свободного
мирового агрегатора качества воздуха — берём почасовой PM2.5 со
192 датчиков в круге 25 км вокруг центра. Из **Open-Meteo** —
бесплатного погодного сервиса — берём температуру, влажность,
давление, ветер, осадки и высоту пограничного слоя для той же
точки. Оттуда же берём прогноз CAMS — наш внешний бейзлайн. Все
три источника ложатся неизменяемыми parquet-файлами на диск;
загрузчик собирает их в базу SQLite; модуль признаков превращает
всё в таблицу, готовую для модели; модуль моделей обучает XGBoost
и бейзлайны; модуль приложения на Streamlit отображает результат.
Ни сервера, ни оркестратора, ни контейнера — один Python-репозиторий.

### RU · тезисы
- **OpenAQ** → PM2.5 (192 датчика, 25 км).
- **Open-Meteo** → погода + бейзлайн CAMS.
- Поток: parquet → SQLite → признаки → XGBoost → Streamlit.
- Один Python-репо, без облака.

---

## Slide 10 — Results

### EN · full speech
Three numbers to set the scale. The main accuracy metric is
**MAE — mean absolute error — in the same units as PM2.5**,
micrograms per cubic metre. XGBoost's MAE is 11.8 for the 6-hour
horizon, 19.4 for 12 hours, and 27.9 for 24 hours. Errors grow with
horizon — as expected.

**On the 24-hour horizon against the three baselines:** persistence,
which naively predicts "tomorrow equals today", gets 44.6; linear
regression gets 35.2; CAMS gets 38.7; XGBoost reaches 27.9. That is
roughly a 37-percent reduction in error compared with persistence
and 28 percent compared with CAMS. **R²** — the share of pollution
variance the model explains, where 0 means useless and 1 means
perfect — rises from 0.21 for persistence and 0.33 for CAMS to 0.62
for XGBoost.

We also ran **SHAP analysis**, which ranks how much each input
variable moved the prediction. The top drivers are the one-hour lag
of PM2.5 itself, then **boundary-layer height — directly confirming
hypothesis H2**, then the 24-hour rolling mean, wind speed, and the
cyclical hour-of-day.

**Known weakness:** during multi-day inversion episodes, when
pollution stays high for days, the model underpredicts the peaks.
This is an expected side-effect of training on mean-squared error,
and we document it openly rather than hide it — this is
hypothesis H3, confirmed.

### EN · bullets
- **MAE:** 11.8 / 19.4 / 27.9 µg/m³ at 6 / 12 / 24 h.
- **24 h:** XGBoost 27.9 vs. persistence 44.6, linear 35.2, CAMS
  38.7 → −37 % vs. persistence, −28 % vs. CAMS.
- **R²:** 0.21 (persistence) → 0.62 (XGBoost).
- **Top SHAP drivers:** lag-1 h PM2.5, **BLH (H2 ✓)**, 24 h rolling
  mean, wind speed, hour-of-day.
- **Known weakness:** peak underprediction on multi-day inversions
  (H3 ✓ — documented, not hidden).

### RU · полный текст
Три числа, чтобы задать масштаб. Основная метрика точности —
**MAE, средняя абсолютная ошибка в тех же единицах, что PM2.5** —
микрограммах на кубический метр. MAE модели XGBoost: 11,8 для
горизонта 6 часов, 19,4 для 12 часов, 27,9 для 24 часов. Ошибка
растёт с горизонтом — как и ожидалось.

**На горизонте 24 часа против трёх бейзлайнов:** персистенс — это
наивный прогноз «завтра как сегодня» — 44,6; линейная регрессия
35,2; CAMS 38,7; XGBoost 27,9. Это примерно 37 процентов снижения
ошибки против персистенса и 28 процентов против CAMS. **R²** —
доля дисперсии загрязнения, которую модель объясняет (0 — бесполезно,
1 — идеально) — растёт с 0,21 у персистенса и 0,33 у CAMS до 0,62
у XGBoost.

Мы также провели **SHAP-анализ** — он ранжирует, насколько каждый
входной признак сдвигал прогноз. Главные драйверы: лаг PM2.5 за час,
затем **высота пограничного слоя — прямое подтверждение гипотезы H2**,
затем 24-часовая скользящая средняя, скорость ветра, час суток.

**Известная слабость:** во время многодневных инверсионных эпизодов,
когда загрязнение держится высоким несколько дней подряд, модель
недооценивает пики. Это ожидаемый побочный эффект обучения на
среднеквадратичной ошибке, и мы документируем это открыто, а не
прячем — это гипотеза H3, подтверждена.

### RU · тезисы
- **MAE:** 11,8 / 19,4 / 27,9 µг/м³ на 6 / 12 / 24 ч.
- **24 ч:** XGBoost 27,9 vs. persistence 44,6, linear 35,2,
  CAMS 38,7 → −37 % vs. persistence, −28 % vs. CAMS.
- **R²:** 0,21 (persistence) → 0,62 (XGBoost).
- **Топ SHAP-драйверы:** PM2.5 лаг-1 ч, **BLH (H2 ✓)**, 24 ч
  скользящая средняя, скорость ветра, час суток.
- **Известная слабость:** недооценка пиков на многодневных
  инверсиях (H3 ✓ — задокументировано).

---

## Slide 11 — Conclusion and future work

### EN · full speech
All three hypotheses from chapter one are confirmed — H1, XGBoost
beats every baseline on every horizon; H2, boundary-layer height is
among the top-three drivers; H3, the model underpredicts peaks on
multi-day inversions, documented as a known failure mode. The full
pipeline is delivered end-to-end through the Streamlit MVP.

Five future-work directions. First, per-sensor bias correction by
co-locating a few LCS devices with Kazhydromet reference stations.
Second, quantile regression to attach honest prediction intervals to
the peaks — directly addressing H3. Third, extending the same
pipeline to PM10, NO₂, and O₃ with only new parameter identifiers.
Fourth, replicating for Shymkent and Karaganda — these cities have
similar geography and LCS coverage. Fifth, a dissertation-topic
publication targeting a Scopus Q2 venue.

### EN · bullets
- **H1 ✓, H2 ✓, H3 ✓** (documented weakness).
- End-to-end pipeline + Streamlit MVP delivered.
- **Future:** sensor bias correction; quantile regression for peak
  intervals; extend to PM10/NO₂/O₃; replicate for Shymkent/Karaganda;
  Scopus Q2 publication.

### RU · полный текст
Все три гипотезы из первой главы подтверждены: H1 — XGBoost
обыгрывает все бейзлайны на всех горизонтах; H2 — высота пограничного
слоя входит в топ-3 драйверов; H3 — модель недооценивает пики на
многодневных инверсиях, задокументировано как известный режим
ошибки. Пайплайн реализован полностью и доведён до Streamlit MVP.

Пять направлений дальнейшей работы. Первое — покомпонентная
коррекция смещения через ко-локацию нескольких LCS-датчиков с
референсными станциями Казгидромета. Второе — квантильная регрессия
для честных интервальных оценок пиков, что напрямую адресует H3.
Третье — расширение того же пайплайна на PM10, NO₂ и O₃, только с
заменой идентификаторов параметров. Четвёртое — тиражирование на
Шымкент и Караганду — близкие по географии и LCS-покрытию. Пятое —
публикация по теме диссертации с целью в журнал уровня Scopus Q2.

### RU · тезисы
- **H1 ✓, H2 ✓, H3 ✓** (задокументированная слабость).
- Пайплайн целиком + Streamlit MVP реализованы.
- **Дальше:** коррекция смещения датчиков, квантильная регрессия
  для пиков, расширение на PM10/NO₂/O₃, тиражирование на Шымкент
  и Караганду, публикация в Scopus Q2.

---

## Slide 12 — Publications

### EN · full speech
I have one prior peer-reviewed publication with Professor
Naizabayeva — a hybrid music-recommendation system. The topic is
different, but the *research method* is the same one this thesis
uses: combining several signals into one model, rigorously comparing
against baselines, and reporting both accuracy and beyond-accuracy
metrics. A publication on the dissertation topic is in preparation.

### EN · bullets
- Prior paper: hybrid music-recommendation system — method transfer,
  not topic transfer.
- Dissertation-topic paper: in preparation.

### RU · полный текст
У меня есть одна рецензированная публикация в соавторстве с
профессором Найзабаевой — по гибридной системе рекомендации музыки.
Тема отличается, но *метод исследования* тот же, что используется в
диссертации: соединение нескольких сигналов в одну модель, строгое
сравнение с бейзлайнами, отчёт по метрикам точности и за её
пределами. Публикация по теме диссертации — в подготовке.

### RU · тезисы
- Предыдущая статья: гибридная рекомендация музыки — перенос
  метода, а не темы.
- Статья по теме диссертации — в подготовке.

---

## Slide 13 — Thank you

### EN
Thank you for your attention — ready for questions.

### RU
Спасибо за внимание — готов ответить на вопросы.

---

## Q&A — anticipated questions

### EN

- **Why XGBoost and not an LSTM?**
  Our dataset is mid-sized — under one million tabular rows with
  engineered lags. XGBoost gives the best accuracy-interpretability
  trade-off at this size and fits on free-tier CPU deployment; LSTMs
  need more data and are harder to host for free.

- **Why not co-locate with reference stations?**
  Co-location requires physical access to reference instruments and
  is out of scope for a four-week master's project. LCS readings are
  treated as a *relative* signal — and this limitation is stated
  explicitly in chapter four.

- **Why does the data window start October 2024?**
  Of the 192 sensors, only about one station has data for winter
  2023-24; most AirGradient devices came online in 2025. The
  562-day continuous window is the longest the actual fleet supports.

- **How is data leakage prevented?**
  Time-series cross-validation with an expanding window; no random
  shuffling; features depend only on past values; the holdout is
  always chronologically later than the training split.

### RU

- **Почему XGBoost, а не LSTM?**
  Объём данных средний — меньше миллиона табличных строк с
  инженерными лагами. XGBoost даёт лучший компромисс
  «точность/интерпретируемость» при этом размере и помещается в
  бесплатное CPU-развёртывание; LSTM требует больше данных и
  сложнее в бесплатном хостинге.

- **Почему не сделали ко-локацию с эталонными станциями?**
  Ко-локация требует физического доступа к эталонным приборам и
  выходит за рамки четырёхнедельного проекта. LCS-показания
  трактуются как *относительный* сигнал — это ограничение явно
  оговорено в четвёртой главе.

- **Почему окно данных начинается в октябре 2024?**
  Из 192 датчиков только ~один покрывает зиму 2023-24; большинство
  AirGradient-устройств появились в 2025. Непрерывное окно в 562 дня
  — максимум, который обеспечивает реальный парк.

- **Как предотвращается утечка данных?**
  Кросс-валидация временных рядов с расширяющимся окном; без
  случайной перемешки; признаки зависят только от прошлого; holdout
  всегда хронологически позже обучающего отрезка.
