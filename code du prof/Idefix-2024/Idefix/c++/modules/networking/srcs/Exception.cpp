#include "networking/Exception.h"

namespace networking {

char const * DisconnectedException::what () {
    return "Socket disconnected exception";
}

}
