#pragma once
#include <vector>
#include <memory>
#include "Platform.h"
#include "Enemy.h"
#include "Collectible.h"

class Level {
private:
    std::vector<std::unique_ptr<Platform>> platforms;
    std::vector<std::unique_ptr<Enemy>> enemies;
    std::vector<std::unique_ptr<Collectible>> collectibles;
    std::vector<std::unique_ptr<Entity>> staticObjects;
    
    int width, height;
    std::string backgroundPath;
    
public:
    Level(int width, int height);
    ~Level();
    
    void loadFromFile(const std::string& filename);
    void update(float deltaTime);
    void render(SDL_Renderer* renderer);
    
    void addPlatform(std::unique_ptr<Platform> platform);
    void addEnemy(std::unique_ptr<Enemy> enemy);
    void addCollectible(std::unique_ptr<Collectible> collectible);
    
    // Collision detection
    std::vector<Entity*> getCollidingEntities(const Entity& entity);
    
    // Getters
    const std::vector<std::unique_ptr<Platform>>& getPlatforms() const { return platforms; }
    const std::vector<std::unique_ptr<Enemy>>& getEnemies() const { return enemies; }
    const std::vector<std::unique_ptr<Collectible>>& getCollectibles() const { return collectibles; }
};