# Prior publication — brief for the defence

**Paper.** Izimov A., Naizabayeva L. K. *A Hybrid Music Recommendation
System: Integrating Collaborative Filtering and Audio Feature
Analysis.*
**Source file.** `articles/HYBRID_MUSIC_RECOMMENDATION_SYSTEM.docx`

---

## EN · what the paper is about

### What it does
A **hybrid music recommendation system** that suggests songs. Given a
song a user likes, it returns similar songs — by combining two
sources of signal that are usually used in isolation: *who listens to
what* (collaborative signal) and *what the music actually sounds like*
(audio content).

### Why
- Single-signal recommenders fail on the edges: **collaborative
  filtering** (CF) breaks on new tracks or sparse listeners
  (cold-start / sparsity); **content-based** systems produce less
  diverse lists.
- Real music catalogs (Spotify-scale: millions of tracks) have a
  **long tail** — most tracks have very few listeners. Handling
  this long tail is a core research challenge.
- Combining the two signals into one model is the obvious idea, but
  *how* to combine them — and whether graph methods actually
  outperform matrix methods — is the open question.

### How it works — one paragraph
The paper builds a **bipartite graph** where one kind of node is a
*playlist* and the other is a *song*; a playlist–song edge exists if
the song appears in the playlist. Each song node is additionally
annotated with a **512-dim audio embedding** produced by a
pre-trained deep network (L3-Net / VGGish / MusicNN). A **graph
neural network — PinSage** — learns embeddings for every song by
aggregating features from its graph neighbours, selected via
personalised PageRank. Similar songs end up with similar embeddings;
"recommend songs" becomes "retrieve nearest neighbours in that
embedding space".

### What it uses
- **Data:** Spotify Web API — bipartite playlist-song graph with
  112 050 songs, 53 092 playlists, ~4.4 M edges; Last.fm LFM-1B —
  1.85 M song co-occurrence pairs (training labels).
- **Audio embeddings:** L3-Net, VGGish, MusicNN (all pre-trained).
- **Core model:** PinSage (scalable graph convolutional network
  with random-walk neighbour sampling).
- **Baselines:** node2vec, Personalized PageRank, playlist-track
  matrix CF, track-track matrix CF, and three content-based
  nearest-neighbour retrievers (one per audio embedding).
- **Metrics:** accuracy (Hit-Rate@10/100/500, MRR) *and*
  beyond-accuracy — intra-list diversity, inter-list diversity,
  catalog coverage, mean recommended degree, Low-Degree MRR,
  Sparse MRR.

### What it found
- **Graph-based methods consistently beat matrix-based CF**,
  confirming that the playlist-song graph encodes rich similarity
  that matrix factorisation misses.
- **PinSage is the balanced choice:** not the highest single
  accuracy (PPR wins that), but the best trade-off — good accuracy,
  high catalog coverage, healthy intra-list diversity, and no
  runaway popularity bias.
- **Audio embedding quality matters:** replacing the best embedding
  (L3-Net) with a weaker one (MusicNN) drops HR@10 by ~12×.
- **Long tail is not a problem** for graph methods — counter to
  expectations — suggesting the graph structure alone compensates
  for item sparsity.

### Why it matters for the dissertation defence
The paper uses **exactly the research method pattern** I apply in
the thesis:
1. **Hybrid signal combination** (CF + audio) → parallel in thesis:
   pollution history + meteorology.
2. **Rigorous baseline comparison** (7 baselines, not just one) →
   parallel: persistence / linear / CAMS in the thesis.
3. **Accuracy + beyond-accuracy reporting** → parallel: MAE/RMSE/R²
   plus error-regime analysis on episodes.
4. **Ablation study** on what actually drives performance → parallel:
   SHAP analysis in the thesis.

This is why the paper is relevant even though the topic is different:
the *methodological rigour* transfers directly.

---

## RU · о чём статья

### Что делает
**Гибридная система рекомендации музыки.** По любимой песне
возвращает похожие, объединяя два сигнала, которые обычно используют
по отдельности: *кто что слушает* (коллаборативный сигнал) и *как
песня звучит* (аудиоконтент).

### Зачем
- Однофакторные рекомендеры ломаются на краях: **коллаборативная
  фильтрация** (CF) плохо работает на новых треках и редких
  слушателях (cold-start, sparsity); **контент-базированные**
  системы дают менее разнообразные списки.
- У реальных каталогов (уровня Spotify — миллионы треков) —
  **длинный хвост**: у большинства треков мало прослушиваний. Его
  обработка — ключевая исследовательская задача.
- Объединить два сигнала — идея очевидная, но *как* объединять и
  действительно ли графовые методы превосходят матричные — вопрос
  открытый.

### Как это работает — одним абзацем
Строится **двудольный граф**: один тип узлов — *плейлисты*, другой
— *песни*; ребро есть, если песня входит в плейлист. Каждой
песне-узлу дополнительно приписан **512-мерный аудиоэмбеддинг**,
полученный предобученной глубокой нейросетью (L3-Net / VGGish /
MusicNN). **Граф-нейронная сеть PinSage** обучает для каждой песни
эмбеддинг, агрегируя признаки соседей по графу, выбранных
персонализированным PageRank. Похожие песни получают близкие
эмбеддинги; «порекомендовать похожие» превращается в «найти ближайших
соседей в этом векторном пространстве».

### Что использует
- **Данные:** Spotify Web API — двудольный граф плейлист-песня
  (112 050 песен, 53 092 плейлиста, ~4,4 М рёбер); Last.fm LFM-1B —
  1,85 М пар со-встречаемости (обучающие метки).
- **Аудиоэмбеддинги:** L3-Net, VGGish, MusicNN (все предобученные).
- **Основная модель:** PinSage (масштабируемая GCN с
  случайно-блужданной выборкой соседей).
- **Бейзлайны:** node2vec, Personalized PageRank, матричный CF
  плейлист-трек, матричный CF трек-трек и три контент-базированных
  поиска ближайших соседей (по одному на аудиоэмбеддинг).
- **Метрики:** точность (Hit-Rate@10/100/500, MRR) *и*
  за-пределами-точности — внутри- и меж-списочное разнообразие,
  покрытие каталога, средняя степень рекомендаций, Low-Degree MRR,
  Sparse MRR.

### Что выявлено
- **Графовые методы стабильно обыгрывают матричные CF** — значит,
  двудольный граф несёт богатую информацию о сходстве, которую
  матричное разложение упускает.
- **PinSage — сбалансированный выбор:** не абсолютный лидер по
  точности (PPR впереди), но лучший компромисс — хорошая точность,
  высокое покрытие каталога, хорошее внутрисписочное разнообразие и
  нет перекоса в популярность.
- **Качество аудиоэмбеддинга критично:** замена L3-Net на MusicNN
  роняет HR@10 примерно в 12 раз.
- **Длинный хвост не становится проблемой** для графовых методов —
  вопреки ожиданиям, — значит, структура графа сама компенсирует
  разрежённость.

### Почему это важно для защиты диссертации
В статье применён **ровно тот же паттерн исследования**, что и в
диссертации:
1. **Комбинация гибридных сигналов** (CF + аудио) → параллель в
   диссертации: история загрязнения + метеорология.
2. **Строгое сравнение с бейзлайнами** (7, а не один) → параллель:
   персистенс / линейная / CAMS.
3. **Метрики точности + beyond-accuracy** → параллель: MAE/RMSE/R²
   плюс анализ режимов ошибок на эпизодах.
4. **Ablation-исследование движущих факторов** → параллель:
   SHAP-анализ в диссертации.

Вот почему статья актуальна для защиты, несмотря на другую тему:
*методологическая строгость* переносится напрямую.
