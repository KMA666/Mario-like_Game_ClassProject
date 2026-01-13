#include "gameengine.h"
#include <QGraphicsRectItem>
#include <QDebug>

GameEngine* GameEngine::m_instance = nullptr;

GameEngine* GameEngine::instance()
{
    if (!m_instance) {
        m_instance = new GameEngine();
    }
    return m_instance;
}

GameEngine::GameEngine(QObject *parent)
    : QObject(parent)
{
    qDebug() << "游戏引擎创建";
}

GameEngine::~GameEngine()
{
    if (m_timer && m_timer->isActive()) {
        m_timer->stop();
    }

    // 清理对象
    for (GameObject* obj : m_objects) {
        delete obj;
    }
    m_objects.clear();

    qDebug() << "游戏引擎销毁";
}

void GameEngine::init(QGraphicsScene *scene)
{
    m_scene = scene;
    initScene();

    m_timer = new QTimer(this);
    connect(m_timer, &QTimer::timeout, this, &GameEngine::updateGame);

    m_running = false;
    m_paused = false;

    qDebug() << "游戏引擎初始化完成";
}

void GameEngine::initScene()
{
    if (!m_scene) return;

    // 背景
    m_scene->setBackgroundBrush(QColor(135, 206, 235));

    // 地面
    QGraphicsRectItem *ground = new QGraphicsRectItem(0, 550, 800, 50);
    ground->setBrush(Qt::green);
    ground->setPen(Qt::NoPen);
    m_scene->addItem(ground);

    // 平台
    QGraphicsRectItem *platform = new QGraphicsRectItem(200, 400, 200, 20);
    platform->setBrush(QColor(139, 69, 19));
    platform->setPen(Qt::NoPen);
    m_scene->addItem(platform);

    qDebug() << "场景初始化完成";
}

void GameEngine::start()
{
    if (m_running) return;

    m_running = true;
    m_paused = false;
    m_timer->start(30); // 33帧/秒

    emit gameStarted();
    qDebug() << "游戏开始";
}

void GameEngine::pause()
{
    if (!m_running || m_paused) return;

    m_timer->stop();
    m_paused = true;

    emit gamePaused();
    qDebug() << "游戏暂停";
}

void GameEngine::resume()
{
    if (!m_running || !m_paused) return;

    m_timer->start(30);
    m_paused = false;

    emit gameResumed();
    qDebug() << "游戏继续";
}

void GameEngine::reset()
{
    m_timer->stop();

    // 清理对象
    for (GameObject* obj : m_objects) {
        if (m_scene) {
            m_scene->removeItem(obj);
        }
        delete obj;
    }
    m_objects.clear();

    m_running = false;
    m_paused = false;

    qDebug() << "游戏重置";
}

void GameEngine::updateGame()
{
    if (!m_running || m_paused) return;

    // 更新所有对象
    for (GameObject* obj : m_objects) {
        if (obj) {
            obj->update();
        }
    }

    // 更新场景
    if (m_scene) {
        m_scene->update();
    }
}

void GameEngine::keyPress(QKeyEvent *event)
{
    switch (event->key()) {
    case Qt::Key_Left:
        qDebug() << "左键按下";
        break;
    case Qt::Key_Right:
        qDebug() << "右键按下";
        break;
    case Qt::Key_Space:
        qDebug() << "空格键按下";
        break;
    case Qt::Key_P:
        if (m_paused) {
            resume();
        } else {
            pause();
        }
        break;
    case Qt::Key_R:
        reset();
        start();
        break;
    case Qt::Key_S:
        start();
        break;
    }
}

void GameEngine::addObject(GameObject *obj)
{
    if (!obj) return;

    m_objects.append(obj);
    if (m_scene) {
        m_scene->addItem(obj);
    }

    qDebug() << "添加游戏对象，总数:" << m_objects.size();
}
