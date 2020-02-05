#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cstring>

#include "util.hpp"
#include "dataframe.hpp"

/*
 *dataframe_t parse_csv(const char *path)
 *{
 *    int i = 0;
 *    std::string line;
 *    data_t data;
 *    fields_t fields;
 *    dataframe_t r_data;
 *
 *    if (!path) {
 *        std::cerr << "parse_csv()::fail::no path" << std::endl;
 *        return r_data;
 *    }
 *
 *    std::ifstream istrm(path);
 *    if (!istrm.is_open()) {
 *        std::cerr << "Failed to open test_ifstream.cc" << std::endl;
 *        istrm.close();
 *        return r_data;
 *    }
 *    else {
 *        std::getline(istrm, line);
 *        fields = split(line, ',');
 *
 *        for (std::string line; getline(istrm, line);) {
 *            std::vector<std::string> line_splitted = split(line, ',');
 *            line_t df_line;
 *            for (int i = 0; i < fields.size(); i++) df_line.insert({fields[i], line_splitted[i]});
 *            data.push_back(df_line);
 *        }
 *
 *        r_data.data   = data;
 *        r_data.fields = fields;
 *    }
 *    istrm.close();
 *
 *    return r_data;
 *}
 */

/*
 *int write_csv(dataframe_t& df, const char *path)
 *{
 *    std::ofstream ostrm(path);
 *
 *    [> We open the file stream <]
 *    if (ostrm.is_open()) {
 *        [> Init the new file by putting the correct fields <]
 *        [> string use as buffer for the data to be written <]
 *        std::string new_line;
 *        for (std::string field : df.fields) { new_line.append(field); new_line.append(","); }
 *        new_line[new_line.length() - 1] = '\n';
 *        ostrm << new_line;
 *        new_line.clear();
 *        new_line.shrink_to_fit();
 *        [> Adding each line of data to the file <]
 *        for (line_t line : df.data) {
 *            //for (std::string elt : line) { new_line.append(elt); new_line.append(","); }
 *            for (std::string field : df.fields) { new_line.append(line[field]); new_line.append(","); }
 *            new_line[new_line.length() - 1] = '\n';
 *            ostrm << new_line;
 *            new_line.clear();
 *            new_line.shrink_to_fit();
 *        }
 *    } else {
 *        std::cerr << "Output stream failed to open" << std::endl;
 *        return -1;
 *    }
 *
 *    ostrm.close();
 *    
 *    return 0;
 *}
 */

std::vector<std::string> split(std::string& a_str, char split_c)
{
    fields_t splitted;
    size_t pos = 0, start_part = 0;

    for (; pos < a_str.length(); pos++) {
        if (a_str[pos] == split_c) {
            memset((char*) (a_str.data() + pos), 0, 1);
            splitted.push_back(a_str.data() + start_part);

            start_part = pos + 1;
        }
    }
    splitted.push_back(a_str.data() + start_part);

    return splitted;
}

/*
 *std::vector<dataframe_t> month_splitter(dataframe_t i_df, int nb_month_to_split)
 *{
 *    std::vector<dataframe_t> v_df;
 *    std::string tmp;
 *    int curr_year, curr_month;
 *    fields_t splitted_line;
 *    size_t month_start, month_length, pos;
 *
 *    month_start = 0;
 *    month_length = 0;
 *    pos = 0;
 *
 *    tmp = i_df.data[0]["date"];
 *    splitted_line = split(tmp, '/');
 *    curr_year = std::stoi(splitted_line[0]);
 *    curr_month = std::stoi(splitted_line[1]);
 *
 *    //while ((curr_year == std::stoi(splitted_line[0])) && (curr_month == std::stoi(splitted_line[1]))) { 
 *        //tmp = i_df.data[pos][att2idx("date")];
 *        //splitted_line = split(tmp, '/');
 *        //pos++; 
 *    //}
 *
 *    std::cout << pos << std::endl;
 *
 *    return v_df;
 *}
 */

/*
 *dataframe_t copy_df(dataframe_t& i_df)
 *{
 *    dataframe_t df_copy;
 *
 *    std::copy(i_df.fields.begin(), i_df.fields.end(), std::back_inserter(df_copy.fields));
 *    std::copy(i_df.data.begin(), i_df.data.end(), std::back_inserter(df_copy.data));
 *
 *    return df_copy;
 *}
 */

/*
 *dataframe_t slice_df(dataframe_t& i_df, size_t start, size_t length)
 *{
 *    dataframe_t df_slice;
 *
 *    std::copy(i_df.fields.begin(), i_df.fields.end(), std::back_inserter(df_slice.fields));
 *    if (start + length > i_df.data.size()) length = i_df.data.size() - start;
 *    if (start > i_df.data.size()) start = i_df.data.size();
 *    std::copy(i_df.data.begin() + start, i_df.data.begin() + start + length, std::back_inserter(df_slice.data));
 *    for (size_t i = start; i < start + length; i++) df_slice.data.push_back(line_t(i_df.data[i]));
 *
 *    return df_slice;
 *}
 */

/*
 *void print_df(dataframe_t df, size_t start, size_t number_of_line, bool print_fields)
 *{
 *    std::string buffer;
 *    if (print_fields) {
 *        for (field_t field : df.fields) { buffer.append(field); buffer.append(","); }
 *        buffer.back() = '\n';
 *        std::cout << buffer;
 *        buffer.clear();
 *        buffer.shrink_to_fit();
 *    }
 *    for (size_t i = start; i < start + number_of_line; i++) {
 *        for (field_t field : df.fields) {
 *            buffer.append(df.data[i][field]); buffer.append(",");
 *        }
 *        buffer.back() = '\n';
 *        std::cout << buffer;
 *        buffer.clear();
 *        buffer.shrink_to_fit();
 *    }
 *}
 */

size_t att2idx(const char *att)
{
    if      (strncmp(att, "id_user", 7) == 0) return 0;
    else if (strncmp(att, "date"   , 4) == 0) return 1;
    else if (strncmp(att, "hours"  , 5) == 0) return 2;
    else if (strncmp(att, "id_item", 7) == 0) return 3;
    else if (strncmp(att, "price"  , 5) == 0) return 4;
    else if (strncmp(att, "qty"    , 3) == 0) return 5;

    return -1; 
}


