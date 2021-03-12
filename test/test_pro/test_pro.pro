TEMPLATE = app
CONFIG += console c++11
CONFIG -= app_bundle
CONFIG -= qt

CONFIG *= FIRST SECOND

contains(CONFIG, FIRST) {
SOURCES += \
    first.cpp

HEADERS += \
    first.h
}

contains(CONFIG, SECOND) {
SOURCES += \
    second.cpp

HEADERS += \
    second.h
}

SOURCES += \
        main.cpp

HEADERS +=
