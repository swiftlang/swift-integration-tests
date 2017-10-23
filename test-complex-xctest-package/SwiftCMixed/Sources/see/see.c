#include "see.h"

int (^simpleBlock)(int) = ^(int a){
    return a+1;
};

int foo() {
    return simpleBlock(4);
}
