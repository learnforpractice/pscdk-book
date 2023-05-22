cdt-cc -c -o say_hello.o say_hello.c
cdt-ar rcs libsay_hello.a say_hello.o
python-contract build --linker-flags="libsay_hello.a" test.codon
