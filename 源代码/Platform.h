#pragma once
#include "Entity.h"

enum class PlatformType {
    SOLID,
    BREAKABLE,
    MOVING,
    SPIKE
};

class Platform : public Entity {
private:
    PlatformType type;
    SDL_Color color;
    
public:
    Platform(float x, float y, float width, float height, PlatformType type);
    ~Platform() override = default;
    
    void update(float deltaTime) override;
    void render(SDL_Renderer* renderer) override;
    void handleCollision(Entity* other) override;
    
    PlatformType getType() const { return type; }
};