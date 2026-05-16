# ABSTRACT / АННОТАЦИЯ / АҢДАТПА

---

## ABSTRACT (English)

**Development of an intelligent system for investigating and solving ecological problems**

Master's thesis — Program 7M06106 "Software Engineering", KBTU, 2026  
Supervisor: Naizabayeva Lyazat Kydyrgaliyevna, Doctor of Technical Sciences, Professor

The relevance of the present work is determined by the acute public health challenge of wintertime PM2.5 air pollution in Almaty, Kazakhstan. The city's mountain-basin topography and coal-dependent private-sector heating combine to produce seasonal inversion episodes in which the atmospheric boundary layer collapses to 10–50 m and daily-mean PM2.5 concentrations reach 74–81 μg/m³ — five to six times the WHO 24-hour guideline of 15 μg/m³. Despite this severity, no open, reproducible, locally calibrated short-term PM2.5 forecast has been available to residents or municipal agencies.

The **aim** of the work is to develop and evaluate an intelligent short-term PM2.5 forecasting system for Almaty built entirely on open data and deployable on free-tier infrastructure.

The **object of study** is short-term PM2.5 concentration dynamics in Almaty. The **subject of study** is machine-learning models for hourly PM2.5 forecasting on low-cost-sensor observations under inversion-dominated mountain-basin conditions.

**Research methods** include data engineering via the OpenAQ v3 and Open-Meteo APIs, supervised learning with gradient-boosted trees (XGBoost) and Ridge regression, temporal 80/20 train-test splitting, error-regime analysis under varying boundary-layer regimes, and comparison against persistence and CAMS global chemistry-transport model baselines.

The **principal results** are as follows. XGBoost achieves RMSE = 23.44 μg/m³ and R² = 0.545 at the 6-hour forecast horizon on a 2,311-hour held-out winter test set (December 2025 – April 2026), outperforming the CAMS global model by 41% in RMSE. Ridge regression outperforms XGBoost at 12 and 24-hour horizons (RMSE 25.85 and 27.24 μg/m³ respectively), establishing that model complexity must be matched to forecast horizon and training-set size. All locally trained models substantially outperform CAMS (negative R² at all horizons), confirming the value of local LCS-based calibration over freely available global chemistry-transport output.

**Scientific novelty**: (1) the first publicly evaluated PM2.5 forecasting model calibrated for Almaty's LCS network and inversion-dominated winter meteorology; (2) a fully reproducible open-source pipeline directly transferable to other Central Asian cities sharing Almaty's data-availability profile. **Practical significance**: a free-access Streamlit web application providing 6, 12, and 24-hour PM2.5 forecasts for Almaty with no authentication requirement.

The thesis consists of **60 pages**, **3 figures**, **8 tables**, **25 sources**, **1 appendix**.

**Keywords**: PM2.5 forecasting, Almaty, XGBoost, low-cost sensors, boundary layer height, air quality, gradient boosting

---

## АҢДАТПА (Қазақша)

**Экологиялық мәселелерді зерттеу және шешуге арналған интеллектуалды жүйені әзірлеу**

Магистрлік диссертация — 7M06106 «Бағдарламалық жасақтама инженериясы» мамандығы, ҚБТУ, 2026 ж.  
Ғылыми жетекші: Найзабаева Ляззат Қыдырғалиқызы, техника ғылымдарының докторы, профессор

Жұмыстың **өзектілігі** Қазақстанның Алматы қаласында қысқы мезгілдегі PM2.5 бөлшектерімен ауа ластануының өткір қоғамдық денсаулық мәселесімен анықталады. Қаланың тау қазаншұңқыры топографиясы мен жеке сектордың көмірмен жылытуы инверсия эпизодтарын туғызады: атмосфера шекаралық қабатының биіктігі 10–50 м-ге дейін төмендейді, ал PM2.5 тәуліктік орташа концентрациясы 74–81 мкг/м³-ге жетеді — бұл ДДҰ нормасынан (15 мкг/м³) бес-алты есе жоғары. Тұрғындар мен қалалық қызметтер үшін ешқандай ашық, қайта шығарылатын, жергілікті калибрленген қысқамерзімді болжам болмаған.

Жұмыстың **мақсаты** — тек ашық деректер көздеріне негізделген және тегін бұлттық инфрақұрылымда орналастырылатын Алматы үшін PM2.5 концентрациясын қысқамерзімді болжайтын интеллектуалды жүйені әзірлеу және бағалау.

**Зерттеу объектісі** — Алматыдағы PM2.5 концентрациясының қысқамерзімді динамикасы. **Зерттеу пәні** — инверсиялы тау котловинасы жағдайында арзан датчиктер (LCS) деректері негізінде PM2.5 сағаттық болжауына арналған машиналық оқыту модельдері.

**Зерттеу әдістері**: OpenAQ v3 және Open-Meteo API арқылы деректер инженериясы; XGBoost градиенттік бустинг және жоташа регрессия негізінде бақылаулы оқыту; 80/20 уақыттық бөлу бойынша тексеру; қателік режимдерін талдау; персистентті болжам мен CAMS жаһандық химиялық тасымал моделімен салыстыру.

**Негізгі нәтижелер**: XGBoost 6 сағаттық горизонтта RMSE = 23,44 мкг/м³ және R² = 0,545 мәндерін көрсетеді, CAMS-тан RMSE бойынша 41%-ға асып озады. Жоташа регрессия 12 және 24 сағаттық горизонттарда XGBoost-тан жақсырақ нәтиже береді (RMSE тиісінше 25,85 және 27,24 мкг/м³). Барлық жергілікті үйрентілген модельдер барлық горизонттарда CAMS-тан едәуір жоғары нәтиже береді (R² ≤ −0,18).

**Ғылыми жаңалығы**: (1) Алматының LCS желісі мен инверсиялы қыс метеорологиясына калибрленген бірінші жарияланған PM2.5 болжау моделі; (2) Орталық Азияның басқа қалаларына ауыстырылатын толық шығарылатын ашық бағдарламалық желі. **Практикалық маңыздылығы**: аутентификация қажет етпейтін, Алматы үшін 6, 12 және 24 сағаттық PM2.5 болжамдарын ұсынатын ашық Streamlit веб-қосымшасы.

Диссертация **60 беттен**, **3 суреттен**, **8 кестеден**, **25 дереккөзден**, **1 қосымшадан** тұрады.

**Түйін сөздер**: PM2.5 болжау, Алматы, XGBoost, арзан датчиктер, шекаралық қабат биіктігі, ауа сапасы, градиенттік бустинг

---

## АННОТАЦИЯ (Русский)

**Разработка интеллектуальной системы для исследования и решения экологических проблем**

Магистерская диссертация — специальность 7M06106 «Программная инженерия», КБТУ, 2026 г.  
Научный руководитель: Найзабаева Лязат Кыдыргалиевна, доктор технических наук, профессор

**Актуальность** работы определяется острой проблемой загрязнения атмосферного воздуха взвешенными частицами PM2.5 в зимний период в Алматы. Горно-котловинная топография города в сочетании с угольным отоплением частного сектора формирует инверсионные эпизоды, при которых высота пограничного слоя атмосферы снижается до 10–50 м, а суточная средняя концентрация PM2.5 достигает 74–81 мкг/м³ — в пять-шесть раз выше норматива ВОЗ (15 мкг/м³). При этом ни одного открытого, воспроизводимого, локально калиброванного краткосрочного прогноза качества воздуха для жителей и городских служб Алматы не существовало.

**Цель работы** — разработка и оценка интеллектуальной системы краткосрочного прогнозирования концентрации PM2.5 для Алматы на основе исключительно открытых источников данных с развёртыванием на бесплатной облачной инфраструктуре.

**Объект исследования** — динамика краткосрочных концентраций PM2.5 в атмосфере Алматы. **Предмет исследования** — модели машинного обучения для почасового прогнозирования PM2.5 по данным малозатратных датчиков (LCS) в условиях инверсионной горно-котловинной метеорологии.

**Методы исследования**: инжиниринг данных через API OpenAQ v3 и Open-Meteo; обучение с учителем на основе градиентного бустинга (XGBoost) и гребневой регрессии; валидация с временны́м разбиением 80/20; анализ режимов ошибок при различной высоте пограничного слоя; сравнение с моделями персистентности и глобальной химико-транспортной моделью CAMS.

**Основные результаты**: XGBoost достигает RMSE = 23,44 мкг/м³ и R² = 0,545 на горизонте 6 часов на отложенной тестовой выборке из 2 311 часов (декабрь 2025 — апрель 2026), превосходя CAMS на 41% по RMSE. Гребневая регрессия превосходит XGBoost на горизонтах 12 и 24 часа (RMSE 25,85 и 27,24 мкг/м³ соответственно). Все локально обученные модели существенно превосходят CAMS (R² ≤ −0,18 на всех горизонтах), подтверждая ценность локальной калибровки на LCS-данных.

**Научная новизна**: (1) первая опубликованная модель прогнозирования PM2.5, откалиброванная для сети LCS Алматы и инверсионной зимней метеорологии; (2) полностью воспроизводимый открытый программный конвейер, переносимый на другие города Центральной Азии. **Практическая значимость**: веб-приложение Streamlit с открытым доступом, обеспечивающее прогнозы PM2.5 на горизонтах 6, 12 и 24 часа для Алматы без необходимости аутентификации.

Диссертация состоит из **60 страниц**, **3 рисунков**, **8 таблиц**, **25 источников**, **1 приложения**.

**Ключевые слова**: прогнозирование PM2.5, Алматы, XGBoost, малозатратные датчики, высота пограничного слоя, качество воздуха, градиентный бустинг
