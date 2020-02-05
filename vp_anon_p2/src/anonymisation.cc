#include "dataframe.hpp"
#include "anonymisation.hpp"
#include "util.hpp"
#include <vector>
#include <set>
#include <unordered_map>
#include <string.h>
#include <iostream>

void pseudonymize(std::vector<Dataframe> &v_df)
{
    for (Dataframe df : v_df) {
        /* Get the list of uids in a set */
        std::set<std::string> uids;
        /* Keep a table of correspondances of new uids within a month to be
         * consistent.
         *   key       value
         * old_uid -> new_uid
         */
        //std::map<std::string, std::string> corresp;
        std::unordered_map<std::string, std::vector<size_t>> transacs;

        for (size_t i = 0; i < df.size(); i++) {
            /* We create a hashmap id_user -> indexes of the transactions made
             * by the client 
             */
            line_t line = df.get_data()[i];
            bool uid_is_in = transacs.find(line[att2idx("id_user")]) != transacs.end();
            if (!uid_is_in) transacs[line[att2idx("id_user")]] = {};
            transacs[line[att2idx("id_user")]].push_back(i);
        }

        //for (size_t i = 0; i < df.size(); i++)
        /* Put all the transactions that the current uid has done */
        /* If DEL the new uid must be DEL */
    }
}
