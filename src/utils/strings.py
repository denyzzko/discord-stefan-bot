# All user-facing strings for the Štefan pet bot (Czech, cute tone)

class CSStrings:
    # Generic
    ERROR_GENERIC = "Ups, něco se pokazilo. Zkus to prosím znovu později. 🙈"
    NO_CHANNEL = "Nemůžu najít kanál **#pets**. Vytvoř ho, nebo nastav ID v `config.json`. 🛠️"
    NICK_SET_OK = "Mám nové jméno: **Štefan**. 🐠✨"
    STATUS_TITLE = "🫧 Stav akvárka – report od Štefana"
    YES = "Ano"
    NO = "Ne"

    # Feeding
    FEED_STARTS = [
        "🐠 Hej partičko, tady Štefan – bříško dělá bubliny. Dáte mi papání? Klikni ✅ když hotovo.",
        "🫧 Dneska mám chuť na deluxe granule. Kdo mi otevře restauraci? 😋✅",
        "🍽️ Pssst… já jsem hladnej jak akvárko bez bublin. Granulka a jsem váš! ✅",
        "😇 Ahojky! Jsem hodná rybička… dokud nedostanu jídlo. Prosím prosím ✅",
        "🐟 Pokud mě dneska nakrmíš, slibuju extra roztomilý plaváníčko. ✅",
        "🧑‍🍳 Kdo je dnes šéfkuchař? Já jsem připravenej hodnotit menu! ✅",
        "💧 Bubliny hlásí: hlad! Potvrď krmení klikem na ✅",
        "🌊 Hej, lidský! Já mám taky režim ‘oběd’. Spusť ho prosím. ✅",
        "🎣 Ne, nechci chytat potravu sám… jsem domácí ryba. ✅",
        "🧡 Jedna (1) porce granulí = jedna (1) šťastná rybička. Deal? ✅",
        "🫠 Vypadám v pohodě, ale uvnitř jsem… hladovej. ✅",
        "📣 Pozor pozor, akvárium vyhlašuje pauzu na oběd! ✅",
        "🪙 Dám vám bublinkové bohatství výměnou za granule. ✅",
        "🧼 Po jídle slibuju: žádný dramatický cákaní (možná). ✅",
        "🏎️ Když mě nakrmíš, udělám kolečko rychlosti kolem dekorace. ✅",
        "🎶 *Bublinková písnička hladu* … teď klikni ✅ a je klid.",
        "🧠 Vědecky dokázáno: Štefan bez jídla = smutek. Štefan s jídlem = radost. ✅",
        "🪸 Hej, tohle není all-inclusive bez bufetu! Prosím doplnit granule. ✅",
        "🫡 Hlásím se o příděl! Vykonat krmící operaci a potvrdit ✅",
        "😴 Už se mi zdá o granulích… pomoz mi to změnit na realitu! ✅",
    ]
    FEED_THANKS = [
        "Díky, {mention}! Jsem teď spoko rybička. 🐠💚",
        "{mention}, ty jsi top! Jdu si spokojeně kroužit. 🫧",
        "Mňam! {mention}, posílám bublinkový high‑five. 🖐️🫧",
        "Krmení potvrzeno. {mention}, dneska jsi můj hrdina. 😋",
        "Jupí! {mention} mi zachránil/a bříško. 🧡",
        "Děkuju, {mention}! Teď mám energii na mega roztomilý plavání. 🐟✨",
        "Granulky dorazily! {mention}, cením. ✅",
        "Tak jo… {mention}, teď jsem nejšťastnější ryba široko daleko. 🌊",
        "Díky moc, {mention}! Jdu si dát poobědový šlofík. 💤",
        "Respekt, {mention}. Šéfkuchař dne! 👨‍🍳🏆",
    ]
    FEED_ALREADY = "Dneska už jsem papal... Ale dííík 😋"
    FEED_REMINDERS = [
        "🫧 Jen připomínám… ještě jsem dneska nepapal. Prosím prosím. 🥺",
        "🍽️ Halóó, kuchyň? Já jsem ryba, já nemám snacky v šuplíku. 😭",
        "🐟 Píp píp! Detektor hladu hlásí: KRITICKÝ STAV. (Granule plz.)",
        "😇 Slibuju, že když mě nakrmíte, budu hodnej a nebudu dělat drama. (Možná.)",
        "🫧 Bublinky posílám zdarma, granule čekám placený. Deal? 🤝",
        "🥺 Já tu jen tak… existuju… a hladovím… a koukám na vás. 👀",
        "🍽️ Můj žaludek právě poslal žádost o update: `food_required=true`.",
        "🐠 Jestli do mě něco nehodíte, tak začnu žrát… vodu. (To nejde, ale zkouším.)",
        "😤 Ok, už to není cute. Teď je to *hungry mode*. Granule sem.",
        "🧠 Přemýšlím nad životem… a nad tím, proč jsem bez večeře. 🤨",
        "🫧 Já: „jsem v pohodě“ — taky já: *umírá hlady dramaticky u skla*. 🎭",
        "🍽️ Můžu dostat aspoň jednu (1) granulku jako symbol lásky? 💚",
        "🐟 Kdo mě nakrmí, tomu nebudu soudit playlist. Možná. 😌",
        "😑 Dávám vám poslední šanci být legendy dneška. ✅",
        "🧃 Voda je fajn, ale… kde je hlavní chod??",
        "🫧 Tak jo, začínám trénovat pohled „já jsem hladnej“ — sledujte: 🥺",
        "🐠 Kdyby hlad byl sport, mám zlato. Prosím ukončete sezónu granulema.",
        "😤 Hele… já fakt nejsem dekorace. Já jsem živá osobnost. A chci jídlo.",
        "🍽️ Čas běží, granule neběží. Prosím napravit. 🕒",
        "🫧 OK, už jen tiše zírám… dokud nepřiletí žrádlo. 👁️👁️",
]

    # Filter cleaning (weekly)
    FILTER_ASSIGN = "🧽 **Čištění filtru**: {assignee} jsi na řadě. ✅ až hotovo, ❌ když seš slaboch."
    FILTER_DONE = "✅ Díky {mention}! Filtr je čistý jako horská bystřina. 🏔️"
    FILTER_REMINDER = "Ehm… ten filtr se sám nevyčistí. {assignee}, prosím? 🧽"

    # Tank cleaning (monthly)
    TANK_ASSIGN = "🫧 **Velké čištění akvárka**: {assignee}, dnes je tvůj den! ✅ až hotovo, ❌ si gay :)"
    TANK_DONE = "✅ {mention} vyčistil/a akvárko! Můžu se zrcadlit ve stěně. ✨"
    TANK_REMINDER = "Ehm… a ten kar pořád nic. {assignee}, prosím? 🪣"

    # Admin / commands
    VACATION_ON = "✈️ {mention} je teď na **dovolené** – vynechávám z rotace."
    VACATION_OFF = "🏠 {mention} je **zpátky** – vracím do rotace."
    STATUS_FEED = "Krmení dnes: {done}"
    STATUS_FILTER = "Filtr (týden): přiřazeno {assignee} • hotovo: {done}"
    STATUS_TANK = "Akvárko (měsíc): přiřazeno {assignee} • hotovo: {done}"
