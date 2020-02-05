#include <iostream>
#include <vector>

#include "dataframe.hpp"
#include "util.hpp"

int test_parse_csv();
int test_write_csv();
int test_att2idx();
int test_month_splitter();
int test_df_copy();
int test_print_df();
int test_slice_df();

int test_parse_csv()
{
    dataframe_t gt;

    gt = parse_csv("data/ground_truth.csv");

    print_df(gt);

    return 0;
}

int test_write_csv()
{
    dataframe_t gt;

    gt = parse_csv("data/ground_truth.csv");

    if (write_csv(gt, "gt_copy.csv")) {
        std::cerr << "CSV writing failed" << std::endl;
        return -2;
    }

    return 0;
}

int test_att2idx()
{
    std::cout << att2idx("id_user") << std::endl;
    std::cout << att2idx("date") << std::endl;
    std::cout << att2idx("hours") << std::endl;
    std::cout << att2idx("id_item") << std::endl;
    std::cout << att2idx("price") << std::endl;
    std::cout << att2idx("qty") << std::endl;

    return 0;
}

int test_month_splitter()
{
    return 0;
}

int test_df_copy()
{
    dataframe_t gt, gt_copy;

    gt = parse_csv("data/ground_truth.csv");

    gt_copy = copy_df(gt);

    gt_copy.fields[0] = "a";
    gt_copy.fields[1] = "b";
    gt_copy.fields[2] = "c";
    gt_copy.fields[3] = "d";
    gt_copy.fields[4] = "e";
    gt_copy.fields[5] = "f";
    print_df(gt_copy, 0, 10);
    print_df(gt, 0, 10);

    return (gt.data.size() != gt_copy.data.size()) || (gt.fields.size() != gt_copy.fields.size());
}

int test_print_df()
{
    dataframe_t gt;

    gt = parse_csv("data/ground_truth.csv");

    for (field_t field : gt.fields) std::cout << field << " ";
    std::cout << std::endl;
    print_df(gt, gt.data.size() - 10);

    return 0;
}

int test_slice_df()
{
    dataframe_t gt;

    gt = parse_csv("data/ground_truth.csv");

    print_df(slice_df(gt, gt.data.size() + 10, 10));
    print_df(slice_df(gt, gt.data.size() - 5, 10));

    return 0;
}

