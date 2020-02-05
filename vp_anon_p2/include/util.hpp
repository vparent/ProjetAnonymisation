#include <vector>
#include <string>
#include <unordered_map>

#include "dataframe.hpp"

typedef std::string          field_t;
typedef std::string          elt_t;
typedef std::vector<elt_t>   line_t;
typedef std::vector<field_t> fields_t;
typedef std::vector<line_t>  data_t;

typedef struct _dataframe_t {
    data_t   data;
    fields_t fields;
} dataframe_t;

/* Utility functions */

/* parse a csv file,
 * returns a dataframe_t object, containing the fields name and the data */
dataframe_t parse_csv(const char *path);

/* 
 * Store the dataframe as a csv file, at the given path.
 */
int write_csv(dataframe_t& df, const char *path);

/* split a string using the character passed,
 * returns a vector of strings */
std::vector<std::string> split(std::string& a_str, char c);

/* Split the data of the given dataframe by month */
std::vector<Dataframe> month_splitter(Dataframe i_df, int nb_month_to_split = 13);

/* Complete copy of a dataframe structure to another dataframe
 * params:
 *  - df : the dataframe structure we're copying.
 *  - start: the line index from where we're copying.
 *  - length: the number of line we're copying: 0 means we're copying to the
 *            end.
 */
dataframe_t copy_df(dataframe_t& i_df);

/* Returns a dataframe_t structure from the given start with length elements
 */
dataframe_t slice_df(dataframe_t& i_df, size_t start, size_t length);

/* Print the content of the dataframe in the standard output. 
 * params:
 *  - df : dataframe to print
 *  - number_of_line : number if line to print, 0 means everything will be
 *                     printed.
 *  - start: line to start printing from.
 */
void print_df(dataframe_t df, size_t start = 0, size_t number_of_line = 0, bool print_fields = true);

/* Returns the index of the data from the attribute */
size_t att2idx(const char *att);

