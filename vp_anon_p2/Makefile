CXX=g++
CC=gcc
LD=ld

C_FLAGS=-O3 -Wall
LD_FLAGS=

SRC_DIR=src
SRC=util.cc dataframe.cc

TST_DIR=tests
TST_INC=tests
TST=test_util.cc test_dataframe.cc test_main.cc

INC_DIR=include

all : test month_split

test: $(TST_DIR)/*.cc $(SRC_DIR)/*.cc
	if [ ! -d cache ]; then mkdir cache; fi;
	if [ ! -d bin ]; then mkdir bin; fi;
	$(CXX) -o bin/$@ tests/{test_anonymisation.cc,test_dataframe.cc,test_main.cc} src/{anonymisation.cc,util.cc,dataframe.cc} -I$(INC_DIR) -I$(TST_INC) $(C_FLAGS)

month_split: $(SRC_DIR)/*.cc
	if [ ! -d cache ]; then mkdir cache; fi;
	if [ ! -d cache ]; then mkdir bin; fi;
	$(CXX) -o bin/$@ $(SRC_DIR)/*.cc -I$(INC_DIR) $(C_FLAGS)

clean:
	if [ -d cache ]; then rm -rf cache; fi;
	if [ -d bin ]; then rm -rf bin; fi;
	find . -name '\.o' -type f -exec rm {} \; ;
