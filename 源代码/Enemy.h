#pragma once
#include "Entity.h"

enum class EnemyType {
    GOOMBA,
    KOOPA,
    BOWSER,
    CHEEP_CHEEP
};

class Enemy : public Entity {
protected:
    EnemyType type;
    float speed;
    bool movingRight;
    bool alive;
    
public:
    Enemy(float x, float y, EnemyType type);
    ~Enemy() override = default;
    
    void update(float deltaTime) override;
    void render(SDL_Renderer* renderer) override;
    void handleCollision(Entity* other) override;
    
    virtual void move() = 0;
    virtual void die() = 0;
    
    bool isAlive() const { return alive; }
    void kill() { alive = false; }
    EnemyType getType() const { return type; }
};

// 具体敌人类型
class Goomba : public Enemy {
public:
    Goomba(float x, float y);
    void move() override;
    void die() override;
};