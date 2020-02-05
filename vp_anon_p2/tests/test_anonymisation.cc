#include "dataframe.hpp"
#include "anonymisation.hpp"
#include "tests.hpp"

int test_anonymisation()
{
    Dataframe gt("data/ground_truth.csv");

    std::vector<Dataframe> split = gt.month_split();
    pseudonymize(split);

    return 0;
}
