#ifndef GAMEOBJECT_H
#define GAMEOBJECT_H

#include <QObject>
#include <QGraphicsItem>
#include <QPainter>

// 游戏对象基类
class GameObject : public QObject, public QGraphicsItem
{
public:
    GameObject(QObject *parent = nullptr);

    // 纯虚函数（队友实现）
    virtual void update() = 0;

    // QGraphicsItem接口
    QRectF boundingRect() const override;
    void paint(QPainter *painter, const QStyleOptionGraphicsItem *option,
               QWidget *widget = nullptr) override;

    // 基础功能
    void setPosition(qreal x, qreal y);
    void setSize(qreal w, qreal h);
    QColor getColor() const { return m_color; }
    void setColor(const QColor &color) { m_color = color; }

protected:
    qreal m_x = 0;
    qreal m_y = 0;
    qreal m_width = 32;
    qreal m_height = 32;
    QColor m_color = Qt::gray;
};

#endif // GAMEOBJECT_H
