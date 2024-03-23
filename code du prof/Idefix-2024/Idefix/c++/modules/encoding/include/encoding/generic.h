#pragma once

#include <any>

namespace encoding {

class Generic
{
public:
    Generic() : _value(nullptr) {}
    template<typename T> Generic(const T &v) : _value(v) {}
    template<typename T> const T &value() const { return *std::any_cast<T>(&_value); }
    template<typename T> T &value() { return *std::any_cast<T>(&_value); }
    const std::type_info& type() { return _value.type(); }
    const std::any& get() const { return _value; }
protected:
    std::any _value;
};

}
