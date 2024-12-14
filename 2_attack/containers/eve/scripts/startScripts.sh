bash ./init_arp-spoofing.sh
bash ./init_forwarding.sh
bash ./load_lib.sh
iptables -A FORWARD -j NFQUEUE --queue-num 0 #отправляем в очередь, откуда потом будем считывать