#pragma once
#include <vector>
#include "Particle.h"

class ParticleSystem {
private:
    std::vector<Particle> particles;
    int maxParticles;
    
public:
    ParticleSystem(int maxParticles = 100);
    ~ParticleSystem();
    
    void addParticle(const Vector2& position, const Vector2& velocity, 
                     SDL_Color color, float lifetime);
    void update(float deltaTime);
    void render(SDL_Renderer* renderer);
    void clear();
    
    bool isEmpty() const { return particles.empty(); }
};