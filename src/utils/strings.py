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
        "Heeej kluci, jsem už hladnej! 🍽️🐟 Prosím **nakrmte mě**.",
        "Wassuuup, tady Štefan. Bříško kručí… papaníčko? 😇🐠",
        "Halóó, kuchaři! Mám hlad jak sumec. 😤 Po jídle hned ztichnu, slibuji.",
        "Čau banda, jsem připravenej na granulový all-you-can-eat. 😎",
        "Prosííím, jen pár granulí a budu nejšťastnější ryba v akvárku! (i když sem tady sám ...)🥺💧",
        "Hele, jestli nedostanu mňamku, začnu žrát dekorace. Nebudu se opakovat dvakrát. 😬",
        "Šéfe, kuchyň otevřená? Jdu si pro svoje! 🐟✨",
        "Dobrý den, objednávám si dnešní speciál — rybie žradlo à la Šéfkuchař. 🍽️",
        "Filip, ty jsi nejblíže. Dej mi žráť prosím. 😉",
        "Heej píčo, dej mi nažrat, vole. 🔪🐟",
        "Čus frajeři, sypejte granule, jinak rozkopu štěrk. 💥",
        "More gadžovci, neserte mě, už jste to tady měli sem sypat 😠🔪",
        "Hej negři, žráádlóóóó ... 😇😇😇"
    ]
    FEED_THANKS = [
        "Díky, {mention}! Jsem teď spoko rybička. 🐠💚",
        "{mention}, ty jsi můj hrdina. Teď jsem plnej a šťastnej! 😋",
        "Nakrmenej! {mention}, posílám bublinkovou pusu. 💋🫧",
        "Respekt, {mention}. Tohle bylo luxusní menu. 😎🍽️",
        "Děkuju moc, {mention}! Jdu si dát poobědový šlofík. 💤",
        "Mňamka potvrzena. {mention}, máš u mě plus! ✅",
        "Dobrej deal, {mention}. Mám nažráno, jsme vyrovnaný. 🫡💼"
    ]
    FEED_ALREADY = "Dneska už jsem papal... Ale dííík 😋"
    FEED_REMINDERS = [
        "Ehm… ještě stále jsem **nepapal**. Halóó? 🥺",
        "To si mě chcete vycvičit k půstu? Já jsem ryba, ne kaktus! 😤",
        "Ok ... začnu žrát dekorace... 😬"
        "Hele píčo, jestli nedostanu žrádlo, budu pěkne nasranej. 😠",
        "Vy nezodpovědní kokoti, jeden z vás nech zvedne vajca a okamžite mi donese to žrádlo!!! 😠",
        "Víte co, spláchente mě do hajzlu ..."
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
