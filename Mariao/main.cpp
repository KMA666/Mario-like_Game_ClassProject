#include <QApplication>
#include <QMainWindow>
#include <QGraphicsView>
#include <QGraphicsScene>
#include <QMenuBar>
#include <QStatusBar>
#include <QLabel>
#include <QKeyEvent>
#include <QTimer>
#include <QMessageBox>
#include <QDebug>

#include "gameengine.h"
#include "gameobject.h"

// ==============================================
// GameObject的实现
// ==============================================

GameObject::GameObject(QObject *parent)
    : QObject(parent)
    , QGraphicsItem()
{
    setFlag(QGraphicsItem::ItemIsFocusable, false);
}

QRectF GameObject::boundingRect() const
{
    return QRectF(0, 0, m_width, m_height);
}

void GameObject::paint(QPainter *painter, const QStyleOptionGraphicsItem *option,
                       QWidget *widget)
{
    Q_UNUSED(option);
    Q_UNUSED(widget);

    painter->setBrush(m_color);
    painter->setPen(Qt::black);
    painter->drawRect(0, 0, m_width, m_height);
}

void GameObject::setPosition(qreal x, qreal y)
{
    m_x = x;
    m_y = y;
    setPos(x, y);
}

void GameObject::setSize(qreal w, qreal h)
{
    m_width = w;
    m_height = h;
    prepareGeometryChange();
}

// ==============================================
// 测试对象类
// ==============================================
class TestObject : public GameObject
{
public:
    TestObject(qreal x, qreal y, QColor color)
    {
        setPosition(x, y);
        setSize(30, 30);
        m_color = color;
        m_direction = 1;
    }

    void update() override
    {
        // 简单左右移动
        m_x += 2 * m_direction;

        if (m_x > 770) {
            m_x = 770;
            m_direction = -1;
            m_color = Qt::red;
        } else if (m_x < 0) {
            m_x = 0;
            m_direction = 1;
            m_color = Qt::blue;
        }

        setPos(m_x, m_y);
    }

private:
    int m_direction;
};

// ==============================================
// 主窗口类
// ==============================================
class MainWindow : public QMainWindow
{
public:
    MainWindow(QWidget *parent = nullptr)
        : QMainWindow(parent)
    {
        setupWindow();
        setupMenu();
        setupGame();

        // 3秒后自动开始
        QTimer::singleShot(3000, [this]() {
            GameEngine::instance()->start();
        });
    }

protected:
    void keyPressEvent(QKeyEvent *e) override
    {
        GameEngine::instance()->keyPress(e);
        QMainWindow::keyPressEvent(e);
    }

private:
    void setupWindow()
    {
        setWindowTitle("超级马里奥 - 多文件架构");
        setFixedSize(850, 700);

        // 游戏视图
        m_view = new QGraphicsView(this);
        m_view->setGeometry(10, 40, 800, 600);
        m_view->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
        m_view->setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);

        // 游戏场景
        m_scene = new QGraphicsScene(this);
        m_scene->setSceneRect(0, 0, 800, 600);
        m_view->setScene(m_scene);

        // 焦点
        m_view->setFocusPolicy(Qt::StrongFocus);
        m_view->setFocus();

        // 状态栏
        statusBar()->showMessage("准备开始游戏...");
    }

    void setupMenu()
    {
        QMenu *gameMenu = menuBar()->addMenu("游戏(&G)");

        QAction *startAct = gameMenu->addAction("开始(&S)");
        startAct->setShortcut(Qt::Key_S);
        connect(startAct, &QAction::triggered, []() {
            GameEngine::instance()->start();
        });

        QAction *pauseAct = gameMenu->addAction("暂停(&P)");
        pauseAct->setShortcut(Qt::Key_P);
        connect(pauseAct, &QAction::triggered, []() {
            GameEngine::instance()->pause();
        });

        QAction *resumeAct = gameMenu->addAction("继续(&C)");
        resumeAct->setShortcut(Qt::Key_C);
        connect(resumeAct, &QAction::triggered, []() {
            GameEngine::instance()->resume();
        });

        gameMenu->addSeparator();

        QAction *resetAct = gameMenu->addAction("重置(&R)");
        resetAct->setShortcut(Qt::Key_R);
        connect(resetAct, &QAction::triggered, []() {
            GameEngine::instance()->reset();
            GameEngine::instance()->start();
        });

        gameMenu->addSeparator();

        QAction *exitAct = gameMenu->addAction("退出(&X)");
        exitAct->setShortcut(Qt::Key_Escape);
        connect(exitAct, &QAction::triggered, this, &QMainWindow::close);

        // 帮助菜单
        QMenu *helpMenu = menuBar()->addMenu("帮助(&H)");
        QAction *aboutAct = helpMenu->addAction("关于(&A)");
        connect(aboutAct, &QAction::triggered, []() {
            QMessageBox::about(nullptr, "关于",
                "超级马里奥课程设计\n"
                "成员A：架构与引擎\n\n"
                "已完成：\n"
                "• 游戏框架架构\n"
                "• 多文件项目结构\n"
                "• 游戏主循环\n"
                "• 场景管理系统\n"
                "• 键盘输入处理\n"
                "• 对象管理系统");
        });
    }

    void setupGame()
    {
        GameEngine *engine = GameEngine::instance();
        engine->init(m_scene);

        // 添加测试对象
        engine->addObject(new TestObject(100, 500, Qt::red));
        engine->addObject(new TestObject(300, 520, Qt::blue));
        engine->addObject(new TestObject(500, 540, Qt::green));

        // 连接信号
        connect(engine, &GameEngine::gameStarted, []() {
            qDebug() << "信号：游戏开始";
        });

        connect(engine, &GameEngine::gamePaused, []() {
            qDebug() << "信号：游戏暂停";
        });

        connect(engine, &GameEngine::gameResumed, []() {
            qDebug() << "信号：游戏继续";
        });
    }

private:
    QGraphicsView *m_view;
    QGraphicsScene *m_scene;
};

// ==============================================
// 主函数
// ==============================================
int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    MainWindow window;
    window.show();

    return app.exec();
}

// 注意：移除了 #include "main.moc"，因为MainWindow没有Q_OBJECT宏
