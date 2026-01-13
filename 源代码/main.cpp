#include "GameEngine.h"
#include <iostream>

int main(int argc, char* argv[]) {
    try {
        GameEngine game;
        game.initialize();
        game.run();
        game.shutdown();
    }
    catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return -1;
    }
    
    return 0;
}