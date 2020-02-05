#! /usr/bin/python3
import src.util as u
import src.anon as a


def main():

    # print("merging item set classes...")
    # gt0 = a.merge_item_set_classes(u.gt)
    # print("done")
    r_gt = u.gt
    nb_deleted = 0
    for i in range(3):
        print("uniform_nb_transac")
        r_gt, nb_deleted = a.uniform_nb_transac(r_gt, nb_deleted, len(u.gt) / 2)
        print("done")

    print("pseudonymisation")
    ngt = u.month_split(r_gt)
    ngt = a.pseudonym_hash_per_month(ngt)
    print("done")

    print("uniformisation date")
    ngt = [a.uniform_date(gt) for gt in ngt]
    print("done")

    print("uniformisation hours")
    ngt = [a.uniform_hours(gt) for gt in ngt]

    print("writing")
    u.write_data("2-COINSTI.csv", ngt)
    print("done")


if __name__ == '__main__':
    main()
