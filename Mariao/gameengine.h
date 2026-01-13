#ifndef GAMEENGINE_H
#define GAMEENGINE_H

#include <QObject>
#include <QGraphicsScene>
#include <QTimer>
#include <QKeyEvent>
#include <QList>
#include "gameobject.h"

class GameEngine : public QObject
{
    Q_OBJECT

public:
    // 单例模式
    static GameEngine* instance();

    // 引擎控制
    void init(QGraphicsScene *scene);
    void start();
    void pause();
    void resume();
    void reset();

    // 输入处理
    void keyPress(QKeyEvent *event);

    // 游戏对象管理
    void addObject(GameObject *obj);

    // 状态查询
    bool isRunning() const { return m_running; }
    bool isPaused() const { return m_paused; }
    QGraphicsScene* getScene() const { return m_scene; }

signals:
    void gameStarted();
    void gamePaused();
    void gameResumed();

private slots:
    void updateGame();

private:
    GameEngine(QObject *parent = nullptr);
    ~GameEngine();  // 现在是公有的

    void initScene();

    static GameEngine* m_instance;

    QGraphicsScene *m_scene = nullptr;
    QTimer *m_timer = nullptr;
    QList<GameObject*> m_objects;
    bool m_running = false;
    bool m_paused = false;
};

#endif // GAMEENGINE_H
