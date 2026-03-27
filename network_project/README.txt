Проект включает:
1. Базовую часть: TCP сервер и клиент.
2. Дополнительную часть:
   - многопоточный TCP сервер;
   - UDP сервер и клиент;
   - сервер на selectors.

Запуск:
1. Базовая часть:
   python tcp_server.py
   python tcp_client.py

2. Многопоточный сервер:
   python threaded_tcp_server.py
   python threaded_tcp_client.py

3. UDP версия:
   python udp_server.py
   python udp_client.py

4. Сервер на selectors:
   python selector_server.py
   python selector_client.py

Порты:
- 5000: базовый TCP
- 5001: многопоточный TCP
- 5002: UDP
- 5003: selectors 

