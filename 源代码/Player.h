#pragma once
#include "Entity.h"
#include "Physics.h"

class Player : public Entity {
private:
    Physics physics;
    bool isGrounded;
    bool facingRight;
    float jumpForce;
    float moveSpeed;
    int lives;
    int coins;
    
public:
    Player(float x, float y);
    ~Player() override;
    
    void update(float deltaTime) override;
    void render(SDL_Renderer* renderer) override;
    void handleCollision(Entity* other) override;
    
    void handleInput(InputManager* input);
    void jump();
    void moveLeft();
    void moveRight();
    void stopHorizontalMovement();
    
    // Getters and setters
    bool getIsGrounded() const { return isGrounded; }
    bool getFacingRight() const { return facingRight; }
    int getLives() const { return lives; }
    int getCoins() const { return coins; }
    void addCoin() { coins++; }
    void loseLife() { lives--; }
};