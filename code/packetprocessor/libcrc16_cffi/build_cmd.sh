gcc -c -Wall -Werror -fpic src/crc16.c -Iinclude/
gcc -shared -o libcrc16.so crc16.o
echo "Now you must install libcrc16.so by copying it to /usr/local/lib/ and then running ldconfig"


