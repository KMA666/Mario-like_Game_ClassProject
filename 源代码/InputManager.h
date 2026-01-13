#pragma once
#include <SDL2/SDL.h>
#include <map>

enum class KeyState {
    PRESSED,
    RELEASED,
    HELD
};

class InputManager {
private:
    std::map<SDL_Keycode, KeyState> keyStates;
    std::map<SDL_Keycode, KeyState> prevKeyStates;
    int mouseX, mouseY;
    bool mouseButtons[3];

public:
    InputManager();
    void update();
    void processEvent(const SDL_Event& event);
    
    bool isKeyPressed(SDL_Keycode key) const;
    bool isKeyReleased(SDL_Keycode key) const;
    bool isKeyDown(SDL_Keycode key) const;
    
    void getMousePosition(int& x, int& y) const;
    bool isMouseButtonDown(int button) const;
};