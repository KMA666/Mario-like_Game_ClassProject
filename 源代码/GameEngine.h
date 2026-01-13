#pragma once
#include <memory>
#include "RenderWindow.h"
#include "InputManager.h"
#include "SceneManager.h"

class GameEngine {
private:
    std::unique_ptr<RenderWindow> renderWindow;
    std::unique_ptr<InputManager> inputManager;
    std::unique_ptr<SceneManager> sceneManager;
    bool isRunning;

public:
    GameEngine();
    ~GameEngine();
    
    void initialize();
    void run();
    void update(float deltaTime);
    void render();
    void handleEvents();
    void shutdown();
    
    /**
     * @brief 获取运行状态
     * 
     * @return bool 返回当前对象的运行状态，true表示正在运行，false表示未运行
     */
    bool getIsRunning() const { return isRunning; }
    void setIsRunning(bool running) { isRunning = running; }
};