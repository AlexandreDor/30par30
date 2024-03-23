#pragma once

#include <getopt.h>
#include <typeindex>
#include <map>
#include <any>
#include <iostream>

using namespace std;

using ParsedArgs = std::map<std::string,std::any>;

typedef struct Option {
    std::type_index type;
    char short_name;
    std::string long_name;
    std::string action;
    std::any defaultValue;
    bool required;
    std::string help;
};

class ArgumentParser
{
public:
    ArgumentParser() {}
    template <typename T> void add_argument(char sopt, std::string lopt, T defaultValue,
        std::string action = "store", bool required = false, std::string help="")
    {
        Option opt = {std::type_index(typeid(T)),sopt,lopt,action,std::any(defaultValue),required,help};
        _options.push_back(opt);
        _optionMapping.insert(std::make_pair(sopt,_options.size()-1));
    }
    ParsedArgs parse_args(int argc, char** argv)
    {
        std::string short_options = "";
        struct option* long_options = new struct option[_options.size()+1];
        int i = 0;
        for (auto opt : _options)
        {
            short_options = short_options + opt.short_name;
            if (opt.action=="store") short_options = short_options + ':';
            long_options[i].name = opt.long_name.c_str();
            long_options[i].has_arg = opt.action=="store" ? required_argument : no_argument;
            long_options[i].flag = nullptr;
            long_options[i].val = 0;
            i ++;
        }
        long_options[i] = {0,0,0,0};
        ParsedArgs result;
        for (auto opt : _options)
            result.insert(std::make_pair(opt.long_name,opt.defaultValue));
        while (true) 
        {
            char opt = getopt_long (argc, argv, short_options.c_str(),long_options, 0);
            if (opt == -1) {
                break;
            }
            if (_optionMapping.find(opt) != _optionMapping.end())
            {
                unsigned int index = _optionMapping.find(opt)->second;
                Option option = _options[index];
                if (option.action == "store") {
                    std::any value;
                    if (optarg==nullptr) usage("missing value for option "+option.long_name);
                    if (option.type==std::type_index(typeid(int))) value = atoi(optarg);
                    if (option.type==std::type_index(typeid(float))) value = atof(optarg);
                    else if (option.type==std::type_index(typeid(std::string))) value = std::string(optarg);
                    result[option.long_name] = value;
                } else {
                    result[option.long_name] = true;
                }
            }
            else
                usage("unrecognized option "+opt);
        }
        return result;
    }
    void usage(const std::string& message)
    {
        std::cerr << message << std::endl;
        exit(EXIT_FAILURE);
    }
protected:
    std::vector<Option> _options;
    std::map<char, unsigned int> _optionMapping;
};
