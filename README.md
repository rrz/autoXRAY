# autoXRAY - личный ВПН сервер
Bash-скрипт для автоматической настройки ядра [Xray](https://github.com/XTLS/Xray-core). Предназначен для удобного получения актуальных конфигураций VPN для семейного/личного использования, настраивает selfsteal VLESS [XHTTP](https://github.com/XTLS/Xray-core/discussions/4113#discussioncomment-11468947) / [RAW](https://github.com/XTLS/REALITY/blob/main/README.en.md) REALITY.

Актуальный репозиторий: [rrz/autoXRAY](https://github.com/rrz/autoXRAY).

Новая версия `autoXRAY2.sh` использует TLS на порту 443, Xray v26.9.9 и Telegram Web Proxy. Подписка содержит только ссылки на подключения; маршруты выбираются в клиентском приложении. Прежние `autoXRAY1.sh` и `autoXRAYselfRUbrEUxhttp.sh` сохранены.

**UPD5: Добавлены MTProto FakeTLS, Hysteria2, можно выбирать ставить ли MTP/WARP** 

**UPD4: Основной скрипт автоматически ставит WARP-cli.** 

**UPD3: Основной и Экспериментальный скрипты объединены, ss2022 удален.** 

**UPD2: Описание неактуальных скриптов перемещено в [oldScriptReadme.md](https://github.com/rrz/autoXRAY/blob/main/old/oldScriptReadme.md).**

**UPD1: Добавлен новый раздел — [построение моста RU -> EU](#%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%B0%D0%B8%D0%B2%D0%B0%D0%B5%D0%BC-%D0%BC%D0%BE%D1%81%D1%82-ru---eu).**

Тестируется на: чистом Debian 12 с root правами.

===========================================================================

## Конфигурация со стандартной подпиской (рекомендуется)
Будем использовать маскировку под собственный сайт (selfsteal), который крутится на вашем же VPS. 

Для установки надо [арендовать VPS](#выбор-сервера-подбирал-промо-тарифы) и [получить домен](#получаем-домен).

Подписка содержит обычные `vless://`/`hy2://` ссылки и не добавляет собственную маршрутизацию. Поэтому HAPP и INCY могут применить любой профиль, выбранный пользователем. Готовые профили для нужного клиента доступны в [hydraponique/roscomvpn-routing](https://github.com/hydraponique/roscomvpn-routing).

### Личные ссылки для друзей

После установки `autoXRAY2.sh` доступна команда `autoxray-user`. Она сохраняет исходную подписку владельца и добавляет каждому человеку отдельные ключи VLESS и Hysteria2. Подписки содержат только ссылки на подключения; маршрутизация остаётся в клиенте.

```bash
sudo autoxray-user add Маша       # создать доступ и вывести личные ссылки
sudo autoxray-user list           # все пользователи и ссылки
sudo autoxray-user link Маша      # только ссылка на подписку
sudo autoxray-user status         # последнее подтверждённое подключение каждого
sudo autoxray-user status Маша
sudo autoxray-user remove Маша    # отключить доступ и удалить страницу
```

`status` читает журнал Xray и показывает время последнего запроса через VPN по часам сервера. Это не статус «онлайн прямо сейчас»; если приложение подключилось, но ещё не передало трафик, записи может не быть. Имена могут быть на русском. Ссылки содержат случайный токен, а не имя человека.

Для сервера, на котором `autoXRAY2.sh` установлен до появления этой команды, установите файл из текущей копии репозитория и выполните инициализацию. Существующая подписка сохранится:

```bash
sudo install -m 755 autoxray-user /usr/local/bin/autoxray-user
sudo autoxray-user init
```

```bash

bash -c "$(curl -L https://raw.githubusercontent.com/rrz/autoXRAY/main/autoXRAY2.sh)" -- вашДОМЕН.com
```

**Вы получите:**
1) VLESS XHTTP TLS на 443 порту.
2) VLESS RAW TLS VISION на 443 порту.
3) Hysteria2 на 443 порту.
4) Telegram Web Proxy на 443 порту при выборе установки.
5) vless XHTTP tls EXTRA - 8443 порт
6) vless WS tls - 8443 порт
7) vless GRPC tls - 8443 порт
8) MTProto proxy FakeTLS на 443 порту.


===========================================================================

## Выбор сервера (подбирал промо тарифы)

- [XorekCloud](https://xorek.cloud/?from=28522) - промо тариф за 149 руб./мес. (полноценный за 249).
- [netgrid](https://netgrid.host/ru?from=5893) - промо от 2€
- [intezio](https://intezio.net/?ref=3d2bf6736da6) - промо от 179 руб.
- [notbad](https://my.notbad.cloud/?from=188) - от 3$, есть оплата рублями, хороший курс и канал.
- [senko.digital](https://senko.digital/?ref=47670) - от 2€, есть днс-хостинг и домены для selfsteel, есть оплата СБП.

- [cloudcore](https://cloudcore.ru/?affiliate_uuid=e9ad7432-7898-4de2-8606-38eb90e0c1a6) - ru сервера от 100 рублей, для моста ru-eu.


Имейте в виду, что подсети популярных хостинг-провайдеров, таких как аеза, pq(ufo), ishosting и др., заблокированы многими провайдерами(РКН). К ним порой даже невозможно подключиться по SSH (без VPN). Поэтому, пожалуйста, не используйте их или не жалуйтесь, что у вас не работает основной скрипт.


## Получаем домен

**Получаем бесплатный поддомен**: регестрируемся в [cloudns](https://www.cloudns.net/aff/id/1919804/). Далее: Управление -> DNS Хостинг -> Создать зону -> Свободная зона -> вводим рандомное имя для поддомена.
Теперь надо создать A-запись: Новая запись -> Тип А -> Хост (имя субдомена) -> Указывает на (IP адрес вашего VPS).

Еще бесплатный поддомен можно получить тут: https://www.duckdns.org/ или https://freedns.afraid.org/

**Платный домен и бесплатный днс-хостинг можно получить** в [senko.digital](https://senko.digital/?ref=47670). Здесь же можно арендовать промо VPS.
Платные сервисы, как правило, работают стабильнее.

Помните, что DNS-записи обновляются не сразу: иногда это занимает 15 минут, иногда — час и более. Проверить - [xseo.in/dns](https://xseo.in/dns).



## Настройка VPN
**Скопируйте конфиг (страничка подписки) в специализированное приложение:**

- iOS/macOS: [Happ](https://www.happ.su/main/ru), [INCY](https://incy.cc/) или [v2rayTun](https://v2raytun.com/)
- Android: [Happ](https://www.happ.su/main/ru), [INCY](https://incy.cc/) или [v2rayTun](https://v2raytun.com/)
- Windows: [Happ](https://www.happ.su/main/ru), [INCY](https://incy.cc/), [winLoadXray](https://github.com/xVRVx/winLoadXRAY/releases/latest/download/winLoadXRAY.exe) или [v2rayN](https://github.com/2dust/v2rayN/releases/)
- Linux: [Happ](https://www.happ.su/main/ru), [INCY](https://incy.cc/) или [v2rayN](https://github.com/2dust/v2rayN/releases/)


===========================================================================

## Пояснение и рекомендации

Сейчас в сети много инструкций по установке GUI-панелей, таких как PasarGuard, 3x-ui или новая RemnaWave. Однако все они избыточны для домашнего использования, так как предназначены для крупных проектов и отличаются высокой сложностью настройки (также используют ядро xray). 

Мануал, который необходимо пройти до получения первого рабочего конфига, занимает более 10 страниц. 
Кроме того, подходящий конфиг для Xray нужно ещё поискать и правильно настроить — с этим отлично справляется данный скрипт.

Без GUI и базы данных Xray потребляет меньше ресурсов сервера и отлично подходит для запуска на слабых VPS-конфигурациях!

При каждом запуске autoXRAY генерирует новые UUID, ключи и пароли для защиты пользователей.

**Преимущества selfsteal**
- Сайт всегда работает на вашем ВПС - устраняется точка отказа.
- Ниже пинг - быстрее соединение.
- Не используются CDN, которые есть на многих популярных сайтах.
- Лучше маскировка - т.к. сайт находится в той же сети что и сервер.

**Перейти на алгоритм BBR**
Текущий скрипт автоматически настраивает включение BBR.
Если у вас много одновременных подключений, то можно включить алгоритм BBR (от гугла) - поможет повысить пропускную способность VPN.
Проверка текущего алгоритма: sysctl net.ipv4.tcp_congestion_control


## Как обновить autoXRAY

**Весь скрипт**: если пользуетесь подпиской, то запомните ее ссылку, переустановите скрипт и поменяйте путь на старый в /var/www/домен/xxxXXXxxx.json после этого обновите подписку в приложении.
Если только ключами, то такой возможности нет. P.S.: удобно воспользоваться QR-кодом для переноса на мобильное устройство.

**Только ядро**
```bash
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install
```
**Обновить WARP-cli**
```bash
bash <(curl -fsSL https://gitlab.com/fscarmen/warp/-/raw/main/menu.sh) v
```

## Как удалить скрипт
**Удаляем nginx & certbot**
```
systemctl disable nginx certbot; systemctl stop nginx certbot; apt remove nginx certbot -y
```

**Удаляем WARP-cli**
```
echo -e "y" | bash <(curl -fsSL https://gitlab.com/fscarmen/warp/-/raw/main/menu.sh) u
```

**Удаляем XRAY**
```
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ remove --purge
```

**Удаляем MTProto Telemt**
```
systemctl stop telemt; systemctl disable telemt; rm -f /etc/systemd/system/telemt.service /bin/telemt; systemctl daemon-reload
```

## Создание конфигов для нескольких пользователей

Это не нужно, потому что одним конфигом могут пользоваться сразу несколько человек, а чтобы управлять пользователями, следить за их трафиком нужны уже gui панели: 3x-ui или Remnawave, PasarGuard.

## Смена паролей и сайта маскировки

Запустите скрипт заново - он сформирует новые конфигурации VPN для YouTube, chatGPT и других нужных сайтов.

## Повышенная маскировка

Настоятельно рекомендуется: сменить порт ssh со стандартного 22 на другой и/или сделать вход на сервер по ключу. Настроить файрвол и оставить открытыми порты для работы скрипта: ваш ssh порт, 80 для certbot, 443, 8443, 10443 для xray, 2408 для warp

Если вы хотите погрузиться в дело конфигурации xray есть отличный [справочник](https://xtls.github.io/ru/config/outbounds/vless.html) и [руководство](https://github.com/XTLS/Xray-core/discussions/3518).

Редактировать конфиг можно тут: **/usr/local/etc/xray/config.json**

После изменений ядро надо перезапустить: **systemctl restart xray**


===========================================================================

## Настраиваем мост RU -> EU
Многие столкнулись с блокировками хостинг-сетей по TLS (особенно при использовании мобильного интернета). Существует решение — построение моста между серверами в разных локациях. Для этого необходимо:

1) На EU VPS ставим основной скрипт и берем получившуюся ссылку VLESS XHTTP TLS:
```bash
bash -c "$(curl -L https://raw.githubusercontent.com/rrz/autoXRAY/main/autoXRAY2.sh)" -- поддомен1.вашДОМЕН.com

```
2) На RU VPS ставим скрипт моста, передав ссылку VLESS XHTTP TLS:
```bash
bash -c "$(curl -L https://raw.githubusercontent.com/rrz/autoXRAY/main/bridgeTLSxhttp.sh)" -- поддомен2.вашДОМЕН.com "vless://вашКонфигXHTTP"
```
Установится прокси мост между серверами, итоговая цепочка: конфиг клиента -> ru VPS -> eu VPS -> зарубежный сайт

Также можно взять vless RAW reality VISION и использовать предыдущий скрипт моста:
```bash
bash -c "$(curl -L https://raw.githubusercontent.com/rrz/autoXRAY/main/old/autoXRAYselfstealConfRUbrEU.sh)" -- поддомен2.вашДОМЕН.com "vless://вашКонфигRAW"
```
Также теперь можно использовать несколько xhttp конфигов, все они будут добавлены в мост.

-- поддомен2.Домен.Ком "vless://xhttp1" "vless://xhttp2" "vless://xhttp3"

===

**Если вы хотите пускать YouTube через ruVPS (у вас он без ТСПУ или вы поставили и настроили [zapret4rocket](https://github.com/IndeecFOX/zapret4rocket))**

Тогда в конфиге ruVPS, который лежит /usr/local/etc/xray/config.json надо добавить в секцию "domain": [сюда], "outboundTag": "direct"
```bash
"geosite:youtube",
"youtube.com",
"googlevideo.com",
"ytimg.com",
"ggpht.com",
```
и перезапустить ядро: **systemctl restart xray**

===========================================================================

## Отключение или рекдактирование маршрутов WARP-cli
В конфиге /usr/local/etc/xray/config.json находим 
```bash
	{
	  "outboundTag": "warp",
	  "domain": ["2ip.io","habr.com","geosite:google-gemini","geosite:canva","geosite:openai","geosite:whatsapp","geosite:category-ru"]
	}
```
**Чтобы отключить**: меняем "outboundTag": "warp" на "outboundTag": "direct"


**Чтобы рекдактировать**: меняем строку "domain"

После изменений ядро надо перезапустить: **systemctl restart xray**

После этого можно удалить WARP-cli, если это необходимо.

**Если возникла ошбика при установке WARP** - [читайте инструкцию.](https://github.com/rrz/autoXRAY/blob/main/test/warp-readme.md)

===========================================================================
# Сборка с MTProto proxy FakeTLS для ТГ

В связи с начавшейся блокировкой Telegram выпускаю новую сборку с MTProxy на порту 443 и маскировкой под собственный сайт на основе [Telemt](https://github.com/telemt/telemt/blob/main/docs/QUICK_START_GUIDE.ru.md).

**Принцип работы**

443 XRAY -> MTP TELEMT -> сайт заглушка

Конфигурация: /etc/telemt/telemt.toml

===========================================================================

Скрипты будут дорабатываться до актуального состояния.

**[Поддержать автора.](https://github.com/xVRVx/autoXRAY)**
