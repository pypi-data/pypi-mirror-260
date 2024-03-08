#include <iostream>
#include <string>
#include <sstream>

#include "utils.h"


std::string VectoString(const float* vec, const int vec_size){
    std::ostringstream oss;
    if (vec_size > 1)
        oss << "[";
    for (int i = 0; i < vec_size; ++i) {
        oss << vec[i];
        if (i < vec_size -1)
            oss << ", ";
    }
    if (vec_size > 1)
        oss << "]";
    return oss.str();
}

int binaryToDecimal(const BoolVector& binaryPath) {
    int decimal = 0;
    for (int i = binaryPath.size() - 1, j = 0; i >= 0; --i, ++j) {
        decimal += binaryPath[i] * (1 << j);
    }
    return decimal + (1 << binaryPath.size()) - 1;
}


