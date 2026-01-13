#pragma once
#include <SDL2/SDL.h>
#include <string>

class RenderWindow {
private:
    SDL_Window* window;
    SDL_Renderer* renderer;
    int width, height;
    std::string title;

public:
    RenderWindow(const std::string& title, int width, int height);
    ~RenderWindow();
    
    SDL_Texture* loadTexture(const std::string& filePath);
    void clear();
    void display();
    void render(SDL_Texture* texture, SDL_Rect src, SDL_Rect dst, double angle = 0.0);
    
    SDL_Renderer* getRenderer() const { return renderer; }
    SDL_Window* getWindow() const { return window; }
};