#pragma once
#include "Vector2.h"

class Physics {
private:
    Vector2 gravity;
    float groundLevel;
    
public:
    Physics();
    ~Physics();
    
    Vector2 applyGravity(const Vector2& velocity, float deltaTime);
    Vector2 applyFriction(const Vector2& velocity, float friction, float deltaTime);
    Vector2 updatePosition(const Vector2& position, const Vector2& velocity, float deltaTime);
    
    bool checkGroundCollision(const Vector2& position, const Vector2& size, float groundY);
    Vector2 resolveCollision(const Vector2& pos1, const Vector2& size1, 
                           const Vector2& pos2, const Vector2& size2);
};