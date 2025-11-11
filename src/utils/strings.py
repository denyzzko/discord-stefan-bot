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
    FEED_START = "Heeej kluci, jsem už hladnej! 🍽️🐟 Prosím **nakrmite mě**."
    FEED_THANKS = "Díky, {mention}! Jsem teď spoko rybička. 🐠💚"
    FEED_ALREADY = "Dneska už jsem papal... Ale dííík 😋"
    FEED_REMINDERS = [
        "Ehm… ještě stále jsem **nepapal**. Halóó? 🥺",
        "To si mě chcete vycvičit k půstu? Já jsem ryba, ne kaktus! 😤",
        "Ok ... začnu žrát dekorace... 😬"
        "Hele píčo, jestli nedostanu žrádlo, budu pěkne nasratej. 😠",
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
