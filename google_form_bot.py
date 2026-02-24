import requests
import random
import time
import json
import os

URL = "https://docs.google.com/forms/d/e/1FAIpQLSehIJDYbGUUvTEWOiq6WQQ_eV250l7B4-f8VHz8AGdzxucFoQ/formResponse"
TOTAL_RESPONSES = 104
STATE_FILE = "state.json"

# --- Варианты ответов ---
options_map = {
    "entry.457041491": ["16 лет и младше", "17–18 лет", "19–20 лет", "21–22 года", "23 года и старше"],
    "entry.900081255": ["Мужской", "Женский"],
    "entry.2072137170": ["г. Астана", "г. Алматы", "г. Шымкент", "Актюбинская область", "Алматинская область", "Атырауская область", "Восточно-Казахстанская область", "Западно-Казахстанская область", "Карагандинская область", "Кызылординская область", "Туркестанская область"],
    "entry.1467051264": ["Школа", "Университет / Вуз", "Работа"],
    "entry.2049384046": ["Казахский", "Русский", "Английский", "Смешанный (несколько языков)"],
    "entry.997831765": ["Казахский", "Русский", "Английский"],
    "entry.2016190063": ["Казахский", "Русский", "Английский"],
    "entry.1708145665": ["1", "2", "3", "4", "5"],
    "entry.1452720691": ["Сложно понимать специфические термины.", "Преподаватель говорит слишком быстро.", "Трудно быстро конспектировать и переводить одновременно.", "Сложно задавать вопросы или отвечать на занятиях.", "Трудностей нет, я всё понимаю."],
    "entry.1794521284": ["Ищу перевод или объяснение на родном языке в интернете.", "Прошу одногруппников/друзей объяснить на более понятном языке.", "Пытаюсь догадаться по смыслу и контексту.", "Жду, когда преподаватель объяснит еще раз."],
    "entry.286483656": ["Да, постоянно (смешиваю термины из разных языков).", "Иногда (когда не хватает слов на одном языке).", "Нет, стараюсь использовать только один язык."],
    "entry.737822750": ["Да, это значительно облегчает понимание материала.", "Немного помогает, но мешает погружению в основной язык обучения.", "Нет, это только создает путаницу."],
    "entry.331049506": ["1", "2", "3", "4", "5"],
    "entry.1295596769": ["На родном языке (понимание темы происходит быстрее и глубже).", "На языке обучения (даже если он не родной, мне проще усваивать академический материал именно на нем).", "Смешанно: термины легче понимать на английском/языке обучения, а общую суть — на родном языке.", "Разницы нет, я одинаково эффективно воспринимаю информацию на любом из языков."]
}

unique_sentences = [
    "Мне так удобнее.", "Привычка", "Легче усваивать информацию.",
    "Потому что это мой родной язык.", "Так быстрее запоминается.",
    "Преподаватель так объясняет.", "Меньше трачу времени на перевод.",
    "Больше практики на этом языке.", "Английский нужен для будущей профессии.",
    "В IT все термины на английском.", "Учебники в основном на английском.",
    "Привык к английскому языку.", "Я всегда так разговариваю.",
    "На родном всегда проще излагать мысли.", "Потому что в школе так учили.",
    "Это язык, на котором я думают.", "Не нужно тратить время на подбор слов.",
    "Все мои друзья так говорят.", "Этот язык кажется мне более логичным для этих тем.",
    "Так сложилось исторически.", "В моей сфере все ресурсы на английском.",
    "Язык обучения обязывает.", "Просто привыкла за время учебы.",
    "Так проще коммуницировать с коллегами.", "Меньше шансов ошибиться в терминологии.",
    "Русский язык богаче на академические термины в моей специальности.",
    "Я лучше формулирую мысли на этом языке.", "В университете все материалы на английском.",
    "Привычка со школы, мы так учились.", "Потому что перевод иногда искажает смысл.",
    "Оригинальные источники всегда точнее.", "На английском термины короче и понятнее.",
    "Мой мозг автоматически переключается на этот язык.", "Мне так легче воспринимать сложные концепции.",
    "На родном языке я лучше понимаю контекст.", "Это экономит мои ментальные ресурсы.",
    "Я чувствую себя увереннее.", "Так эффективнее готовиться к экзаменам.",
    "В нашем регионе все так говорят.", "Так проще находить ответы в гугле.",
    "Мне нравится звучание терминов на этом языке.", "Потому что вся литература написана так.",
    "Это мой базовый язык общения.", "Я планирую работать за рубежом.",
    "Так удобнее писать конспекты.", "Для меня важна точность определений, на английском это проще.",
    "Я вырос в двуязычной среде, мне так органичнее.", "Потому что русский - мой основной язык.",
    "Английский более универсален в науке.", "Так удобнее обсуждать темы с однокурсниками.",
    "Меньше стресса при обучении.", "Родной язык дает более глубокое понимание.",
    "Я читаю профессиональные форумы на английском.", "Термины на казахском часто сложно переведены.",
    "Перевод многих терминов просто не существует.", "Это позволяет мне быстрее читать техническую документацию.",
    "На языке оригинала всегда лучше.", "Мне проще читать код и комментарии на английском.",
    "Сложные вещи лучше объяснять простыми словами на родном языке.", "Англоязычный YouTube очень помогает в учебе.",
    "Привык еще с лицея.", "Я билингв, мне без разницы, но так выходит чаще.",
    "Просто не хочу лишний раз напрягаться с переводом.", "Так мы работаем на практике.",
    "Моя будущая специальность требует именно этого языка.", "В интернете больше туториалов.",
    "На лекциях используют этот язык.", "Большинство терминов - это заимствования, проще использовать их напрямую.",
    "Я лучше запоминаю визуально на английском.", "Мне так проще структурировать информацию.",
    "Общий язык с международным сообществом.", "Мой словарный запас на этом языке больше.",
    "Так понятнее суть явлений.", "Потому что я так привыкла с самого начала.",
    "Язык IT - это английский язык.", "На русском больше качественной адаптированной литературы.",
    "Мне комфортнее.", "Так информация усваивается более естественно.",
    "Потому что переводчики часто врут.", "Я люблю этот язык.", "У нас в семье все так говорят.",
    "Преподаватель требует использовать оригинал.", "На казахском некоторые слова звучат непривычно.",
    "Это расширяет мой кругозор.", "Я готовлюсь к IELTS, поэтому везде использую английский.",
    "Так просто быстрее.", "Не вижу смысла переводить то, что и так понятно.",
    "Мой мозг так настроен.", "Язык программирования сам по себе на английском.",
    "В IT-сфере нет смысла учить термины на русском.", "Большую часть времени я потребляю контент на этом языке.",
    "Просто я ленивый переводить.", "Легче доносить свою мысль до других.",
    "Мне так посоветовали старшекурсники.", "Все передовые статьи выходят на английском.",
    "Потому что курсы на Coursera на английском.", "Русскоязычное коммьюнити программистов очень большое.",
    "Так сложилось.", "Так удобнее шпаргалки писать.", "Потому что я учился в НИШ.",
    "Мне нравится этот язык.", "Я хочу свободно говорить о своей профессии.",
    "Это избавляет от двойной работы.", "Так меньше путаницы.", "На казахском я лучше понимаю общую картину.",
    "Удобно", "Я привык так общаться.", "Так быстрее работает мозг.",
    "Это самый логичный выбор.", "Это экономит кучу времени.", "Потому что так проще.",
    "Легко.", "Без понятия.", "Не знаю."
]

popular_ones = ["Просто так", "Мне так удобнее", "Не знаю", "удобно"]

# ---------- Функции ----------
def classify_sentence(sentence):
    s = sentence.lower()
    native_lang_keywords = ['казахск', 'русск', 'родн', 'материнск']
    negative_words = ['непривыч', 'сложн', 'трудн', 'тяжел', 'стран', 'проблем', 'не хватает', 'не существует']
    if any(lang in s for lang in native_lang_keywords) and any(neg in s for neg in negative_words):
        return 'learning'
    if any(word in s for word in ['билингв', 'смешан', 'оба', 'поперемен', 'двуязычн']):
        return 'mixed'
    if any(word in s for word in ['английск', 'язык обучени', 'университет', 'академическ', 'термин',
                                   'професси', 'будущ', 'оригинал', 'литератур', 'учебник', 'курс', 'it',
                                   'код', 'техническ', 'документаци', 'карьер', 'зарубеж', 'международн',
                                   'ielts', 'coursera', 'туториал', 'форум', 'статьи', 'программирован']):
        return 'learning'
    if any(word in s for word in ['родн', 'казахск', 'русск', 'материнск', 'своём языке']):
        return 'native'
    if any(word in s for word in ['разниц', 'одинаков', 'всё равно', 'без разниц', 'не важно', 'любом языке']):
        return 'none'
    return 'neutral'

def format_text_randomly(text):
    text = text.strip()
    if random.random() < 0.4 and text:
        text = text[0].lower() + text[1:]
    if text.endswith('.'):
        if random.random() < 0.5:
            text = text[:-1]
        elif random.random() < 0.1:
            text = text[:-1] + "..."
    else:
        if random.random() < 0.3:
            text += "."
    return text

def generate_profile(index, english_indices):
    """
    Генерирует согласованный профиль респондента.
    Возвращает словарь с ключами:
        age, gender, region, occupation, native_lang, school_lang, uni_lang
    """
    profile = {}

    # --- Род занятий (с учётом возраста) ---
    # Сначала выбираем род занятий с общими весами
    occ_weights = [0.10, 0.85, 0.05]  # школа, универ, работа
    occupation = random.choices(options_map["entry.1467051264"], weights=occ_weights, k=1)[0]
    profile['occupation'] = occupation

    # --- Возраст (согласован с родом занятий) ---
    age_options = options_map["entry.457041491"]
    if occupation == "Школа":
        age_weights = [0.3, 0.7, 0.0, 0.0, 0.0]  # только до 18 лет
    elif occupation == "Университет / Вуз":
        age_weights = [0.0, 0.3, 0.5, 0.15, 0.05]  # 17-23+
    else:  # Работа
        age_weights = [0.0, 0.0, 0.2, 0.3, 0.5]   # в основном старше 21
    profile['age'] = random.choices(age_options, weights=age_weights, k=1)[0]

    # --- Пол (без ограничений) ---
    profile['gender'] = random.choice(options_map["entry.900081255"])

    # --- Регион (с сохранением прежних весов) ---
    regions = options_map["entry.2072137170"]
    region_weights = [0.25, 0.35, 0.20] + [0.20/17] * (len(regions)-3)
    profile['region'] = random.choices(regions, weights=region_weights, k=1)[0]

    # --- Родной язык ---
    if index in english_indices:
        native_lang = "Английский"
    else:
        # Можно добавить зависимость от региона, но для простоты оставим общие веса
        native_lang = random.choices(["Казахский", "Русский"], weights=[0.65, 0.35], k=1)[0]
    profile['native_lang'] = native_lang

    # --- Язык в школе (зависит от родного языка) ---
    if native_lang == "Казахский":
        # С вероятностью 0.85 казахский, 0.1 русский, 0.05 английский (спецшколы)
        school_lang = random.choices(
            ["Казахский", "Русский", "Английский"],
            weights=[0.85, 0.10, 0.05], k=1)[0]
    elif native_lang == "Русский":
        school_lang = random.choices(
            ["Казахский", "Русский", "Английский"],
            weights=[0.10, 0.85, 0.05], k=1)[0]
    else:  # Английский
        school_lang = random.choices(
            ["Казахский", "Русский", "Английский"],
            weights=[0.05, 0.10, 0.85], k=1)[0]
    profile['school_lang'] = school_lang

    # --- Язык обучения (для учёбы/работы) ---
    if occupation == "Университет / Вуз":
        # Студенты могут учиться на разных языках
        if native_lang == "Казахский":
            uni_weights = [0.30, 0.10, 0.40, 0.20]  # каз, рус, англ, смеш
        elif native_lang == "Русский":
            uni_weights = [0.10, 0.35, 0.35, 0.20]
        else:  # Английский
            uni_weights = [0.05, 0.05, 0.70, 0.20]
    elif occupation == "Школа":
        # Школьники учатся на языке школы (обычно совпадает с school_lang)
        # Но могут быть смешанные классы, поэтому добавим вариант "Смешанный"
        if school_lang == "Казахский":
            uni_weights = [0.90, 0.02, 0.01, 0.07]
        elif school_lang == "Русский":
            uni_weights = [0.02, 0.90, 0.01, 0.07]
        else:  # Английский
            uni_weights = [0.01, 0.01, 0.90, 0.08]
    else:  # Работа
        # Для работающих язык общения может быть любым, чаще смешанный или русский/казахский
        uni_weights = [0.30, 0.40, 0.10, 0.20]
    profile['uni_lang'] = random.choices(options_map["entry.2049384046"], weights=uni_weights, k=1)[0]

    return profile

def generate_one_response(index, english_indices, categorized):
    # Генерируем согласованный профиль
    profile = generate_profile(index, english_indices)

    data = {"fvv": "1"}

    # Заполняем ответы на основе профиля
    data["entry.457041491"] = profile['age']
    data["entry.900081255"] = profile['gender']
    data["entry.2072137170"] = profile['region']
    data["entry.1467051264"] = profile['occupation']
    data["entry.997831765"] = profile['native_lang']
    data["entry.2016190063"] = profile['school_lang']
    data["entry.2049384046"] = profile['uni_lang']

    # Флаг обучения на неродном языке (исключая полностью совпадающий)
    native = profile['native_lang']
    uni = profile['uni_lang']
    is_studying_foreign = (uni != native) and (uni != "Смешанный (несколько языков)")

    # --- 8. Легкость понимания ---
    if is_studying_foreign:
        understanding_weights = [0.05, 0.15, 0.45, 0.25, 0.10]
    else:
        understanding_weights = [0.0, 0.05, 0.15, 0.40, 0.40]
    data["entry.1708145665"] = random.choices(options_map["entry.1708145665"], weights=understanding_weights, k=1)[0]

    # --- 9. Трудности (множественный выбор) ---
    understanding_score = int(data["entry.1708145665"])
    if understanding_score >= 4:
        data["entry.1452720691"] = "Трудностей нет, я всё понимаю."
    else:
        diffs = options_map["entry.1452720691"][:-1]  # все, кроме последнего
        chosen_diffs = random.sample(diffs, k=random.randint(1, 2))
        data["entry.1452720691"] = chosen_diffs

    # --- 10. Действие ---
    action_weights = [0.45, 0.30, 0.15, 0.10]
    data["entry.1794521284"] = random.choices(options_map["entry.1794521284"], weights=action_weights, k=1)[0]

    # --- 11. Код-свитчинг ---
    if is_studying_foreign or uni == "Смешанный (несколько языков)":
        cs_weights = [0.60, 0.30, 0.10]
    else:
        cs_weights = [0.20, 0.40, 0.40]
    data["entry.286483656"] = random.choices(options_map["entry.286483656"], weights=cs_weights, k=1)[0]

    # --- 12. Помощь от перехода ---
    if is_studying_foreign:
        help_weights = [0.65, 0.25, 0.10]
    else:
        help_weights = [0.20, 0.30, 0.50]
    data["entry.737822750"] = random.choices(options_map["entry.737822750"], weights=help_weights, k=1)[0]

    # --- 13. Усилия ---
    if is_studying_foreign:
        effort_weights = [0.05, 0.20, 0.40, 0.25, 0.10]
    else:
        effort_weights = [0.60, 0.20, 0.10, 0.05, 0.05]
    data["entry.331049506"] = random.choices(options_map["entry.331049506"], weights=effort_weights, k=1)[0]

    # --- 14. На каком языке легче ---
    if is_studying_foreign:
        easier_weights = [0.40, 0.15, 0.35, 0.10]
    else:
        easier_weights = [0.80, 0.05, 0.05, 0.10]
    data["entry.1295596769"] = random.choices(options_map["entry.1295596769"], weights=easier_weights, k=1)[0]

    # --- 15. Выбор фразы (с учётом ответа на 14) ---
    choice_14 = data["entry.1295596769"]
    if "На родном языке" in choice_14:
        target_cat = 'native'
    elif "На языке обучения" in choice_14:
        target_cat = 'learning'
    elif "Смешанно" in choice_14:
        target_cat = 'mixed'
    elif "Разницы нет" in choice_14:
        target_cat = 'none'
    else:
        target_cat = 'neutral'

    if random.random() < 0.9:
        if categorized[target_cat]:
            ans = categorized[target_cat].pop(0)
        elif categorized['neutral']:
            ans = categorized['neutral'].pop(0)
        else:
            for cat in categorized:
                if categorized[cat]:
                    ans = categorized[cat].pop(0)
                    break
            else:
                ans = random.choice(popular_ones)
    else:
        ans = random.choice(popular_ones)

    ans = format_text_randomly(ans)
    data["entry.593581296"] = ans
    data["pageHistory"] = "0"

    return data, ans, categorized

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    else:
        random.shuffle(unique_sentences)
        categorized = {'native': [], 'learning': [], 'mixed': [], 'none': [], 'neutral': []}
        for s in unique_sentences:
            cat = classify_sentence(s)
            categorized[cat].append(s)
        for cat in categorized:
            random.shuffle(categorized[cat])
        english_indices = random.sample(range(TOTAL_RESPONSES), 2)
        return {
            'sent_count': 0,
            'english_indices': english_indices,
            'categorized': categorized
        }

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def main():
    state = load_state()
    sent_count = state['sent_count']
    english_indices = state['english_indices']
    categorized = state['categorized']

    if sent_count >= TOTAL_RESPONSES:
        print(f"Все {TOTAL_RESPONSES} анкет уже отправлены. Завершаем.")
        return

    print(f"Отправка анкеты #{sent_count + 1}...")

    payload, phrase, updated_categorized = generate_one_response(sent_count, english_indices, categorized)

    # Небольшая задержка для естественности
    if random.random() < 0.7:
        delay = random.uniform(0, 30)
        print(f"⏳ Задержка {delay:.1f} сек")
        time.sleep(delay)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://docs.google.com/forms/d/e/1FAIpQLSce7JvrJXbHWyWDoJmInk5A4sY5F_-4sUoQB-2G8-XC_N5Kwg/viewform',
        'Origin': 'https://docs.google.com',
    }

    try:
        response = requests.post(URL, data=payload, headers=headers)
        if response.status_code == 200:
            print(f"✅ Анкета #{sent_count + 1} отправлена. Фраза: \"{phrase}\"")
            state['sent_count'] = sent_count + 1
            state['categorized'] = updated_categorized
            save_state(state)
        else:
            print(f"❌ Ошибка: статус {response.status_code}")
            print(f"Текст ответа: {response.text[:200]}")
    except Exception as e:
        print(f"🔴 Исключение: {e}")

if __name__ == "__main__":
    main()

