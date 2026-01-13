QT += core gui widgets

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++11

# 成员A负责的文件
SOURCES += \
    main.cpp \
    gameengine.cpp

HEADERS += \
    gameengine.h \
    gameobject.h

FORMS +=

# 简化设置
TEMPLATE = app
TARGET = SuperMario
