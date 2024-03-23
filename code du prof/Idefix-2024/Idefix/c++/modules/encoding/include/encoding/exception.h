#pragma once

#include <exception>

namespace encoding {

class NoEncoderForType : public std::exception {
public:
    char const * what ();
};

}
