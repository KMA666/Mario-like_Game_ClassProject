#pragma once
#include <SDL2/SDL.h>
#include <string>

struct Vector2 {
    float x, y;
    Vector2(float x = 0, float y = 0) : x(x), y(y) {}
};

class Entity {
protected:
    Vector2 position;
    Vector2 size;
    Vector2 velocity;
    SDL_Texture* texture;
    bool active;
    
public:
    Entity(float x, float y, float width, float height);
    virtual ~Entity();
    
    virtual void update(float deltaTime) = 0;
    virtual void render(SDL_Renderer* renderer) = 0;
    virtual void handleCollision(Entity* other) = 0;
    
    // Getters and Setters
    Vector2 getPosition() const { return position; }
    Vector2 getSize() const { return size; }
    Vector2 getVelocity() const { return velocity; }
    void setPosition(Vector2 pos) { position = pos; }
    void setSize(Vector2 s) { size = s; }
    void setVelocity(Vector2 vel) { velocity = vel; }
    bool isActive() const { return active; }
    void setActive(bool a) { active = a; }
    
    SDL_Rect getBounds() const;
    bool checkCollision(const Entity& other) const;
};