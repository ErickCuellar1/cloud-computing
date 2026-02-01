
#include <iostream>
#include <omp.h>

#define N 250
#define chunk 50
#define mostrar 20

void imprimeArreglo(float* d);

int main() {

    std::cout << "Sumando Arreglos en Paralelo!" << std::endl;

    float a[N], b[N], r[N];
    int i;

    int pedazos = chunk;

    for (i = 0; i < N; i++) {
        a[i] = i;
        b[i] = i + 10;
    }

    

#pragma omp parallel for shared(a,b,c,pedazos) private(i) schedule(static, pedazos)
    for (i = 0; i < N; i++) {
        r[i] = a[i] + b[i];
    }

    std::cout << "Imprimiendo los primeros " << mostrar << " elementos del arreglo a" << std::endl;
    imprimeArreglo(a);
    std::cout << "Imprimiendo los primeros " << mostrar << " elementos del arreglo b" << std::endl;
    imprimeArreglo(b);
    std::cout << "Imprimiendo los primeros " << mostrar << " elementos del arreglo r" << std::endl;
    imprimeArreglo(r);

}

void imprimeArreglo(float* d) {
    for (int x = 0; x < mostrar; x++) {
        std::cout << d[x] << " - ";
    }
    std::cout << std::endl;
}