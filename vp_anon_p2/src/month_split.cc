#include <dataframe.hpp>
#include <util.hpp>
#include <iostream>
#include <vector>

int main(int argc, char **argv)
{
    Dataframe df;
    int nb_month_to_split = 0;
    std::string path = "data/ground_truth.csv";

    if (argc > 1) path = argv[1];
    if (df.parse_csv(path.c_str())) std::cerr << "Failed to parse " << path << std::endl;

    std::vector<Dataframe> l_df = df.month_split(nb_month_to_split);
    std::vector<std::string> splitted_path = split(path, '/');
    std::string name = split(splitted_path[splitted_path.size()-1], '.')[0];

    for (size_t i = 0; i < l_df.size(); i++) {
        std::string filename = std::string("cache/" + name + "_month" + std::to_string(i+1) + ".csv");
        if (l_df[i].write_csv(filename.c_str())) std::cerr << "Writing month " << i << " failed" << std::endl;
    }

    return 0;
}
