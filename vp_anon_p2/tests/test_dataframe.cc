#include <iostream>

#include "dataframe.hpp"

int test_dataframe()
{
    Dataframe gt;

    gt.parse_csv("data/ground_truth.csv");

    //gt.write_csv("test_copy.csv");
    //Dataframe copy = gt.copy();
    //copy.write_csv("test_copy_write.csv");

    //Dataframe slice = gt.slice(0, 15);

    //std::cout << gt.get_data().size() << std::endl;
    //std::cout << slice.get_data().size() << std::endl;

    //gt.print(0, 15);
    //std::cout << std::endl;
    //slice.print(0, 15);

    std::vector<Dataframe> v_df = gt.month_split();

    concat_df_to_csv("cache/test_concat.csv", v_df);

    return 0;
}
