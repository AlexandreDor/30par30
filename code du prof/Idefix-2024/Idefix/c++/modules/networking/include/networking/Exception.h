#pragma once

#include <exception>

namespace networking {

/**
 * @brief Exception levée en cas de problème sur une socket
 * 
 */
class DisconnectedException : public std::exception {
public:
    char const * what ();
};

}
