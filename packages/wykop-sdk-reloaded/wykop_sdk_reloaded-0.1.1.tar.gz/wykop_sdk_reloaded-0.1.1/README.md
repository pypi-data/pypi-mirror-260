# Wykop SDK Reaload

SDK umozliwijące komunikację z API (v3) wykopu na podstawie [oficjalnej dokumentacji](https://doc.wykop.pl/#/).


## Przykładowe uzycie

```python
from wykop_sdk_reloaded.v3.client import AuthClient, WykopApiClient

auth = AuthClient("<APP_KEY>", "<APP_SECRET>")
auth.auth_user("<USER_JWT_TOKEN>", "<USER_REFRESH_TOKEN>"))

api = WykopApiClient(auth)

# tworzy wpis na mikroblogu
api.entries_create("michal bialek sami wiecie co #wykop")
```

W razie wątpliwości przeczytaj README do końca i rzuć okiem na [testy](https://github.com/lukas346/wykop_sdk_reloaded/blob/main/tests/test_client.py).

## Autoryzacja przez Wykop API

### Utworzenie aplikacji 

By móc korzystać z api wykopu potrzebujecie utworzyć aplikację na stronie [dev.wykop.pl](https://dev.wykop.pl).


Klikacie w przycisk "utwórz aplikację". Zaznaczacie uprawnienia wedle uznania.

![](https://i.ibb.co/Yb1C27t/Zrzut-ekranu-2024-03-7-o-12-45-54.png)

Akceptujecie regulamin i klikacie "dodaj aplikację".

Na liście powinna ukazać wam się świezo dodana pozycja:

![](https://i.ibb.co/M11m064/Zrzut-ekranu-2024-03-7-o-12-48-48.png)

Kopiujecie klucz API oraz Sekret i wklejacie go do tego fragmentu kodu:
```python
auth = AuthClient("<APP_KEY>", "<APP_SECRET>")
```

Dzięki temu mozecie wykonywać ządania przez SDK. **Uwaga, by móc tworzyć, edytować, usuwać, głosować i mieć dostęp do powiadomień musicie się dodatkowo zalogować. Ten etap wystarczy do pobierania danych i w sumie nic poza tym.**

## Zalogowanie uzytkownikiem

By móc tworzyć, edytować, usuwać, głosować i mieć dostęp do powiadomień musicie się dodatkowo zalogować. Oto instrukcja jak to zrobić.


Gdy juz macie dane aplikacji wywołujecie metodę `.wykop_connect()` klasy `AuthClient` która zwraca Wam link pod który musicie się udać.
```python
from wykop_sdk_reloaded.v3.client import AuthClient

auth = AuthClient("<APP_KEY>", "<APP_SECRET>")
auth.auth_user("<USER_JWT_TOKEN>", "<USER_REFRESH_TOKEN>"))

# zwraca link do wykopu na który musicie wejsc
auth.wykop_connect()
``` 

Link powinien wyglądać tak: `https://wykop.pl/connect/10d711dfc86f361b6a3349dd1b71c19132f88cc1`

Po wejściu powinno wam wyskoczyć okienko łączące wasze konto z aplikacją. Wybierzcie jakie uprawnienia powinien mieć wasz uzytkownik api a następnie kliknijcie "połącz z aplikacją".

![](https://i.ibb.co/1LG7HQL/Zrzut-ekranu-2024-03-7-o-13-03-56.png)

Po kliknięciu zostajecie przekierowani na stronę zdefiniowaną przy tworzeniu aplikacji w polu "Podaj adres zwrotny dla WykopConnect". 

U mnie będzie to: `http://test/?token=eyJ041424iJ3QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImphbmNpb3Bhbi1VzZXItaXAiOiIz42342MTU2NTU0Iiwicm9sZXMiOlsiUk9MRV9VU0VSIl42424ImFwcC1rZXkiOiJ3NTVkOWZhYzg4NTBmYjgwYjA2MDQ0MmE1M2Q0ODk4ODdkIiwiZXhwIjoxNzA5ODk5Njg56XqK2UE3i8h9NJVUjD32OoL3STtkXlkJ_RLFWSFQbuVU&rtoken=3e39e42414248c4c79ee221ef8f10af55252db20139eb5c2617a188115f7c2758`

Wyciągacie z URLa token i rtoken, zapisujecie gdzieś sobie na przykład w pliku `.env` waszej aplikacji i teraz w końcu mozecie korzystac z pelni mozliwosci wykopowego api.

```python
from wykop_sdk_reloaded.v3.client import AuthClient, WykopApiClient

auth = AuthClient("<APP_KEY>", "<APP_SECRET>")
# USER_JWT_TOKEN to token, a USER_REFRESH_TOKEN to rtoken z urla
auth.auth_user("<USER_JWT_TOKEN>", "<USER_REFRESH_TOKEN>"))

api = WykopApiClient(auth)

# tworzy wpis na mikroblogu
api.entries_create("michal bialek sami wiecie co #wykop")
```

Michal Białek jak zwykle przekombinował ale co mozna poradzic.

## Kontakt

SDK nie jest kompletne, jeśli będzie Wam czegoś brakowało to dodajcie swoje Issue albo PR, które są oczywiście mile widziane.

## Dokumentacja

[Link](http://htmlpreview.github.io/?https://github.com/lukas346/wykop_sdk_reloaded/blob/main/docs/index.html)