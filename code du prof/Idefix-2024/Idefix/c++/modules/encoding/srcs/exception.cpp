#include "encoding/exception.h"

namespace encoding {

char const * NoEncoderForType::what () {
    return "No encoder found for";
}

}