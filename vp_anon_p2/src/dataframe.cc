#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <map>

#include "dataframe.hpp"
#include "util.hpp"

std::map<std::string, size_t> attMap = {
        {"id_user", 0},
        {"date"   , 1},
        {"hours"  , 2},
        {"id_item", 3},
        {"price"  , 4},
};

Dataframe::Dataframe(const char *csv_file_path) : _data(), _fields()
{
    if (csv_file_path) parse_csv(csv_file_path);
}

Dataframe::Dataframe(fields_t fields, data_t data)
{
    std::copy(fields.begin(), fields.end(), std::back_inserter(_fields));
    std::copy(data.begin(), data.end(), std::back_inserter(_data));
}

Dataframe::Dataframe(std::vector<Dataframe> v_df) : _data(), _fields()
{
    if (v_df.size() > 0) {
        for (size_t i = 0; i < v_df[0].get_fields().size(); i++) _fields.push_back(v_df[0].get_fields()[i]);

        //for (Dataframe df : v_df) std::copy(df.get_data().begin(), df.get_data().end(), std::back_inserter(this->_data));
        for (size_t i = 0; i < v_df.size(); i++) for (size_t j = 0; j < v_df[i].size(); j++) _data.push_back(v_df[i].get_data()[j]);
    }
}

int Dataframe::parse_csv(const char *path)
{
    if (!path) {
        std::cerr << "dataframe::parse_csv()::fail::no_path_or_path_invalid" << std::endl;
        return 1;
    }

    std::ifstream istrm(path);
    if (!istrm.is_open()) {
        std::cerr << "dataframe::parse_csv::file_failed_to_open" << std::endl;
        istrm.close();
        return 1;
    } else {
        std::string line;
        std::getline(istrm, line);
        _fields = split(line, ',');

        for (std::string line; getline(istrm, line);) {
            _data.push_back(split(line, ','));
        }
        istrm.close();
    }

    return 0;
}

int Dataframe::write_csv(const char *path)
{
    if (!path) {
        std::cerr << "dataframe::write_csv::invalid_path" << std::endl;
        return 1;
    }

    std::ofstream ostrm(path);

    /* We open the file stream */
    if (ostrm.is_open()) {
        /* Init the new file by putting the correct fields */
        /* string we use as buffer for data to be written  */
        std::string new_line;
        for (field_t field : _fields) { new_line.append(field); new_line.append(","); }
        new_line.pop_back();
        ostrm << new_line << std::endl;
        new_line.clear();
        new_line.shrink_to_fit();
        /* Adding each line of data to the file */
        for (line_t line : _data) {
            for (elt_t elt : line) { new_line.append(elt); new_line.append(","); }
            new_line.pop_back();
            ostrm << new_line << std::endl;
            new_line.clear();
            new_line.shrink_to_fit();
        }
    } else {
        std::cerr << "dataframe::write_csv::stream_failed_to_open" << std::endl;
        return 1;
    }

    return 0;
}

Dataframe Dataframe::copy()
{
    Dataframe copy = slice(0, _data.size());

    return copy;
}

Dataframe Dataframe::slice(size_t start, size_t length)
{
    fields_t slice_fields(_fields);
    data_t   slice_datas;

    if (start > _data.size()) start = _data.size();
    if (start + length > _data.size()) length = _data.size() - start;
    for (size_t i = start; i < length; i++) slice_datas.push_back(_data[i]);

    Dataframe ret_slice(slice_fields, slice_datas);

    return ret_slice;
}

void Dataframe::print(size_t start, size_t length, bool print_fields)
{
    if (print_fields) print_line(_fields);
    if (length == 0) length = _data.size();

    if (start > _data.size()) start = _data.size();
    if (start + length > _data.size()) length = _data.size() - start;
    for (size_t i = start; i < start + length; i++) print_line(_data[i]);
}

data_t Dataframe::get_data()
{
    return _data;
}

fields_t Dataframe::get_fields()
{
    return _fields;
}

std::vector<Dataframe> Dataframe::month_split(int nb_month_to_split)
{
    int curr_year = 0, curr_month = 0;
    size_t month_start = 0, pos = 0, month_length = 0;
    std::vector<Dataframe> v_df;

    if (nb_month_to_split == 0) nb_month_to_split = 13;

    for (int i = 0; i < nb_month_to_split; i++) {
        line_t splitted_line;
        std::vector<line_t> part;
        std::string tmp;

        tmp = _data[month_start][att2idx("date")];
        splitted_line = split(tmp, '/');
        curr_year = std::stoi(splitted_line[0]);
        curr_month = std::stoi(splitted_line[1]);

        while ((curr_year == std::stoi(splitted_line[0])) && (curr_month == std::stoi(splitted_line[1])) && (pos <= size())) {
            if (pos < _data.size()) {
                tmp = _data[pos][att2idx("date")];
                splitted_line = split(tmp, '/');
            }
            pos++;
        }

        month_length = pos - month_start - 1;
        if (month_start + month_length > size()) month_length = size() - month_start;
        std::copy(_data.begin() + month_start, _data.begin() + month_start + month_length, std::back_inserter(part));

        v_df.push_back(Dataframe(_fields, part));
        month_start = pos - 1;

        part.clear();
        part.shrink_to_fit();
    }

    return v_df;
}

size_t Dataframe::size() {
    return _data.size();
}

void print_line(line_t line)
{
    std::string buffer;
    for (elt_t elt : line) { buffer.append(elt); buffer.append(","); }
    buffer.pop_back();
    std::cout << buffer << std::endl;
}

int concat_df_to_csv(const char *path, std::vector<Dataframe> v_df)
{
    if (!path) {
        std::cerr << "dataframe::write_csv::invalid_path" << std::endl;
        return 1;
    }

    std::ofstream ostrm(path);

    /* We open the file stream */
    if (ostrm.is_open()) {
        /* Init the new file by putting the correct fields */
        /* string we use as buffer for data to be written  */
        std::string new_line;
        for (field_t field : v_df[0].get_fields()) { new_line.append(field); new_line.append(","); }
        new_line.pop_back();
        ostrm << new_line << std::endl;
        new_line.clear();
        new_line.shrink_to_fit();
        /* Adding each line of data to the file */
        for (Dataframe df : v_df) {
            for (line_t line : df.get_data()) {
                for (elt_t elt : line) { new_line.append(elt); new_line.append(","); }
                new_line.pop_back();
                ostrm << new_line << std::endl;
                new_line.clear();
                new_line.shrink_to_fit();
            }
        }
    } else {
        std::cerr << "dataframe::write_csv::stream_failed_to_open" << std::endl;
        return 1;
    }

    return 0;
}

