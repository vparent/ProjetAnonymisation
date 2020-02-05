#ifndef DATAFRAME_HPP_IDWXAOH3
#define DATAFRAME_HPP_IDWXAOH3

#include <vector>
#include <string>

typedef std::string          field_t;
typedef std::string          elt_t;
typedef std::vector<elt_t>   line_t;
typedef std::vector<field_t> fields_t;
typedef std::vector<line_t>  data_t;


class Dataframe {

    public:
        /* Construct a Dataframe object from a csv file */
        Dataframe(const char *csv_file_path = NULL);
        /* Construct a Dataframe object from a vector of line_t and field_t */
        Dataframe(fields_t fields, data_t data);
        /* Construct a new dataframe from a vector of dataframes
         * by concatenation.
         * The Dataframes in the vector must share the same fields, the fields
         * tag are taken from the first element of the vector.
         */
        Dataframe(std::vector<Dataframe>);

        int                     parse_csv(const char *path);
        int                     write_csv(const char *path);
        Dataframe               copy();
        Dataframe               slice(size_t start = 0, size_t length = 0);
        void                    print(size_t start = 0, size_t length = 0, bool print_fields = true);
        data_t                  get_data();
        fields_t                get_fields();
        std::vector<Dataframe>  month_split(int nb_month_to_split = 13);
        size_t                  size();

    private:
        data_t   _data;
        fields_t _fields;
};

void print_line(line_t line);
int concat_df_to_csv(const char *path, std::vector<Dataframe> v_df);

#endif /* end of include guard: DATAFRAME_HPP_IDWXAOH3 */
